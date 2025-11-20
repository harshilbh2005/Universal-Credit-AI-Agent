import pypdf
import re

def clean_text(text):
    """
    Basic cleaning to remove headers/footers common in UK Act PDFs.
    """
    lines = text.split('\n')
    cleaned_lines = []
    
    # Patterns to filter out based on the specific document structure
    patterns_to_remove = [
        r"Universal Credit Act 2025 \(c\. 22\)",  # The running header
        r"^\d+$",                                 # Standalone page numbers
        r"^Subject to correction$"                # Common draft watermark (safety check)
    ]
    
    for line in lines:
        line = line.strip()
        # Skip empty lines
        if not line:
            continue
            
        # Skip lines that match our noise patterns
        is_noise = False
        for pattern in patterns_to_remove:
            if re.search(pattern, line):
                is_noise = True
                break
        
        if not is_noise:
            cleaned_lines.append(line)
            
    return "\n".join(cleaned_lines)

def extract_text_from_pdf(pdf_path):
    print(f"Processing {pdf_path}...")
    try:
        reader = pypdf.PdfReader(pdf_path)
        full_text = ""
        
        for i, page in enumerate(reader.pages):
            raw_text = page.extract_text()
            if raw_text:
                full_text += clean_text(raw_text) + "\n"
                
        print(f"Successfully extracted {len(reader.pages)} pages.")
        return full_text
        
    except Exception as e:
        print(f"Error reading PDF: {e}")
        return None

if __name__ == "__main__":
    # Run extraction
    extracted_text = extract_text_from_pdf("ukpga_20250022_en.pdf")
    
    if extracted_text:
        # Save to file so we can inspect it and use it in the next step
        with open("extracted_text.txt", "w", encoding="utf-8") as f:
            f.write(extracted_text)
        print("Saved clean text to 'extracted_text.txt'")
        
        # Preview the first 500 characters
        print("\n--- PREVIEW ---")
        print(extracted_text[:500])
        print("...")