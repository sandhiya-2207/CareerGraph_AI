import pandas as pd


def calculate_career_scores(data, user_skills):
    """
    Calculate weighted skill-match percentage
    for every career.
    """

    # Convert user skills into a clean set
    user_skills = set(
        skill.strip().title()
        for skill in user_skills
        if skill.strip()
    )

    career_scores = {}

    # Check every career
    for career in data["Job_Role"].unique():

        career_data = data[
            data["Job_Role"] == career
        ]

        # Total importance of all skills
        total_importance = career_data[
            "Importance"
        ].sum()

        # Importance of skills the user already has
        matched_importance = career_data[
            career_data["Skill"].isin(user_skills)
        ]["Importance"].sum()

        # Calculate percentage
        if total_importance > 0:
            score = (
                matched_importance / total_importance
            ) * 100
        else:
            score = 0

        career_scores[career] = round(score, 2)

    return career_scores