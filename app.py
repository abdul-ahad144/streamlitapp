import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from utils.metrics import *

# -----------------------
# PAGE CONFIG
# -----------------------
st.set_page_config(page_title="PragyanAI Dashboard", layout="wide")

# -----------------------
# PREMIUM CSS
# -----------------------
st.markdown("""
<style>

/* Background */
body {
    background: #f6f8fb;
}

/* Sidebar Premium Blue Glass */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #1e3c72, #2a5298);
    backdrop-filter: blur(12px);
    border-right: 1px solid rgba(255,255,255,0.2);
}

[data-testid="stSidebar"] * {
    color: white !important;
}

/* KPI Cards */
.metric-card {
    background-color: #111;
    padding: 15px;
    border-radius: 12px;
    text-align: center;
    color: white;
    box-shadow: 0 8px 25px rgba(0,0,0,0.2);
}

/* Buttons */
button {
    border-radius: 10px !important;
}

</style>
""", unsafe_allow_html=True)

# -----------------------
# TITLE
# -----------------------
st.markdown("<h1 style='text-align: center;'>🚀 PragyanAI Placement Intelligence Engine</h1>", unsafe_allow_html=True)

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

if domain:
    df = df[df["Domain"].isin(domain)]

if company:
    df = df[df["Company_Tier"].isin(company)]

# -----------------------
# KPI
# -----------------------
st.markdown("## 📊 Overview")

c1, c2, c3, c4 = st.columns(4)

c1.markdown(f"<div class='metric-card'><h3>Students</h3><h2>{len(df)}</h2></div>", unsafe_allow_html=True)
c2.markdown(f"<div class='metric-card'><h3>Success Rate</h3><h2>{interview_success_rate(df):.2%}</h2></div>", unsafe_allow_html=True)
c3.markdown(f"<div class='metric-card'><h3>Efficiency</h3><h2>{round_efficiency(df):.2%}</h2></div>", unsafe_allow_html=True)
c4.markdown(f"<div class='metric-card'><h3>Placed</h3><h2>{df['Joined'].sum()}</h2></div>", unsafe_allow_html=True)

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
    "🧠 Skills"
])

# -----------------------
# FUNNEL
# -----------------------
with tab1:
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
    if "Failed_Stage" in df.columns:
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
    st.bar_chart(df.groupby("Skill_Programs_Completed")["Joined"].mean())
    st.bar_chart(df.groupby("Internship_Count")["Joined"].mean())
    st.bar_chart(df.groupby("Projects_Count")["Joined"].mean())
    st.bar_chart(df.groupby("Domain")["Joined"].mean())

# -----------------------
# EXTRA COMPONENTS
# -----------------------

# 🎯 Placement Probability
st.markdown("## 🎯 Placement Probability Calculator")

cgpa = st.slider("CGPA", 0.0, 10.0, 7.0)
skills = st.slider("Skill Programs", 0, 5, 2)
projects = st.slider("Projects", 0, 10, 3)
internships = st.slider("Internships", 0, 5, 1)

prob = (cgpa + skills + projects + internships) / 25
st.metric("Estimated Probability", f"{prob:.2%}")

# 🔍 Student Search
st.markdown("## 🔍 Student Search")

sid = st.text_input("Enter Student ID")
if sid:
    result = df[df["Student_ID"].astype(str) == sid]
    if not result.empty:
        st.dataframe(result)
    else:
        st.warning("Not found")

# 📥 Download
st.markdown("## 📥 Download Data")

csv = df.to_csv(index=False).encode('utf-8')
st.download_button("Download CSV", csv, "data.csv", "text/csv")

# 🏆 Top Students
st.markdown("## 🏆 Top Students")

top = df.sort_values(by="CGPA", ascending=False).head(10)
top = top.drop(columns=["Failed_Stage"], errors="ignore")
st.dataframe(top, hide_index=True)

# -----------------------
# INSIGHTS (LAST)
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
