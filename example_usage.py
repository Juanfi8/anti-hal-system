#!/usr/bin/env python
"""
Example script demonstrating how to use the resume tailoring functions.

This script shows how to:
1. Read JSON files
2. Prepare context for the AI
3. Use the tailoring function

Note: To run the full tailoring process, you need a valid GEMINI_API_KEY in your .env file.
"""

from resume_tailor import read_json_file, prepare_resume_context

def main():
    """Demonstrate usage of resume tailoring functions."""
    
    print("=" * 60)
    print("Resume Tailoring System - Example Usage")
    print("=" * 60)
    
    # Example 1: Read JSON files
    print("\n1. Reading JSON files...")
    try:
        resume = read_json_file("data/sample_resume.json")
        job_desc = read_json_file("data/sample_job_description.json")
        
        print(f"✓ Resume loaded: {resume['personal_info']['name']}")
        print(f"✓ Job description loaded: {job_desc['job_title']} at {job_desc['company']}")
        
    except FileNotFoundError as e:
        print(f"✗ Error: {e}")
        return
    
    # Example 2: Prepare context
    print("\n2. Preparing context for AI...")
    context = prepare_resume_context(
        "data/sample_resume.json",
        "data/sample_job_description.json"
    )
    
    print(f"✓ Context prepared ({len(context)} characters)")
    print("\nContext preview (first 500 chars):")
    print("-" * 60)
    print(context[:500])
    print("...")
    print("-" * 60)
    
    # Example 3: Instructions for full tailoring
    print("\n3. To run full resume tailoring:")
    print("   - Set GEMINI_API_KEY in .env file")
    print("   - Run: python resume_tailor.py data/sample_resume.json data/sample_job_description.json output.json")
    
    print("\n" + "=" * 60)
    print("Example completed successfully!")
    print("=" * 60)

if __name__ == "__main__":
    main()
