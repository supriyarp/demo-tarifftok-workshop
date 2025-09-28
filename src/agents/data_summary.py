"""
Data Summary Agent - Provides information about available data.
"""

import time
from src.core.models import AgentState, QueryIntent
from src.core.data_loader import data_loader


def data_summary_node(state: AgentState) -> AgentState:
    """
    LangGraph node function for providing data summary.
    
    Args:
        state: Current agent state
        
    Returns:
        Updated state with data summary
    """
    try:
        # Record start time
        start_time = time.time()
        
        # Get data summary
        data_summary = data_loader.get_data_summary()
        
        # Create summary response
        summary_text = f"""Our tariff database contains comprehensive information:

📊 Data Overview:
• {data_summary['total_records']} total tariff records
• {len(data_summary['countries'])} countries: {', '.join([str(c) for c in data_summary['countries']])}
• {len(data_summary['product_types'])} product categories: {', '.join([str(p) for p in data_summary['product_types']])}

📅 Date Range:
• From: {data_summary['date_range']['earliest']}
• To: {data_summary['date_range']['latest']}

📈 Tariff Range:
• Minimum: {data_summary['tariff_range']['min']:.2%}
• Maximum: {data_summary['tariff_range']['max']:.2%}

I can provide current rates, historical changes, and comparisons between countries and products."""
        
        state.response = summary_text
        state.step = "data_summary_complete"
        state.error = None
        
        # Record timing
        execution_time = time.time() - start_time
        state.node_timings["data_summary"] = execution_time
        
        return state
        
    except Exception as e:
        state.error = f"Data summary failed: {str(e)}"
        state.step = "error"
        return state
