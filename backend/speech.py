"""
Speech module for AI Translator Chatbot.
Handles Speech-to-Text (STT) and Text-to-Speech (TTS) with accent support.
"""

import os
import io
import tempfile
from typing import Optional, Dict, Tuple

import speech_recognition as sr
from gtts import gTTS
from gtts.lang import tts_langs
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

# Initialize OpenAI API key
openai_api_key = os.getenv("OPENAI_API_KEY")


class SpeechService:
    """Service for handling speech recognition and synthesis."""

    def __init__(self) -> None:
        self.recognizer = sr.Recognizer()
        self.recognizer.energy_threshold = 300
        self.recognizer.dynamic_energy_threshold = True

        # Accent mappings for TTS
        self.accent_tlds = {
            "british": "co.uk",
            "american": "com",
            "neutral": "com.au",  # Australian accent as neutral
        }
        # Cache supported TTS languages
        self.tts_languages = {code.lower() for code in tts_langs().keys()}

    def _normalize_tts_language(self, language: str) -> str:
        """
        Map requested language codes to ones supported by gTTS.

        Falls back to a close alternative or English if unsupported.
        """
        if not language:
            return "en"

        lang = language.lower()

        # Direct support
        if lang in self.tts_languages:
            return lang

        # Simple aliases / fallbacks
        aliases = {
            "zh-cn": "zh-cn",
            "zh-tw": "zh-tw",
            "pt-br": "pt",
            "az": "tr",  # Azeri -> Turkish as a reasonable fallback
        }
        mapped = aliases.get(lang)
        if mapped and mapped.lower() in self.tts_languages:
            return mapped.lower()

        # Default safe fallback
        return "en"
    
    def speech_to_text(
        self, 
        audio_data: bytes, 
        language: str = "en"
    ) -> Dict[str, any]:
        """
        Convert speech audio to text.
        
        Args:
            audio_data: Audio data bytes
            language: Language code for recognition (default: "en")
            
        Returns:
            Dictionary with transcription result
        """
        try:
            # Create temporary audio file
            with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp_file:
                tmp_file.write(audio_data)
                tmp_file_path = tmp_file.name
            
            try:
                # Load audio file
                with sr.AudioFile(tmp_file_path) as source:
                    audio = self.recognizer.record(source)
                
                # Try Google Speech Recognition first
                try:
                    text = self.recognizer.recognize_google(audio, language=language)
                    return {
                        "success": True,
                        "text": text,
                        "language": language,
                        "method": "google"
                    }
                except sr.UnknownValueError:
                    return {
                        "success": False,
                        "error": "Could not understand audio",
                        "language": language
                    }
                except sr.RequestError as e:
                    # Fallback to OpenAI Whisper if available
                    if openai_api_key:
                        return self._whisper_stt(tmp_file_path, language)
                    return {
                        "success": False,
                        "error": f"Speech recognition service error: {e}",
                        "language": language
                    }
            finally:
                # Clean up temporary file
                if os.path.exists(tmp_file_path):
                    os.unlink(tmp_file_path)
                    
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "language": language
            }
    
    def _whisper_stt(self, audio_path: str, language: str) -> Dict[str, any]:
        """Fallback STT using OpenAI Whisper."""
        try:
            if not openai_api_key:
                return {
                    "success": False,
                    "error": "OpenAI API key not configured",
                    "language": language
                }
            with open(audio_path, "rb") as audio_file:
                client = OpenAI(api_key=openai_api_key)
                transcript = client.audio.transcriptions.create(
                    model="whisper-1",
                    file=audio_file,
                    language=language if language != "auto" else None
                )
                return {
                    "success": True,
                    "text": transcript.text,
                    "language": language,
                    "method": "whisper"
                }
        except Exception as e:
            return {
                "success": False,
                "error": f"Whisper STT error: {e}",
                "language": language
            }
    
    def text_to_speech(
        self, 
        text: str, 
        language: str = "en",
        accent: str = "neutral"
    ) -> Optional[bytes]:
        """
        Convert text to speech audio.
        
        Args:
            text: Text to convert to speech
            language: Language code (default: "en")
            accent: Accent preference - "british", "american", or "neutral" (default: "neutral")
            
        Returns:
            Audio data as bytes, or None if error
        """
        try:
            if not text or not text.strip():
                return None

            # Get TLD for accent
            tld = self.accent_tlds.get(accent.lower(), "com.au")

            # Normalize language to one supported by gTTS
            tts_language = self._normalize_tts_language(language)

            # Create TTS
            tts = gTTS(text=text, lang=tts_language, tld=tld, slow=False)
            
            # Generate audio to bytes
            audio_buffer = io.BytesIO()
            tts.write_to_fp(audio_buffer)
            audio_buffer.seek(0)
            
            return audio_buffer.read()
        except Exception as e:
            print(f"TTS error: {e}")
            return None
    
    def get_supported_accents(self) -> list:
        """Get list of supported accents."""
        return list(self.accent_tlds.keys())
    
    def is_valid_accent(self, accent: str) -> bool:
        """Check if accent is supported."""
        return accent.lower() in self.accent_tlds


# Singleton instance
speech_service = SpeechService()
