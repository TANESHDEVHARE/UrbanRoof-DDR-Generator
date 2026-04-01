import re


def extract_temperature(text):

    temps = re.findall(r'(\d+\.?\d*)\s?°C', text)

    return [float(t) for t in temps]


def analyze_thermal(text):

    temps = extract_temperature(text)

    if len(temps) < 2:
        return "Insufficient thermal data"

    delta = max(temps) - min(temps)

    if delta > 5:
        return f"High thermal variation ({delta}°C) → strong moisture presence"

    elif delta > 2:
        return f"Moderate variation ({delta}°C) → possible dampness"

    else:
        return f"Low variation ({delta}°C) → normal"