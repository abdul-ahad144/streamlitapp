import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# -------------------------------
# LOAD DATA
# -------------------------------
url = "https://raw.githubusercontent.com/pragyanaischool/VTU_Internship_DataSets/refs/heads/main/student_data_placement_interview_funnel_analysis_project_10.csv"
df = pd.read_csv(url)

st.title("🚀 PragyanAI Placement Intelligence Dashboard")

# -------------------------------
# SIDEBAR FILTERS
# -------------------------------
st.sidebar.header("Filters")

domain = st.sidebar.selectbox("Select Domain", df["Domain"].unique())
company = st.sidebar.selectbox("Company Tier", df["Company_Tier"].unique())

filtered_df = df[
    (df["Domain"] == domain) &
    (df["Company_Tier"] == company)
]

# -------------------------------
# 1. FUNNEL VISUALIZATION
# -------------------------------
st.header("📊 Placement Funnel")

funnel = {
    "Applied": df["Applied"].sum(),
    "Shortlisted": df["Shortlisted"].sum(),
    "Interview": df["Interview_Attended"].sum(),
    "Offer": df["Offer_Received"].sum(),
    "Joined": df["Joined"].sum()
}

st.bar_chart(funnel)

# -------------------------------
# 2. ROUND FAILURE ANALYSIS
# -------------------------------
st.header("🔥 Round-wise Failure")

failure_counts = df["Failed_Stage"].value_counts()
st.bar_chart(failure_counts)

# -------------------------------
# 3. ROLE ANALYSIS
# -------------------------------
st.header("💼 Role Distribution")

role_counts = filtered_df["Job_Role"].value_counts()
st.bar_chart(role_counts)

# -------------------------------
# 4. SALARY DISTRIBUTION
# -------------------------------
st.header("💰 Salary Distribution")

fig, ax = plt.subplots()
ax.hist(filtered_df["Salary_LPA"], bins=20)
st.pyplot(fig)

# -------------------------------
# 5. CGPA VS SUCCESS
# -------------------------------
st.header("🎓 CGPA vs Placement")

cgpa_success = df.groupby("CGPA")["Joined"].mean()
st.line_chart(cgpa_success)

# -------------------------------
# 6. SKILL GAP INSIGHT
# -------------------------------
st.header("🧠 Skill Gap Insight")

st.write("Students failing mostly in Coding and Tech rounds")
st.write("Skills + Projects + Internships increase success probability")

# -------------------------------
# 7. INTERVIEW SUCCESS RATE
# -------------------------------
st.header("📈 Interview Success Rate")

interviews = df["Interview_Attended"].sum()
offers = df["Offer_Received"].sum()

if interviews > 0:
    success_rate = offers / interviews
    st.metric("Success Rate", f"{success_rate:.2%}")

# -------------------------------
# 8. KEY INSIGHTS
# -------------------------------
st.header("📌 Key Insights")

st.markdown("""
- Interview stage is biggest bottleneck  
- Coding + Tech rounds cause maximum failure  
- Projects + Internships = strongest signals  
- GenAI roles are hardest  
- Success = Clearing interview rounds  
""")
