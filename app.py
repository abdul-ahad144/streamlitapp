import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from utils.metrics import *

# -----------------------
# CONFIG
# -----------------------
st.set_page_config(layout="wide")
st.title("🚀 PragyanAI Placement Intelligence Engine")

# -----------------------
# LOAD DATA
# -----------------------
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

# -----------------------
# SIDEBAR FILTERS
# -----------------------
st.sidebar.header("🔍 Filters")

domain = st.sidebar.multiselect("Domain", df["Domain"].unique(), default=df["Domain"].unique())
company = st.sidebar.multiselect("Company Tier", df["Company_Tier"].unique(), default=df["Company_Tier"].unique())

df = df[(df["Domain"].isin(domain)) & (df["Company_Tier"].isin(company))]

# -----------------------
# KPI METRICS
# -----------------------
st.subheader("📊 Key Metrics")

col1, col2, col3 = st.columns(3)

col1.metric("Interview Success Rate", f"{interview_success_rate(df):.2%}")
col2.metric("Round Efficiency", f"{round_efficiency(df):.2%}")
col3.metric("Total Students", len(df))

# -----------------------
# FUNNEL
# -----------------------
st.subheader("📉 Placement Funnel")

funnel = {
    "Applied": df["Applied"].sum(),
    "Shortlisted": df["Shortlisted"].sum(),
    "Interview": df["Interview_Attended"].sum(),
    "Offer": df["Offer_Received"].sum(),
    "Joined": df["Joined"].sum()
}

st.bar_chart(funnel)

# -----------------------
# FAILURE ANALYSIS
# -----------------------
st.subheader("🔥 Round Failure Analysis")

failure = df["Failed_Stage"].value_counts()
st.bar_chart(failure)

# -----------------------
# ROLE ANALYSIS
# -----------------------
st.subheader("💼 Role Difficulty")

role = df["Job_Role"].value_counts()
st.bar_chart(role)

# -----------------------
# SALARY DISTRIBUTION
# -----------------------
st.subheader("💰 Salary Distribution")

fig, ax = plt.subplots()
ax.hist(df["Salary_LPA"], bins=30)
st.pyplot(fig)

# -----------------------
# CGPA VS SUCCESS
# -----------------------
st.subheader("🎓 CGPA vs Placement")

cgpa = df.groupby("CGPA")["Joined"].mean()
st.line_chart(cgpa)

# -----------------------
# SKILL IMPACT
# -----------------------
st.subheader("🧠 Skill Program Impact")

skill = df.groupby("Skill_Programs_Completed")["Joined"].mean()
st.bar_chart(skill)

# -----------------------
# INTERNSHIP IMPACT
# -----------------------
st.subheader("🏢 Internship Impact")

intern = df.groupby("Internship_Count")["Joined"].mean()
st.bar_chart(intern)

# -----------------------
# PROJECT IMPACT
# -----------------------
st.subheader("📁 Project Impact")

proj = df.groupby("Projects_Count")["Joined"].mean()
st.bar_chart(proj)

# -----------------------
# DOMAIN GAP
# -----------------------
st.subheader("⚠️ Domain Gap")

domain_gap = df.groupby("Domain")["Joined"].mean()
st.bar_chart(domain_gap)

# -----------------------
# SEGMENTATION
# -----------------------
st.subheader("👥 Student Segmentation")

placed = df[df["Joined"] == 1]
failed = df[(df["Interview_Attended"] == 1) & (df["Offer_Received"] == 0)]

col1, col2 = st.columns(2)

col1.write("### ✅ Placed Students")
col1.write(f"Count: {len(placed)}")

col2.write("### ❌ Interview Failures")
col2.write(f"Count: {len(failed)}")

# -----------------------
# INSIGHTS
# -----------------------
st.subheader("📌 Key Insights")

st.markdown("""
- Interview stage is biggest bottleneck  
- Coding + Tech rounds cause maximum failure  
- Projects + Internships are strongest signals  
- GenAI roles are hardest  
- Success = Clearing interview rounds  
""")

# -----------------------
# IMPROVEMENT ENGINE
# -----------------------
st.subheader("🚀 Improvement Strategy")

st.markdown("""
**1. Interview Prep Engine**
- Coding practice
- Mock interviews

**2. Project-Based Learning**
- Real-world projects

**3. Role-Based Training**
- DS vs AI vs GenAI

**4. Weak Round Fix**
- Aptitude → Practice tests
- Coding → DSA
- Tech → Mock interviews
- HR → Communication
""")
