"""
Simple pipeline for the TariffTok AI system.
"""

from typing import Dict, Any
from src.core.models import AgentState
from src.agents.query_parser import parse_query_node
from src.agents.tariff_lookup import tariff_lookup_node
from src.agents.response_formatter import response_formatter_node


def run_tariff_analysis(query: str) -> Dict[str, Any]:
    """
    Run complete tariff analysis pipeline.
    
    Args:
        query: User's natural language query
        
    Returns:
        Dictionary with analysis results
    """
    # Create initial state
    state = AgentState(
        query=query,
        step="initial"
    )
    
    try:
        # Step 1: Parse query
        state = parse_query_node(state)
        
        # Step 2: Lookup tariff
        state = tariff_lookup_node(state)
        
        # Step 3: Format response
        state = response_formatter_node(state)
        
    except Exception as e:
        state.error = f"Pipeline error: {str(e)}"
        state.response = "I encountered an error processing your request. Please try again."
        state.step = "error"
    
    # Return results
    return {
        "query": state.query,
        "response": state.response,
        "tariff_info": state.tariff_result.dict() if state.tariff_result else None,
        "comparison_data": [result.dict() for result in state.tariff_results] if state.tariff_results else None,
        "error": state.error,
        "step": state.step
    }
