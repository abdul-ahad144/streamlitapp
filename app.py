import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from utils.metrics import *

# -----------------------
# PAGE CONFIG
# -----------------------
st.set_page_config(page_title="PragyanAI Dashboard", layout="wide")

# -----------------------
# CUSTOM CSS
# -----------------------
st.markdown("""
<style>
button[data-baseweb="tab"] {
    color: black !important;
    font-weight: 600;
}
button[data-baseweb="tab"][aria-selected="true"] {
    color: black !important;
}
[data-baseweb="tab"]::after {
    display: none !important;
}
[data-baseweb="tab-highlight"] {
    height: 3px !important;
    background: orange !important;
    border-radius: 0px !important;
}
</style>
""", unsafe_allow_html=True)

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

domain = st.sidebar.multiselect("Domain", df["Domain"].unique())
company = st.sidebar.multiselect("Company Tier", df["Company_Tier"].unique())
role = st.sidebar.multiselect("Job Role", df["Job_Role"].unique())

apply_filter = st.sidebar.button("Apply Filters")
reset_filter = st.sidebar.button("Reset Filters")

if apply_filter:
    if domain:
        df = df[df["Domain"].isin(domain)]
    if company:
        df = df[df["Company_Tier"].isin(company)]
    if role:
        df = df[df["Job_Role"].isin(role)]

if reset_filter:
    st.rerun()

# -----------------------
# KPI
# -----------------------
st.subheader("📊 Overview")

col1, col2, col3, col4 = st.columns(4)

col1.metric("Students", len(df))
col2.metric("Success Rate", f"{interview_success_rate(df):.2%}")
col3.metric("Efficiency", f"{round_efficiency(df):.2%}")
col4.metric("Placed", df["Joined"].sum())

# -----------------------
# TABS
# -----------------------
tab1, tab2, tab3, tab4 = st.tabs([
    "📉 Funnel",
    "🔥 Failures",
    "💼 Roles & Salary",
    "🧠 Skills"
])

# -----------------------
# FUNNEL
# -----------------------
with tab1:
    st.subheader("Placement Funnel")
    funnel = {
        "Applied": df["Applied"].sum(),
        "Shortlisted": df["Shortlisted"].sum(),
        "Interview": df["Interview_Attended"].sum(),
        "Offer": df["Offer_Received"].sum(),
        "Joined": df["Joined"].sum()
    }
    st.bar_chart(funnel)

# -----------------------
# FAILURE
# -----------------------
with tab2:
    st.subheader("Failure Analysis")
    st.bar_chart(df["Failed_Stage"].value_counts())

# -----------------------
# ROLES + SALARY
# -----------------------
with tab3:
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Role Distribution")
        st.bar_chart(df["Job_Role"].value_counts())

    with col2:
        st.subheader("Salary Distribution")
        fig, ax = plt.subplots()
        ax.hist(df["Salary_LPA"], bins=30)
        st.pyplot(fig)

# -----------------------
# SKILLS
# -----------------------
with tab4:
    st.subheader("Skill Impact")

    if "Skill_Programs" in df.columns:
        st.bar_chart(df.groupby("Skill_Programs")["Joined"].mean())

    if "Internships" in df.columns:
        st.bar_chart(df.groupby("Internships")["Joined"].mean())

    if "Projects" in df.columns:
        st.bar_chart(df.groupby("Projects")["Joined"].mean())

# -----------------------
# STUDENT SEARCH
# -----------------------
st.subheader("🔍 Student Search")

sid = st.text_input("Enter Student ID")

if sid:
    result = df[df["Student_ID"].astype(str) == sid]

    # REMOVE FAILED_STAGE
    result = result.drop(columns=["Failed_Stage"], errors="ignore")

    # REMOVE INDEX
    st.dataframe(result, hide_index=True)

# -----------------------
# DOWNLOAD
# -----------------------
st.subheader("📥 Download Data")

csv = df.to_csv(index=False).encode('utf-8')
st.download_button("Download CSV", csv, "data.csv")

# -----------------------
# TOP STUDENTS
# -----------------------
st.subheader("🏆 Top Students")

top = df.sort_values(by="CGPA", ascending=False).head(10)

# REMOVE FAILED_STAGE
top = top.drop(columns=["Failed_Stage"], errors="ignore")

# REMOVE INDEX
st.dataframe(top, hide_index=True)

# -----------------------
# INSIGHTS
# -----------------------
st.subheader("📌 Insights")

st.write("Interview stage biggest bottleneck")
st.write("Coding + Tech failures high")
st.write("Projects + internships boost success")

# -----------------------
# FOOTER
# -----------------------
st.markdown("---")
st.write("🚀 Built with Streamlit")
