EXPECTED_AREAS = [
    "Hall", "Bedroom", "Bathroom",
    "Kitchen", "External Wall", "WC"
]


def validate_data(structured_data):

    missing = []

    for area in EXPECTED_AREAS:
        if len(structured_data.get(area, [])) == 0:
            missing.append(area)

    completeness = 1 - (len(missing) / len(EXPECTED_AREAS))

    return {
        "missing_areas": missing,
        "completeness_score": round(completeness, 2)
    }