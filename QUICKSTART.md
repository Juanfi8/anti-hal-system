# Quick Start Guide

This guide will help you get started with the Resume Tailoring System quickly.

## Prerequisites

1. Python 3.8 or higher
2. Google Gemini API key

## Setup (5 minutes)

### 1. Get Your Gemini API Key

1. Visit https://makersuite.google.com/app/apikey
2. Sign in with your Google account
3. Click "Create API Key"
4. Copy your API key

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure API Key

```bash
cp .env.example .env
# Edit .env and replace 'your_gemini_api_key_here' with your actual API key
```

## Usage

### Basic Example

```bash
python resume_tailor.py data/sample_resume.json data/sample_job_description.json tailored_resume.json
```

### Using Your Own Data

1. Create your resume JSON file (see `data/sample_resume.json` for format)
2. Create your job description JSON file (see `data/sample_job_description.json` for format)
3. Run the tailoring command:

```bash
python resume_tailor.py path/to/your_resume.json path/to/job_description.json output.json
```

## Testing Without API Key

Run the example script to test the JSON reading and context preparation without needing an API key:

```bash
python example_usage.py
```

## Troubleshooting

### "GEMINI_API_KEY not found"
- Make sure you've created the `.env` file
- Check that your API key is correctly set in `.env`
- Ensure there are no extra spaces or quotes around the API key

### "Invalid JSON" error
- Validate your JSON files at https://jsonlint.com/
- Make sure files are UTF-8 encoded
- Check for missing commas or brackets

### API Rate Limits
- Gemini has rate limits based on your usage tier
- If you hit limits, wait a few moments before retrying
- Consider upgrading your API tier for higher limits

## Next Steps

- Customize the prompt in `prepare_resume_context()` for your specific needs
- Adjust the model configuration in `create_gemini_config()` for different quality/speed tradeoffs
- Add your own validation logic to ensure tailored resumes meet your standards

## Support

For issues or questions:
1. Check the full README.md for detailed documentation
2. Review the example files in the `data/` directory
3. Run the test suite: `python -m unittest test_resume_tailor -v`
