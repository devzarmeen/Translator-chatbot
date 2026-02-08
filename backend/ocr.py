"""
OCR module for AI Translator Chatbot.
Handles image-to-text extraction using OCR.
"""

import os
from typing import Optional, Dict
import pytesseract
from PIL import Image
import io
from dotenv import load_dotenv

load_dotenv()

# Configure Tesseract path if provided in environment variables
tesseract_cmd = os.getenv("TESSERACT_CMD")
if tesseract_cmd:
    pytesseract.pytesseract.tesseract_cmd = tesseract_cmd


class OCRService:
    """Service for handling OCR operations."""
    
    def __init__(self):
        # Try to detect Tesseract installation
        try:
            pytesseract.get_tesseract_version()
        except Exception:
            print("Warning: Tesseract OCR not found. OCR functionality may not work.")
            print("Install Tesseract from: https://github.com/UB-Mannheim/tesseract/wiki")
            print("Or set TESSERACT_CMD in .env file if installed in custom location.")
    
    def extract_text_from_image(
        self, 
        image_data: bytes, 
        language: str = "eng"
    ) -> Dict[str, any]:
        """
        Extract text from image using OCR.
        
        Args:
            image_data: Image data as bytes
            language: OCR language code (default: "eng" for English)
            
        Returns:
            Dictionary with extracted text and metadata
        """
        try:
            # Convert bytes to PIL Image
            image = Image.open(io.BytesIO(image_data))
            
            # Perform OCR
            extracted_text = pytesseract.image_to_string(image, lang=language)
            
            # Clean up extracted text
            extracted_text = extracted_text.strip()
            
            if not extracted_text:
                return {
                    "success": False,
                    "error": "No text found in image",
                    "extracted_text": ""
                }
            
            return {
                "success": True,
                "extracted_text": extracted_text,
                "language": language,
                "confidence": None  # Tesseract doesn't provide confidence by default
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "extracted_text": ""
            }
    
    def get_supported_ocr_languages(self) -> list:
        """Get list of supported OCR languages."""
        try:
            langs = pytesseract.get_languages()
            return langs
        except Exception:
            return ["eng"]  # Default to English if Tesseract not available
    
    def is_supported_ocr_language(self, lang_code: str) -> bool:
        """Check if OCR language is supported."""
        try:
            supported = self.get_supported_ocr_languages()
            return lang_code in supported
        except Exception:
            return lang_code == "eng"


# Singleton instance
ocr_service = OCRService()
