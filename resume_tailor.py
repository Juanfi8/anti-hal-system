"""
Resume Tailoring Application using Gemini AI

This module provides functionality to tailor a person's resume for a specific
job description using Google's Gemini AI.
"""

import json
import sys
from pathlib import Path
from typing import Any, Dict, Optional

import google.generativeai as genai

from llm_config import create_gemini_client, get_missing_config, validate_config
from utils import (
    extract_json_from_response,
    prepare_resume_context,
    read_json_file,
    validate_job_description_data,
    validate_resume_data,
)


def tailor_resume(resume_path: str, job_description_path: str, output_path: Optional[str] = None) -> Dict[str, Any]:
    """
    Tailor a resume for a specific job description using Gemini AI.

    Args:
        resume_path: Path to the resume JSON file
        job_description_path: Path to the job description JSON file
        output_path: Optional path to save the tailored resume (if None, won't save to file)

    Returns:
        Dictionary containing the tailored resume
    """
    # Load and validate data
    resume_data = read_json_file(resume_path)
    job_data = read_json_file(job_description_path)

    if not validate_resume_data(resume_data):
        raise ValueError("Invalid resume data structure")

    if not validate_job_description_data(job_data):
        raise ValueError("Invalid job description data structure")

    # Prepare the context
    context = prepare_resume_context(resume_data, job_data)

    # Create Gemini client
    client = create_gemini_client()

    try:
        # Generate the tailored resume
        response = client.generate_content(context)

        # Extract the content from the response
        response_text = response.text if response.text else ""

        # Try to extract JSON from the response
        tailored_resume = extract_json_from_response(response_text)

    except Exception as e:
        raise Exception(f"Error generating tailored resume: {str(e)}")

    # Save to file if output path is provided
    if output_path:
        output_file = Path(output_path)
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(tailored_resume, f, indent=2, ensure_ascii=False)
        print(f"Tailored resume saved to: {output_path}")

    return tailored_resume


def main():
    """
    Main function to demonstrate usage of the resume tailoring application.
    """
    if len(sys.argv) < 3:
        print("Usage: python resume_tailor.py <resume_path> <job_description_path> [output_path]")
        print("\nExample:")
        print("  python resume_tailor.py data/resume.json data/job_description.json data/tailored_resume.json")
        sys.exit(1)

    resume_path = sys.argv[1]
    job_description_path = sys.argv[2]
    output_path = sys.argv[3] if len(sys.argv) > 3 else "output/tailored_resume.json"

    # Ensure output directory exists
    output_file = Path(output_path)
    output_file.parent.mkdir(parents=True, exist_ok=True)

    # Validate configuration
    if not validate_config():
        missing = get_missing_config()
        print("Error: Missing required environment variables:")
        for var in missing:
            print(f"  - {var}")
        print("\nPlease set these variables in your .env file.")
        sys.exit(1)

    try:
        print("Reading input files...")
        print(f"Resume: {resume_path}")
        print(f"Job Description: {job_description_path}")
        print("\nTailoring resume... (this may take a moment)")

        tailored_resume = tailor_resume(resume_path, job_description_path, output_path)

        print("\n" + "=" * 50)
        print("Resume tailoring completed successfully!")
        print("=" * 50)
        print("Tailored resume preview:")
        print(json.dumps(tailored_resume, indent=2)[:500] + "...")

    except Exception as e:
        print(f"\nError: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()
