import re

AREAS = [
    "Hall", "Bedroom", "Bathroom",
    "Kitchen", "Terrace", "External Wall",
    "WC", "Parking"
]


def extract_structured_data(docs):

    structured = {area: [] for area in AREAS}

    for doc in docs:
        text = doc.page_content

        for area in AREAS:
            if area.lower() in text.lower():
                structured[area].append(text)

    return structured