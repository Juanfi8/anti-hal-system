def format_resume_as_text(resume_json):
    """
    Convert structured resume JSON to natural language text.
    This creates a comprehensive text representation for AlignScore comparison.

    Args:
        resume_json (dict): Structured resume data

    Returns:
        str: Natural language text representation
    """
    text_parts = []

    # Personal Information
    if "personal_info" in resume_json:
        personal = resume_json["personal_info"]
        personal_text = format_personal_info(personal)
        if personal_text:
            text_parts.append(personal_text)

    # Education
    if "education" in resume_json:
        education_text = format_education(resume_json["education"])
        if education_text:
            text_parts.append(education_text)

    # Work Experience
    if "work_experience" in resume_json:
        work_text = format_work_experience(resume_json["work_experience"])
        if work_text:
            text_parts.append(work_text)

    # Skills
    if "skills" in resume_json:
        skills_text = format_skills(resume_json["skills"])
        if skills_text:
            text_parts.append(skills_text)

    # Projects (if any)
    if "projects" in resume_json:
        projects_text = format_projects(resume_json["projects"])
        if projects_text:
            text_parts.append(projects_text)

    # Join all parts with double newlines
    return "\n\n".join(text_parts)


def format_personal_info(personal):
    """Format personal information section."""
    parts = []

    if "name" in personal:
        parts.append(f"Name: {personal['name']}")

    if "email" in personal:
        parts.append(f"Email: {personal['email']}")

    if "phone" in personal:
        parts.append(f"Phone: {personal['phone']}")

    if "location" in personal:
        parts.append(f"Location: {personal['location']}")

    if "github" in personal:
        parts.append(f"GitHub: {personal['github']}")

    if "linkedin" in personal:
        parts.append(f"LinkedIn: {personal['linkedin']}")

    if "website" in personal:
        parts.append(f"Website: {personal['website']}")

    return ". ".join(parts) + "." if parts else ""


def format_work_experience(work_list):
    """Format work experience section."""
    if not work_list:
        return ""

    experiences = []
    for job in work_list:
        job_parts = []

        # Job title and company
        title = job.get("title", "Position")
        company = job.get("company", "Company")
        job_parts.append(f"{title} at {company}")

        # Dates
        start_date = job.get("start_date", "")
        end_date = job.get("end_date", "Present")
        if start_date:
            job_parts.append(f"from {start_date} to {end_date}")

        # Location
        if "location" in job:
            job_parts.append(f"in {job['location']}")

        # Create header
        header = " ".join(job_parts) + "."

        # Responsibilities/achievements
        responsibilities = []
        if "responsibilities" in job:
            if isinstance(job["responsibilities"], list):
                responsibilities = list(job["responsibilities"])  # Create a copy
            else:
                responsibilities = [job["responsibilities"]]

        if "achievements" in job:
            if isinstance(job["achievements"], list):
                responsibilities.extend(job["achievements"])
            else:
                responsibilities.append(job["achievements"])

        # Description
        if "description" in job:
            responsibilities.insert(0, job["description"])

        # Format the full job entry
        job_text = header
        if responsibilities:
            resp_text = " ".join(responsibilities)
            job_text += f" {resp_text}"

        experiences.append(job_text)

    return " ".join(experiences)


def format_education(education_list):
    """Format education section."""
    if not education_list:
        return ""

    education_entries = []
    for edu in education_list:
        edu_parts = []

        # Degree and field/major
        degree = edu.get("degree", "")
        major = edu.get("major", edu.get("field", ""))

        if degree and major:
            edu_parts.append(f"{degree} in {major}")
        elif degree:
            edu_parts.append(degree)
        elif major:
            edu_parts.append(f"Studies in {major}")

        # Institution
        if "institution" in edu or "school" in edu:
            institution = edu.get("institution", edu.get("school", ""))
            edu_parts.append(f"from {institution}")

        # Graduation date
        if "graduation_date" in edu:
            edu_parts.append(f"graduated in {edu['graduation_date']}")
        elif "end_date" in edu:
            edu_parts.append(f"graduated in {edu['end_date']}")
        elif "year" in edu:
            edu_parts.append(f"graduated in {edu['year']}")

        # GPA
        if "gpa" in edu:
            edu_parts.append(f"with GPA {edu['gpa']}")

        # Location
        if "location" in edu:
            edu_parts.append(f"in {edu['location']}")

        education_entries.append(" ".join(edu_parts) + ".")

        # Relevant courses - add as separate sentence
        if "relevant_courses" in edu:
            courses = edu["relevant_courses"]
            if isinstance(courses, list):
                courses_str = ", ".join(courses)
            else:
                courses_str = courses
            education_entries.append(f"Relevant courses: {courses_str}.")

    return " ".join(education_entries)


def format_skills(skills):
    """Format skills section."""
    if not skills:
        return ""

    if isinstance(skills, dict):
        # If skills are categorized
        skill_parts = []
        processed_categories = set()

        # Define the order of standard categories
        standard_categories = ["technical", "languages", "tools", "soft_skills"]

        # Process standard categories in order
        for category in standard_categories:
            if category in skills:
                skill_list = skills[category]
                if isinstance(skill_list, list):
                    skills_str = ", ".join(skill_list)
                else:
                    skills_str = skill_list
                # Capitalize category name for display
                display_name = category.replace("_", " ").title()
                skill_parts.append(f"{display_name}: {skills_str}")
                processed_categories.add(category)

        # Process any other categories not in the standard list
        for category, skill_list in skills.items():
            if category not in processed_categories:
                if isinstance(skill_list, list):
                    skills_str = ", ".join(skill_list)
                else:
                    skills_str = skill_list
                display_name = category.replace("_", " ").title()
                skill_parts.append(f"{display_name}: {skills_str}")

        return ". ".join(skill_parts) + "."

    elif isinstance(skills, list):
        # If skills are a flat list
        return "Skills include " + ", ".join(skills) + "."

    else:
        return f"Skills include {skills}."


def format_projects(projects):
    """Format projects section."""
    if not projects:
        return ""

    project_entries = []
    for project in projects:
        if isinstance(project, dict):
            proj_parts = []

            name = project.get("name", project.get("title", ""))
            if name:
                proj_parts.append(f"Project: {name}")

            description = project.get("description", "")
            if description:
                proj_parts.append(description)

            technologies = project.get("technologies", project.get("tech_stack", []))
            if technologies:
                if isinstance(technologies, list):
                    tech_str = ", ".join(technologies)
                else:
                    tech_str = technologies
                proj_parts.append(f"Technologies used: {tech_str}.")

            date = project.get("date", project.get("year", ""))
            if date:
                proj_parts.append(f"in {date}")

            # Achievements
            achievements = project.get("achievements", [])
            if achievements:
                if isinstance(achievements, list):
                    achieve_str = " ".join(achievements)
                else:
                    achieve_str = achievements
                proj_parts.append(achieve_str)

            # URL
            if "url" in project:
                proj_parts.append(f"(Repository: {project['url']})")

            project_entries.append(" ".join(proj_parts) + ".")
        else:
            project_entries.append(str(project))

    return " ".join(project_entries)
