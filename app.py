import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from utils.metrics import *

st.set_page_config(layout="wide")
st.title("🚀 PragyanAI Placement Intelligence Engine")

# -----------------------
# LOAD DATA (FIXED)
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

# IMPORTANT FIX
df.columns = df.columns.str.strip()

# -----------------------
# SIDEBAR
# -----------------------
st.sidebar.header("🔍 Filters")

domain = st.sidebar.multiselect("Domain", df["Domain"].unique() if "Domain" in df.columns else [])
company = st.sidebar.multiselect("Company_Tier", df["Company_Tier"].unique() if "Company_Tier" in df.columns else [])

if domain:
    df = df[df["Domain"].isin(domain)]

if company:
    df = df[df["Company_Tier"].isin(company)]

# -----------------------
# KPI
# -----------------------
st.subheader("📊 Metrics")

col1, col2, col3 = st.columns(3)

col1.metric("Success Rate", f"{interview_success_rate(df):.2%}")
col2.metric("Efficiency", f"{round_efficiency(df):.2%}")
col3.metric("Students", len(df))

# -----------------------
# FUNNEL
# -----------------------
st.subheader("📉 Funnel")

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
# FAILURE
# -----------------------
if "Failed_Stage" in df.columns:
    st.subheader("🔥 Failures")
    st.bar_chart(df["Failed_Stage"].value_counts())

# -----------------------
# ROLE
# -----------------------
if "Job_Role" in df.columns:
    st.subheader("💼 Roles")
    st.bar_chart(df["Job_Role"].value_counts())

# -----------------------
# SALARY
# -----------------------
if "Salary_LPA" in df.columns:
    st.subheader("💰 Salary")
    fig, ax = plt.subplots()
    ax.hist(df["Salary_LPA"])
    st.pyplot(fig)

# -----------------------
# SAFE GROUPBY FUNCTION
# -----------------------
def safe_groupby(col):
    if col in df.columns:
        return df.groupby(col)["Joined"].mean()
    return None

# -----------------------
# SKILLS
# -----------------------
skill = safe_groupby("Skill_Programs_Completed")
if skill is not None:
    st.subheader("🧠 Skills")
    st.bar_chart(skill)

# -----------------------
# INTERNSHIP
# -----------------------
intern = safe_groupby("Internship_Count")
if intern is not None:
    st.subheader("🏢 Internship")
    st.bar_chart(intern)

# -----------------------
# PROJECT
# -----------------------
proj = safe_groupby("Projects_Count")
if proj is not None:
    st.subheader("📁 Projects")
    st.bar_chart(proj)

# -----------------------
# DOMAIN
# -----------------------
domain_gap = safe_groupby("Domain")
if domain_gap is not None:
    st.subheader("⚠️ Domain Gap")
    st.bar_chart(domain_gap)

# -----------------------
# INSIGHTS
# -----------------------
st.subheader("📌 Insights")

st.write("Interview stage biggest bottleneck")
st.write("Coding + Tech rounds cause failure")
st.write("Projects + internships increase success")
