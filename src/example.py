from pdf_processor import TenderPDFProcessor
import json
from pathlib import Path
import os

def process_tender_document(pdf_path: str):
    """Example function showing how to process a tender document."""
    print(f"Processing tender document: {pdf_path}")
    
    # Initialize the processor
    processor = TenderPDFProcessor(pdf_path)
    
    # Extract all information
    info = processor.extract_all_information()
    
    # Print extracted information
    print("\nExtracted Information:")
    print("-" * 50)
    print(f"Tender ID: {info['tender_id']}")
    print(f"Publication Date: {info['publication_date']}")
    print(f"Submission Deadline: {info['submission_deadline']}")
    print(f"Contract Value: {info['contract_value']}")
    print("\nCPV Codes:")
    for cpv in info['cpv_codes']:
        print(f"- {cpv}")
    
    # Get document summary
    print("\nDocument Summary:")
    print("-" * 50)
    print(processor.get_text_summary())
    
    # Export to JSON
    output_file = Path(pdf_path).stem + "_info.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(info, f, indent=2)
    print(f"\nExported information to: {output_file}")

if __name__ == "__main__":
    # Get the absolute path to the PDF file
    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(current_dir)
    sample_pdf = os.path.join(project_root, "data", "2025-OJS098-00331813-en.pdf")
    
    if not os.path.exists(sample_pdf):
        print(f"Error: PDF file not found at {sample_pdf}")
        print("Please make sure the PDF file exists in the data directory.")
    else:
        process_tender_document(sample_pdf) 