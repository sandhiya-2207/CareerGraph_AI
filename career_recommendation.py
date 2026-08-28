import pandas as pd


def calculate_career_scores(data, user_skills):

    user_skills = set(
        skill.strip().title()
        for skill in user_skills
        if skill.strip()
    )

    career_scores = {}

    for career in data["Job_Role"].unique():

        career_data = data[
            data["Job_Role"] == career
        ]

        total_importance = career_data[
            "Importance"
        ].sum()

        matched_importance = career_data[
            career_data["Skill"].isin(user_skills)
        ]["Importance"].sum()

        if total_importance > 0:

            score = (
                matched_importance
                / total_importance
            ) * 100

        else:

            score = 0

        career_scores[career] = round(score, 2)

    return career_scores