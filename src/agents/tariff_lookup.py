"""
Tariff Lookup Agent - Retrieves tariff data from CSV files.
"""

from datetime import date
from typing import Optional
from src.core.models import AgentState, TariffResult, Country, ProductType, QueryIntent
from src.core.data_loader import data_loader


class TariffLookupAgent:
    """Handles tariff data lookup and retrieval."""
    
    def __init__(self):
        """Initialize the tariff lookup agent."""
        self.data_loader = data_loader
    
    def lookup_tariff(
        self, 
        country: Country, 
        product_type: ProductType, 
        as_of_date: Optional[date] = None,
        include_history: bool = True
    ) -> TariffResult:
        """
        Look up tariff rate for specific country and product type.
        
        Args:
            country: Country of origin
            product_type: Product category
            as_of_date: Date to use for lookup
            include_history: Whether to include historical comparison data
            
        Returns:
            TariffResult object
        """
        try:
            if include_history:
                # Get current and previous tariff data
                current_data, previous_data = self.data_loader.get_tariff_with_history(
                    country, product_type, as_of_date
                )
                
                if current_data:
                    result_data = {
                        "country": current_data.country,
                        "product_type": current_data.product_type,
                        "tariff_rate": current_data.current_tariff,
                        "effective_date": current_data.start_time,
                        "found": True,
                        "message": None
                    }
                    
                    # Add historical data if available
                    if previous_data:
                        result_data.update({
                            "previous_rate": previous_data.current_tariff,
                            "previous_date": previous_data.start_time
                        })
                    
                    return TariffResult(**result_data)
                else:
                    return TariffResult(
                        country=country,
                        product_type=product_type,
                        tariff_rate=0.0,
                        effective_date=None,
                        found=False,
                        message=f"No tariff data found for {product_type.value} from {country.value}"
                    )
            else:
                # Use simple lookup without history
                tariff_data = self.data_loader.get_tariff_rate(country, product_type, as_of_date)
                
                if tariff_data:
                    return TariffResult(
                        country=tariff_data.country,
                        product_type=tariff_data.product_type,
                        tariff_rate=tariff_data.current_tariff,
                        effective_date=tariff_data.start_time,
                        found=True,
                        message=None
                    )
                else:
                    return TariffResult(
                        country=country,
                        product_type=product_type,
                        tariff_rate=0.0,
                        effective_date=None,
                        found=False,
                        message=f"No tariff data found for {product_type.value} from {country.value}"
                    )
                
        except Exception as e:
            return TariffResult(
                country=country,
                product_type=product_type,
                tariff_rate=0.0,
                effective_date=None,
                found=False,
                message=f"Error looking up tariff: {str(e)}"
            )
    
    def handle_comparison_query(self, parsed_query) -> list[TariffResult]:
        """
        Handle comparison queries by looking up tariffs for multiple countries.
        
        Args:
            parsed_query: Parsed query with comparison intent
            
        Returns:
            List of TariffResult objects
        """
        results = []
        
        # Extract countries from parsed entities
        mentioned_countries = parsed_query.parsed_entities.get("countries_mentioned", [])
        product_type = parsed_query.product_type
        
        if not product_type:
            # If no specific product type, try to infer or use a default
            product_type = ProductType.ELECTRONICS  # Default to electronics
        
        # If no countries mentioned in parsed entities, try to extract from original query
        if not mentioned_countries:
            # Simple keyword-based extraction as fallback
            query_lower = parsed_query.original_query.lower()
            available_countries = [c.value.lower() for c in self.data_loader.get_available_countries()]
            
            for country_name in available_countries:
                if country_name in query_lower:
                    mentioned_countries.append(country_name.title())  # Convert back to proper case
        
        # If still no countries found, return error
        if not mentioned_countries:
            return [TariffResult(
                country=Country.USA,  # Placeholder
                product_type=product_type,
                tariff_rate=0.0,
                effective_date=None,
                found=False,
                message="Could not identify countries to compare. Please specify countries like 'Compare tariffs between China and Vietnam for Electronics'."
            )]
        
        for country_name in mentioned_countries:
            try:
                country = Country(country_name)
                result = self.lookup_tariff(country, product_type)
                results.append(result)
            except ValueError:
                # Country not in our supported list
                results.append(TariffResult(
                    country=Country.USA,  # Placeholder
                    product_type=product_type,
                    tariff_rate=0.0,
                    effective_date=None,
                    found=False,
                    message=f"Country '{country_name}' is not supported in our tariff database"
                ))
        
        return results
    
    def get_data_summary(self) -> dict:
        """
        Get summary of available tariff data.
        
        Returns:
            Dictionary with data summary
        """
        return self.data_loader.get_data_summary()


def tariff_lookup_node(state: AgentState) -> AgentState:
    """
    LangGraph node function for tariff lookup.
    
    Args:
        state: Current agent state
        
    Returns:
        Updated state with tariff results
    """
    agent = TariffLookupAgent()
    
    try:
        parsed_query = state.parsed_query
        if not parsed_query:
            state.error = "No parsed query available for tariff lookup"
            state.step = "error"
            return state
        
        # Handle different query intents
        if parsed_query.intent == QueryIntent.TARIFF_RATE:
            if parsed_query.country and parsed_query.product_type:
                # Single country/product lookup
                tariff_result = agent.lookup_tariff(
                    parsed_query.country, 
                    parsed_query.product_type
                )
                state.tariff_result = tariff_result
                state.step = "lookup_complete"
                state.error = None
                return state
            else:
                # Missing required information
                state.error = f"Missing required information. Need both country and product type. " \
                            f"Available countries: {', '.join([c.value for c in data_loader.get_available_countries()])}. " \
                            f"Available products: {', '.join([p.value for p in data_loader.get_available_product_types()])}"
                state.step = "error"
                return state
        
        elif parsed_query.intent == QueryIntent.COMPARISON:
            # Handle comparison queries
            tariff_results = agent.handle_comparison_query(parsed_query)
            if tariff_results:
                state.tariff_results = tariff_results
                # For backward compatibility, also set tariff_result to first result
                state.tariff_result = tariff_results[0] if len(tariff_results) == 1 else None
                state.step = "lookup_complete"
                state.error = None
                return state
            else:
                state.error = "No tariff data found for comparison"
                state.step = "error"
                return state
        
        elif parsed_query.intent == QueryIntent.GENERAL_INFO:
            # Return data summary
            data_summary = agent.get_data_summary()
            state.response = f"Available tariff data: {data_summary['countries']} countries, " \
                           f"{data_summary['product_types']} product types, " \
                           f"{data_summary['total_records']} total records. " \
                           f"Date range: {data_summary['date_range']['earliest']} to {data_summary['date_range']['latest']}"
            state.step = "lookup_complete"
            state.error = None
            return state
        
        elif parsed_query.intent == QueryIntent.UNSUPPORTED:
            # Handle unsupported queries (hypothetical scenarios, margin analysis, etc.)
            state.error = ("I cannot perform hypothetical scenario analysis, margin analysis, or other business calculations. "
                          "This system only provides current tariff rates and historical changes. "
                          "Please ask about current tariffs (e.g., 'What's the tariff rate for Toys from India?') "
                          "or how rates have changed over time.")
            state.step = "error"
            return state
        
        else:
            state.error = f"Unknown query intent: {parsed_query.intent}"
            state.step = "error"
            return state
            
    except Exception as e:
        state.error = f"Tariff lookup failed: {str(e)}"
        state.step = "error"
        return state
