"""
LLM Configuration for Resume Tailoring Application

This module handles configuration for the Gemini AI integration.
"""

import os
from typing import Optional

import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


def create_gemini_client(api_key: Optional[str] = None, model: str = "gemini-2.5-flash") -> genai.GenerativeModel:
    """
    Create and configure Gemini AI client using Google Gen AI library.

    Args:
        api_key: Gemini API key. If None, will try to get from GEMINI_API_KEY env var
        model: Gemini model name

    Returns:
        Configured GenerativeModel for Gemini

    Raises:
        ValueError: If API key is not found
    """
    if api_key is None:
        api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        raise ValueError("GEMINI_API_KEY not found. Please set it in .env file or pass as parameter.")

    genai.configure(api_key=api_key)

    model = genai.GenerativeModel(model)

    return model


def validate_config() -> bool:
    """
    Validate that the configuration is properly set up.

    Returns:
        True if configuration is valid, False otherwise
    """
    api_key = os.getenv("GEMINI_API_KEY")
    return api_key is not None


def get_missing_config() -> list[str]:
    """
    Get list of missing required configuration.

    Returns:
        List of missing configuration items
    """
    missing = []
    if not os.getenv("GEMINI_API_KEY"):
        missing.append("GEMINI_API_KEY")
    return missing
