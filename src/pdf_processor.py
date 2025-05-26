import pdfplumber
import re
from datetime import datetime
from typing import Dict, Any, Optional
import nltk
from nltk.tokenize import word_tokenize

# Download required NLTK data
nltk.download('punkt')

class TenderPDFProcessor:
    def __init__(self, file_path: str):
        """Initialize the PDF processor with a file path."""
        self.file_path = file_path
        self.text = None
        self.pages = []
        self._load_pdf()

    def _load_pdf(self):
        """Load the PDF file and extract text from all pages."""
        with pdfplumber.open(self.file_path) as pdf:
            self.pages = pdf.pages
            self.text = '\n'.join(page.extract_text() for page in self.pages)

    def _find_pattern(self, pattern: str) -> Optional[str]:
        """Helper method to find patterns in text."""
        match = re.search(pattern, self.text)
        return match.group(1) if match else None

    def extract_tender_id(self) -> Optional[str]:
        """Extract tender ID from the document."""
        patterns = [
            r'Document\s+No:\s*([0-9-]+)',
            r'Reference\s+number:\s*([0-9-]+)',
            r'Tender\s+ID:\s*([0-9-]+)'
        ]
        
        for pattern in patterns:
            result = self._find_pattern(pattern)
            if result:
                return result
        return None

    def extract_dates(self) -> Dict[str, Optional[str]]:
        """Extract important dates from the document."""
        date_patterns = {
            'publication_date': r'Date of publication:\s*(\d{2}/\d{2}/\d{4})',
            'submission_deadline': r'Time limit[^:]*:\s*(\d{2}/\d{2}/\d{4})',
        }
        
        dates = {}
        for key, pattern in date_patterns.items():
            dates[key] = self._find_pattern(pattern)
        return dates

    def extract_contract_value(self) -> Optional[str]:
        """Extract contract value information."""
        patterns = [
            r'Value\s+excluding\s+VAT:\s*([^\n]+)',
            r'Estimated\s+value:\s*([^\n]+)',
            r'Contract\s+value:\s*([^\n]+)'
        ]
        
        for pattern in patterns:
            result = self._find_pattern(pattern)
            if result:
                return result.strip()
        return None

    def extract_cpv_codes(self) -> list:
        """Extract CPV (Common Procurement Vocabulary) codes."""
        cpv_pattern = r'CPV[^:]*:\s*(\d{8}[-\d]*)'
        return re.findall(cpv_pattern, self.text)

    def extract_all_information(self) -> Dict[str, Any]:
        """Extract all relevant information from the tender document."""
        dates = self.extract_dates()
        
        return {
            'tender_id': self.extract_tender_id(),
            'publication_date': dates.get('publication_date'),
            'submission_deadline': dates.get('submission_deadline'),
            'contract_value': self.extract_contract_value(),
            'cpv_codes': self.extract_cpv_codes(),
        }

    def get_text_summary(self, max_length: int = 500) -> str:
        """Get a summary of the tender document text."""
        if not self.text:
            return ""
        
        # Simple extractive summary - first few sentences
        sentences = self.text.split('.')
        summary = []
        current_length = 0
        
        for sentence in sentences:
            if current_length + len(sentence) > max_length:
                break
            summary.append(sentence.strip())
            current_length += len(sentence)
        
        return '. '.join(summary) + '.' 