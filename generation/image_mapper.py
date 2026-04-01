def map_images_to_sections(images):

    mapping = {
        "Hall": [],
        "Bedroom": [],
        "Bathroom": [],
        "Kitchen": [],
        "Terrace": [],
        "External Wall": [],
        "WC": [],
        "Parking": []
    }

    for img in images:
        if isinstance(img, dict):
            page = img.get("page")
            path = img.get("path")
            area = img.get("area")
        else:
            page = None
            path = img
            area = None

        if area in mapping and path:
            mapping[area].append(img)
            continue

        if page is None or not path:
            continue

        # 🔥 SMART PAGE BASED HEURISTIC
        if page <= 3:
            mapping["Hall"].append(img)

        elif page <= 6:
            mapping["Bedroom"].append(img)

        elif page <= 10:
            mapping["Bathroom"].append(img)

        elif page <= 15:
            mapping["External Wall"].append(img)

        else:
            mapping["WC"].append(img)

    return mapping