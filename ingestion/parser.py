try:
    import fitz  # PyMuPDF
except ModuleNotFoundError:
    fitz = None
import os
import re


AREAS = [
    "Hall", "Bedroom", "Bathroom",
    "Kitchen", "Terrace", "External Wall",
    "WC", "Parking"
]


def _detect_area(text):
    text_lower = text.lower()

    if "external wall" in text_lower:
        return "External Wall"

    if "common bathroom" in text_lower:
        return "Bathroom"

    if "bathroom" in text_lower:
        return "Bathroom"

    if re.search(r"\bwc\b", text_lower):
        return "WC"

    for area in AREAS:
        if area.lower() in text_lower:
            return area

    return None


def load_documents(pdf_path, image_prefix=None):

    if fitz is None:
        raise RuntimeError("PyMuPDF is required for PDF parsing. Install it with: python -m pip install pymupdf")

    doc = fitz.open(pdf_path)
    prefix = image_prefix or os.path.splitext(os.path.basename(pdf_path))[0]

    text_data = []
    images = []

    os.makedirs("outputs/images", exist_ok=True)

    seen_hashes = set()  # 🔥 avoid duplicates

    for page_num, page in enumerate(doc):

        # 🔹 Extract text
        text = page.get_text()

        area = _detect_area(text)

        text_data.append({
            "page_content": text,
            "metadata": {"page": page_num + 1, "area": area}
        })

        # 🔥 Extract images
        for img_index, img in enumerate(page.get_images(full=True)):

            xref = img[0]
            base_image = doc.extract_image(xref)

            image_bytes = base_image["image"]
            ext = base_image["ext"]

            # 🔥 SIZE FILTER (remove icons/logos)
            if len(image_bytes) < 10000:
                continue

            # 🔥 DIMENSION FILTER (VERY IMPORTANT)
            width = base_image.get("width", 0)
            height = base_image.get("height", 0)

            aspect_ratio = width / height if height != 0 else 0

            if aspect_ratio > 3 or aspect_ratio < 0.3:
                continue

            # 🔥 REMOVE KNOWN BRAND / UI IMAGES
            img_text = base_image.get("image", b"")

            if b"UrbanRoof" in img_text or b"BOSCH" in img_text:
                continue

            # 🔥 REMOVE DUPLICATES (by hash)
            img_hash = hash(image_bytes)
            if img_hash in seen_hashes:
                continue
            seen_hashes.add(img_hash)

            # 🔥 SAVE IMAGE
            img_path = f"outputs/images/{prefix}_page{page_num+1}_{img_index}.{ext}"

            with open(img_path, "wb") as f:
                f.write(image_bytes)

            # ✅ STRUCTURED FORMAT
            images.append({
                "path": img_path,
                "page": page_num + 1,
                "area": area,
                "source": prefix,
                "width": width,
                "height": height
            })

    # 🔥 Add image references into LLM context (clean + useful)
    image_text = "\n".join([
        f"[Image on Page {img['page']} (Area: {img.get('area') or 'Unknown'}): {img['path']}]"
        for img in images
    ])

    text_data.append(
        {
            "page_content": image_text,
            "metadata": {"type": "image_info"}
        }
    )

    return text_data, images