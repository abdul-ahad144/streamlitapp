# -----------------------
# INTERVIEW SUCCESS RATE
# -----------------------
def interview_success_rate(df):
    if "Interview_Attended" in df.columns and "Offer_Received" in df.columns:
        interviews = df["Interview_Attended"].sum()
        offers = df["Offer_Received"].sum()
        return offers / interviews if interviews > 0 else 0
    return 0


# -----------------------
# ROUND EFFICIENCY (FIXED)
# -----------------------
def round_efficiency(df):
    # NEW LOGIC (REALISTIC)
    if "Interview_Attended" in df.columns and "Offer_Received" in df.columns:
        interviews = df["Interview_Attended"].sum()
        offers = df["Offer_Received"].sum()
        return offers / interviews if interviews > 0 else 0
    return 0
