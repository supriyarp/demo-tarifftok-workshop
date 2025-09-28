"""
Data loader for CSV tariff data.
"""

import pandas as pd
import os
from datetime import date
from typing import Optional, List
from src.core.models import TariffData, Country, ProductType
from src.core.config import settings


class TariffDataLoader:
    """Loads and manages tariff data from CSV files."""
    
    def __init__(self, data_path: Optional[str] = None):
        """Initialize the data loader."""
        self.data_path = data_path or settings.data_path
        self._tariffs_df = None
        self._cache_valid = False
    
    @property
    def tariffs_df(self) -> pd.DataFrame:
        """Load and cache tariffs data."""
        if self._tariffs_df is None or not self._cache_valid:
            csv_path = os.path.join(self.data_path, "tariffs.csv")
            if not os.path.exists(csv_path):
                raise FileNotFoundError(f"Tariffs CSV not found at {csv_path}")
            
            self._tariffs_df = pd.read_csv(csv_path)
            # Convert start_time to date
            self._tariffs_df['start_time'] = pd.to_datetime(self._tariffs_df['start_time']).dt.date
            self._cache_valid = True
        
        return self._tariffs_df
    
    def get_tariff_rate(
        self, 
        country: Country, 
        product_type: ProductType, 
        as_of_date: Optional[date] = None
    ) -> Optional[TariffData]:
        """
        Get tariff rate for specific country and product type.
        
        Args:
            country: Country of origin
            product_type: Product category
            as_of_date: Date to use for tariff lookup (defaults to latest)
            
        Returns:
            TariffData object or None if not found
        """
        df = self.tariffs_df
        
        # Filter by country and product type
        filtered = df[
            (df['country'] == country.value) & 
            (df['product_type'] == product_type.value)
        ]
        
        if filtered.empty:
            return None
        
        # If no date specified, use the latest tariff
        if as_of_date is None:
            latest_tariff = filtered.loc[filtered['start_time'].idxmax()]
        else:
            # Find the most recent tariff that's not in the future
            valid_tariffs = filtered[filtered['start_time'] <= as_of_date]
            if valid_tariffs.empty:
                # Use the earliest available tariff
                latest_tariff = filtered.loc[filtered['start_time'].idxmin()]
            else:
                latest_tariff = valid_tariffs.loc[valid_tariffs['start_time'].idxmax()]
        
        return TariffData(
            country=country,
            product_type=product_type,
            current_tariff=float(latest_tariff['current_tariff']),
            start_time=latest_tariff['start_time']
        )
    
    def get_tariff_with_history(
        self, 
        country: Country, 
        product_type: ProductType, 
        as_of_date: Optional[date] = None
    ) -> tuple[Optional[TariffData], Optional[TariffData]]:
        """
        Get current tariff rate and previous rate for historical comparison.
        
        Args:
            country: Country of origin
            product_type: Product category
            as_of_date: Date to use for tariff lookup (defaults to latest)
            
        Returns:
            Tuple of (current_tariff_data, previous_tariff_data)
        """
        df = self.tariffs_df
        
        # Filter by country and product type
        filtered = df[
            (df['country'] == country.value) & 
            (df['product_type'] == product_type.value)
        ]
        
        if filtered.empty:
            return None, None
        
        # Sort by date
        filtered = filtered.sort_values('start_time')
        
        # If no date specified, use the latest tariff
        if as_of_date is None:
            current_tariff = filtered.iloc[-1]  # Latest
            previous_tariff = filtered.iloc[-2] if len(filtered) > 1 else None
        else:
            # Find tariffs up to the specified date
            valid_tariffs = filtered[filtered['start_time'] <= as_of_date]
            if valid_tariffs.empty:
                current_tariff = filtered.iloc[0]  # Earliest
                previous_tariff = None
            else:
                current_tariff = valid_tariffs.iloc[-1]  # Latest valid
                # Find previous tariff
                previous_tariffs = valid_tariffs.iloc[:-1]
                previous_tariff = previous_tariffs.iloc[-1] if len(previous_tariffs) > 0 else None
        
        # Convert to TariffData objects
        current_data = TariffData(
            country=country,
            product_type=product_type,
            current_tariff=float(current_tariff['current_tariff']),
            start_time=current_tariff['start_time']
        )
        
        previous_data = None
        if previous_tariff is not None:
            previous_data = TariffData(
                country=country,
                product_type=product_type,
                current_tariff=float(previous_tariff['current_tariff']),
                start_time=previous_tariff['start_time']
            )
        
        return current_data, previous_data
    
    def get_available_countries(self) -> List[Country]:
        """Get list of available countries in the tariff data."""
        countries = self.tariffs_df['country'].unique().tolist()
        return [Country(country) for country in countries if country in [c.value for c in Country]]
    
    def get_available_product_types(self) -> List[ProductType]:
        """Get list of available product types in the tariff data."""
        product_types = self.tariffs_df['product_type'].unique().tolist()
        return [ProductType(pt) for pt in product_types if pt in [p.value for p in ProductType]]
    
    def get_data_summary(self) -> dict:
        """Get summary of available data."""
        df = self.tariffs_df
        return {
            "total_records": len(df),
            "countries": [c.value for c in self.get_available_countries()],
            "product_types": [p.value for p in self.get_available_product_types()],
            "date_range": {
                "earliest": df['start_time'].min().isoformat(),
                "latest": df['start_time'].max().isoformat()
            },
            "tariff_range": {
                "min": float(df['current_tariff'].min()),
                "max": float(df['current_tariff'].max())
            }
        }


# Global data loader instance
data_loader = TariffDataLoader()
