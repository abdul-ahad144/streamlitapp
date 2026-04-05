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
/* TAB TEXT */
button[data-baseweb="tab"] {
    color: black !important;
    font-weight: 600;
}

/* ACTIVE TAB TEXT */
button[data-baseweb="tab"][aria-selected="true"] {
    color: black !important;
}

/* REMOVE DEFAULT U-SHAPE */
[data-baseweb="tab"]::after {
    display: none !important;
}

/* STRAIGHT ORANGE LINE ONLY */
[data-baseweb="tab-highlight"] {
    height: 3px !important;
    background: orange !important;
    border-radius: 0px !important;  /* 🔥 no curve */
}

/* BACKGROUND */
body {
    background: #f6f8fb;
}

/* TITLE */
.title {
    font-size: 42px;
    font-weight: 700;
    text-align: center;
    background: linear-gradient(90deg, #3a7bd5, #00d2ff);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

/* PREMIUM TAG */
.premium-tag {
    text-align: center;
    font-size: 14px;
    color: #fff;
    background: linear-gradient(90deg, #ff7e5f, #feb47b);
    display: inline-block;
    padding: 6px 12px;
    border-radius: 20px;
    margin-bottom: 10px;
}

/* KPI CARD */
.metric-card {
    background: white;
    padding: 20px;
    border-radius: 18px;
    text-align: center;
    box-shadow: 0 10px 30px rgba(0,0,0,0.08);
    transition: 0.3s;
}

.metric-card:hover {
    transform: translateY(-5px);
}

/* SECTION */
.section {
    background: white;
    padding: 20px;
    border-radius: 15px;
    margin-bottom: 20px;
    box-shadow: 0 5px 20px rgba(0,0,0,0.05);
}

/* SIDEBAR */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #ffffff, #f3f6fb);
    border-right: 1px solid #eee;
}

/* BUTTON */
button {
    border-radius: 10px !important;
    background: linear-gradient(90deg, #3a7bd5, #00d2ff);
    color: white !important;
}

/* TABLE */
[data-testid="stDataFrame"] {
    border-radius: 12px;
}

</style>
""", unsafe_allow_html=True)

# -----------------------
# PREMIUM TAG + TITLE
# -----------------------
st.markdown("<div style='text-align:center;'><span class='premium-tag'>💎 ULTRA PREMIUM DASHBOARD</span></div>", unsafe_allow_html=True)
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

domain = st.sidebar.multiselect(
    "Domain",
    df["Domain"].unique() if "Domain" in df.columns else []
)

company = st.sidebar.multiselect(
    "Company Tier",
    df["Company_Tier"].unique() if "Company_Tier" in df.columns else []
)

role = st.sidebar.multiselect(
    "Job Role",
    df["Job_Role"].unique() if "Job_Role" in df.columns else []
)

# -----------------------
# BUTTONS
# -----------------------
apply_filter = st.sidebar.button("Apply Filters")
reset_filter = st.sidebar.button("Reset Filters")

# APPLY FILTERS
if apply_filter:
    if domain:
        df = df[df["Domain"].isin(domain)]

    if company:
        df = df[df["Company_Tier"].isin(company)]

    if role:
        df = df[df["Job_Role"].isin(role)]

# RESET FILTER
if reset_filter:
    st.rerun()

# -----------------------
# KPI CARDS
# -----------------------
st.markdown("## 📊 Overview")

col1, col2, col3, col4 = st.columns(4)

col1.markdown(f"<div class='metric-card'><h3>Students</h3><h2>{len(df)}</h2></div>", unsafe_allow_html=True)

col2.markdown(f"<div class='metric-card'><h3>Success Rate</h3><h2>{interview_success_rate(df):.2%}</h2></div>", unsafe_allow_html=True)

col3.markdown(f"<div class='metric-card'><h3>Efficiency</h3><h2>{round_efficiency(df):.2%}</h2></div>", unsafe_allow_html=True)

col4.markdown(f"<div class='metric-card'><h3>Placed</h3><h2>{df['Joined'].sum() if 'Joined' in df.columns else 0}</h2></div>", unsafe_allow_html=True)

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
tab1, tab2, tab3, tab4 = st.tabs([
    "📉 Funnel",
    "🔥 Failures",
    "💼 Roles & Salary",
    "🧠 Skills & Insights"
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
# FAILURE
# -----------------------
with tab2:
    st.subheader("Failure Analysis")

    if "Failed_Stage" in df.columns:
        st.bar_chart(df["Failed_Stage"].value_counts())

# -----------------------
# ROLE + SALARY
# -----------------------
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

# -----------------------
# SKILLS
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
# EXTRA COMPONENTS
# -----------------------
st.markdown("## 🎯 Placement Probability Calculator")

cgpa = st.slider("CGPA", 0.0, 10.0, 7.0)
skills = st.slider("Skill Programs", 0, 5, 2)
projects = st.slider("Projects", 0, 10, 3)
internships = st.slider("Internships", 0, 5, 1)

prob = (cgpa + skills + projects + internships) / 25
st.metric("Estimated Probability", f"{prob:.2%}")

# -----------------------
# STUDENT SEARCH
# -----------------------
st.markdown("## 🔍 Student Search")

if "Student_ID" in df.columns:
    sid = st.text_input("Enter Student ID")
    if sid:
        result = df[df["Student_ID"].astype(str) == sid]
        if not result.empty:
            st.dataframe(result)
        else:
            st.warning("Not found")

# -----------------------
# DOWNLOAD
# -----------------------
st.markdown("## 📥 Download Data")

csv = df.to_csv(index=False).encode('utf-8')
st.download_button("Download CSV", csv, "data.csv", "text/csv")

# -----------------------
# TOP STUDENTS
# -----------------------
st.markdown("## 🏆 Top Students")

if "CGPA" in df.columns:
    st.dataframe(df.sort_values(by="CGPA", ascending=False).head(10))

# -----------------------
# INSIGHTS
# -----------------------
st.markdown("## 📌 Key Insights")

st.success("Interview stage biggest bottleneck")
st.warning("Coding + Tech rounds cause failure")
st.info("Projects + internships boost success")
st.error("GenAI roles hardest")

# -----------------------
# FOOTER
# -----------------------
st.markdown("---")
st.markdown("🚀 Built with Streamlit | PragyanAI Engine")
