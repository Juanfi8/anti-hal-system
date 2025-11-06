# Resume Tailoring System with Gemini AI

An AI-powered resume tailoring application that uses Google's Gemini AI to customize resumes for specific job descriptions.

## Installation

1. Clone the repository:
```bash
git clone https://github.com/Juanfi8/anti-hal-system.git
cd anti-hal-system
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up your environment variables:
```bash
cp .env.example .env
# Edit .env and add your GEMINI_API_KEY
```

## Usage

### Command Line Interface

Basic usage:
```bash
python resume_tailor.py <resume_path> <job_description_path> [output_path]
```

Example:
```bash
python resume_tailor.py data/sample_resume.json data/sample_job_description.json
# Output will be saved to output/tailored_resume.json by default

# Or specify a custom output path:
python resume_tailor.py data/sample_resume.json data/sample_job_description.json custom_output.json
```

### Programmatic Usage

```python
from resume_tailor import tailor_resume, read_json_file, prepare_resume_context

# Tailor a resume (saves to output/tailored_resume.json by default)
tailored_resume = tailor_resume(
    resume_path="data/sample_resume.json",
    job_description_path="data/sample_job_description.json"
)

# Or specify a custom output path:
tailored_resume = tailor_resume(
    resume_path="data/sample_resume.json",
    job_description_path="data/sample_job_description.json",
    output_path="output/tailored_resume.json"
)

# Read JSON files separately
resume = read_json_file("data/sample_resume.json")
job_desc = read_json_file("data/sample_job_description.json")

# Prepare context for custom processing
context = prepare_resume_context(
    "data/sample_resume.json",
    "data/sample_job_description.json"
)
```

## JSON Format

### Resume JSON Structure

```json
{
  "personal_info": {
    "name": "Your Name",
    "email": "your.email@example.com",
    "phone": "+1-555-0123",
    "location": "City, State",
    "linkedin": "linkedin.com/in/yourprofile",
    "github": "github.com/yourprofile"
  },
  "professional_summary": "Your professional summary here...",
  "skills": ["Skill1", "Skill2", "Skill3"],
  "experience": [
    {
      "title": "Job Title",
      "company": "Company Name",
      "location": "City, State",
      "start_date": "YYYY-MM",
      "end_date": "YYYY-MM or Present",
      "responsibilities": ["Responsibility 1", "Responsibility 2"]
    }
  ],
  "education": [
    {
      "degree": "Degree Name",
      "institution": "University Name",
      "location": "City, State",
      "graduation_date": "YYYY-MM"
    }
  ],
  "projects": [
    {
      "name": "Project Name",
      "description": "Project description",
      "technologies": ["Tech1", "Tech2"]
    }
  ],
  "certifications": ["Certification 1", "Certification 2"]
}
```

### Job Description JSON Structure

```json
{
  "job_title": "Job Title",
  "company": "Company Name",
  "location": "City, State",
  "job_type": "Full-time/Part-time/Contract",
  "description": "Job description...",
  "responsibilities": ["Responsibility 1", "Responsibility 2"],
  "required_qualifications": ["Qualification 1", "Qualification 2"],
  "preferred_qualifications": ["Preferred 1", "Preferred 2"],
  "technical_skills": ["Skill1", "Skill2"]
}
```

## Sample Data

The repository includes sample files in the `data/` directory:
- `sample_resume.json`: Example resume
- `sample_job_description.json`: Example job description

You can use these to test the application or as templates for your own data.

## How It Works

1. **Read Input Files**: The application reads your resume and job description from JSON files
2. **Context Preparation**: Combines both inputs into a structured prompt with detailed instructions
3. **AI Processing**: Uses Google's Gemini AI to analyze and tailor the resume
4. **Smart Modifications**: The AI identifies relevant sections to modify while preserving factual information
5. **Output Generation**: Produces a tailored resume in JSON format

## Configuration

### Gemini Model Configuration

You can customize the model configuration in `resume_tailor.py`:

```python
generation_config = {
    "temperature": 0.7,        # Adjust for creativity (0.0-1.0)
    "top_p": 0.95,             # Nucleus sampling parameter
    "top_k": 40,               # Top-k sampling parameter
    "max_output_tokens": 8192, # Maximum length of output
}

model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",  # Or "gemini-1.5-pro" for better quality
    generation_config=generation_config,
)
```

## Troubleshooting

### API Key Issues
- Make sure your `.env` file contains a valid `GEMINI_API_KEY`
- Verify your API key at [Google AI Studio](https://makersuite.google.com/app/apikey)

### JSON Parsing Errors
- Ensure your JSON files are valid (use a JSON validator)
- Check for proper UTF-8 encoding

### Import Errors
- Make sure all dependencies are installed: `pip install -r requirements.txt`

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is open source and available under the MIT License.

## Disclaimer

This tool is designed to help tailor resumes by emphasizing relevant experience and skills. It should not be used to fabricate experience or qualifications. Always ensure that your tailored resume accurately represents your actual skills and experience.
