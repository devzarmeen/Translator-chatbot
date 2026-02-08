"""
Backend modules for AI Translator Chatbot.
"""

from .translation import translation_service, TranslationService, LANGUAGES
from .speech import speech_service
from .ocr import ocr_service
from .state_manager import StateManager, ConversationMessage, Bookmark

__all__ = [
    "translation_service",
    "TranslationService",
    "LANGUAGES",
    "speech_service",
    "ocr_service",
    "StateManager",
    "ConversationMessage",
    "Bookmark",
]
