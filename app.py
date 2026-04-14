import streamlit as st
import PyPDF2
import matplotlib.pyplot as plt
from skills import skills_list


# -------- FUNCTIONS --------

def extract_text_from_pdf(file):
    text = ""
    pdf_reader = PyPDF2.PdfReader(file)

    for page in pdf_reader.pages:
        if page.extract_text():
            text += page.extract_text()

    return text.lower()


def extract_skills(text):
    found_skills = []

    for skill in skills_list:
        if skill.lower() in text:
            found_skills.append(skill)

    return found_skills


def calculate_score(found_skills):
    total_skills = len(skills_list)
    score = (len(found_skills) / total_skills) * 100
    return round(score, 2)


def suggest_roles(skills):
    roles = []

    if "python" in skills and "machine learning" in skills:
        roles.append("Machine Learning Engineer")

    if "sql" in skills and "excel" in skills:
        roles.append("Data Analyst")

    if "javascript" in skills or "react" in skills:
        roles.append("Frontend Developer")

    if "node js" in skills:
        roles.append("Backend Developer")

    if "aws" in skills or "azure" in skills:
        roles.append("Cloud Engineer")

    if "java" in skills:
        roles.append("Software Developer")

    if not roles:
        roles.append("Non-technical role")

    return roles


# -------- UI --------

st.title("🚀 AI Resume Analyzer")
st.markdown("### Analyze your resume and get smart insights 💡")
st.divider()

uploaded_file = st.file_uploader("Upload your Resume (PDF)", type=["pdf"])


if uploaded_file is not None:

    text = extract_text_from_pdf(uploaded_file)
    skills = extract_skills(text)
    score = calculate_score(skills)
    roles = suggest_roles(skills)

    # -------- ROLES --------
    st.subheader("💼 Suggested Roles")
    for role in roles:
        st.success(f"👉 {role}")

    # -------- SCORE --------
    st.subheader("📊 Resume Score")
    st.progress(int(score))
    st.write(f"{score} / 100")
    st.divider()

    # ✅ IMPORTANT: define missing FIRST (ONLY ONCE)
    missing = list(set(skills_list) - set(skills))

    # -------- CHART --------
    st.subheader("📈 Skill Analysis Chart")

    labels = ["Found Skills", "Missing Skills"]
    values = [len(skills), len(missing)]

    fig, ax = plt.subplots()
    ax.bar(labels, values)

    st.pyplot(fig)

    # -------- SUMMARY --------
    st.subheader("📊 Score Breakdown")
    st.write(f"✅ Skills Found: {len(skills)}")
    st.write(f"❌ Missing Skills: {len(missing)}")
    st.divider()

    # -------- SKILLS FOUND --------
    st.subheader("✅ Skills Found")
    for skill in skills:
        st.success(f"✔ {skill}")

    # -------- MISSING SKILLS --------
    st.subheader("❌ Missing Skills")
    for skill in missing:
        st.error(f"✖ {skill}")