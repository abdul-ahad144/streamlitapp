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
# ROUND EFFICIENCY (NEW LOGIC)
# -----------------------
def round_efficiency(df):
    possible_cols = ["Cleared_R1", "Cleared_R2", "Cleared_R3"]

    existing_cols = [col for col in possible_cols if col in df.columns]

    if len(existing_cols) == 0:
        return 0

    cleared = df[existing_cols].sum().sum()

    total = len(df) * len(existing_cols)

    return cleared / total if total > 0 else 0
