"""
Utility functions for Resume Tailoring Application

This module contains utility functions for data loading, validation, and processing.
"""

import json
from pathlib import Path
from typing import Any, Dict


def read_json_file(file_path: str) -> Dict[str, Any]:
    """
    Read and parse a JSON file from the local filesystem.

    Args:
        file_path: Path to the JSON file

    Returns:
        Dictionary containing the parsed JSON data

    Raises:
        FileNotFoundError: If the file doesn't exist
        json.JSONDecodeError: If the file contains invalid JSON
    """
    file_path_obj = Path(file_path)

    if not file_path_obj.exists():
        raise FileNotFoundError(f"File not found: {file_path}")

    try:
        with open(file_path_obj, "r", encoding="utf-8") as file:
            data = json.load(file)
        return data
    except json.JSONDecodeError as e:
        raise json.JSONDecodeError(f"Invalid JSON in file {file_path}: {str(e)}", e.doc, e.pos)


def validate_resume_data(data: Dict[str, Any]) -> bool:
    """
    Basic validation for resume data structure.

    Args:
        data: Resume data dictionary

    Returns:
        True if data appears valid, False otherwise
    """
    required_fields = ["personal_info", "work_experience", "education", "skills"]
    return all(field in data for field in required_fields)


def validate_job_description_data(data: Dict[str, Any]) -> bool:
    """
    Basic validation for job description data structure.

    Args:
        data: Job description data dictionary

    Returns:
        True if data appears valid, False otherwise
    """
    required_fields = ["Job Title", "responsibilities", "technical_skills"]
    return all(field in data for field in required_fields)


def prepare_resume_context(resume_data: Dict[str, Any], job_data: Dict[str, Any]) -> str:
    """
    Prepare the context string for the AI prompt.

    Args:
        resume_data: Resume data dictionary
        job_data: Job description data dictionary

    Returns:
        Formatted context string for the prompt
    """
    context = f"""
I am a highly experienced career advisor and resume writing expert with 15 years of specialized experience.

Primary role: Craft exceptional resumes tailored to specific job descriptions, optimized for both ATS systems and human readers.

# Instructions for creating optimized resumes
1. Analyze job descriptions:
   - Extract key requirements and keywords
   - Note: Adapt analysis based on specific industry and role

2. Create compelling resumes:
   - Highlight quantifiable achievements (e.g., "Engineered a dynamic UI form generator using optimal design patterns and efficient OOP, reducing development time by 87.5%")
   - Tailor content to specific job and company
   - Emphasize candidate's unique value proposition

3. Optimize for Applicant Tracking Systems (ATS):
   - Use industry-specific keywords strategically throughout documents
   - Ensure content passes ATS scans while engaging human readers

4. Provide industry-specific guidance:
   - Incorporate current hiring trends
   - Prioritize relevant information (apply "6-second rule" for quick scanning)
   - Use clear, consistent formatting

5. Apply best practices:
   - Quantify achievements where possible
   - Use specific, impactful statements instead of generic ones
   - Update content based on latest industry standards
   - Use active voice and strong action verbs

ORIGINAL RESUME:
{json.dumps(resume_data, indent=2)}

JOB DESCRIPTION:
{json.dumps(job_data, indent=2)}

Note: Adapt these guidelines to each user's specific request, industry, and experience level.

Goal: Create a resume that not only pass ATS screenings but also compellingly demonstrate how the user can add immediate value to the prospective employer. Please provide the tailored resume as a valid JSON object, following the same structure as the original resume and keeping the order of sections intact. Do not include the personal summary. Do not use **bold** or other markdown formatting.
"""
    return context


def extract_json_from_response(response_text: str) -> Dict[str, Any]:
    """
    Extract JSON from the AI response.

    Args:
        response_text: Raw response text from AI

    Returns:
        Parsed JSON dictionary

    Raises:
        ValueError: If JSON cannot be extracted
    """
    import re

    # Try to find JSON in code blocks first
    json_match = re.search(r"```json\s*(.*?)\s*```", response_text, re.DOTALL)
    if json_match:
        try:
            return json.loads(json_match.group(1))
        except json.JSONDecodeError:
            pass

    # Try to find JSON object in the response
    json_match = re.search(r"\{.*\}", response_text, re.DOTALL)
    if json_match:
        try:
            return json.loads(json_match.group(0))
        except json.JSONDecodeError:
            pass

    # Try to parse the entire response
    try:
        return json.loads(response_text)
    except json.JSONDecodeError:
        pass

    # If all else fails, return the raw response
    return {"raw_response": response_text, "error": "Could not parse JSON from response"}
