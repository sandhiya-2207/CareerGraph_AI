import os
import pandas as pd
import streamlit as st

st.write("Current folder:", os.getcwd())
st.write("Files:", os.listdir("."))

st.write("Data folder exists:", os.path.exists("data"))

if os.path.exists("data"):
    st.write("Data folder files:", os.listdir("data"))


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="CareerGraph AI",
    page_icon="🎯",
    layout="wide"
)


# ============================================================
# LOAD DATA
# ============================================================

# Find the main CareerGraph_AI folder automatically
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Correct location of career_data.csv
DATA_PATH = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "data",
    "career_data.csv"
)

# Check whether the CSV file exists
if not os.path.exists(DATA_PATH):
    st.error("career_data.csv was not found.")
    st.write("Python is looking for the file here:")
    st.code(DATA_PATH)
    st.stop()


# Read CSV file
data = pd.read_csv(DATA_PATH)


# ============================================================
# FIND THE REQUIRED COLUMNS
# ============================================================

# Job role column
job_column = None

possible_job_columns = [
    "Job_Role",
    "Job Role",
    "JobRole",
    "Career",
    "Career_Role",
    "Role"
]

for column in possible_job_columns:
    if column in data.columns:
        job_column = column
        break


# Skill column
skill_column = None

possible_skill_columns = [
    "Skills",
    "Skill",
    "Required_Skills",
    "Required Skills",
    "Skill_Set",
    "Skill Set"
]

for column in possible_skill_columns:
    if column in data.columns:
        skill_column = column
        break


# If the expected columns are not found
if job_column is None:
    st.error("Job Role column was not found in career_data.csv.")
    st.write("Columns found in your CSV:")
    st.write(list(data.columns))
    st.stop()


if skill_column is None:
    st.error("Skills column was not found in career_data.csv.")
    st.write("Columns found in your CSV:")
    st.write(list(data.columns))
    st.stop()


# ============================================================
# CLEAN DATA
# ============================================================

data[job_column] = data[job_column].astype(str).str.strip()
data[skill_column] = data[skill_column].astype(str).str.strip()


# ============================================================
# FUNCTION TO CONVERT SKILLS INTO A LIST
# ============================================================

def split_skills(skill_text):

    if pd.isna(skill_text):
        return []

    skill_text = str(skill_text)

    # Support different separators
    for separator in [";", "|", ","]:
        if separator in skill_text:
            skills = skill_text.split(separator)
            return [
                skill.strip()
                for skill in skills
                if skill.strip()
            ]

    # If only one skill exists
    return [skill_text.strip()]


# ============================================================
# CREATE CAREER → SKILLS MAPPING
# ============================================================

career_skills = {}

for _, row in data.iterrows():

    career = row[job_column]

    skills = split_skills(row[skill_column])

    if career not in career_skills:
        career_skills[career] = set()

    for skill in skills:
        if skill:
            career_skills[career].add(skill)


# ============================================================
# NORMALIZE SKILLS
# ============================================================

def normalize_skill(skill):

    return (
        str(skill)
        .strip()
        .lower()
        .replace("-", " ")
        .replace("_", " ")
    )


# ============================================================
# PAGE TITLE
# ============================================================

st.title("🎯 CareerGraph AI")

st.subheader(
    "Data-Driven Skill-to-Career Intelligence System"
)

st.write(
    "Map your current skills → identify missing skills → "
    "discover suitable careers → build your learning priorities."
)


# ============================================================
# SIDEBAR
# ============================================================

st.sidebar.header("🧑‍💻 Your Skills")

st.sidebar.write(
    "Enter the skills you already know."
)

user_input = st.sidebar.text_area(
    "Current Skills",
    placeholder="Example:\nPython\nSQL\nExcel",
    height=150
)


# ============================================================
# CONVERT USER INPUT INTO SKILLS
# ============================================================

if user_input.strip():

    # Accept comma, newline and semicolon
    user_skills = (
        user_input
        .replace(",", "\n")
        .replace(";", "\n")
        .split("\n")
    )

    user_skills = [
        skill.strip()
        for skill in user_skills
        if skill.strip()
    ]

else:

    user_skills = []


normalized_user_skills = {
    normalize_skill(skill)
    for skill in user_skills
}


# ============================================================
# SHOW USER SKILLS
# ============================================================

if user_skills:

    st.write("### ✅ Your Current Skills")

    skill_text = " • ".join(user_skills)

    st.info(skill_text)

else:

    st.info(
        "Enter your current skills in the sidebar to generate "
        "career recommendations."
    )


# ============================================================
# CAREER CALCULATION
# ============================================================

career_results = []


for career, required_skill_set in career_skills.items():

    required_skills = list(required_skill_set)

    normalized_required = {
        normalize_skill(skill)
        for skill in required_skills
    }

    # Skills already known by user
    matched_skills = []

    for skill in required_skills:

        if normalize_skill(skill) in normalized_user_skills:

            matched_skills.append(skill)


    # Skills user still needs
    missing_skills = []

    for skill in required_skills:

        if normalize_skill(skill) not in normalized_user_skills:

            missing_skills.append(skill)


    # Calculate career match percentage
    total_required = len(required_skills)

    if total_required > 0:

        match_percentage = (
            len(matched_skills) /
            total_required
        ) * 100

    else:

        match_percentage = 0


    career_results.append({

        "Career": career,

        "Match Percentage": round(
            match_percentage,
            2
        ),

        "Matched Skills": matched_skills,

        "Skills to Develop": missing_skills,

        "Required Skills": required_skills

    })


# ============================================================
# SORT CAREERS
# ============================================================

career_results = sorted(
    career_results,
    key=lambda x: x["Match Percentage"],
    reverse=True
)


# ============================================================
# DISPLAY RESULTS
# ============================================================

if user_skills and career_results:

    st.divider()

    st.header("📊 Career Recommendations")

    st.write(
        "Careers are ranked according to how closely "
        "your current skills match the required skills."
    )


    # ========================================================
    # TOP CAREER
    # ========================================================

    top_career = career_results[0]

    st.success(
        f"🏆 Best Career Match: "
        f"{top_career['Career']} "
        f"({top_career['Match Percentage']}%)"
    )


    # ========================================================
    # SUMMARY CARDS
    # ========================================================

    col1, col2, col3 = st.columns(3)

    with col1:

        st.metric(
            "Current Skills",
            len(user_skills)
        )

    with col2:

        st.metric(
            "Careers Analyzed",
            len(career_results)
        )

    with col3:

        st.metric(
            "Top Match",
            f"{top_career['Match Percentage']}%"
        )


    st.divider()


    # ========================================================
    # CAREER TABLE
    # ========================================================

    st.subheader("🔗 Career Skill Connections")


    table_data = []


    for index, result in enumerate(career_results):

        matched = result["Matched Skills"]

        missing = result["Skills to Develop"]

        required = result["Required Skills"]


        matched_text = (
            ", ".join(matched)
            if matched
            else "None"
        )


        missing_text = (
            ", ".join(missing)
            if missing
            else "None"
        )


        required_text = (
            ", ".join(required)
            if required
            else "None"
        )


        table_data.append({

            "Rank": index + 1,

            "Career": result["Career"],

            "Career Match %":
                f"{result['Match Percentage']}%",

            "Skills You Have":
                matched_text,

            "Skills to Develop":
                missing_text,

            "Skills Required":
                required_text

        })


    result_df = pd.DataFrame(table_data)


    st.dataframe(
        result_df,
        use_container_width=True,
        hide_index=True
    )


    # ========================================================
    # DETAILED CAREER ANALYSIS
    # ========================================================

    st.divider()

    st.header("🎓 Detailed Career Skill Gap")


    selected_career = st.selectbox(
        "Select a career to view the skill gap:",
        [
            result["Career"]
            for result in career_results
        ]
    )


    selected_result = None


    for result in career_results:

        if result["Career"] == selected_career:

            selected_result = result

            break


    if selected_result:

        col1, col2 = st.columns(2)


        # ====================================================
        # MATCHED SKILLS
        # ====================================================

        with col1:

            st.subheader("✅ Skills You Already Have")

            if selected_result["Matched Skills"]:

                for skill in selected_result["Matched Skills"]:

                    st.write(
                        f"✅ {skill}"
                    )

            else:

                st.write(
                    "No matching skills yet."
                )


        # ====================================================
        # MISSING SKILLS
        # ====================================================

        with col2:

            st.subheader("📚 Skills You Need to Develop")

            if selected_result["Skills to Develop"]:

                for skill in selected_result["Skills to Develop"]:

                    st.write(
                        f"📌 {skill}"
                    )

            else:

                st.success(
                    "You already have all the listed skills!"
                )


        # ====================================================
        # CAREER SKILL GAP SCORE
        # ====================================================

        st.divider()

        total_skills = len(
            selected_result["Required Skills"]
        )

        missing_count = len(
            selected_result["Skills to Develop"]
        )


        if total_skills > 0:

            skill_gap_score = (
                missing_count /
                total_skills
            ) * 100

        else:

            skill_gap_score = 0


        st.subheader("📈 Skill Gap Score")


        st.progress(
            int(skill_gap_score)
        )


        st.write(
            f"Skill Gap: "
            f"**{round(skill_gap_score, 2)}%**"
        )


        st.caption(
            "Lower skill-gap percentage means you are "
            "closer to being ready for this career."
        )


# ============================================================
# INFORMATION WHEN NO SKILLS ARE ENTERED
# ============================================================

else:

    st.divider()

    st.header("🚀 How CareerGraph AI Works")

    col1, col2, col3, col4 = st.columns(4)


    with col1:

        st.subheader("1️⃣")

        st.write("Current Skills")

        st.write(
            "Enter the skills you already know."
        )


    with col2:

        st.subheader("2️⃣")

        st.write("Skill Gap")

        st.write(
            "The system identifies skills "
            "you are missing."
        )


    with col3:

        st.subheader("3️⃣")

        st.write("Career Match")

        st.write(
            "Your skills are compared with "
            "different career roles."
        )


    with col4:

        st.subheader("4️⃣")

        st.write("Learning Priority")

        st.write(
            "You receive the skills you "
            "should develop next."
        )


# ============================================================
# FOOTER
# ============================================================

st.divider()

st.caption(
    "CareerGraph AI • Skill-to-Career Intelligence System"
)
