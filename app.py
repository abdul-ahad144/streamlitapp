import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from utils.metrics import *

# -----------------------
# PAGE CONFIG
# -----------------------
st.set_page_config(
    page_title="PragyanAI Dashboard",
    layout="wide",
)

# -----------------------
# CUSTOM CSS (PRO UI)
# -----------------------
st.markdown("""
<style>
.metric-card {
    background-color: #111;
    padding: 15px;
    border-radius: 12px;
    text-align: center;
    color: white;
}
</style>
""", unsafe_allow_html=True)

# -----------------------
# TITLE
# -----------------------
st.markdown("<h1 style='text-align: center;'>🚀 PragyanAI Placement Intelligence Engine</h1>", unsafe_allow_html=True)

# -----------------------
# LOAD DATA (FIXED ✅)
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

# IMPORTANT FIX (hidden spaces remove)
df.columns = df.columns.str.strip()

# -----------------------
# SIDEBAR
# -----------------------
st.sidebar.header("🔍 Smart Filters")

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
# KPI CARDS
# -----------------------
st.markdown("## 📊 Overview")

col1, col2, col3, col4 = st.columns(4)

col1.markdown(f"<div class='metric-card'><h3>Students</h3><h2>{len(df)}</h2></div>", unsafe_allow_html=True)

col2.markdown(
    f"<div class='metric-card'><h3>Success Rate</h3><h2>{interview_success_rate(df):.2%}</h2></div>",
    unsafe_allow_html=True
)

col3.markdown(
    f"<div class='metric-card'><h3>Efficiency</h3><h2>{round_efficiency(df):.2%}</h2></div>",
    unsafe_allow_html=True
)

col4.markdown(
    f"<div class='metric-card'><h3>Placed</h3><h2>{df['Joined'].sum() if 'Joined' in df.columns else 0}</h2></div>",
    unsafe_allow_html=True
)

# -----------------------
# SAFE GROUPBY FUNCTION
# -----------------------
def safe_groupby(col):
    if col in df.columns:
        return df.groupby(col)["Joined"].mean()
    return None

# -----------------------
# TABS
# -----------------------
tab1, tab2, tab3, tab4 = st.tabs([
    "📉 Funnel",
    "🔥 Failures",
    "💼 Roles & Salary",
    "🧠 Skills & Insights"
])

# -----------------------
# TAB 1: FUNNEL
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
# TAB 2: FAILURE
# -----------------------
with tab2:
    st.subheader("Round Failure Analysis")

    if "Failed_Stage" in df.columns:
        failure = df["Failed_Stage"].value_counts()
        st.bar_chart(failure)

# -----------------------
# TAB 3: ROLE + SALARY
# -----------------------
with tab3:
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Role Distribution")
        if "Job_Role" in df.columns:
            role = df["Job_Role"].value_counts()
            st.bar_chart(role)

    with col2:
        st.subheader("Salary Distribution")
        if "Salary_LPA" in df.columns:
            fig, ax = plt.subplots()
            ax.hist(df["Salary_LPA"], bins=30)
            st.pyplot(fig)

# -----------------------
# TAB 4: SKILLS + INSIGHTS
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
# INSIGHTS
# -----------------------
st.markdown("## 📌 Key Insights")

st.success("Interview stage is biggest bottleneck")
st.warning("Coding + Tech rounds cause maximum failure")
st.info("Projects + Internships boost success")
st.error("GenAI roles are hardest")

# -----------------------
# FOOTER
# -----------------------
st.markdown("---")
st.markdown("### 🚀 Built with Streamlit | PragyanAI Engine")
