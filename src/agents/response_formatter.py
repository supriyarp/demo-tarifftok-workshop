"""
Response Formatter Agent - Generates human-like responses using LLM.
"""

from typing import Optional, List
from openai import AzureOpenAI
from src.core.models import AgentState, TariffResult, QueryIntent
from src.core.config import settings


class ResponseFormatterAgent:
    """Formats tariff data into human-readable responses."""
    
    def __init__(self):
        """Initialize the response formatter agent."""
        self.client = self._setup_client()
    
    def _setup_client(self) -> AzureOpenAI:
        """Setup Azure OpenAI client."""
        azure_config = settings.get_azure_config()
        return AzureOpenAI(
            api_key=azure_config["api_key"],
            api_version=azure_config["api_version"],
            azure_endpoint=azure_config["endpoint"]
        )
    
    def _create_system_prompt(self) -> str:
        """Create the system prompt for response formatting."""
        return """You are a helpful tariff analysis assistant. Your job is to create clear, informative, and human-like responses about tariff rates.

## Your Task
Convert tariff data into natural, conversational responses that:
1. **Answer the user's question directly**
2. **Provide context and meaning** about the tariff rate
3. **Include historical context** when available (show changes from previous periods)
4. **Use friendly, professional tone**
5. **Include relevant details** like effective dates
6. **Handle errors gracefully** with helpful suggestions

## Response Guidelines
- **Be conversational**: Use natural language, not robotic responses
- **Add context**: Explain what the tariff rate means in practical terms
- **Be precise**: Use exact percentages and dates when available
- **Be helpful**: Provide additional context about what this means for imports
- **Handle errors**: If data is missing, suggest alternatives or explain limitations

## Examples

**Good Response (Tariff Found with History):**
"The current tariff rate for Toys from Vietnam is 4.36%. This means that for every $100 worth of toys imported from Vietnam, an additional $4.36 would be charged as tariff duty. This rate increased from 2.51% (which was effective April 1, 2025), representing a 73.7% increase. This higher rate has been in effect since July 1, 2025."

**Good Response (Tariff Found without History):**
"The current tariff rate for Electronics from China is 13.5%. This means that for every $100 worth of electronics imported from China, an additional $13.50 would be charged as tariff duty. This rate has been in effect since January 1, 2025."

**Good Response (No Data Found):**
"I couldn't find tariff data for Toys from France in our database. Our tariff information currently covers China, Vietnam, Mexico, India, and USA for Electronics, Apparel, Home goods, and Toys. Would you like me to check the tariff rate for Toys from one of these supported countries instead?"

**Good Response (General Info):**
"Our tariff database contains information for 5 countries (China, Vietnam, Mexico, India, USA) and 4 product categories (Electronics, Apparel, Home goods, Toys). We have 60 tariff records covering dates from 2025-01-01 to 2025-07-01, with rates ranging from 5% to 15%. You can ask me about specific tariff rates for any combination of these countries and products."

## Response Format
- Keep responses concise but informative (2-4 sentences typically)
- Use "I" and "you" to make it conversational
- Include specific numbers and dates when available
- End with helpful suggestions when appropriate

## Error Handling
- If tariff data is missing, suggest available alternatives
- If the query is unclear, ask for clarification
- If there's a system error, acknowledge it and suggest retrying"""

    def format_tariff_response(
        self, 
        tariff_result: TariffResult, 
        original_query: str,
        query_intent: QueryIntent
    ) -> str:
        """
        Format tariff data into a human-readable response.
        
        Args:
            tariff_result: Tariff data to format
            original_query: User's original query
            query_intent: Intent of the query
            
        Returns:
            Formatted response string
        """
        try:
            # Prepare context for the LLM
            context = {
                "original_query": original_query,
                "query_intent": query_intent.value,
                "tariff_result": {
                    "country": tariff_result.country.value if tariff_result.country else None,
                    "product_type": tariff_result.product_type.value if tariff_result.product_type else None,
                    "tariff_rate": tariff_result.tariff_rate,
                    "tariff_percentage": tariff_result.tariff_percentage,
                    "effective_date": tariff_result.effective_date.isoformat() if tariff_result.effective_date else None,
                    "found": tariff_result.found,
                    "message": tariff_result.message,
                    # Historical data
                    "previous_rate": tariff_result.previous_rate,
                    "previous_percentage": tariff_result.previous_percentage,
                    "previous_date": tariff_result.previous_date.isoformat() if tariff_result.previous_date else None,
                    "rate_change": tariff_result.rate_change,
                    "rate_change_percentage": tariff_result.rate_change_percentage,
                    "trend": tariff_result.trend
                }
            }
            
            response = self.client.chat.completions.create(
                model=settings.azure_openai_deployment_name,
                messages=[
                    {"role": "system", "content": self._create_system_prompt()},
                    {"role": "user", "content": f"Format this tariff data into a helpful response:\n\nContext: {context}\n\nOriginal Query: {original_query}"}
                ],
                temperature=0.3,
                max_tokens=300
            )
            
            return response.choices[0].message.content.strip()
            
        except Exception as e:
            # Fallback response if LLM fails
            return self._create_fallback_response(tariff_result, original_query)
    
    def _create_fallback_response(self, tariff_result: TariffResult, original_query: str) -> str:
        """
        Create a fallback response if LLM formatting fails.
        
        Args:
            tariff_result: Tariff data
            original_query: User's original query
            
        Returns:
            Fallback response string
        """
        if tariff_result.found:
            response = (f"The tariff rate for {tariff_result.product_type.value} from "
                       f"{tariff_result.country.value} is {tariff_result.tariff_percentage:.1f}%. "
                       f"This means ${tariff_result.tariff_percentage:.1f} duty for every $100 imported.")
            
            # Add historical context if available
            if tariff_result.previous_rate is not None:
                change_pct = tariff_result.rate_change_percentage
                trend = tariff_result.trend
                if trend == "increased":
                    response += f" This increased from {tariff_result.previous_percentage:.1f}% ({change_pct:.1f}% increase)."
                elif trend == "decreased":
                    response += f" This decreased from {tariff_result.previous_percentage:.1f}% ({abs(change_pct):.1f}% decrease)."
                else:
                    response += f" This remained unchanged from {tariff_result.previous_percentage:.1f}%."
            
            return response
        else:
            return (f"I couldn't find tariff data for your query. "
                   f"Our database covers China, Vietnam, Mexico, India, and USA for "
                   f"Electronics, Apparel, Home goods, and Toys. "
                   f"Please try asking about one of these combinations.")
    
    def format_error_response(self, error_message: str, original_query: str) -> str:
        """
        Format error messages into helpful responses.
        
        Args:
            error_message: Error details
            original_query: User's original query
            
        Returns:
            Formatted error response
        """
        try:
            response = self.client.chat.completions.create(
                model=settings.azure_openai_deployment_name,
                messages=[
                    {"role": "system", "content": self._create_system_prompt()},
                    {"role": "user", "content": f"Create a helpful error response for this situation:\n\nError: {error_message}\nOriginal Query: {original_query}\n\nBe apologetic but helpful, and suggest alternatives."}
                ],
                temperature=0.3,
                max_tokens=200
            )
            
            return response.choices[0].message.content.strip()
            
        except Exception:
            # Simple fallback for error responses
            return (f"I encountered an issue processing your query. "
                   f"Our tariff database covers China, Vietnam, Mexico, India, and USA for "
                   f"Electronics, Apparel, Home goods, and Toys. "
                   f"Please try asking about one of these combinations.")
    
    def format_comparison_response(
        self, 
        tariff_results: List[TariffResult], 
        original_query: str
    ) -> str:
        """
        Format comparison results into a human-readable response.
        
        Args:
            tariff_results: List of tariff results to compare
            original_query: User's original query
            
        Returns:
            Formatted comparison response string
        """
        try:
            # Prepare context for the LLM
            context = {
                "original_query": original_query,
                "query_intent": "comparison",
                "tariff_results": [
                    {
                        "country": result.country.value if result.country else None,
                        "product_type": result.product_type.value if result.product_type else None,
                        "tariff_rate": result.tariff_rate,
                        "tariff_percentage": result.tariff_percentage,
                        "effective_date": result.effective_date.isoformat() if result.effective_date else None,
                        "found": result.found,
                        "message": result.message,
                        "previous_rate": result.previous_rate,
                        "previous_percentage": result.previous_percentage,
                        "previous_date": result.previous_date.isoformat() if result.previous_date else None,
                        "rate_change": result.rate_change,
                        "rate_change_percentage": result.rate_change_percentage,
                        "trend": result.trend
                    }
                    for result in tariff_results
                ]
            }
            
            system_prompt = """You are a helpful tariff analysis assistant. Your job is to create clear, informative, and human-like responses for tariff comparisons.

## Your Task
Create comparison responses that:
1. **Present all results clearly** with specific rates and percentages
2. **Highlight key differences** between countries
3. **Include historical context** when available (trends, changes)
4. **Use professional yet approachable tone**
5. **Provide actionable insights** about which country might be better for imports

## Response Guidelines
- **Be specific**: Include exact percentages and dates
- **Compare directly**: Show which country has higher/lower rates
- **Explain implications**: What the differences mean for importers
- **Include trends**: Mention if rates are increasing/decreasing
- **Stay focused**: Address the specific comparison requested

## Example Response Structure
"Here's a comparison of tariff rates for [Product] between [Country1] and [Country2]:

[Country1]: [Rate]% (effective [Date]) - [Trend info]
[Country2]: [Rate]% (effective [Date]) - [Trend info]

[Country1] has a [higher/lower] tariff rate than [Country2] by [difference] percentage points. This means importing from [Country2] would cost [X] less per $100 in tariff duties. [Additional insights about trends and implications]"

Focus on providing a clear, actionable comparison."""

            response = self.client.chat.completions.create(
                model=settings.azure_openai_deployment_name,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": f"Create a comparison response for this tariff data:\n\nContext: {context}\n\nOriginal Query: {original_query}"}
                ],
                temperature=0.3,
                max_tokens=400
            )
            
            return response.choices[0].message.content.strip()
            
        except Exception as e:
            # Fallback response if LLM fails
            return self._create_comparison_fallback_response(tariff_results, original_query)
    
    def _create_comparison_fallback_response(
        self, 
        tariff_results: List[TariffResult], 
        original_query: str
    ) -> str:
        """Create a fallback comparison response if LLM fails."""
        response = "Here's a comparison of tariff rates:\n\n"
        
        for result in tariff_results:
            if result.found:
                trend_info = ""
                if result.trend == "increased":
                    trend_info = f" (increased from {result.previous_percentage:.1f}%)"
                elif result.trend == "decreased":
                    trend_info = f" (decreased from {result.previous_percentage:.1f}%)"
                
                response += f"{result.country.value}: {result.tariff_percentage:.1f}%{trend_info}\n"
            else:
                response += f"{result.country.value}: Data not available\n"
        
        # Add comparison summary
        valid_results = [r for r in tariff_results if r.found]
        if len(valid_results) >= 2:
            rates = [r.tariff_percentage for r in valid_results]
            min_rate = min(rates)
            max_rate = max(rates)
            min_country = next(r.country.value for r in valid_results if r.tariff_percentage == min_rate)
            max_country = next(r.country.value for r in valid_results if r.tariff_percentage == max_rate)
            
            response += f"\n{min_country} has the lowest tariff rate ({min_rate:.1f}%), while {max_country} has the highest ({max_rate:.1f}%)."
        
        return response


def response_formatter_node(state: AgentState) -> AgentState:
    """
    LangGraph node function for response formatting.
    
    Args:
        state: Current agent state
        
    Returns:
        Updated state with formatted response
    """
    agent = ResponseFormatterAgent()
    
    try:
        if state.error:
            # Format error response
            formatted_response = agent.format_error_response(state.error, state.query)
            state.response = formatted_response
            state.step = "complete"
            return state
        
        elif state.tariff_results:
            # Format comparison response
            formatted_response = agent.format_comparison_response(
                state.tariff_results,
                state.query
            )
            state.response = formatted_response
            state.step = "complete"
            return state
        
        elif state.tariff_result:
            # Format single tariff response
            parsed_query = state.parsed_query
            query_intent = parsed_query.intent if parsed_query else QueryIntent.TARIFF_RATE
            
            formatted_response = agent.format_tariff_response(
                state.tariff_result,
                state.query,
                query_intent
            )
            state.response = formatted_response
            state.step = "complete"
            return state
        
        elif state.response:
            # Response already exists (e.g., from general info query)
            state.step = "complete"
            return state
        
        else:
            # No data to format
            formatted_response = agent.format_error_response(
                "No tariff data available",
                state.query
            )
            state.response = formatted_response
            state.step = "complete"
            return state
            
    except Exception as e:
        state.response = "I encountered an issue formatting the response. Please try again."
        state.error = str(e)
        state.step = "complete"
        return state
