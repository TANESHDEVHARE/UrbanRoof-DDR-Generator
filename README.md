# DDR Generator 🏠🔍

[![Streamlit](https://static.streamlit.io/badges/using_streamlit_app_badges.svg)](https://streamlit.io/)

## 🖥️ Live Demo

[![Demo](https://img.shields.io/badge/Streamlit-Live_Demo-FF4B4B?style=for-the-badge&logo=streamlit)](http://localhost:8501)

**Local Live Demo:** http://localhost:8501  
**Network Access:** http://192.168.29.125:8501  
**🌐 Deploy Public Demo:** [Streamlit Cloud](https://urbanroof-ddr-generator-taneshdevhare.streamlit.app/)

## Overview

**DDR Generator** is an AI-powered tool that automatically generates **Detailed Diagnostic Reports (DDR)** from property inspection PDFs and thermal imaging reports. 

It intelligently extracts key observations (dampness, leaks, cracks, thermal anomalies), correlates inspection findings with thermal data, and produces professional PDF reports with embedded images.

## ✨ Features

- **Dual PDF Processing**: Handles both inspection reports and thermal imaging PDFs
- **Smart Content Extraction**: Keyword-based relevance scoring for inspection issues (damp, leaks, cracks, etc.)
- **Thermal Anomaly Detection**: Identifies temperature variations and moisture patterns
- **AI-Powered Report Generation**: LLM-driven synthesis of findings into structured DDR
- **Professional PDF Output**: ReportLab-generated PDFs with embedded images
- **Streamlit Web Interface**: Upload files → Generate report → Download PDF
- **Production Ready**: Vector stores, reasoning engines, validation pipelines

## 📱 Assets

### Architecture Diagram
![AI Architecture](Assets/AI%20Arch.jpeg)

### Sample Generated DDR Report
![Sample DDR](Assets/DDR_Report.pdf)

**Sample DDR Text Preview:**
```
Detailed Diagnostic Report (DDR)

1. Property Issue Summary:
- Multiple areas in the property show dampness at skirting levels including Hall, Bedroom, Master Bedroom, and Kitchen.
[...]

7. Missing or Unclear Information:
- Exact locations of thermal images relative to impacted areas are not specified.
```

## 🚀 Quick Start

### Prerequisites
- Python 3.9+
- Git
- OpenAI API key 

### Installation
```bash
git clone <repository-url>
cd DDR_Generator
pip install -r requirements.txt
```

### Run the App
```bash
streamlit run app/streamlit_app.py
```

## 📋 Usage

1. **Upload Files**:
   - Inspection PDF (observations, findings, defects)
   - Thermal PDF (temperature maps, anomaly images)

2. **Click "Generate DDR"**

3. **Download**: Professional PDF report with analysis + images

**Sample Files** (`given/`):
- `Sample Report.pdf` (inspection)
- `Thermal Images.pdf` (thermal)

## 🏗️ Project Structure

```
DDR_Generator/
├── app/              # Streamlit UI ⭐
├── core/             # Engines & LLM
├── generation/       # AI + PDF generation
├── ingestion/        # PDF parsing
├── Assets/           # Screenshots ⭐
├── given/            # Samples
├── outputs/          # Generated PDFs
└── requirements.txt
```


---

⭐ **If this helps, star the repo!**

