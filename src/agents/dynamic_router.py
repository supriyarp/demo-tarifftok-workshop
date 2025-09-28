"""
Dynamic Router Agent - Handles routing decisions based on query intent and state.
"""

import time
from typing import List, Dict, Any
from src.core.models import AgentState, QueryIntent


class DynamicRouterAgent:
    """Handles dynamic routing decisions for the LangGraph execution."""
    
    def __init__(self):
        """Initialize the dynamic router agent."""
        self.routing_rules = {
            QueryIntent.TARIFF_RATE: ["parse_query", "tariff_lookup", "response_formatter"],
            QueryIntent.COMPARISON: ["parse_query", "tariff_lookup", "response_formatter"],
            QueryIntent.GENERAL_INFO: ["parse_query", "data_summary", "response_formatter"],
            QueryIntent.UNSUPPORTED: ["parse_query", "error_handler", "response_formatter"]
        }
    
    def determine_next_nodes(self, state: AgentState) -> List[str]:
        """
        Determine the next nodes to execute based on current state.
        
        Args:
            state: Current agent state
            
        Returns:
            List of next node names to execute
        """
        current_node = state.current_node
        
        # If we're at the start, determine initial routing
        if current_node == "start":
            return ["parse_query"]
        
        # If we just parsed the query, route based on intent
        if current_node == "parse_query":
            if state.parsed_query and state.parsed_query.intent:
                return self.routing_rules.get(state.parsed_query.intent, ["error_handler"])
            else:
                return ["error_handler"]
        
        # If we completed tariff lookup, go to response formatter
        if current_node == "tariff_lookup":
            return ["response_formatter"]
        
        # If we completed data summary, go to response formatter
        if current_node == "data_summary":
            return ["response_formatter"]
        
        # If we completed response formatter, we're done
        if current_node == "response_formatter":
            return ["end"]
        
        # If we hit an error handler, try to recover or end
        if current_node == "error_handler":
            return ["end"]
        
        # Default fallback
        return ["end"]
    
    def should_retry_node(self, state: AgentState, node_name: str) -> bool:
        """
        Determine if a node should be retried after an error.
        
        Args:
            state: Current agent state
            node_name: Name of the node that failed
            
        Returns:
            True if the node should be retried
        """
        max_retries = 2
        current_retries = state.retry_count.get(node_name, 0)
        return current_retries < max_retries
    
    def get_retry_node(self, state: AgentState, failed_node: str) -> str:
        """
        Get the node to retry after a failure.
        
        Args:
            state: Current agent state
            failed_node: Name of the node that failed
            
        Returns:
            Name of the node to retry
        """
        return failed_node
    
    def get_fallback_nodes(self, state: AgentState) -> List[str]:
        """
        Get fallback nodes when primary routing fails.
        
        Args:
            state: Current agent state
            
        Returns:
            List of fallback node names
        """
        return ["error_handler", "response_formatter"]


def router_node(state: AgentState) -> AgentState:
    """
    LangGraph node function for dynamic routing.
    
    Args:
        state: Current agent state
        
    Returns:
        Updated state with routing decisions
    """
    router = DynamicRouterAgent()
    
    try:
        # Record start time for current node
        if not state.current_node_start_time:
            state.current_node_start_time = time.time()
        
        # Determine next nodes
        next_nodes = router.determine_next_nodes(state)
        state.next_nodes = next_nodes
        
        # Update execution path
        if state.current_node not in state.execution_path:
            state.execution_path.append(state.current_node)
        
        # Record timing for current node
        if state.current_node_start_time:
            execution_time = time.time() - state.current_node_start_time
            state.node_timings[state.current_node] = execution_time
        
        # Update execution summary
        state.execution_summary.update({
            "current_node": state.current_node,
            "next_nodes": next_nodes,
            "execution_path": state.execution_path.copy(),
            "node_timings": state.node_timings.copy()
        })
        
        state.step = "routed"
        state.error = None
        
        return state
        
    except Exception as e:
        state.error = f"Routing failed: {str(e)}"
        state.step = "error"
        state.next_nodes = ["error_handler"]
        return state
