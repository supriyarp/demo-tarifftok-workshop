"""
Dynamic LangGraph Pipeline with Graphviz Visualization.
"""

import time
from typing import Dict, Any, List, Optional
from src.core.models import AgentState
from src.agents.query_parser import parse_query_node
from src.agents.tariff_lookup import tariff_lookup_node
from src.agents.response_formatter import response_formatter_node
from src.agents.dynamic_router import router_node
from src.agents.data_summary import data_summary_node
from src.agents.error_handler import error_handler_node


class DynamicLangGraphPipeline:
    """Dynamic LangGraph-style pipeline with execution tracking and visualization."""
    
    def __init__(self):
        """Initialize the dynamic pipeline."""
        self.node_registry = {
            "start": self._start_node,
            "parse_query": parse_query_node,
            "tariff_lookup": tariff_lookup_node,
            "response_formatter": response_formatter_node,
            "data_summary": data_summary_node,
            "error_handler": error_handler_node,
            "router": router_node,
            "end": self._end_node
        }
        
        self.graph_structure = {
            "start": ["router"],
            "router": ["parse_query", "error_handler"],
            "parse_query": ["router"],
            "tariff_lookup": ["router"],
            "data_summary": ["router"],
            "response_formatter": ["end"],
            "error_handler": ["end"],
            "end": []
        }
    
    def _start_node(self, state: AgentState) -> AgentState:
        """Start node - initializes execution tracking."""
        state.current_node = "start"
        state.current_node_start_time = time.time()
        state.execution_path = ["start"]
        state.step = "started"
        return state
    
    def _end_node(self, state: AgentState) -> AgentState:
        """End node - finalizes execution tracking."""
        state.current_node = "end"
        state.step = "completed"
        
        # Calculate total execution time
        if state.execution_path:
            total_time = sum(state.node_timings.values())
            state.execution_time = total_time
        
        return state
    
    def execute_node(self, state: AgentState, node_name: str) -> AgentState:
        """
        Execute a specific node and update state.
        
        Args:
            state: Current agent state
            node_name: Name of the node to execute
            
        Returns:
            Updated state after node execution
        """
        if node_name not in self.node_registry:
            state.error = f"Unknown node: {node_name}"
            return state
        
        # Update current node
        state.current_node = node_name
        state.current_node_start_time = time.time()
        
        try:
            # Execute the node
            node_func = self.node_registry[node_name]
            state = node_func(state)
            
            # Record timing
            if state.current_node_start_time:
                execution_time = time.time() - state.current_node_start_time
                state.node_timings[node_name] = execution_time
            
            # Update execution path
            if node_name not in state.execution_path:
                state.execution_path.append(node_name)
            
            return state
            
        except Exception as e:
            state.error = f"Node {node_name} failed: {str(e)}"
            state.step = "error"
            return state
    
    def run_dynamic_analysis(self, query: str) -> Dict[str, Any]:
        """
        Run complete dynamic tariff analysis pipeline.
        
        Args:
            query: User's natural language query
            
        Returns:
            Dictionary with analysis results and execution metadata
        """
        # Create initial state
        state = AgentState(
            query=query,
            current_node="start",
            step="initial"
        )
        
        total_start_time = time.time()
        
        try:
            # Execute the dynamic pipeline
            current_node = "start"
            max_iterations = 20  # Prevent infinite loops
            iteration = 0
            
            while current_node != "end" and iteration < max_iterations:
                iteration += 1
                
                # Execute current node
                state = self.execute_node(state, current_node)
                
                if state.error and current_node != "error_handler":
                    # Route to error handler
                    current_node = "error_handler"
                    continue
                
                # Determine next node based on current state
                if current_node == "start":
                    current_node = "parse_query"
                elif current_node == "parse_query":
                    if state.parsed_query and state.parsed_query.intent:
                        if state.parsed_query.intent in ["tariff_rate", "comparison"]:
                            current_node = "tariff_lookup"
                        elif state.parsed_query.intent == "general_info":
                            current_node = "data_summary"
                        else:
                            current_node = "error_handler"
                    else:
                        current_node = "error_handler"
                elif current_node in ["tariff_lookup", "data_summary"]:
                    current_node = "response_formatter"
                elif current_node == "response_formatter":
                    current_node = "end"
                elif current_node == "error_handler":
                    current_node = "end"
                else:
                    current_node = "end"
            
            # Finalize execution
            state = self.execute_node(state, "end")
            
        except Exception as e:
            state.error = f"Pipeline error: {str(e)}"
            state.step = "error"
        
        # Calculate total execution time
        total_execution_time = time.time() - total_start_time
        state.execution_time = total_execution_time
        
        # Return results with execution metadata
        return {
            "query": state.query,
            "response": state.response,
            "tariff_info": state.tariff_result.dict() if state.tariff_result else None,
            "comparison_data": [result.dict() for result in state.tariff_results] if state.tariff_results else None,
            "error": state.error,
            "step": state.step,
            "execution_path": state.execution_path,
            "execution_time": state.execution_time,
            "current_node": state.current_node,
            "node_timings": state.node_timings,
            "execution_summary": state.execution_summary
        }
    
    def generate_graphviz_dot(self, execution_path: Optional[List[str]] = None) -> str:
        """
        Generate Graphviz DOT representation of the LangGraph.
        
        Args:
            execution_path: Optional path to highlight in the graph
            
        Returns:
            DOT format string for Graphviz
        """
        dot_lines = [
            "digraph TariffTokAI {",
            "    rankdir=TB;",
            "    node [shape=box, style=filled, fontname=\"Arial\", fontsize=10];",
            "    edge [fontname=\"Arial\", fontsize=8];",
            "",
            "    // Node definitions",
            "    start [label=\"🚀 Start\", fillcolor=\"#e1f5fe\", color=\"#0277bd\"];",
            "    router [label=\"🧭 Router\\n(Dynamic Decision)\", fillcolor=\"#fff3e0\", color=\"#f57c00\"];",
            "    parse_query [label=\"🔍 Parse Query\\n(LLM Analysis)\", fillcolor=\"#f3e5f5\", color=\"#7b1fa2\"];",
            "    tariff_lookup [label=\"📊 Tariff Lookup\\n(Data Retrieval)\", fillcolor=\"#e8f5e8\", color=\"#388e3c\"];",
            "    data_summary [label=\"📋 Data Summary\\n(Info Response)\", fillcolor=\"#e3f2fd\", color=\"#1976d2\"];",
            "    response_formatter [label=\"💬 Response Formatter\\n(LLM Generation)\", fillcolor=\"#fce4ec\", color=\"#c2185b\"];",
            "    error_handler [label=\"⚠️ Error Handler\\n(Recovery)\", fillcolor=\"#ffebee\", color=\"#d32f2f\"];",
            "    end [label=\"✅ End\", fillcolor=\"#e8f5e8\", color=\"#2e7d32\"];",
            "",
            "    // Edge definitions",
            "    start -> router;",
            "    router -> parse_query [label=\"Query Intent\"];",
            "    router -> error_handler [label=\"Error\"];",
            "    parse_query -> router [label=\"Parsed\"];",
            "    tariff_lookup -> router [label=\"Data Found\"];",
            "    data_summary -> router [label=\"Summary Ready\"];",
            "    response_formatter -> end [label=\"Complete\"];",
            "    error_handler -> end [label=\"Handled\"];",
            "",
            "    // Dynamic routing labels",
            "    router -> tariff_lookup [label=\"TARIFF_RATE\\nCOMPARISON\", style=dashed];",
            "    router -> data_summary [label=\"GENERAL_INFO\", style=dashed];",
            "    router -> error_handler [label=\"UNSUPPORTED\", style=dashed];",
            "",
            "    // Execution path highlighting",
        ]
        
        # Add execution path highlighting if provided
        if execution_path:
            dot_lines.append("    // Highlighted execution path")
            for i, node in enumerate(execution_path):
                if i < len(execution_path) - 1:
                    next_node = execution_path[i + 1]
                    dot_lines.append(f"    {node} -> {next_node} [color=\"red\", penwidth=3, label=\"EXECUTED\"];")
        
        dot_lines.extend([
            "",
            "    // Styling",
            "    { rank=same; start; }",
            "    { rank=same; parse_query; tariff_lookup; data_summary; }",
            "    { rank=same; response_formatter; error_handler; }",
            "    { rank=same; end; }",
            "}"
        ])
        
        return "\n".join(dot_lines)
    
    def get_execution_statistics(self, execution_path: List[str], node_timings: Dict[str, float]) -> Dict[str, Any]:
        """
        Get execution statistics for the pipeline run.
        
        Args:
            execution_path: List of executed nodes
            node_timings: Timing for each node
            
        Returns:
            Dictionary with execution statistics
        """
        total_time = sum(node_timings.values())
        
        return {
            "total_nodes_executed": len(execution_path),
            "execution_path": execution_path,
            "total_execution_time": total_time,
            "node_timings": node_timings,
            "average_node_time": total_time / len(execution_path) if execution_path else 0,
            "slowest_node": max(node_timings.items(), key=lambda x: x[1]) if node_timings else None,
            "fastest_node": min(node_timings.items(), key=lambda x: x[1]) if node_timings else None
        }


# Global pipeline instance
dynamic_pipeline = DynamicLangGraphPipeline()


def run_tariff_analysis(query: str) -> Dict[str, Any]:
    """
    Run complete tariff analysis using dynamic LangGraph pipeline.
    
    Args:
        query: User's natural language query
        
    Returns:
        Dictionary with analysis results and execution metadata
    """
    return dynamic_pipeline.run_dynamic_analysis(query)


def get_graph_visualization(execution_path: Optional[List[str]] = None) -> str:
    """
    Get Graphviz DOT representation of the LangGraph.
    
    Args:
        execution_path: Optional path to highlight in the graph
        
    Returns:
        DOT format string for Graphviz
    """
    return dynamic_pipeline.generate_graphviz_dot(execution_path)
