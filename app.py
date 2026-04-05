import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from utils.metrics import *

# -----------------------
# PAGE CONFIG
# -----------------------
st.set_page_config(page_title="PragyanAI Dashboard", layout="wide")

# -----------------------
# TITLE
# -----------------------
st.title("🚀 PragyanAI Placement Intelligence Engine")

# -----------------------
# LOAD DATA
# -----------------------
@st.cache_data
def load_data():
    url = "https://raw.githubusercontent.com/pragyanaischool/VTU_Internship_DataSets/refs/heads/main/student_data_placement_interview_funnel_analysis_project_10.csv"
    try:
        df = pd.read_csv(url)
    except:
        df = pd.read_csv(url, encoding='latin1', on_bad_lines='skip')
    return df

df = load_data()
df.columns = df.columns.str.strip()

# -----------------------
# SIDEBAR FILTERS
# -----------------------
st.sidebar.header("🔍 Filters")

domain = st.sidebar.multiselect(
    "Domain",
    df["Domain"].unique() if "Domain" in df.columns else []
)

company = st.sidebar.multiselect(
    "Company Tier",
    df["Company_Tier"].unique() if "Company_Tier" in df.columns else []
)

if domain:
    df = df[df["Domain"].isin(domain)]

if company:
    df = df[df["Company_Tier"].isin(company)]

# -----------------------
# KPI
# -----------------------
st.subheader("📊 Overview")

col1, col2, col3, col4 = st.columns(4)

col1.metric("Students", len(df))
col2.metric("Success Rate", f"{interview_success_rate(df):.2%}")
col3.metric("Efficiency", f"{round_efficiency(df):.2%}")
col4.metric("Placed", df["Joined"].sum() if "Joined" in df.columns else 0)

# -----------------------
# SAFE GROUP FUNCTION
# -----------------------
def safe_group(col):
    if col in df.columns:
        return df.groupby(col)["Joined"].mean()
    return None

# -----------------------
# TABS
# -----------------------
tab1, tab2, tab3, tab4 = st.tabs([
    "Funnel",
    "Failures",
    "Roles",
    "Skills"
])

# -----------------------
# FUNNEL
# -----------------------
with tab1:
    st.subheader("Placement Funnel")

    if "Applied" in df.columns:
        funnel = {
            "Applied": df["Applied"].sum(),
            "Shortlisted": df["Shortlisted"].sum(),
            "Interview": df["Interview_Attended"].sum(),
            "Offer": df["Offer_Received"].sum(),
            "Joined": df["Joined"].sum()
        }
        st.bar_chart(funnel)

# -----------------------
# FAILURES
# -----------------------
with tab2:
    st.subheader("Failure Analysis")

    if "Failed_Stage" in df.columns:
        st.bar_chart(df["Failed_Stage"].value_counts())

# -----------------------
# ROLES
# -----------------------
with tab3:
    st.subheader("Role Distribution")

    if "Job_Role" in df.columns:
        st.bar_chart(df["Job_Role"].value_counts())

    if "Salary_LPA" in df.columns:
        st.subheader("Salary Distribution")
        fig, ax = plt.subplots()
        ax.hist(df["Salary_LPA"], bins=30)
        st.pyplot(fig)

# -----------------------
# SKILLS
# -----------------------
with tab4:
    st.subheader("Skill Impact")
    skill = safe_group("Skill_Programs")
    if skill is not None:
        st.bar_chart(skill)

    st.subheader("Internship Impact")
    intern = safe_group("Internships")
    if intern is not None:
        st.bar_chart(intern)

    st.subheader("Project Impact")
    proj = safe_group("Projects")
    if proj is not None:
        st.bar_chart(proj)

    st.subheader("Domain Gap")
    domain_gap = safe_group("Domain")
    if domain_gap is not None:
        st.bar_chart(domain_gap)

# -----------------------
# PLACEMENT PROBABILITY
# -----------------------
st.subheader("🎯 Placement Probability Calculator")

cgpa = st.slider("CGPA", 0.0, 10.0, 7.0)
skills = st.slider("Skill Programs", 0, 5, 2)
projects = st.slider("Projects", 0, 10, 3)
internships = st.slider("Internships", 0, 5, 1)

prob = (cgpa + skills + projects + internships) / 25
st.metric("Estimated Probability", f"{prob:.2%}")

# -----------------------
# STUDENT SEARCH
# -----------------------
st.subheader("🔍 Student Search")

if "Student_ID" in df.columns:
    sid = st.text_input("Enter Student ID")
    if sid:
        result = df[df["Student_ID"].astype(str) == sid]
        if not result.empty:
            st.dataframe(result, hide_index=True)
        else:
            st.warning("Student not found")

# -----------------------
# DOWNLOAD
# -----------------------
st.subheader("📥 Download Data")

csv = df.to_csv(index=False).encode('utf-8')
st.download_button("Download CSV", csv, "placement_data.csv", "text/csv")

# -----------------------
# TOP STUDENTS
# -----------------------
st.subheader("🏆 Top Students")

if "CGPA" in df.columns:
    top = df.sort_values(by="CGPA", ascending=False).head(10)
    top = top.drop(columns=["Failed_Stage"], errors="ignore")
    st.dataframe(top, hide_index=True)

# -----------------------
# INSIGHTS
# -----------------------
st.subheader("📌 Key Insights")

st.write("• Interview stage biggest bottleneck")
st.write("• Coding + Tech rounds cause failure")
st.write("• Projects + internships boost success")
st.write("• GenAI roles hardest")

# -----------------------
# FOOTER
# -----------------------
st.markdown("---")
st.write("🚀 Built with Streamlit")
