import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from utils.metrics import *

# -----------------------
# PAGE CONFIG
# -----------------------
st.set_page_config(page_title="PragyanAI Dashboard", layout="wide")

# -----------------------
# CUSTOM CSS (ULTRA UI)
# -----------------------
st.markdown("""
<style>

/* BACKGROUND */
body {
    background-color: #0f1117;
}

/* TITLE */
.title {
    font-size: 42px;
    font-weight: 700;
    text-align: center;
    background: linear-gradient(90deg, #4facfe, #00f2fe);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

/* KPI CARD */
.metric-card {
    background: rgba(255, 255, 255, 0.05);
    padding: 20px;
    border-radius: 18px;
    text-align: center;
    backdrop-filter: blur(12px);
    box-shadow: 0 10px 40px rgba(0,0,0,0.4);
    transition: 0.3s;
}

.metric-card:hover {
    transform: scale(1.05);
}

/* SECTION */
.section {
    background: rgba(255,255,255,0.04);
    padding: 20px;
    border-radius: 15px;
    margin-bottom: 20px;
}

/* SIDEBAR */
[data-testid="stSidebar"] {
    background-color: #111;
}

/* BUTTON */
button {
    border-radius: 10px !important;
}

/* TABLE */
[data-testid="stDataFrame"] {
    border-radius: 12px;
}

</style>
""", unsafe_allow_html=True)

# -----------------------
# TITLE
# -----------------------
st.markdown("<div class='title'>🚀 PragyanAI Placement Intelligence Engine</div>", unsafe_allow_html=True)

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

domain = st.sidebar.multiselect("Domain", df["Domain"].unique() if "Domain" in df.columns else [])
company = st.sidebar.multiselect("Company Tier", df["Company_Tier"].unique() if "Company_Tier" in df.columns else [])
role = st.sidebar.multiselect("Job Role", df["Job_Role"].unique() if "Job_Role" in df.columns else [])

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
# KPI CARDS
# -----------------------
st.markdown("<div class='section'>", unsafe_allow_html=True)

col1, col2, col3, col4 = st.columns(4)

col1.markdown(f"<div class='metric-card'><h4>Students</h4><h2>{len(df)}</h2></div>", unsafe_allow_html=True)
col2.markdown(f"<div class='metric-card'><h4>Success Rate</h4><h2>{interview_success_rate(df):.2%}</h2></div>", unsafe_allow_html=True)
col3.markdown(f"<div class='metric-card'><h4>Efficiency</h4><h2>{round_efficiency(df):.2%}</h2></div>", unsafe_allow_html=True)
col4.markdown(f"<div class='metric-card'><h4>Placed</h4><h2>{df['Joined'].sum() if 'Joined' in df.columns else 0}</h2></div>", unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)

# -----------------------
# SAFE GROUPBY
# -----------------------
def safe_groupby(col):
    if col in df.columns:
        return df.groupby(col)["Joined"].mean()
    return None

# -----------------------
# TABS
# -----------------------
st.markdown("<div class='section'>", unsafe_allow_html=True)

tab1, tab2, tab3, tab4 = st.tabs([
    "📉 Funnel",
    "🔥 Failures",
    "💼 Roles & Salary",
    "🧠 Skills & Insights"
])

with tab1:
    if "Applied" in df.columns:
        st.subheader("Placement Funnel")
        funnel = {
            "Applied": df["Applied"].sum(),
            "Shortlisted": df["Shortlisted"].sum(),
            "Interview": df["Interview_Attended"].sum(),
            "Offer": df["Offer_Received"].sum(),
            "Joined": df["Joined"].sum()
        }
        st.bar_chart(funnel)

with tab2:
    if "Failed_Stage" in df.columns:
        st.subheader("Failure Analysis")
        st.bar_chart(df["Failed_Stage"].value_counts())

with tab3:
    col1, col2 = st.columns(2)

    with col1:
        if "Job_Role" in df.columns:
            st.subheader("Role Distribution")
            st.bar_chart(df["Job_Role"].value_counts())

    with col2:
        if "Salary_LPA" in df.columns:
            st.subheader("Salary Distribution")
            fig, ax = plt.subplots()
            ax.hist(df["Salary_LPA"], bins=30)
            st.pyplot(fig)

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

st.markdown("</div>", unsafe_allow_html=True)

# -----------------------
# TOP STUDENTS
# -----------------------
st.markdown("<div class='section'>", unsafe_allow_html=True)

st.markdown("### 🏆 Top Students")

if "CGPA" in df.columns:
    top_students = df.sort_values(by="CGPA", ascending=False).head(10)
    top_students = top_students.drop(columns=["Failed_Stage"], errors="ignore")
    st.dataframe(top_students, hide_index=True)

st.markdown("</div>", unsafe_allow_html=True)

# -----------------------
# FOOTER
# -----------------------
st.markdown("---")
st.markdown("🚀 Built with Streamlit | PragyanAI Engine")
