"""
Translation module for AI Translator Chatbot.

This version is **powered by the Groq API** for:
- high‑quality multilingual translation (any language → any language)
- optional text simplification via LLM

We still use `deep_translator` only for lightweight language detection
and as a potential future fallback, but all primary translation is done
through Groq chat completions.
"""

import os
from typing import Optional, Dict, Tuple

from deep_translator import GoogleTranslator
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")


LANGUAGES: Dict[str, str] = {
    "af": "afrikaans",
    "sq": "albanian",
    "am": "amharic",
    "ar": "arabic",
    "hy": "armenian",
    "az": "azerbaijani",
    "eu": "basque",
    "be": "belarusian",
    "bn": "bengali",
    "bs": "bosnian",
    "bg": "bulgarian",
    "ca": "catalan",
    "ceb": "cebuano",
    "ny": "chichewa",
    "zh-cn": "chinese (simplified)",
    "zh-tw": "chinese (traditional)",
    "co": "corsican",
    "hr": "croatian",
    "cs": "czech",
    "da": "danish",
    "nl": "dutch",
    "en": "english",
    "eo": "esperanto",
    "et": "estonian",
    "tl": "filipino",
    "fi": "finnish",
    "fr": "french",
    "fy": "frisian",
    "gl": "galician",
    "ka": "georgian",
    "de": "german",
    "el": "greek",
    "gu": "gujarati",
    "ht": "haitian creole",
    "ha": "hausa",
    "haw": "hawaiian",
    "iw": "hebrew",
    "hi": "hindi",
    "hmn": "hmong",
    "hu": "hungarian",
    "is": "icelandic",
    "ig": "igbo",
    "id": "indonesian",
    "ga": "irish",
    "it": "italian",
    "ja": "japanese",
    "jw": "javanese",
    "kn": "kannada",
    "kk": "kazakh",
    "km": "khmer",
    "ko": "korean",
    "ku": "kurdish (kurmanji)",
    "ky": "kyrgyz",
    "lo": "lao",
    "la": "latin",
    "lv": "latvian",
    "lt": "lithuanian",
    "lb": "luxembourgish",
    "mk": "macedonian",
    "mg": "malagasy",
    "ms": "malay",
    "ml": "malayalam",
    "mt": "maltese",
    "mi": "maori",
    "mr": "marathi",
    "mn": "mongolian",
    "my": "myanmar (burmese)",
    "ne": "nepali",
    "no": "norwegian",
    "ps": "pashto",
    "fa": "persian",
    "pl": "polish",
    "pt": "portuguese",
    "pa": "punjabi",
    "ro": "romanian",
    "ru": "russian",
    "sm": "samoan",
    "gd": "scots gaelic",
    "sr": "serbian",
    "st": "sesotho",
    "sn": "shona",
    "sd": "sindhi",
    "si": "sinhala",
    "sk": "slovak",
    "sl": "slovenian",
    "so": "somali",
    "es": "spanish",
    "su": "sundanese",
    "sw": "swahili",
    "sv": "swedish",
    "tg": "tajik",
    "ta": "tamil",
    "te": "telugu",
    "th": "thai",
    "tr": "turkish",
    "uk": "ukrainian",
    "ur": "urdu",
    "uz": "uzbek",
    "vi": "vietnamese",
    "cy": "welsh",
    "xh": "xhosa",
    "yi": "yiddish",
    "yo": "yoruba",
    "zu": "zulu",
}


class TranslationService:
    """Service for handling translations and language operations via Groq."""

    def __init__(self) -> None:
        self.supported_languages: Dict[str, str] = LANGUAGES
        self.language_codes: Dict[str, str] = {v: k for k, v in LANGUAGES.items()}
        self._client: Optional[Groq] = None

    @property
    def client(self) -> Groq:
        """
        Lazily‑initialised Groq client.

        Raises:
            RuntimeError: if GROQ_API_KEY is missing.
        """
        if self._client is None:
            if not GROQ_API_KEY:
                raise RuntimeError(
                    "GROQ_API_KEY not configured. Please set it in your environment or .env file."
                )
            self._client = Groq(api_key=GROQ_API_KEY)
        return self._client

    def detect_language(self, text: str) -> Tuple[str, float]:
        """
        Detect the language of the input text using GoogleTranslator.detect.
        """
        try:
            stripped = text.strip()
            if not stripped:
                return "en", 0.0

            detection = GoogleTranslator(source="auto", target="en").detect(stripped)
            # deep-translator returns a language code string
            lang_code = detection or "en"
            return lang_code, 1.0
        except Exception:
            return "en", 0.0

    def translate_text(
        self,
        text: str,
        target_lang: str = "en",
        source_lang: Optional[str] = None,
    ) -> Dict[str, object]:
        """
        Translate text to target language using Groq chat completions.

        The prompt is carefully structured so that the model returns only the
        translated text (no explanations) in the requested target language.
        """
        try:
            stripped = text.strip()
            if not stripped:
                return {
                    "success": False,
                    "error": "Empty text provided",
                }

            # Detect language if not explicitly provided
            if source_lang is None or source_lang == "auto":
                source_lang, confidence = self.detect_language(stripped)
            else:
                confidence = 1.0

            if source_lang == target_lang:
                return {
                    "success": True,
                    "original_text": stripped,
                    "translated_text": stripped,
                    "source_language": source_lang,
                    "target_language": target_lang,
                    "confidence": confidence,
                }

            source_name = self.get_language_name(source_lang)
            target_name = self.get_language_name(target_lang)

            system_prompt = (
                "You are a world-class translation engine. "
                "Your job is to accurately translate text from a source language to a "
                "target language while preserving meaning, tone, and formatting.\n"
                "CRITICAL REQUIREMENTS:\n"
                "- Respond with **ONLY** the translated text.\n"
                "- Do NOT add explanations, notes, or quotes.\n"
                "- Maintain markdown formatting when present.\n"
            )

            user_prompt = (
                f"Source language: {source_name} ({source_lang})\n"
                f"Target language: {target_name} ({target_lang})\n\n"
                f"Text to translate:\n{text}\n"
            )

            completion = self.client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt},
                ],
                temperature=0.3,
                max_tokens=2048,
            )

            translated_text = (
                completion.choices[0].message.content.strip()
                if completion and completion.choices
                else ""
            )

            if not translated_text:
                return {
                    "success": False,
                    "error": "Empty translation returned from Groq API",
                    "original_text": text,
                }

            return {
                "success": True,
                "original_text": stripped,
                "translated_text": translated_text,
                "source_language": source_lang,
                "target_language": target_lang,
                "confidence": confidence,
            }
        except Exception as e:
            return {
                "success": False,
                "error": f"Translation error via Groq: {e}",
                "original_text": text,
            }

    def simplify_text(self, text: str, target_lang: str = "en") -> Dict[str, object]:
        """
        Simplify complex text into beginner-friendly language using Groq.
        """
        try:
            language_name = self.supported_languages.get(target_lang, "English")
            system_prompt = (
                "You are a helpful assistant that simplifies complex text into "
                "easy, beginner-friendly language.\n"
                "Requirements:\n"
                "- Keep the original meaning.\n"
                "- Use simpler vocabulary and short sentences.\n"
                "- Respond ONLY with the simplified text in the requested language.\n"
            )

            user_prompt = (
                f"Target language: {language_name} ({target_lang})\n\n"
                f"Text to simplify:\n{text}\n"
            )

            completion = self.client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt},
                ],
                max_tokens=1000,
                temperature=0.5,
            )

            simplified_text = (
                completion.choices[0].message.content.strip()
                if completion and completion.choices
                else ""
            )

            if not simplified_text:
                return {
                    "success": False,
                    "error": "Empty simplification returned from Groq API",
                    "original_text": text,
                }

            return {
                "success": True,
                "original_text": text,
                "simplified_text": simplified_text,
                "target_language": target_lang,
            }
        except Exception as e:
            return {
                "success": False,
                "error": f"Simplification error via Groq: {e}",
                "original_text": text,
            }

    def get_language_name(self, lang_code: str) -> str:
        """Get full language name from code."""
        return self.supported_languages.get(lang_code, lang_code)

    def get_language_code(self, lang_name: str) -> str:
        """Get language code from full name."""
        return self.language_codes.get(lang_name.lower(), "en")

    def is_supported_language(self, lang_code: str) -> bool:
        """Check if language code is supported."""
        return lang_code in self.supported_languages


def translation_service(
    text: str,
    target_lang: str = "en",
    source_lang: Optional[str] = None,
) -> Dict[str, object]:
    """
    Functional API for translations used by the frontend.
    """
    service = TranslationService()
    return service.translate_text(text=text, target_lang=target_lang, source_lang=source_lang)
