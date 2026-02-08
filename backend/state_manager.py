"""
State management module for AI Translator Chatbot.
Handles session state, conversation memory, and bookmarks.
"""

from typing import List, Dict, Optional
from datetime import datetime
import json


class ConversationMessage:
    """Represents a single message in the conversation."""
    
    def __init__(
        self, 
        role: str, 
        content: str, 
        timestamp: Optional[datetime] = None,
        metadata: Optional[Dict] = None
    ):
        self.role = role  # "user" or "assistant"
        self.content = content
        self.timestamp = timestamp or datetime.now()
        self.metadata = metadata or {}
        self.liked = False
        self.disliked = False
    
    def to_dict(self) -> Dict:
        """Convert message to dictionary."""
        return {
            "role": self.role,
            "content": self.content,
            "timestamp": self.timestamp.isoformat(),
            "metadata": self.metadata,
            "liked": self.liked,
            "disliked": self.disliked
        }
    
    @classmethod
    def from_dict(cls, data: Dict):
        """Create message from dictionary."""
        msg = cls(
            role=data["role"],
            content=data["content"],
            timestamp=datetime.fromisoformat(data["timestamp"]),
            metadata=data.get("metadata", {})
        )
        msg.liked = data.get("liked", False)
        msg.disliked = data.get("disliked", False)
        return msg


class Bookmark:
    """Represents a saved bookmark."""
    
    def __init__(
        self, 
        original_text: str,
        translated_text: str,
        source_lang: str,
        target_lang: str,
        timestamp: Optional[datetime] = None,
        notes: Optional[str] = None
    ):
        self.original_text = original_text
        self.translated_text = translated_text
        self.source_lang = source_lang
        self.target_lang = target_lang
        self.timestamp = timestamp or datetime.now()
        self.notes = notes or ""
    
    def to_dict(self) -> Dict:
        """Convert bookmark to dictionary."""
        return {
            "original_text": self.original_text,
            "translated_text": self.translated_text,
            "source_lang": self.source_lang,
            "target_lang": self.target_lang,
            "timestamp": self.timestamp.isoformat(),
            "notes": self.notes
        }
    
    @classmethod
    def from_dict(cls, data: Dict):
        """Create bookmark from dictionary."""
        return cls(
            original_text=data["original_text"],
            translated_text=data["translated_text"],
            source_lang=data["source_lang"],
            target_lang=data["target_lang"],
            timestamp=datetime.fromisoformat(data["timestamp"]),
            notes=data.get("notes", "")
        )


class StateManager:
    """Manages application state, conversation history, and bookmarks."""
    
    def __init__(self):
        self.conversation_history: List[ConversationMessage] = []
        self.bookmarks: List[Bookmark] = []
        # Language preferences
        self.source_language: str = "auto"  # "auto" = auto-detect
        self.user_language_lock: Optional[str] = None
        self.auto_english_mode: bool = False
        self.simplifier_mode: bool = False
        self.selected_accent: str = "neutral"
        self.target_language: str = "en"
    
    def add_message(
        self, 
        role: str, 
        content: str, 
        metadata: Optional[Dict] = None
    ):
        """Add a message to conversation history."""
        message = ConversationMessage(role, content, metadata=metadata)
        self.conversation_history.append(message)
        return message
    
    def get_conversation_context(self, max_messages: int = 10) -> List[Dict]:
        """Get recent conversation context for AI responses."""
        recent_messages = self.conversation_history[-max_messages:]
        return [msg.to_dict() for msg in recent_messages]
    
    def clear_conversation(self):
        """Clear all conversation history."""
        self.conversation_history = []
    
    def toggle_message_like(self, message_index: int):
        """Toggle like status for a message."""
        if 0 <= message_index < len(self.conversation_history):
            msg = self.conversation_history[message_index]
            msg.liked = not msg.liked
            if msg.liked:
                msg.disliked = False
    
    def toggle_message_dislike(self, message_index: int):
        """Toggle dislike status for a message."""
        if 0 <= message_index < len(self.conversation_history):
            msg = self.conversation_history[message_index]
            msg.disliked = not msg.disliked
            if msg.disliked:
                msg.liked = False
    
    def add_bookmark(
        self,
        original_text: str,
        translated_text: str,
        source_lang: str,
        target_lang: str,
        notes: Optional[str] = None
    ) -> Bookmark:
        """Add a bookmark."""
        bookmark = Bookmark(
            original_text=original_text,
            translated_text=translated_text,
            source_lang=source_lang,
            target_lang=target_lang,
            notes=notes
        )
        self.bookmarks.append(bookmark)
        return bookmark
    
    def remove_bookmark(self, bookmark_index: int):
        """Remove a bookmark by index."""
        if 0 <= bookmark_index < len(self.bookmarks):
            self.bookmarks.pop(bookmark_index)
    
    def get_bookmarks(self) -> List[Dict]:
        """Get all bookmarks as dictionaries."""
        return [bm.to_dict() for bm in self.bookmarks]
    
    def set_user_language_lock(self, lang_code: Optional[str]):
        """Set or clear user language lock."""
        self.user_language_lock = lang_code
    
    def set_auto_english_mode(self, enabled: bool):
        """Enable or disable auto-translate-to-English mode."""
        self.auto_english_mode = enabled
    
    def set_simplifier_mode(self, enabled: bool):
        """Enable or disable simplifier mode."""
        self.simplifier_mode = enabled
    
    def set_accent(self, accent: str):
        """Set TTS accent preference."""
        self.selected_accent = accent
    
    def set_target_language(self, lang_code: str):
        """Set target language for translations."""
        self.target_language = lang_code
    
    def set_source_language(self, lang_code: str):
        """Set source language for translations (or 'auto' to auto-detect)."""
        self.source_language = lang_code
    
    def export_conversation(self) -> str:
        """Export conversation history as JSON."""
        data = {
            "conversation": [msg.to_dict() for msg in self.conversation_history],
            "bookmarks": [bm.to_dict() for bm in self.bookmarks],
            "export_timestamp": datetime.now().isoformat()
        }
        return json.dumps(data, indent=2, ensure_ascii=False)
    
    def import_conversation(self, json_data: str):
        """Import conversation history from JSON."""
        try:
            data = json.loads(json_data)
            self.conversation_history = [
                ConversationMessage.from_dict(msg) 
                for msg in data.get("conversation", [])
            ]
            self.bookmarks = [
                Bookmark.from_dict(bm) 
                for bm in data.get("bookmarks", [])
            ]
        except Exception as e:
            raise ValueError(f"Invalid conversation data: {e}")
