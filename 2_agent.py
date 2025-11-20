import os
import google.generativeai as genai
import json
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure Gemini
# Make sure you have a .env file with GEMINI_API_KEY=your_key_here
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def load_text(filename):
    with open(filename, "r", encoding="utf-8") as f:
        return f.read()

def analyze_act(text):
    print("Initializing Gemini Agent...")
    
    # specific instruction to force JSON output
    generation_config = {
        "temperature": 0.1,
        "response_mime_type": "application/json",
    }

    model = genai.GenerativeModel(
        model_name="gemini-2.5-flash",
        generation_config=generation_config,
    )

    # This prompt combines Task 2 (Summary) and Task 3 (Extraction)
    prompt = f"""
    You are a legal expert AI. Your task is to analyze the "Universal Credit Act 2025".
    
    Input Text:
    {text}

    ---
    
    REQUIREMENTS:
    
    1. **Summarize** the Act in 5-10 bullet points covering:
       - Purpose
       - Key definitions
       - Eligibility changes
       - Obligations
       - Enforcement elements
    
    2. **Extract** specific legislative sections into a structured format. Since this is an amendment act, if a section refers to an external act (like "Welfare Reform Act 2012"), explain the *implication* of the change.
    
    Output must be a VALID JSON object with this exact structure:
    {{
        "summary": [
            "bullet point 1",
            "bullet point 2"
        ],
        "extraction": {{
            "definitions": "Extract key terms defined in the act (e.g., 'tax year', 'relevant CPI percentage').",
            "obligations": "What must the Secretary of State or Department do?",
            "responsibilities": "Who is responsible for implementation?",
            "eligibility": "Who is affected? (e.g., pre-2026 claimants, LCWRA elements).",
            "payments": "Details on standard allowance rates, freezes, or uplifts.",
            "penalties": "Any mention of enforcement or what happens if conditions aren't met.",
            "record_keeping": "Any mention of reporting or data requirements."
        }}
    }}
    """

    print("Sending data to Gemini (this may take a few seconds)...")
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        print(f"API Error: {e}")
        return None

if __name__ == "__main__":
    # 1. Load the text we extracted in Step 1
    cleaned_text = load_text("extracted_text.txt")
    
    # 2. Run the Agent
    json_result = analyze_act(cleaned_text)
    
    # 3. Save Output
    if json_result:
        with open("task_output.json", "w", encoding="utf-8") as f:
            f.write(json_result)
        print("\nSUCCESS! Analysis saved to 'task_output.json'")
        
        # Preview
        data = json.loads(json_result)
        print("\n--- Summary Preview ---")
        for point in data["summary"][:3]:
            print(f"- {point}")