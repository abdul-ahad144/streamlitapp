import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from utils.metrics import *

# -----------------------
# CONFIG
# -----------------------
st.set_page_config(page_title="PragyanAI Dashboard", layout="wide")

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
# SESSION STATE INIT
# -----------------------
if "filtered_df" not in st.session_state:
    st.session_state.filtered_df = df.copy()

# -----------------------
# SIDEBAR FILTERS
# -----------------------
st.sidebar.header("🔍 Filters")

domain = st.sidebar.multiselect("Domain", df["Domain"].unique())
company = st.sidebar.multiselect("Company Tier", df["Company_Tier"].unique())
role = st.sidebar.multiselect("Job Role", df["Job_Role"].unique())

apply = st.sidebar.button("Apply Filters")
reset = st.sidebar.button("Reset Filters")

# -----------------------
# APPLY FILTER LOGIC
# -----------------------
if apply:
    temp_df = df.copy()

    if domain:
        temp_df = temp_df[temp_df["Domain"].isin(domain)]

    if company:
        temp_df = temp_df[temp_df["Company_Tier"].isin(company)]

    if role:
        temp_df = temp_df[temp_df["Job_Role"].isin(role)]

    st.session_state.filtered_df = temp_df

# -----------------------
# RESET FILTER LOGIC
# -----------------------
if reset:
    st.session_state.filtered_df = df.copy()

# -----------------------
# USE FILTERED DATA
# -----------------------
df = st.session_state.filtered_df

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
# SAFE GROUP
# -----------------------
def safe_group(col):
    if col in df.columns:
        return df.groupby(col)["Joined"].mean()
    return None

# -----------------------
# TABS
# -----------------------
tab1, tab2, tab3, tab4 = st.tabs(["Funnel", "Failures", "Roles", "Skills"])

# -----------------------
# FUNNEL
# -----------------------
with tab1:
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
    st.bar_chart(df["Failed_Stage"].value_counts())

# -----------------------
# ROLES
# -----------------------
with tab3:
    st.bar_chart(df["Job_Role"].value_counts())

    fig, ax = plt.subplots()
    ax.hist(df["Salary_LPA"], bins=30)
    st.pyplot(fig)

# -----------------------
# SKILLS
# -----------------------
with tab4:
    st.bar_chart(safe_group("Skill_Programs"))
    st.bar_chart(safe_group("Internships"))
    st.bar_chart(safe_group("Projects"))
    st.bar_chart(safe_group("Domain"))

# -----------------------
# EXTRA
# -----------------------
st.subheader("🎯 Placement Probability")

cgpa = st.slider("CGPA", 0.0, 10.0, 7.0)
skills = st.slider("Skill Programs", 0, 5, 2)
projects = st.slider("Projects", 0, 10, 3)
internships = st.slider("Internships", 0, 5, 1)

prob = (cgpa + skills + projects + internships) / 25
st.metric("Probability", f"{prob:.2%}")

# -----------------------
# DOWNLOAD
# -----------------------
csv = df.to_csv(index=False).encode('utf-8')
st.download_button("Download CSV", csv)

# -----------------------
# TOP STUDENTS
# -----------------------
top = df.sort_values(by="CGPA", ascending=False).head(10)
st.dataframe(top, hide_index=True)

# -----------------------
# INSIGHTS
# -----------------------
st.subheader("📌 Insights")
st.write("Interview stage biggest bottleneck")
st.write("Coding + Tech failures high")
st.write("Projects + internships boost success")
