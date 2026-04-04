import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from utils.metrics import *

# -----------------------
# PAGE CONFIG
# -----------------------
st.set_page_config(page_title="PragyanAI Dashboard", layout="wide")

# -----------------------
# CSS
# -----------------------
st.markdown("""
<style>
body { background: #f6f8fb; }

.title {
    font-size: 42px;
    font-weight: 700;
    text-align: center;
    background: linear-gradient(90deg, #3a7bd5, #00d2ff);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.premium-tag {
    text-align: center;
    font-size: 14px;
    color: white;
    background: linear-gradient(90deg, #ff7e5f, #feb47b);
    padding: 6px 12px;
    border-radius: 20px;
}

.section {
    background: white;
    padding: 20px;
    border-radius: 15px;
    margin-bottom: 20px;
    box-shadow: 0 5px 20px rgba(0,0,0,0.05);
}
</style>
""", unsafe_allow_html=True)

# -----------------------
# TITLE
# -----------------------
st.markdown("<div style='text-align:center'><span class='premium-tag'>💎 ULTRA PREMIUM DASHBOARD</span></div>", unsafe_allow_html=True)
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
# DOWNLOAD BUTTON
# -----------------------
st.download_button(
    "⬇️ Download Dataset",
    data=df.to_csv(index=False),
    file_name="placement_data.csv",
    mime="text/csv"
)

# -----------------------
# FILTERS
# -----------------------
st.sidebar.header("🔍 Filters")

domain = st.sidebar.multiselect("Domain", df["Domain"].unique())
company = st.sidebar.multiselect("Company Tier", df["Company_Tier"].unique())
role = st.sidebar.multiselect("Job Role", df["Job_Role"].unique())

if st.sidebar.button("Apply Filters"):
    if domain:
        df = df[df["Domain"].isin(domain)]
    if company:
        df = df[df["Company_Tier"].isin(company)]
    if role:
        df = df[df["Job_Role"].isin(role)]

if st.sidebar.button("Reset Filters"):
    st.rerun()

# -----------------------
# KPI
# -----------------------
c1, c2, c3, c4 = st.columns(4)
c1.metric("Students", len(df))
c2.metric("Success Rate", f"{interview_success_rate(df):.2%}")
c3.metric("Efficiency", f"{round_efficiency(df):.2%}")
c4.metric("Placed", df["Joined"].sum())

# -----------------------
# NAVBAR
# -----------------------
nav = st.radio("", ["📊 Funnel", "🔥 Failures", "💼 Roles", "🧠 Skills", "📈 Advanced"], horizontal=True)

# -----------------------
# FUNNEL
# -----------------------
if nav == "📊 Funnel":
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
elif nav == "🔥 Failures":
    st.bar_chart(df["Failed_Stage"].value_counts())

# -----------------------
# ROLES
# -----------------------
elif nav == "💼 Roles":
    st.bar_chart(df["Job_Role"].value_counts())
    fig, ax = plt.subplots()
    ax.hist(df["Salary_LPA"], bins=30)
    st.pyplot(fig)

# -----------------------
# SKILLS
# -----------------------
elif nav == "🧠 Skills":
    st.bar_chart(df.groupby("Skill_Programs_Completed")["Joined"].mean())
    st.bar_chart(df.groupby("Internship_Count")["Joined"].mean())
    st.bar_chart(df.groupby("Projects_Count")["Joined"].mean())
    st.bar_chart(df.groupby("Domain")["Joined"].mean())

# -----------------------
# ADVANCED
# -----------------------
elif nav == "📈 Advanced":

    st.subheader("CGPA vs Placement")
    st.line_chart(df.groupby("CGPA")["Joined"].mean())

    st.subheader("Segmentation")

    placed = df[df["Joined"] == 1]
    failed = df[(df["Interview_Attended"] == 1) & (df["Offer_Received"] == 0)]

    col1, col2 = st.columns(2)
    col1.metric("Placed", len(placed))
    col2.metric("Interview Failures", len(failed))

    st.subheader("Insights")
    st.write("Interview stage biggest bottleneck")
    st.write("Coding + Tech failures high")
    st.write("Projects + internships boost success")

# -----------------------
# TOP STUDENTS
# -----------------------
st.subheader("🏆 Top Students")
top_students = df.sort_values(by="CGPA", ascending=False).head(10)
top_students = top_students.drop(columns=["Failed_Stage"], errors="ignore")
st.dataframe(top_students, hide_index=True)

# -----------------------
# FOOTER
# -----------------------
st.markdown("---")
st.markdown("🚀 Built with Streamlit")
