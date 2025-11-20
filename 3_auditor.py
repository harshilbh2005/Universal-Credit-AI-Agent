import os
import json
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def load_file(filename):
    with open(filename, "r", encoding="utf-8") as f:
        return f.read()

def audit_rules(text, previous_analysis):
    print("Initializing Compliance Auditor Agent...")
    
    generation_config = {
        "temperature": 0.0, # Zero temperature for strict logic
        "response_mime_type": "application/json",
    }

    model = genai.GenerativeModel(
        model_name="gemini-2.5-flash",
        generation_config=generation_config,
    )

    # The 6 Rules from the Assignment
    rules = [
        "1. Act must define key terms",
        "2. Act must specify eligibility criteria",
        "3. Act must specify responsibilities of the administering authority",
        "4. Act must include enforcement or penalties",
        "5. Act must include payment calculation or entitlement structure",
        "6. Act must include record-keeping or reporting requirements"
    ]

    prompt = f"""
    You are a strict Legal Compliance Auditor. 
    
    Analyze the "Universal Credit Act 2025" text and the provided summary analysis to determine if the Act complies with the following 6 rules.
    
    ---
    
    INPUT DATA:
    
    Extracted Text (Snippet):
    {text[:5000]} ... [truncated for length]
    
    Previous Analysis (JSON):
    {previous_analysis}
    
    ---
    
    RULES TO CHECK:
    {json.dumps(rules, indent=2)}
    
    ---
    
    INSTRUCTIONS:
    
    For EACH rule, determine:
    1. **Status**: "pass" or "fail". 
       - If the Act mentions it explicitly, it passes.
       - If the Act is silent on it, it fails (be honest).
    2. **Evidence**: Quote the section number or specific text that supports your decision.
    3. **Confidence**: A score from 0-100.
    
    Output must be a strictly formatted JSON List of Objects:
    [
        {{
            "rule": "1. Act must define key terms",
            "status": "pass",
            "evidence": "Section 2 defines 'pre-2026 claimant'...",
            "confidence": 95
        }},
        ...
    ]
    """

    print("Auditing the Act against rules...")
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        print(f"API Error: {e}")
        return None

if __name__ == "__main__":
    # 1. Load data
    text_data = load_file("extracted_text.txt")
    json_data = load_file("task_output.json")
    
    # 2. Run Auditor
    audit_result = audit_rules(text_data, json_data)
    
    # 3. Save Output
    if audit_result:
        with open("audit_report.json", "w", encoding="utf-8") as f:
            f.write(audit_result)
        
        print("\nSUCCESS! Audit saved to 'audit_report.json'")
        
        # Preview
        report = json.loads(audit_result)
        print("\n--- AUDIT REPORT ---")
        for item in report:
            status_icon = "✅" if item['status'] == 'pass' else "❌"
            print(f"{status_icon} {item['rule']}")
            print(f"   Evidence: {item['evidence']}")