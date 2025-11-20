import json

def load_json(filename):
    with open(filename, "r", encoding="utf-8") as f:
        return json.load(f)

if __name__ == "__main__":
    # Load the individual parts
    analysis = load_json("task_output.json")
    audit = load_json("audit_report.json")
    
    # Create the master structure
    final_report = {
        "document_name": "Universal Credit Act 2025",
        "summary_report": analysis["summary"],
        "legislative_extraction": analysis["extraction"],
        "compliance_audit": audit
    }
    
    # Save final deliverable
    with open("FINAL_DELIVERABLE.json", "w", encoding="utf-8") as f:
        json.dump(final_report, f, indent=2)
        
    print("SUCCESS! 'FINAL_DELIVERABLE.json' has been created.")