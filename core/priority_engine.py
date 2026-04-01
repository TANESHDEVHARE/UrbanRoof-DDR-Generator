def classify_severity(text):

    text = text.lower()

    if "leakage all the time" in text or "concealed plumbing" in text:
        return "Critical"

    elif "dampness" in text:
        return "Moderate"

    elif "crack" in text:
        return "Minor"

    return "Normal"