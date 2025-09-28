"""
Pydantic models for the TariffTok AI system.
"""

from datetime import date
from typing import Optional, Dict, Any, List
from pydantic import BaseModel, Field, validator
from enum import Enum
import time


class Country(str, Enum):
    """Supported countries for tariff analysis."""
    CHINA = "China"
    VIETNAM = "Vietnam"
    MEXICO = "Mexico"
    INDIA = "India"
    USA = "USA"


class ProductType(str, Enum):
    """Supported product types for tariff analysis."""
    ELECTRONICS = "Electronics"
    APPAREL = "Apparel"
    HOME = "Home"
    TOYS = "Toys"


class QueryIntent(str, Enum):
    """User query intents."""
    TARIFF_RATE = "tariff_rate"
    COMPARISON = "comparison"
    GENERAL_INFO = "general_info"
    UNSUPPORTED = "unsupported"  # For queries the system cannot handle


class TariffQuery(BaseModel):
    """Parsed user query structure."""
    country: Optional[Country] = None
    product_type: Optional[ProductType] = None
    intent: QueryIntent = QueryIntent.TARIFF_RATE
    confidence: float = Field(ge=0.0, le=1.0, default=0.0)
    original_query: str
    parsed_entities: Dict[str, Any] = Field(default_factory=dict)


class TariffData(BaseModel):
    """Tariff data from CSV."""
    country: Country
    product_type: ProductType
    current_tariff: float = Field(ge=0.0, le=1.0)
    start_time: date


class TariffResult(BaseModel):
    """Tariff lookup result."""
    country: Country
    product_type: ProductType
    tariff_rate: float = Field(ge=0.0, le=1.0)
    tariff_percentage: Optional[float] = Field(ge=0.0, le=100.0, default=None)
    effective_date: Optional[date] = None
    found: bool = True
    message: Optional[str] = None
    
    # Historical data
    previous_rate: Optional[float] = Field(ge=0.0, le=1.0, default=None)
    previous_percentage: Optional[float] = Field(ge=0.0, le=100.0, default=None)
    previous_date: Optional[date] = None
    rate_change: Optional[float] = None  # Absolute change
    rate_change_percentage: Optional[float] = None  # Relative change
    trend: Optional[str] = None  # "increased", "decreased", "unchanged"

    def __init__(self, **data):
        """Initialize with automatic percentage calculation and historical analysis."""
        if 'tariff_percentage' not in data and 'tariff_rate' in data:
            data['tariff_percentage'] = round(data['tariff_rate'] * 100, 2)
            
        if 'previous_percentage' not in data and 'previous_rate' in data:
            data['previous_percentage'] = round(data['previous_rate'] * 100, 2)
        
        # Calculate changes if we have both current and previous rates
        if 'tariff_rate' in data and 'previous_rate' in data and data['previous_rate'] is not None:
            current = data['tariff_rate']
            previous = data['previous_rate']
            
            # Absolute change
            data['rate_change'] = round(current - previous, 4)
            
            # Relative change (percentage change)
            if previous > 0:
                data['rate_change_percentage'] = round(((current - previous) / previous) * 100, 2)
            
            # Determine trend
            if current > previous:
                data['trend'] = "increased"
            elif current < previous:
                data['trend'] = "decreased"
            else:
                data['trend'] = "unchanged"
                
        super().__init__(**data)


class AgentState(BaseModel):
    """LangGraph agent state with dynamic execution tracking."""
    query: str
    parsed_query: Optional[TariffQuery] = None
    tariff_result: Optional[TariffResult] = None
    tariff_results: Optional[List[TariffResult]] = None  # For comparison queries
    response: Optional[str] = None
    error: Optional[str] = None
    step: str = "initial"
    
    # Dynamic execution tracking
    execution_path: List[str] = Field(default_factory=list)  # Track which nodes executed
    node_timings: Dict[str, float] = Field(default_factory=dict)  # Track execution times
    current_node: str = "start"
    next_nodes: List[str] = Field(default_factory=list)  # Dynamic routing decisions
    retry_count: Dict[str, int] = Field(default_factory=dict)  # Error recovery
    execution_summary: Dict[str, Any] = Field(default_factory=dict)  # Metadata
    execution_time: Optional[float] = None  # Total execution time
    current_node_start_time: Optional[float] = None  # Current node start time

    class Config:
        """Pydantic configuration."""
        use_enum_values = True
        validate_assignment = True


class ChatRequest(BaseModel):
    """API request model."""
    message: str


class ChatResponse(BaseModel):
    """API response model."""
    response: str
    tariff_info: Optional[TariffResult] = None
    comparison_data: Optional[List[TariffResult]] = None
    error: Optional[str] = None
    # Execution metadata
    execution_path: Optional[List[str]] = None
    execution_time: Optional[float] = None
    current_node: Optional[str] = None
    node_timings: Optional[Dict[str, float]] = None
    execution_summary: Optional[Dict[str, Any]] = None
