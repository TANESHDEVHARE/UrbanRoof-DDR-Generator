import os
import re

try:
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
    from reportlab.lib.pagesizes import A4
    from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
    from reportlab.lib.units import inch
    from reportlab.lib.utils import ImageReader
except ModuleNotFoundError:
    SimpleDocTemplate = None
    Paragraph = None
    Spacer = None
    Image = None
    A4 = None
    ParagraphStyle = None
    getSampleStyleSheet = None
    inch = 72
    ImageReader = None

from generation.image_mapper import map_images_to_sections


# 🔥 REMOVE FAKE IMAGE TEXT FROM LLM
def clean_line(line):
    line_lower = line.lower()

    if "image:" in line_lower or "photos" in line_lower:
        return None

    if line_lower.strip().startswith("[image on page"):
        return None

    return line


def _match_area(line, areas):
    s = (line or "").strip()
    if s.endswith(":"):
        s = s[:-1].strip()

    for area in areas:
        if s.lower() == area.lower():
            return area

    return None


def create_pdf(report_text, images, output_path="outputs/DDR_Report.pdf"):

    if SimpleDocTemplate is None:
        raise RuntimeError("reportlab is required for PDF generation. Install it with: python -m pip install reportlab")

    os.makedirs(os.path.dirname(output_path) or ".", exist_ok=True)

    doc = SimpleDocTemplate(
        output_path,
        pagesize=A4,
        leftMargin=36,
        rightMargin=36,
        topMargin=36,
        bottomMargin=36,
    )
    styles = getSampleStyleSheet()

    title_style = styles['Title']
    heading_style = styles.get('Heading1', styles['Title'])
    subheading_style = styles.get('Heading2', styles['Heading1'])
    normal_style = styles['Normal']
    bullet_style = ParagraphStyle(
        "DDR-Bullet",
        parent=normal_style,
        leftIndent=18,
        bulletIndent=6,
        spaceBefore=2,
        spaceAfter=2,
    )
    area_style = ParagraphStyle(
        "DDR-Area",
        parent=subheading_style,
        spaceBefore=10,
        spaceAfter=6,
    )

    elements = []

    # Title
    elements.append(Paragraph("Detailed Diagnostic Report (DDR)", title_style))
    elements.append(Spacer(1, 20))

    # Map images to sections
    image_map = map_images_to_sections(images)

    current_section = None
    image_used = False
    used_images = set()
    in_area_observations = False
    areas = list(image_map.keys())

    for raw_line in report_text.split("\n"):

        # 🔥 CLEAN FAKE IMAGE TEXT
        line = clean_line(raw_line)
        if not line:
            continue

        stripped = line.strip()

        if re.match(r"^\d+\.\s+", stripped):
            elements.append(Spacer(1, 10))
            elements.append(Paragraph(stripped, heading_style))
            elements.append(Spacer(1, 6))
            in_area_observations = stripped.startswith("2.") or ("area-wise" in stripped.lower())
            current_section = None
            continue

        if in_area_observations:
            matched_area = _match_area(stripped, areas)
            if matched_area:
                current_section = matched_area
                elements.append(Paragraph(matched_area, area_style))
                elements.append(Spacer(1, 6))

                # 🔥 INSERT IMAGES ONLY AFTER SECTION HEADER
                inserted_any = False
                inserted_count = 0
                max_width = doc.width
                max_height = 3.8 * inch

                for img in image_map.get(current_section, []):
                    img_path = img.get("path") if isinstance(img, dict) else img

                    if not img_path:
                        continue
                    if img_path in used_images:
                        continue
                    if not os.path.exists(img_path):
                        continue

                    try:
                        w = max_width
                        h = max_height
                        if ImageReader is not None:
                            iw, ih = ImageReader(img_path).getSize()
                            if iw and ih:
                                scale = min(max_width / float(iw), max_height / float(ih))
                                w = float(iw) * scale
                                h = float(ih) * scale
                        elements.append(Image(img_path, width=w, height=h))
                        elements.append(Spacer(1, 10))
                        used_images.add(img_path)
                        inserted_any = True
                        image_used = True
                        inserted_count += 1
                    except Exception:
                        continue

                    if inserted_count >= 3:
                        break

                # If no valid image
                if not inserted_any:
                    elements.append(Paragraph("Image Not Available", normal_style))
                    elements.append(Spacer(1, 10))

                # Avoid duplicate insertion
                image_map[current_section] = []

                continue

        if stripped.startswith("-"):
            bullet = stripped.lstrip("-").strip()
            if bullet:
                elements.append(Paragraph(bullet, bullet_style, bulletText="-"))
            else:
                elements.append(Paragraph(stripped, bullet_style))
            elements.append(Spacer(1, 2))
        else:
            elements.append(Paragraph(stripped, normal_style))
            elements.append(Spacer(1, 6))

    # 🔥 FINAL FALLBACK (if no image shown anywhere)
    if not image_used:
        elements.append(Paragraph("Image Not Available", normal_style))

    doc.build(elements)

    return output_path