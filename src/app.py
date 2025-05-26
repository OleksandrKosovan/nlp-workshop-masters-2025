import streamlit as st
import os
from pdf_processor import TenderPDFProcessor
import json
from datetime import datetime

st.set_page_config(
    page_title="EU Tender PDF Processor",
    page_icon="📄",
    layout="wide"
)

st.title("EU Tender PDF Processor")
st.markdown("""
This application helps you extract key information from EU tender PDF documents.
Upload a tender document to get started!
""")

def save_uploaded_file(uploaded_file):
    """Save uploaded file to a temporary location and return the path."""
    temp_dir = "temp"
    if not os.path.exists(temp_dir):
        os.makedirs(temp_dir)
    
    file_path = os.path.join(temp_dir, uploaded_file.name)
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    return file_path

def display_extracted_info(info):
    """Display extracted information in a structured format."""
    st.subheader("Extracted Information")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**Tender ID:**", info['tender_id'] or "Not found")
        st.write("**Publication Date:**", info['publication_date'] or "Not found")
        st.write("**Submission Deadline:**", info['submission_deadline'] or "Not found")
    
    with col2:
        st.write("**Contract Value:**", info['contract_value'] or "Not found")
        st.write("**CPV Codes:**")
        if info['cpv_codes']:
            for cpv in info['cpv_codes']:
                st.write(f"- {cpv}")
        else:
            st.write("No CPV codes found")

def main():
    uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")
    
    if uploaded_file:
        st.success("File uploaded successfully!")
        
        # Save the uploaded file
        file_path = save_uploaded_file(uploaded_file)
        
        try:
            # Process the PDF
            processor = TenderPDFProcessor(file_path)
            
            # Extract information
            info = processor.extract_all_information()
            
            # Display the extracted information
            display_extracted_info(info)
            
            # Show text summary
            st.subheader("Document Summary")
            summary = processor.get_text_summary()
            st.text_area("Summary", summary, height=200)
            
            # Export options
            st.subheader("Export Options")
            if st.button("Export as JSON"):
                # Create download link for JSON
                json_str = json.dumps(info, indent=2)
                st.download_button(
                    label="Download JSON",
                    data=json_str,
                    file_name=f"tender_info_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                    mime="application/json"
                )
            
        except Exception as e:
            st.error(f"Error processing PDF: {str(e)}")
        
        finally:
            # Cleanup
            if os.path.exists(file_path):
                os.remove(file_path)

if __name__ == "__main__":
    main() 