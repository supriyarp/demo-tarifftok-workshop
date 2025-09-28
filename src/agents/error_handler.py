"""
Error Handler Agent - Handles errors and provides recovery mechanisms.
"""

import time
from src.core.models import AgentState


def error_handler_node(state: AgentState) -> AgentState:
    """
    LangGraph node function for error handling.
    
    Args:
        state: Current agent state
        
    Returns:
        Updated state with error handling
    """
    try:
        # Record start time
        start_time = time.time()
        
        # Create helpful error response
        error_response = f"""I encountered an issue processing your query: {state.error if state.error else 'Unknown error'}

🔧 **Troubleshooting Tips:**
• Make sure you're asking about supported countries: China, Vietnam, Mexico, India, USA
• Supported products: Electronics, Apparel, Home, Toys
• Try rephrasing your question more clearly

💡 **Example queries that work:**
• "What's the tariff rate for Electronics from China?"
• "Compare tariff rates for Toys between Vietnam and India"
• "How much tariff is charged on Apparel from Mexico?"

Please try again with a clearer question, and I'll do my best to help!"""
        
        state.response = error_response
        state.step = "error_handled"
        state.error = None
        
        # Record timing
        execution_time = time.time() - start_time
        state.node_timings["error_handler"] = execution_time
        
        return state
        
    except Exception as e:
        # If even error handling fails, provide a basic response
        state.response = "I'm experiencing technical difficulties. Please try again later."
        state.step = "error"
        state.error = str(e)
        return state
