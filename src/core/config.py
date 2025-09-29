"""
Configuration management for TariffTok AI.
"""

import os
from typing import Optional
from pydantic import BaseModel, Field, validator
from dotenv import load_dotenv


class Settings(BaseModel):
    """Application settings."""
    
    # Azure OpenAI Configuration
    azure_openai_api_key: str = Field(..., env="AZURE_OPENAI_API_KEY")
    azure_openai_endpoint: str = Field(..., env="AZURE_OPENAI_ENDPOINT")
    azure_openai_api_version: str = Field("2024-12-01-preview", env="AZURE_OPENAI_API_VERSION")
    azure_openai_deployment_name: str = Field(..., env="AZURE_OPENAI_DEPLOYMENT_NAME")
    azure_openai_model_name: str = Field("gpt-4o", env="AZURE_OPENAI_MODEL_NAME")
    
    # Application Settings
    app_env: str = Field("development", env="APP_ENV")
    debug: bool = Field(False, env="DEBUG")
    
    # Server Settings
    host: str = Field("0.0.0.0", env="HOST")
    port: int = Field(8080, env="PORT")
    
    # Data Settings
    data_path: str = Field("data/retail_tariff_data", env="DATA_PATH")
    
    # Slack Settings
    slack_webhook_url: Optional[str] = Field(None, env="SLACK_WEBHOOK_URL")
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False
    
    @validator("azure_openai_api_key")
    def validate_azure_api_key(cls, v):
        """Validate Azure OpenAI API key."""
        if not v or len(v) < 10:
            raise ValueError("Azure OpenAI API key is required")
        return v
    
    @validator("azure_openai_endpoint")
    def validate_azure_endpoint(cls, v):
        """Validate Azure OpenAI endpoint."""
        if not v or not v.startswith("https://"):
            raise ValueError("Azure OpenAI endpoint must be a valid HTTPS URL")
        return v
    
    def get_azure_config(self) -> dict:
        """Get Azure OpenAI configuration."""
        return {
            "api_key": self.azure_openai_api_key,
            "endpoint": self.azure_openai_endpoint,
            "api_version": self.azure_openai_api_version,
            "deployment_name": self.azure_openai_deployment_name,
            "model_name": self.azure_openai_model_name
        }


def load_settings() -> Settings:
    """Load and validate application settings."""
    # Load environment variables from .env file if it exists
    load_dotenv()
    
    # Debug: Print environment variables (without sensitive values)
    print("🔧 Environment Variables Debug:")
    print(f"AZURE_OPENAI_API_KEY: {'SET' if os.getenv('AZURE_OPENAI_API_KEY') else 'NOT SET'}")
    print(f"AZURE_OPENAI_ENDPOINT: {'SET' if os.getenv('AZURE_OPENAI_ENDPOINT') else 'NOT SET'}")
    print(f"AZURE_OPENAI_DEPLOYMENT_NAME: {'SET' if os.getenv('AZURE_OPENAI_DEPLOYMENT_NAME') else 'NOT SET'}")
    print(f"AZURE_OPENAI_API_VERSION: {os.getenv('AZURE_OPENAI_API_VERSION', 'NOT SET')}")
    print(f"AZURE_OPENAI_MODEL_NAME: {os.getenv('AZURE_OPENAI_MODEL_NAME', 'NOT SET')}")
    print(f"APP_ENV: {os.getenv('APP_ENV', 'NOT SET')}")
    print(f"DEBUG: {os.getenv('DEBUG', 'NOT SET')}")
    print("=" * 50)
    
    # Create settings from environment variables
    settings = Settings(
        azure_openai_api_key=os.getenv("AZURE_OPENAI_API_KEY", ""),
        azure_openai_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT", ""),
        azure_openai_api_version=os.getenv("AZURE_OPENAI_API_VERSION", "2024-12-01-preview"),
        azure_openai_deployment_name=os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME", ""),
        azure_openai_model_name=os.getenv("AZURE_OPENAI_MODEL_NAME", "gpt-4o"),
        app_env=os.getenv("APP_ENV", "development"),
        debug=os.getenv("DEBUG", "false").lower() == "true",
        host=os.getenv("HOST", "0.0.0.0"),
        port=int(os.getenv("PORT", "8080")),
        data_path=os.getenv("DATA_PATH", "data/retail_tariff_data"),
        slack_webhook_url=os.getenv("SLACK_WEBHOOK_URL", None)
    )
    
    return settings


# Global settings instance
settings = load_settings()
