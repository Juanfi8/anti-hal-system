"""
Unit tests for resume_tailor.py

Tests the core functions for reading JSON files and preparing context.
"""

import json
import os
import tempfile
import unittest
from resume_tailor import read_json_file, prepare_resume_context


class TestResumeJsonReader(unittest.TestCase):
    """Test cases for JSON file reading functionality."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.temp_dir = tempfile.mkdtemp()
        
        # Sample resume data
        self.sample_resume = {
            "personal_info": {
                "name": "Test User",
                "email": "test@example.com"
            },
            "skills": ["Python", "JavaScript"],
            "experience": []
        }
        
        # Sample job description data
        self.sample_job = {
            "job_title": "Software Engineer",
            "company": "Test Corp",
            "required_qualifications": ["Python", "JavaScript"]
        }
        
        # Create temp files
        self.resume_path = os.path.join(self.temp_dir, "test_resume.json")
        self.job_path = os.path.join(self.temp_dir, "test_job.json")
        
        with open(self.resume_path, 'w') as f:
            json.dump(self.sample_resume, f)
        
        with open(self.job_path, 'w') as f:
            json.dump(self.sample_job, f)
    
    def tearDown(self):
        """Clean up test files."""
        import shutil
        if os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir)
    
    def test_read_json_file_success(self):
        """Test successful reading of a JSON file."""
        result = read_json_file(self.resume_path)
        self.assertEqual(result, self.sample_resume)
        self.assertIn("personal_info", result)
        self.assertEqual(result["personal_info"]["name"], "Test User")
    
    def test_read_json_file_not_found(self):
        """Test that FileNotFoundError is raised for non-existent files."""
        with self.assertRaises(FileNotFoundError):
            read_json_file("/nonexistent/path/file.json")
    
    def test_read_json_file_invalid_json(self):
        """Test that JSONDecodeError is raised for invalid JSON."""
        invalid_json_path = os.path.join(self.temp_dir, "invalid.json")
        with open(invalid_json_path, 'w') as f:
            f.write("{ invalid json content")
        
        with self.assertRaises(json.JSONDecodeError):
            read_json_file(invalid_json_path)
    
    def test_prepare_resume_context(self):
        """Test context preparation with resume and job description."""
        context = prepare_resume_context(self.resume_path, self.job_path)
        
        # Check that context is a string
        self.assertIsInstance(context, str)
        
        # Check that context contains both resume and job description
        self.assertIn("ORIGINAL RESUME", context)
        self.assertIn("JOB DESCRIPTION", context)
        self.assertIn("INSTRUCTIONS", context)
        
        # Check that actual data is present
        self.assertIn("Test User", context)
        self.assertIn("Software Engineer", context)
        self.assertIn("Test Corp", context)
    
    def test_prepare_resume_context_instructions(self):
        """Test that context includes proper instructions."""
        context = prepare_resume_context(self.resume_path, self.job_path)
        
        # Check for key instructions
        self.assertIn("tailor", context.lower())
        self.assertIn("skills", context.lower())
        self.assertIn("json", context.lower())
        self.assertIn("contact information", context.lower())


class TestDataIntegrity(unittest.TestCase):
    """Test cases to ensure data integrity."""
    
    def test_sample_resume_structure(self):
        """Test that sample resume has required structure."""
        resume_path = "data/sample_resume.json"
        if os.path.exists(resume_path):
            resume = read_json_file(resume_path)
            
            # Check required top-level keys
            self.assertIn("personal_info", resume)
            self.assertIn("skills", resume)
            self.assertIn("experience", resume)
            
            # Check personal info structure
            self.assertIn("name", resume["personal_info"])
            self.assertIn("email", resume["personal_info"])
    
    def test_sample_job_description_structure(self):
        """Test that sample job description has required structure."""
        job_path = "data/sample_job_description.json"
        if os.path.exists(job_path):
            job = read_json_file(job_path)
            
            # Check required keys
            self.assertIn("job_title", job)
            self.assertIn("responsibilities", job)
            self.assertIn("required_qualifications", job)


if __name__ == "__main__":
    unittest.main()
