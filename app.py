import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from utils.metrics import *

# -----------------------
# PAGE CONFIG
# -----------------------
st.set_page_config(page_title="PragyanAI Engine", layout="wide")

st.markdown("<h1 style='text-align:center;'>🚀 PragyanAI Placement Intelligence Engine</h1>", unsafe_allow_html=True)

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
st.sidebar.header("🔍 Advanced Filters")

domain = st.sidebar.multiselect("Domain", df.get("Domain", []).unique() if "Domain" in df.columns else [])
company = st.sidebar.multiselect("Company Tier", df.get("Company_Tier", []).unique() if "Company_Tier" in df.columns else [])
role = st.sidebar.multiselect("Job Role", df.get("Job_Role", []).unique() if "Job_Role" in df.columns else [])

if domain:
    df = df[df["Domain"].isin(domain)]

if company:
    df = df[df["Company_Tier"].isin(company)]

if role:
    df = df[df["Job_Role"].isin(role)]

# -----------------------
# KPI CARDS
# -----------------------
st.markdown("## 📊 Key Metrics")

col1, col2, col3, col4 = st.columns(4)

col1.metric("👨‍🎓 Students", len(df))
col2.metric("📈 Success Rate", f"{interview_success_rate(df):.2%}")
col3.metric("⚡ Efficiency", f"{round_efficiency(df):.2%}")
col4.metric("🎯 Placed", df["Joined"].sum() if "Joined" in df.columns else 0)

# -----------------------
# TABS
# -----------------------
tab1, tab2, tab3, tab4 = st.tabs([
    "📉 Funnel",
    "🔥 Failures",
    "💼 Roles & Salary",
    "🧠 Skills Analysis"
])

# -----------------------
# TAB 1: FUNNEL
# -----------------------
with tab1:
    st.subheader("Placement Funnel Analysis")

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
# TAB 2: FAILURE
# -----------------------
with tab2:
    st.subheader("Failure Analysis")

    if "Failed_Stage" in df.columns:
        st.bar_chart(df["Failed_Stage"].value_counts())

# -----------------------
# TAB 3: ROLE + SALARY
# -----------------------
with tab3:
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Role Distribution")
        if "Job_Role" in df.columns:
            st.bar_chart(df["Job_Role"].value_counts())

    with col2:
        st.subheader("Salary Distribution")
        if "Salary_LPA" in df.columns:
            fig, ax = plt.subplots()
            ax.hist(df["Salary_LPA"], bins=30)
            st.pyplot(fig)

# -----------------------
# SAFE GROUPBY
# -----------------------
def safe_groupby(col):
    if col in df.columns:
        return df.groupby(col)["Joined"].mean()
    return None

# -----------------------
# TAB 4: SKILLS
# -----------------------
with tab4:
    col1, col2 = st.columns(2)

    with col1:
        skill = safe_groupby("Skill_Programs_Completed")
        if skill is not None:
            st.subheader("Skill Impact")
            st.bar_chart(skill)

        intern = safe_groupby("Internship_Count")
        if intern is not None:
            st.subheader("Internship Impact")
            st.bar_chart(intern)

    with col2:
        proj = safe_groupby("Projects_Count")
        if proj is not None:
            st.subheader("Project Impact")
            st.bar_chart(proj)

        domain_gap = safe_groupby("Domain")
        if domain_gap is not None:
            st.subheader("Domain Gap")
            st.bar_chart(domain_gap)

# -----------------------
# SEGMENTATION
# -----------------------
st.markdown("## 👥 Student Segmentation")

placed = df[df["Joined"] == 1] if "Joined" in df.columns else pd.DataFrame()
failed = df[(df["Interview_Attended"] == 1) & (df["Offer_Received"] == 0)] if "Interview_Attended" in df.columns else pd.DataFrame()

col1, col2 = st.columns(2)

col1.success(f"Placed Students: {len(placed)}")
col2.error(f"Interview Failures: {len(failed)}")

# -----------------------
# INSIGHTS
# -----------------------
st.markdown("## 📌 Key Insights")

st.success("Interview stage is biggest bottleneck")
st.warning("Coding + Tech rounds cause maximum failure")
st.info("Projects + Internships boost placement chances")
st.error("GenAI roles require advanced preparation")

# -----------------------
# FOOTER
# -----------------------
st.markdown("---")
st.markdown("🚀 Built with Streamlit | PragyanAI Engine")
