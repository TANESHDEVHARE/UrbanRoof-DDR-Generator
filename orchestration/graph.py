from langgraph.graph import StateGraph
from langchain_core.documents import Document
from generation.ddr_generator import generate_ddr
from core.extractor import extract_structured_data
from core.validator import validate_data
from core.reasoning_engine import analyze_thermal
from core.priority_engine import classify_severity


def build_graph():

    def run(state):

        context = state["context"]

        docs = [Document(page_content=context)]

        structured = extract_structured_data(docs)

        validation = validate_data(structured)

        report = "Detailed Diagnostic Report (DDR)\n\n"

        report += f"Completeness Score: {validation['completeness_score']}\n"

        if validation["missing_areas"]:
            report += f"Missing Areas: {', '.join(validation['missing_areas'])}\n\n"

        for area, texts in structured.items():

            if not texts:
                continue

            combined = " ".join(texts)

            severity = classify_severity(combined)

            thermal_analysis = analyze_thermal(combined)

            report += f"{area}:\n"
            report += f"- Severity: {severity}\n"
            report += f"- Analysis: {thermal_analysis}\n\n"

        return {"output": report}

    return type("Graph", (), {"invoke": run})