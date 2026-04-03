def interview_success_rate(df):
    interviews = df["Interview_Attended"].sum() if "Interview_Attended" in df.columns else 0
    offers = df["Offer_Received"].sum() if "Offer_Received" in df.columns else 0
    return offers / interviews if interviews > 0 else 0


def round_efficiency(df):
    possible_cols = ["Cleared_Round_1", "Cleared_Round_2", "Cleared_Round_3"]
    
    existing_cols = [col for col in possible_cols if col in df.columns]
    
    if len(existing_cols) == 0:
        return 0
    
    cleared = df[existing_cols].sum().sum()
    
    if "Total_Rounds" in df.columns:
        total = df["Total_Rounds"].sum()
    else:
        total = len(df) * len(existing_cols)
    
    return cleared / total if total > 0 else 0
