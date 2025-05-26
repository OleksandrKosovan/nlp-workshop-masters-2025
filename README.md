# EU Tender PDF Processing Workshop

This workshop demonstrates how to build a Proof of Concept (PoC) for processing EU tender PDF files. You'll learn how to extract key information from tender documents using Python.

## Setup

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Project Structure

- `data/` - Contains sample EU tender PDF files
- `src/` - Source code
  - `pdf_processor.py` - Core PDF processing functionality
  - `app.py` - Streamlit web interface
- `requirements.txt` - Project dependencies

## Workshop Steps

1. **Basic PDF Text Extraction**
   - Learn how to extract raw text from PDF files
   - Understand PDF document structure

2. **Key Information Extraction**
   - Extract tender-specific information:
     - Tender ID
     - Publication date
     - Deadline
     - Contract value
     - CPV codes

3. **Data Structuring**
   - Convert extracted information into structured format
   - Export to CSV/JSON

4. **Web Interface**
   - Upload and process PDF files through Streamlit interface
   - View extracted information in a user-friendly format

## Running the Application

Start the Streamlit application:
```bash
streamlit run src/app.py
```

## Notes

- The example uses `pdfplumber` for PDF processing
- NLTK is used for text processing and entity extraction
- Streamlit provides an easy-to-use web interface 