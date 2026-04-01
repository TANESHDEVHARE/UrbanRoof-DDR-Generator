import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import streamlit as st
from ingestion.parser import load_documents
from generation.ddr_generator import generate_ddr
from generation.pdf_generator import create_pdf

def _build_context(docs, keywords, max_chars=18000, max_pages=12):
    image_info_blocks = []
    scored = []

    for d in docs:
        meta = d.get("metadata", {}) if isinstance(d, dict) else {}
        if meta.get("type") == "image_info":
            image_info_blocks.append(d.get("page_content", ""))
            continue

        text = d.get("page_content", "")
        text_lower = text.lower()
        score = 0
        for k in keywords:
            score += text_lower.count(k)

        page = meta.get("page") or 0
        area = meta.get("area")
        scored.append((score, page, area, text))

    scored.sort(key=lambda x: (x[0], x[1]), reverse=True)
    selected = [x for x in scored if x[0] > 0][:max_pages]

    if not selected:
        selected = scored[:max_pages]

    selected.sort(key=lambda x: x[1])

    parts = []
    total = 0
    for score, page, area, text in selected:
        area_part = f" | Area: {area}" if area else ""
        header = f"[Page {page}{area_part}]\n"
        chunk = (header + (text or "").strip()).strip()
        if not chunk:
            continue
        if total + len(chunk) > max_chars:
            remaining = max_chars - total
            if remaining <= 0:
                break
            chunk = chunk[:remaining]
        parts.append(chunk)
        total += len(chunk)
        if total >= max_chars:
            break

    if image_info_blocks:
        image_info = "\n".join([b for b in image_info_blocks if b])
        if image_info:
            parts.append(image_info)

    return "\n\n".join(parts)

st.set_page_config(page_title="DDR Generator", layout="centered")

st.title("🏗️ DDR Generator")
st.markdown("Upload both Inspection and Thermal reports to generate a detailed diagnostic report.")

# Upload inputs
inspection_file = st.file_uploader("Upload Inspection PDF", type=["pdf"])
thermal_file = st.file_uploader("Upload Thermal PDF", type=["pdf"])

# Generate button
if st.button("Generate DDR"):

    if not inspection_file or not thermal_file:
        st.warning("⚠️ Please upload BOTH Inspection and Thermal reports.")
        st.stop()

    with st.spinner("Processing documents..."):

        # Save files
        with open("inspection.pdf", "wb") as f:
            f.write(inspection_file.read())

        with open("thermal.pdf", "wb") as f:
            f.write(thermal_file.read())

        # Load documents
        insp_docs, insp_images = load_documents("inspection.pdf", image_prefix="inspection")
        therm_docs, therm_images = load_documents("thermal.pdf", image_prefix="thermal")

        images = insp_images + therm_images

        inspection_context = _build_context(
            insp_docs,
            keywords=[
                "observation", "finding", "issue", "defect",
                "damp", "dampness", "leak", "leakage", "seep",
                "crack", "spalling", "stain", "mould", "mold",
                "efflorescence", "fungus", "water",
            ],
        )

        thermal_context = _build_context(
            therm_docs,
            keywords=[
                "thermal", "temperature", "temp", "°c", "deg",
                "anomaly", "variation", "moisture", "damp",
                "wet", "leak", "seep",
            ],
        )

        # Combine properly
        context = f"""
        ===== Inspection Report =====
        {inspection_context}

        ===== Thermal Report =====
        {thermal_context}
        """

        try:
            ddr = generate_ddr(context)
        except Exception as e:
            st.error(f"❌ Error generating DDR: {e}")
            st.stop()

    # Display output
    st.subheader("📄 Generated DDR Report")
    st.text_area("DDR Output", ddr, height=500)

    # Generate PDF
    try:
        os.makedirs("outputs", exist_ok=True)

        pdf_path = "outputs/DDR_Report.pdf"
        create_pdf(ddr, images)

        st.success("✅ PDF Generated Successfully")

        # Download button
        with open(pdf_path, "rb") as f:
            st.download_button(
                label="📥 Download DDR PDF",
                data=f,
                file_name="DDR_Report.pdf",
                mime="application/pdf"
            )

    except Exception as e:
        st.error(f"❌ Error generating PDF: {e}")