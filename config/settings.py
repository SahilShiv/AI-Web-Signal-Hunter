"""Runtime settings and environment configuration for AI Web Signal Hunter."""

import os
from pathlib import Path
from typing import Optional
from dotenv import load_dotenv

# Base directory of the project
BASE_DIR = Path(__file__).resolve().parent.parent

# Load environment variables from .env file if present
load_dotenv(BASE_DIR / ".env")


class AppSettings:
    """Manages application configurations with environment fallbacks."""

    def __init__(self):
        # AI Provider settings
        self.groq_api_key: str = os.getenv("GROQ_API_KEY", "").strip()
        self.gemini_api_key: str = (
            os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY", "")
        ).strip()
        self.default_provider: str = os.getenv("DEFAULT_AI_PROVIDER", "Groq").strip()
        self.groq_model: str = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile").strip()
        self.gemini_model: str = os.getenv("GEMINI_MODEL", "gemini-2.5-flash").strip()

        # Crawler settings
        self.crawl_limit: int = int(os.getenv("DEFAULT_CRAWL_LIMIT", "25"))
        self.request_timeout: int = int(os.getenv("REQUEST_TIMEOUT", "12"))
        self.request_delay: float = float(os.getenv("REQUEST_DELAY", "0.8"))
        self.min_relevance_threshold: int = int(os.getenv("MIN_RELEVANCE_THRESHOLD", "60"))
        self.analysis_batch_size: int = int(os.getenv("ANALYSIS_BATCH_SIZE", "5"))
        self.user_agent: str = os.getenv(
            "CRAWLER_USER_AGENT",
            "AI-Web-Signal-Hunter/1.0 (+https://github.com/internship/ai-web-signal-hunter; polite bot)"
        )

        # Database and Storage paths
        self.data_dir: Path = BASE_DIR / "data"
        self.exports_dir: Path = BASE_DIR / "exports"
        self.database_path: Path = self.data_dir / "signals.db"

        # Ensure directories exist
        self.data_dir.mkdir(parents=True, exist_ok=True)
        self.exports_dir.mkdir(parents=True, exist_ok=True)

    def is_groq_available(self) -> bool:
        return bool(self.groq_api_key and len(self.groq_api_key) > 5)

    def is_gemini_available(self) -> bool:
        return bool(self.gemini_api_key and len(self.gemini_api_key) > 5)

    def get_masked_key(self, provider: str) -> str:
        key = self.groq_api_key if provider.lower() == "groq" else self.gemini_api_key
        if not key:
            return "Not Configured"
        if len(key) <= 8:
            return "••••••••"
        return f"{key[:4]}••••••••{key[-4:]}"

    def reload(self):
        """Reload variables from .env file."""
        load_dotenv(BASE_DIR / ".env", override=True)
        self.__init__()


# Global singleton settings instance
settings = AppSettings()

