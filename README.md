# AI Legal Analyst - Universal Credit Act 2025

## 🚀 Overview

This project is an AI-powered agent designed to analyze the **Universal Credit Act 2025**. It extracts raw text from PDF, generates a legal summary, structures key legislative data into JSON, and runs a compliance audit against a set of regulatory rules.

## 🛠️ Architecture

The solution is built using a modular pipeline approach:

1.  **Extraction Layer (`1_extract.py`)**: Uses `pypdf` with custom Regex cleaning to remove legislative artifacts (running headers, page numbers) that confuse standard parsers.
2.  **Analysis Engine (`2_agent.py`)**: Leverages **Gemini 2.5 Flash** with specific prompts to perform semantic summarization and extraction of complex nested clauses.
3.  **Audit Logic (`3_auditor.py`)**: A strict rule-based evaluation agent that cross-references the text against 6 specific legislative requirements.

## 📦 Output

The final output is a structured JSON file `FINAL_DELIVERABLE.json` containing:

- **Executive Summary**: 8 bullet points covering the Act's purpose.
- **Legislative Extraction**: Structured data on eligibility, obligations, and payments.
- **Compliance Audit**: A Pass/Fail report with evidence citations for 6 regulatory rules.

## 🔧 Setup & Usage

### Prerequisites

- Python 3.8+
- A Google Gemini API Key

### Installation

```bash
pip install pypdf google-generativeai python-dotenv
```

### Running the Pipeline

Add your API key to a .env file:
GEMINI_API_KEY=your_key_here

Run the extraction script:
python 1_extract.py

Run the analysis agent:
python 2_agent.py

Run the auditor:
python 3_auditor.py

Generate final report:
python 4_assemble.py

## 🧠 Key Decisions

1. Model Choice: Used Gemini 2.5 Flash for its high speed and long context window, essential for reading full legislative acts in one pass.

2. Handling "Failures": The Audit Agent is designed to be honest. The Universal Credit Act 2025 is an Amendment Act; therefore, it does not contain explicit "Penalties" or "Record Keeping" clauses (which exist in the parent 2012 Act). The agent correctly marks these as FAIL rather than hallucinating compliance.
