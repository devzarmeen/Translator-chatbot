"""
Main Streamlit application for AI Translator Chatbot.

This frontend is designed to feel like a modern GPT-style app:
- dark, colorful gradient theme
- rounded chat bubbles
- bottom chat bar with text, mic, send, and image upload controls
- tab-based navigation for Translator, Image Translation, Voice Translation, and History

Backed by:
- Groq API for multilingual translation + simplification
- Local STT/TTS and OCR utilities from the backend modules
"""

import os
import sys
from pathlib import Path
from datetime import datetime
import hashlib
from typing import Optional

import streamlit as st

# Ensure project root (containing `backend` and `frontend`) is on sys.path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from backend.translation import TranslationService, LANGUAGES
from backend.speech import speech_service
from backend.ocr import ocr_service
from backend.state_manager import StateManager, ConversationMessage


translation_service = TranslationService()

# Page configuration
st.set_page_config(
    page_title="AI Translator Chatbot",
    page_icon="🌐",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ---------------------------------------------------------------------------
# Theme & Layout Styling
# ---------------------------------------------------------------------------

st.markdown(
    """
<style>
/* Global dark theme overrides */
html, body, [data-testid="stAppViewContainer"] {
    background: radial-gradient(circle at top left, #1f2937, #020617 55%, #000000);
    color: #e5e7eb;
}

[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #020617 0%, #020617 50%, #020617 100%);
    border-right: 1px solid rgba(148, 163, 184, 0.3);
}

.gradient-header {
    background: radial-gradient(circle at top left, #4f46e5, #06b6d4);
    -webkit-background-clip: text;
    background-clip: text;
    color: transparent;
}

.chat-container {
    padding: 0.5rem 0.75rem 6rem 0.75rem; /* extra bottom padding for bottom bar */
}

/* Chat bubbles */
[data-testid="stChatMessage"] {
    padding: 0.9rem 1rem;
    border-radius: 1rem;
    margin-bottom: 0.6rem;
}

[data-testid="stChatMessage"] > div {
    font-size: 0.95rem;
}

[data-testid="stChatMessage"][data-testid="stChatMessage-user"] {
    background: linear-gradient(135deg, #4f46e5, #06b6d4);
    color: #f9fafb;
}

[data-testid="stChatMessage"][data-testid="stChatMessage-assistant"] {
    background: rgba(15, 23, 42, 0.9);
    border: 1px solid rgba(148, 163, 184, 0.35);
}

/* Bottom chat bar */
.bottom-chat-bar {
    position: fixed;
    bottom: 0;
    left: 0;
    right: 0;
    padding: 0.75rem 1.2rem 0.9rem 1.2rem;
    background: linear-gradient(180deg, rgba(15,23,42,0.96), rgba(15,23,42,0.98));
    border-top: 1px solid rgba(148, 163, 184, 0.4);
    z-index: 999;
}

.bottom-chat-inner {
    max-width: 960px;
    margin: 0 auto;
    display: flex;
    gap: 0.4rem;
    align-items: center;
}

.bottom-chat-input {
    flex: 1;
}

.bottom-chat-input input {
    background: rgba(15, 23, 42, 0.85) !important;
    border-radius: 9999px !important;
    border: 1px solid rgba(148, 163, 184, 0.5) !important;
    color: #e5e7eb !important;
}

/* Icon buttons inside bottom chat bar */
.bottom-chat-bar [data-testid="baseButton-secondary"] button,
.bottom-chat-bar [data-testid="baseButton-primary"] button {
    border-radius: 9999px !important;
    width: 38px;
    height: 38px;
    padding: 0 !important;
    display: inline-flex;
    align-items: center;
    justify-content: center;
    background: radial-gradient(circle at top left, #111827, #020617) !important;
    border: 1px solid rgba(148, 163, 184, 0.5) !important;
}

.bottom-chat-bar [data-testid="baseButton-primary"] button {
    background: #f9fafb !important;
    color: #020617 !important;
}

.bottom-chat-bar [data-testid="baseButton-secondary"] button p,
.bottom-chat-bar [data-testid="baseButton-primary"] button p {
    font-size: 1.15rem !important;
    margin-bottom: 0 !important;
}

.bookmark-chip {
    padding: 0.35rem 0.55rem;
    border-radius: 9999px;
    border: 1px solid rgba(148, 163, 184, 0.4);
    font-size: 0.75rem;
    display: inline-flex;
    gap: 0.25rem;
    align-items: center;
}
</style>
""",
    unsafe_allow_html=True,
)

# ---------------------------------------------------------------------------
# Session State
# ---------------------------------------------------------------------------

if "state_manager" not in st.session_state:
    st.session_state.state_manager = StateManager()

if "input_text" not in st.session_state:
    st.session_state.input_text = ""

if "active_input_mode" not in st.session_state:
    st.session_state.active_input_mode = "Text"

if "pending_voice_audio" not in st.session_state:
    st.session_state.pending_voice_audio = None

if "pending_image_bytes" not in st.session_state:
    st.session_state.pending_image_bytes = None

if "audio_events" not in st.session_state:
    # Each event: {timestamp, kind, source, audio_bytes, transcript, assistant_text, meta}
    st.session_state.audio_events = []

if "image_events" not in st.session_state:
    # Each event: {timestamp, source, image_bytes, extracted_text, assistant_text, error}
    st.session_state.image_events = []

if "show_quick_mic" not in st.session_state:
    st.session_state.show_quick_mic = False

if "show_quick_image" not in st.session_state:
    st.session_state.show_quick_image = False

if "last_processed_audio_hash" not in st.session_state:
    st.session_state.last_processed_audio_hash = None

if "last_processed_image_hash" not in st.session_state:
    st.session_state.last_processed_image_hash = None

if "sidebar_last_submitted" not in st.session_state:
    st.session_state.sidebar_last_submitted = None

state = st.session_state.state_manager


def get_available_languages():
    """Get list of available languages for selection."""
    return sorted(
        [(code, name.capitalize()) for code, name in LANGUAGES.items()],
        key=lambda x: x[1],
    )

def _sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _append_audio_event(
    *,
    kind: str,
    source: str,
    audio_bytes: bytes,
    transcript: Optional[str] = None,
    assistant_text: Optional[str] = None,
    meta: Optional[dict] = None,
):
    st.session_state.audio_events.append(
        {
            "timestamp": datetime.now().isoformat(timespec="seconds"),
            "kind": kind,
            "source": source,
            "audio_bytes": audio_bytes,
            "transcript": transcript,
            "assistant_text": assistant_text,
            "meta": meta or {},
        }
    )


def _append_image_event(
    *,
    source: str,
    image_bytes: bytes,
    extracted_text: Optional[str] = None,
    assistant_text: Optional[str] = None,
    error: Optional[str] = None,
):
    st.session_state.image_events.append(
        {
            "timestamp": datetime.now().isoformat(timespec="seconds"),
            "source": source,
            "image_bytes": image_bytes,
            "extracted_text": extracted_text,
            "assistant_text": assistant_text,
            "error": error,
        }
    )


def render_audio_section():
    """Dedicated audio section (separate from text chat)."""
    events = list(reversed(st.session_state.audio_events))
    if not events:
        st.caption("No audio messages yet.")
        return

    for idx, ev in enumerate(events):
        st.markdown(f"**{ev['timestamp']}** · `{ev['kind']}` · `{ev['source']}`")
        try:
            st.audio(ev["audio_bytes"])
        except Exception as e:
            st.warning(f"Couldn't render this audio in the browser: {e}")

        if ev.get("transcript"):
            st.write(f"**Transcript:** {ev['transcript']}")
        if ev.get("assistant_text"):
            st.write(ev["assistant_text"])
        st.markdown("---")


def render_image_section():
    """Dedicated image section (separate from text/audio chat)."""
    events = list(reversed(st.session_state.image_events))
    if not events:
        st.caption("No image messages yet.")
        return

    for idx, ev in enumerate(events):
        st.markdown(f"**{ev['timestamp']}** · `{ev['source']}`")
        if ev.get("error"):
            st.error(ev["error"])
        else:
            try:
                # Avoid deprecated parameters; keep a stable width.
                st.image(ev["image_bytes"], caption="Image", width=520)
            except Exception as e:
                st.warning(f"Couldn't display this image preview: {e}")

        if ev.get("extracted_text"):
            st.write(f"**Extracted text:** {ev['extracted_text']}")
        if ev.get("assistant_text"):
            st.write(ev["assistant_text"])
        st.markdown("---")


def render_chat_message(message: ConversationMessage, index: int):
    """Render a chat message with action buttons."""
    role = message.role
    content = message.content
    
    if role == "user":
        with st.chat_message("user"):
            st.write(content)
    else:
        with st.chat_message("assistant"):
            st.write(content)
            
            # Action buttons container
            col1, col2, col3, col4, col5, col6 = st.columns(6)
            
            with col1:
                like_emoji = "👍" if message.liked else "👍"
                if st.button(like_emoji, key=f"like_{index}", help="Like this response"):
                    state.toggle_message_like(index)
                    st.rerun()
            
            with col2:
                dislike_emoji = "👎" if message.disliked else "👎"
                if st.button(dislike_emoji, key=f"dislike_{index}", help="Dislike this response"):
                    state.toggle_message_dislike(index)
                    st.rerun()
            
            with col3:
                if st.button("🔄", key=f"regenerate_{index}", help="Regenerate response"):
                    regenerate_response(index)
            
            with col4:
                if st.button("📋", key=f"copy_{index}", help="Copy text"):
                    st.write("```\n" + content + "\n```")
                    st.success("Text copied! (Use Ctrl+C)")
            
            with col5:
                if st.button("🔊", key=f"read_{index}", help="Read aloud"):
                    read_text_aloud(content)
            
            with col6:
                if st.button("⭐", key=f"bookmark_{index}", help="Bookmark"):
                    bookmark_translation(content, index)


def regenerate_response(message_index: int):
    """Regenerate response for a given message."""
    if message_index < 0 or message_index >= len(state.conversation_history):
        return
    
    # Get the user message that prompted this response
    if message_index > 0:
        user_message = state.conversation_history[message_index - 1]
        if user_message.role == "user":
            # Remove old assistant response
            state.conversation_history.pop(message_index)
            # Process user message again
            process_user_input(user_message.content)


def read_text_aloud(text: str):
    """Read text aloud using TTS."""
    try:
        accent = state.selected_accent
        if not speech_service.is_valid_accent(accent):
            accent = "neutral"

        audio_data = speech_service.text_to_speech(
            text=text,
            language=state.target_language,
            accent=accent,
        )

        if audio_data:
            # Store audio in dedicated audio section (not inside the chat bubble)
            _append_audio_event(
                kind="tts",
                source="read-aloud",
                audio_bytes=audio_data,
                transcript=None,
                assistant_text=f"**TTS ({translation_service.get_language_name(state.target_language)})** for: {text[:140]}{'...' if len(text) > 140 else ''}",
                meta={"accent": accent, "lang": state.target_language},
            )
            st.toast("Audio ready. See the Audio section.", icon="🔊")
        else:
            st.error("Failed to generate speech audio.")
    except Exception as e:
        st.error(f"Error reading text aloud: {e}")


def bookmark_translation(text: str, message_index: int):
    """Bookmark a translation."""
    try:
        # Try to find original text from conversation context
        original_text = text
        if message_index > 0:
            prev_msg = state.conversation_history[message_index - 1]
            if prev_msg.role == "user":
                original_text = prev_msg.content
        
        bookmark = state.add_bookmark(
            original_text=original_text,
            translated_text=text,
            source_lang="auto",
            target_lang=state.target_language
        )
        st.success("Translation bookmarked")
    except Exception as e:
        st.error(f"Error bookmarking: {e}")


def process_user_input(user_input: str):
    """Process user input and generate translated response via Groq."""
    try:
        # Add user message to history
        state.add_message("user", user_input)
        
        # Determine source + target language
        manual_source = getattr(state, "source_language", "auto")
        detected_lang = None
        confidence = 0.0

        if manual_source and manual_source != "auto":
            detected_lang = manual_source
            confidence = 1.0
        else:
            detected_lang, confidence = translation_service.detect_language(user_input)

        target_lang = state.target_language
        if state.auto_english_mode:
            target_lang = "en"
        elif state.user_language_lock:
            target_lang = state.user_language_lock
        
        # Translate text via Groq
        translation_result = translation_service.translate_text(
            text=user_input,
            target_lang=target_lang,
            source_lang=detected_lang or "auto",
        )

        translated_text_for_bookmark = None

        if not translation_result["success"]:
            response_text = f"Translation error: {translation_result.get('error', 'Unknown error')}"
        else:
            translated_text = translation_result["translated_text"]

            # Apply simplifier if enabled
            if state.simplifier_mode:
                simplify_result = translation_service.simplify_text(
                    text=translated_text,
                    target_lang=target_lang,
                )
                if simplify_result["success"]:
                    translated_text = simplify_result["simplified_text"]

            translated_text_for_bookmark = translated_text

            # Build response
            source_lang_name = translation_service.get_language_name(detected_lang)
            target_lang_name = translation_service.get_language_name(target_lang)

            response_text = f"**Translation ({source_lang_name} → {target_lang_name}):**\n\n{translated_text}"

            # Add detected language info if different from target
            if detected_lang != target_lang:
                response_text += f"\n\n*Detected language: {source_lang_name}*"

        # Add assistant response to history
        metadata = {
            "detected_language": detected_lang,
            "target_language": target_lang,
            "confidence": confidence,
        }
        state.add_message("assistant", response_text, metadata=metadata)

        # Automatically bookmark successful translations
        if translated_text_for_bookmark is not None:
            state.add_bookmark(
                original_text=user_input,
                translated_text=translated_text_for_bookmark,
                source_lang=detected_lang,
                target_lang=target_lang,
            )

    except Exception as e:
        error_msg = f"Error processing input: {str(e)}"
        state.add_message("assistant", error_msg)
        st.error(error_msg)


def process_voice_input(audio_data: bytes):
    """Process voice input using STT."""
    try:
        if not audio_data:
            st.error("No audio data received.")
            return

        audio_hash = _sha256_bytes(audio_data)
        if st.session_state.last_processed_audio_hash == audio_hash:
            return
        st.session_state.last_processed_audio_hash = audio_hash

        # Detect language for STT (use target language as hint)
        stt_result = speech_service.speech_to_text(
            audio_data=audio_data,
            language=state.target_language
        )
        
        if stt_result["success"]:
            transcribed_text = stt_result["text"]
            # Add transcript+translation to text chat automatically
            process_user_input(transcribed_text)

            assistant_text = None
            if state.conversation_history and state.conversation_history[-1].role == "assistant":
                assistant_text = state.conversation_history[-1].content

            _append_audio_event(
                kind="stt",
                source=stt_result.get("method", "mic"),
                audio_bytes=audio_data,
                transcript=transcribed_text,
                assistant_text=assistant_text,
                meta={"language_hint": state.target_language},
            )
        else:
            st.error(f"Speech recognition error: {stt_result.get('error', 'Unknown error')}")
    except Exception as e:
        st.error(f"Error processing voice input: {e}")


def process_image_input(image_data: bytes):
    """Process image input using OCR."""
    try:
        if not image_data:
            st.error("No image data received.")
            return

        img_hash = _sha256_bytes(image_data)
        if st.session_state.last_processed_image_hash == img_hash:
            return
        st.session_state.last_processed_image_hash = img_hash

        # Extract text from image
        ocr_result = ocr_service.extract_text_from_image(image_data)
        
        if ocr_result["success"]:
            extracted_text = ocr_result["extracted_text"]
            # Automatically translate extracted text and store media separately
            process_user_input(extracted_text)
            assistant_text = None
            if state.conversation_history and state.conversation_history[-1].role == "assistant":
                assistant_text = state.conversation_history[-1].content

            _append_image_event(
                source="ocr",
                image_bytes=image_data,
                extracted_text=extracted_text,
                assistant_text=assistant_text,
            )
        else:
            err = f"OCR error: {ocr_result.get('error', 'Unknown error')}"
            _append_image_event(source="ocr", image_bytes=image_data, error=err)
            st.error(err)
    except Exception as e:
        err = f"Error processing image: {e}"
        try:
            _append_image_event(source="ocr", image_bytes=image_data, error=err)
        except Exception:
            pass
        st.error(err)


# Sidebar (global settings + bookmarks)
with st.sidebar:
    st.title("⚙️ Controls")

    if not os.getenv("GROQ_API_KEY"):
        st.error("GROQ_API_KEY is not set. Translation will fail until it is configured.")

    st.divider()

    # Language selection (source + target)
    st.subheader("🌐 Language Settings")
    available_langs = get_available_languages()
    lang_options = {name: code for code, name in available_langs}

    # Source language selector with auto-detect
    source_display_names = ["Auto-detect"] + [name for name in lang_options.keys()]
    current_source_code = getattr(state, "source_language", "auto")
    if current_source_code == "auto":
        source_index = 0
    else:
        # +1 offset because 0 is "Auto-detect"
        current_source_name = translation_service.get_language_name(current_source_code).capitalize()
        source_index = source_display_names.index(current_source_name) if current_source_name in source_display_names else 0

    selected_source_display = st.selectbox("Source Language", options=source_display_names, index=source_index)
    if selected_source_display == "Auto-detect":
        state.set_source_language("auto")
    else:
        state.set_source_language(lang_options[selected_source_display])

    # Target language selector
    target_display_names = list(lang_options.keys())
    selected_target_display = translation_service.get_language_name(state.target_language).capitalize()
    target_index = (
        target_display_names.index(selected_target_display)
        if selected_target_display in target_display_names
        else 0
    )
    chosen_target_display = st.selectbox("Target Language", options=target_display_names, index=target_index)
    state.set_target_language(lang_options[chosen_target_display])

    st.divider()

    # Accent selection
    st.subheader("🗣️ Speech Settings")
    accent_options = ["neutral", "british", "american"]
    selected_accent = st.selectbox(
        "TTS Accent",
        options=accent_options,
        index=accent_options.index(state.selected_accent) if state.selected_accent in accent_options else 0,
    )
    state.set_accent(selected_accent)

    st.divider()

    # Feature toggles
    st.subheader("✨ AI Features")
    auto_english = st.toggle(
        "Auto-English Mode",
        value=state.auto_english_mode,
        help="Automatically translate all input to English",
    )
    state.set_auto_english_mode(auto_english)

    simplifier = st.toggle(
        "Simplifier Mode",
        value=state.simplifier_mode,
        help="Post-process translations with Groq to simplify into beginner-friendly language.",
    )
    state.set_simplifier_mode(simplifier)

    language_lock = st.toggle(
        "Language Lock",
        value=state.user_language_lock is not None,
        help="Force all bot responses into the currently selected target language.",
    )
    if language_lock:
        state.set_user_language_lock(state.target_language)
    else:
        state.set_user_language_lock(None)

    st.divider()

    # Bookmarks section
    st.subheader("⭐ Bookmarks")
    bookmarks = state.get_bookmarks()
    if bookmarks:
        for i, bm in enumerate(bookmarks):
            label = f"{bm['original_text'][:22]}..." if len(bm["original_text"]) > 25 else bm["original_text"]
            with st.expander(f"Bookmark {i+1}: {label}"):
                st.markdown(
                    f"<span class='bookmark-chip'>🕒 {bm['timestamp'][:19]}</span>",
                    unsafe_allow_html=True,
                )
                st.write(f"**Original:** {bm['original_text']}")
                st.write(f"**Translated:** {bm['translated_text']}")
                st.write(f"**Languages:** {bm['source_lang']} → {bm['target_lang']}")
                if st.button("🗑️ Delete", key=f"del_bm_{i}"):
                    state.remove_bookmark(i)
                    st.rerun()
    else:
        st.info("No bookmarks yet. Use ⭐ on responses to save translations.")

    st.divider()

    # Reset / Export conversation
    if st.button("🧹 Clear History", use_container_width=True):
        state.clear_conversation()
        st.rerun()

    export_data = state.export_conversation()
    st.download_button(
        label="💾 Export Conversation JSON",
        data=export_data,
        file_name=f"conversation_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
        mime="application/json",
        use_container_width=True,
    )


# ---------------------------------------------------------------------------
# Main content area with GPT-style tabs
# ---------------------------------------------------------------------------

st.markdown(
    "<h1 class='gradient-header'>🌐 AI Translator Chatbot</h1>",
    unsafe_allow_html=True,
)
st.markdown(
    "Experience a **production-ready multilingual translator** with text, voice, and image support powered by **Groq**.",
)

translator_tab, image_tab, voice_tab, history_tab = st.tabs(
    ["💬 Translator", "🖼️ Image Translation", "🎙️ Voice Translation", "📚 History"]
)

# ----------------------- Translator Tab -----------------------
with translator_tab:
    st.markdown("#### Chat")
    with st.container():
        st.markdown("<div class='chat-container'>", unsafe_allow_html=True)
        for i, message in enumerate(state.conversation_history):
            render_chat_message(message, i)
        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("#### Media Inputs")
    with st.expander("🎙️ Audio", expanded=st.session_state.show_quick_mic):
        if st.session_state.show_quick_mic:
            st.markdown("**Record from microphone**")
            try:
                quick_audio = st.audio_input("Mic", key="quick_mic_input", label_visibility="collapsed")
            except Exception as e:
                quick_audio = None
                st.error(f"Microphone not available or permission denied: {e}")

            if quick_audio is not None:
                process_voice_input(quick_audio.getvalue())
                st.session_state.show_quick_mic = False
                st.rerun()

        render_audio_section()

    with st.expander("🖼️ Images", expanded=st.session_state.show_quick_image):
        if st.session_state.show_quick_image:
            quick_image = st.file_uploader(
                "Upload image",
                type=["png", "jpg", "jpeg", "gif", "bmp", "webp", "tiff"],
                key="quick_image_uploader",
            )
            if quick_image is not None:
                try:
                    img_bytes = quick_image.read()
                    process_image_input(img_bytes)
                except Exception as e:
                    st.error(f"Failed to read/process image: {e}")
                finally:
                    st.session_state.show_quick_image = False
                st.rerun()

        render_image_section()

# ----------------------- Image Translation Tab -----------------------
with image_tab:
    st.subheader("Image → Text → Translation")
    image_file = st.file_uploader(
        "Upload an image containing text. OCR will extract it, then you can translate.",
        type=["png", "jpg", "jpeg", "gif", "bmp"],
        key="image_ocr_uploader",
    )
    if image_file is not None:
        try:
            image_bytes = image_file.read()
        except Exception as e:
            image_bytes = None
            st.error(f"Could not read uploaded image: {e}")

        if image_bytes:
            try:
                # Fix deprecated use_column_width warning by using width instead
                st.image(image_bytes, caption="Uploaded image", width=520)
            except Exception:
                st.warning("Image preview could not be displayed, but OCR may still work.")

        if image_bytes and st.button("🔍 Extract & Translate", key="ocr_translate_button"):
            process_image_input(image_bytes)
            st.rerun()

    st.markdown("#### Image Messages")
    render_image_section()

# ----------------------- Voice Translation Tab -----------------------
with voice_tab:
    st.subheader("Voice → Text → Translation")

    st.markdown("**Microphone Input**")
    try:
        mic_audio = st.audio_input("Record from microphone", key="voice_mic_input")
    except Exception as e:
        mic_audio = None
        st.error(f"Microphone not available or permission denied: {e}")

    if mic_audio is not None:
        mic_bytes = mic_audio.getvalue()
        # Auto-translate as soon as recording is available
        process_voice_input(mic_bytes)
        st.rerun()

    st.markdown("---")
    st.markdown("**Upload Audio File**")
    audio_file = st.file_uploader(
        "Upload an audio file (WAV, MP3, OGG, M4A).",
        type=["wav", "mp3", "ogg", "m4a"],
        key="voice_file_uploader",
    )
    if audio_file is not None:
        file_bytes = audio_file.read()
        if st.button("Process Uploaded Audio", key="process_uploaded_audio_btn"):
            process_voice_input(file_bytes)
            st.rerun()

    st.markdown("#### Audio Messages")
    render_audio_section()

# ----------------------- History Tab -----------------------
with history_tab:
    st.subheader("Conversation History")
    st.caption("Review all past translations with timestamps.")

    if not state.conversation_history:
        st.info("No history yet. Start by sending a message in the Translator tab.")
    else:
        for i, msg in enumerate(state.conversation_history):
            ts = msg.timestamp.strftime("%Y-%m-%d %H:%M:%S")
            role_label = "User" if msg.role == "user" else "Assistant"
            st.markdown(f"**{role_label}** · `{ts}`")
            st.write(msg.content)
            st.markdown("---")

    col_h1, col_h2 = st.columns(2)
    with col_h1:
        if st.button("🧹 Clear Conversation Only", key="clear_conv_history"):
            state.clear_conversation()
            st.rerun()
    with col_h2:
        if st.button("🧹 Clear All (Conversation + Bookmarks)", key="clear_all_history"):
            state.clear_conversation()
            state.bookmarks = []
            st.rerun()


# ---------------------------------------------------------------------------
# Bottom Chat Bar (Text + Mic + Image + Send)
# ---------------------------------------------------------------------------

st.markdown("<div class='bottom-chat-bar'><div class='bottom-chat-inner'>", unsafe_allow_html=True)

col_plus, col_input, col_mic, col_send = st.columns([1, 7, 1, 1])

with col_plus:
    image_clicked = st.button("🖼️", key="bottom_image_btn", help="Translate from image")

with col_input:
    with st.container():
        text = st.text_input(
            "Message",
            key="chat_text_input",
            label_visibility="collapsed",
            placeholder="Type your text to translate...",
            value=st.session_state.input_text,
        )
        st.session_state.input_text = text

with col_mic:
    mic_clicked = st.button("🎤", key="bottom_mic_btn", help="Use microphone")

with col_send:
    send_clicked = st.button("➡️", key="bottom_send_btn", help="Send for translation", type="primary")

st.markdown("</div></div>", unsafe_allow_html=True)

# Handle bottom bar actions
if mic_clicked:
    # Render mic recorder (requests mic permission) and auto-translate on completion
    st.session_state.show_quick_mic = True
    st.rerun()

if image_clicked:
    # Render image uploader and auto-translate after OCR
    st.session_state.show_quick_image = True
    st.rerun()

if send_clicked and st.session_state.input_text.strip():
    process_user_input(st.session_state.input_text.strip())
    st.session_state.input_text = ""
    st.rerun()
