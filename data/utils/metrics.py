def interview_success_rate(df):
    interviews = df["Interview_Attended"].sum()
    offers = df["Offer_Received"].sum()
    return offers / interviews if interviews > 0 else 0


def round_efficiency(df):
    cleared = df[["Cleared_Round_1","Cleared_Round_2","Cleared_Round_3"]].sum().sum()
    total = df["Total_Rounds"].sum()
    return cleared / total if total > 0 else 0


def placement_probability(row):
    return (
        row["CGPA"] +
        row["Skill_Programs_Completed"] +
        row["Projects_Count"] +
        row["Internship_Count"]
    )
