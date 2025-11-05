"""
Resume Tailoring Application using AutoGen and Gemini AI

This module provides functionality to tailor a person's resume for a specific
job description using AutoGen agents powered by Google's Gemini AI.
"""

import json
import os
from typing import Dict, Any
from dotenv import load_dotenv
import autogen

# Load environment variables
load_dotenv()


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
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
        return data
    except FileNotFoundError:
        raise FileNotFoundError(f"File not found: {file_path}")
    except json.JSONDecodeError as e:
        raise json.JSONDecodeError(f"Invalid JSON in file {file_path}: {str(e)}", e.doc, e.pos)


def prepare_resume_context(resume_path: str, job_description_path: str) -> str:
    """
    Read resume and job description JSON files and prepare context for the prompt.
    
    Args:
        resume_path: Path to the resume JSON file
        job_description_path: Path to the job description JSON file
        
    Returns:
        Formatted string containing both resume and job description context
    """
    resume = read_json_file(resume_path)
    job_description = read_json_file(job_description_path)
    
    context = f"""
Please tailor the following resume for the given job description.

ORIGINAL RESUME:
{json.dumps(resume, indent=2)}

JOB DESCRIPTION:
{json.dumps(job_description, indent=2)}

INSTRUCTIONS:
1. Analyze the job description and identify key requirements, skills, and qualifications
2. Review the resume and identify sections that need modification to better match the job
3. Keep contact information, education dates, and factual employment history unchanged
4. Modify the following sections to align with the job description:
   - Professional summary/objective
   - Skills section (emphasize relevant skills, reorder if needed)
   - Work experience descriptions (highlight relevant achievements and responsibilities)
   - Project descriptions (if applicable)
5. Use keywords from the job description naturally in the tailored resume
6. Maintain honesty - do not fabricate experience or skills
7. Output the tailored resume in the same JSON format as the input

Please provide the tailored resume as a valid JSON object.
"""
    return context


def create_gemini_config(api_key: str = None) -> Dict[str, Any]:
    """
    Create configuration for Gemini AI model.
    
    Args:
        api_key: Google Gemini API key (if None, will try to get from environment)
        
    Returns:
        Configuration dictionary for AutoGen
    """
    if api_key is None:
        api_key = os.getenv("GEMINI_API_KEY")
    
    if not api_key:
        raise ValueError("GEMINI_API_KEY not found. Please set it in .env file or pass as parameter.")
    
    config_list = [
        {
            "model": "gemini-pro",
            "api_key": api_key,
            "api_type": "google"
        }
    ]
    
    llm_config = {
        "config_list": config_list,
        "temperature": 0.7,
        "timeout": 120,
    }
    
    return llm_config


def tailor_resume(resume_path: str, job_description_path: str, output_path: str = None) -> Dict[str, Any]:
    """
    Tailor a resume for a specific job description using AutoGen agents.
    
    Args:
        resume_path: Path to the resume JSON file
        job_description_path: Path to the job description JSON file
        output_path: Optional path to save the tailored resume (if None, won't save to file)
        
    Returns:
        Dictionary containing the tailored resume
    """
    # Prepare the context
    context = prepare_resume_context(resume_path, job_description_path)
    
    # Create LLM configuration
    llm_config = create_gemini_config()
    
    # Create AutoGen agents
    assistant = autogen.AssistantAgent(
        name="resume_tailor",
        llm_config=llm_config,
        system_message="""You are an expert resume writer and career counselor.
        Your task is to tailor resumes to match specific job descriptions while maintaining
        accuracy and honesty. You understand ATS (Applicant Tracking Systems) and know how
        to optimize resumes with relevant keywords. You always output valid JSON format."""
    )
    
    user_proxy = autogen.UserProxyAgent(
        name="user",
        human_input_mode="NEVER",
        max_consecutive_auto_reply=1,
        code_execution_config=False,
    )
    
    # Initiate the conversation
    user_proxy.initiate_chat(
        assistant,
        message=context
    )
    
    # Extract the tailored resume from the conversation
    # Get the last message from the assistant
    last_message = user_proxy.last_message()
    
    if last_message and "content" in last_message:
        response_content = last_message["content"]
        
        # Try to extract JSON from the response
        try:
            # Find JSON in the response (it might be wrapped in markdown code blocks)
            import re
            json_match = re.search(r'```json\s*(.*?)\s*```', response_content, re.DOTALL)
            if json_match:
                tailored_resume = json.loads(json_match.group(1))
            else:
                # Try to parse the entire response as JSON
                tailored_resume = json.loads(response_content)
        except json.JSONDecodeError:
            # If parsing fails, return the response as-is
            print("Warning: Could not parse response as JSON. Returning raw response.")
            tailored_resume = {"raw_response": response_content}
    else:
        raise ValueError("No response received from the assistant")
    
    # Save to file if output path is provided
    if output_path:
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(tailored_resume, f, indent=2, ensure_ascii=False)
        print(f"Tailored resume saved to: {output_path}")
    
    return tailored_resume


def main():
    """
    Main function to demonstrate usage of the resume tailoring application.
    """
    import sys
    
    if len(sys.argv) < 3:
        print("Usage: python resume_tailor.py <resume_path> <job_description_path> [output_path]")
        print("\nExample:")
        print("  python resume_tailor.py data/resume.json data/job_description.json data/tailored_resume.json")
        sys.exit(1)
    
    resume_path = sys.argv[1]
    job_description_path = sys.argv[2]
    output_path = sys.argv[3] if len(sys.argv) > 3 else "tailored_resume.json"
    
    try:
        print("Reading input files...")
        print(f"Resume: {resume_path}")
        print(f"Job Description: {job_description_path}")
        print("\nTailoring resume... (this may take a moment)")
        
        tailored_resume = tailor_resume(resume_path, job_description_path, output_path)
        
        print("\n" + "="*50)
        print("Resume tailoring completed successfully!")
        print("="*50)
        print(f"\nTailored resume preview:")
        print(json.dumps(tailored_resume, indent=2)[:500] + "...")
        
    except Exception as e:
        print(f"\nError: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()
