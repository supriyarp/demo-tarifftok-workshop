"""
Query Parser Agent - Extracts structured information from natural language queries.
"""

import json
from typing import Dict, Any, Optional
from openai import AzureOpenAI
from src.core.models import AgentState, TariffQuery, Country, ProductType, QueryIntent
from src.core.config import settings
from src.core.data_loader import data_loader


class QueryParserAgent:
    """Parses natural language queries about tariffs."""
    
    def __init__(self):
        """Initialize the query parser agent."""
        self.client = self._setup_client()
        self.available_countries = [c.value for c in data_loader.get_available_countries()]
        self.available_product_types = [p.value for p in data_loader.get_available_product_types()]
    
    def _setup_client(self) -> AzureOpenAI:
        """Setup Azure OpenAI client."""
        azure_config = settings.get_azure_config()
        return AzureOpenAI(
            api_key=azure_config["api_key"],
            api_version=azure_config["api_version"],
            azure_endpoint=azure_config["endpoint"]
        )
    
    def _create_system_prompt(self) -> str:
        """Create the system prompt for query parsing."""
        return f"""You are an expert query parser for a tariff analysis system. Your job is to extract structured information from natural language queries about tariff rates.

## Your Task
Parse user queries and extract:
1. **Country** - Which country the user is asking about
2. **Product Type** - Which product category they're interested in
3. **Intent** - What they want to know (tariff rate, comparison, general info)

## Available Data
**Supported Countries:** {', '.join(self.available_countries)}
**Supported Product Types:** {', '.join(self.available_product_types)}

## Country Aliases (map these to exact names)
- "US", "USA", "United States", "America" → "USA"
- "Chinese", "China" → "China" 
- "Vietnamese", "Vietnam" → "Vietnam"
- "Mexican", "Mexico" → "Mexico"
- "Indian", "India" → "India"

## Product Type Aliases
- "electronic", "electronics", "tech", "technology" → "Electronics"
- "clothing", "apparel", "garments", "fashion" → "Apparel"
- "home goods", "housewares", "household", "home" → "Home"
- "toy", "toys", "games", "playthings" → "Toys"

## Query Intent Classification
- **tariff_rate**: User wants to know the tariff percentage/rate
- **comparison**: User wants to compare tariffs between countries/products
- **general_info**: User asks about available data, capabilities, or general information
- **unsupported**: Queries asking for hypothetical scenarios, margin analysis, what-if analysis, or other capabilities not supported by the system

## Unsupported Query Patterns (classify as "unsupported")
- Hypothetical scenarios: "what if", "analyze margin changes with X% increase", "scenario analysis"
- Margin analysis: "margin impact", "profit analysis", "cost impact analysis"
- Future predictions: "predict", "forecast", "future rates"
- Business analysis: "business impact", "pricing analysis", "competitive analysis"
- Any query asking for calculations beyond current/historical tariff rates

## Output Format
Return ONLY a valid JSON object with this exact structure:
{{
    "country": "CountryName" or null,
    "product_type": "ProductType" or null,
    "intent": "tariff_rate|comparison|general_info|unsupported",
    "confidence": 0.0-1.0,
    "parsed_entities": {{
        "countries_mentioned": ["list", "of", "countries"],
        "products_mentioned": ["list", "of", "products"],
        "keywords": ["tariff", "rate", "percentage", "etc"]
    }}
}}

## Examples

Query: "What's the tariff rate for electronics from China?"
Response:
{{
    "country": "China",
    "product_type": "Electronics", 
    "intent": "tariff_rate",
    "confidence": 0.95,
    "parsed_entities": {{
        "countries_mentioned": ["China"],
        "products_mentioned": ["electronics"],
        "keywords": ["tariff", "rate"]
    }}
}}

Query: "How much tariff is charged on toys imported from Vietnam?"
Response:
{{
    "country": "Vietnam",
    "product_type": "Toys",
    "intent": "tariff_rate", 
    "confidence": 0.9,
    "parsed_entities": {{
        "countries_mentioned": ["Vietnam"],
        "products_mentioned": ["toys"],
        "keywords": ["tariff", "imported"]
    }}
}}

Query: "Analyze margin changes for Toys from India with a 8% tariff increase"
Response:
{{
    "country": "India",
    "product_type": "Toys",
    "intent": "unsupported",
    "confidence": 0.95,
    "parsed_entities": {{
        "countries_mentioned": ["India"],
        "products_mentioned": ["Toys"],
        "keywords": ["analyze", "margin", "changes", "tariff", "increase"]
    }}
}}

Query: "Compare tariffs between China and India for electronics"
Response:
{{
    "country": null,
    "product_type": "Electronics",
    "intent": "comparison",
    "confidence": 0.85,
    "parsed_entities": {{
        "countries_mentioned": ["China", "India"],
        "products_mentioned": ["electronics"],
        "keywords": ["compare", "tariffs"]
    }}
}}

Query: "What data do you have available?"
Response:
{{
    "country": null,
    "product_type": null,
    "intent": "general_info",
    "confidence": 0.95,
    "parsed_entities": {{
        "countries_mentioned": [],
        "products_mentioned": [],
        "keywords": ["data", "available"]
    }}
}}

## Important Rules
1. **Be precise**: Only use exact country/product names from the available lists
2. **Handle ambiguity**: If unclear, set confidence lower and include what you found
3. **Extract everything**: Capture all mentioned countries/products in parsed_entities
4. **JSON only**: Return ONLY the JSON object, no explanations or markdown
5. **Validate data**: If country/product not in available lists, set to null but mention in parsed_entities"""

    def parse_query(self, query: str) -> TariffQuery:
        """
        Parse a natural language query into structured data.
        
        Args:
            query: User's natural language query
            
        Returns:
            TariffQuery object with parsed information
        """
        try:
            response = self.client.chat.completions.create(
                model=settings.azure_openai_deployment_name,
                messages=[
                    {"role": "system", "content": self._create_system_prompt()},
                    {"role": "user", "content": f"Parse this query: {query}"}
                ],
                temperature=0.1,
                response_format={"type": "json_object"}
            )
            
            # Parse the JSON response
            parsed_data = json.loads(response.choices[0].message.content)
            
            # Create TariffQuery object
            return TariffQuery(
                country=Country(parsed_data["country"]) if parsed_data.get("country") else None,
                product_type=ProductType(parsed_data["product_type"]) if parsed_data.get("product_type") else None,
                intent=QueryIntent(parsed_data["intent"]),
                confidence=parsed_data.get("confidence", 0.0),
                original_query=query,
                parsed_entities=parsed_data.get("parsed_entities", {})
            )
            
        except Exception as e:
            # Return a basic query with error information
            return TariffQuery(
                country=None,
                product_type=None,
                intent=QueryIntent.GENERAL_INFO,
                confidence=0.0,
                original_query=query,
                parsed_entities={"error": str(e)}
            )


def parse_query_node(state: AgentState) -> AgentState:
    """
    LangGraph node function for query parsing.
    
    Args:
        state: Current agent state
        
    Returns:
        Updated state with parsed query
    """
    agent = QueryParserAgent()
    
    try:
        parsed_query = agent.parse_query(state.query)
        
        # Update the state object directly
        state.parsed_query = parsed_query
        state.step = "parsed"
        state.error = None
        
        return state
    except Exception as e:
        state.error = f"Query parsing failed: {str(e)}"
        state.step = "error"
        return state
