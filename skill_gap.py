def calculate_skill_gap(required_skills, user_skills):

    # Clean and normalize user skills
    user_skills_clean = set(
        skill.strip().lower()
        for skill in user_skills
        if skill.strip()
    )

    # Clean and normalize required skills
    required_skills_clean = [
        skill.strip()
        for skill in required_skills
        if skill.strip()
    ]

    matched_skills = []
    missing_skills = []

    # Check every required skill
    for skill in required_skills_clean:

        if skill.lower() in user_skills_clean:

            matched_skills.append(skill)

        else:

            missing_skills.append(skill)

    return matched_skills, missing_skills