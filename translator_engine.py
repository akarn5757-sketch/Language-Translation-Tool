"""
Core Translation Engine for CodeAlpha Language Translation Tool
Supports Google Translate API with auto-language detection, error handling,
text-to-speech (TTS), and clipboard operations.
"""

import threading
import requests
from typing import Tuple, Dict, Optional

# Comprehensive mapping of supported languages (105+ languages)
SUPPORTED_LANGUAGES: Dict[str, str] = {
    "Auto Detect": "auto",
    "Afrikaans": "af",
    "Albanian": "sq",
    "Amharic": "am",
    "Arabic": "ar",
    "Armenian": "hy",
    "Azerbaijani": "az",
    "Basque": "eu",
    "Belarusian": "be",
    "Bengali": "bn",
    "Bosnian": "bs",
    "Bulgarian": "bg",
    "Catalan": "ca",
    "Cebuano": "ceb",
    "Chinese (Simplified)": "zh-CN",
    "Chinese (Traditional)": "zh-TW",
    "Corsican": "co",
    "Croatian": "hr",
    "Czech": "cs",
    "Danish": "da",
    "Dutch": "nl",
    "English": "en",
    "Esperanto": "eo",
    "Estonian": "et",
    "Filipino": "tl",
    "Finnish": "fi",
    "French": "fr",
    "Frisian": "fy",
    "Galician": "gl",
    "Georgian": "ka",
    "German": "de",
    "Greek": "el",
    "Gujarati": "gu",
    "Haitian Creole": "ht",
    "Hausa": "ha",
    "Hawaiian": "haw",
    "Hebrew": "iw",
    "Hindi": "hi",
    "Hmong": "hmn",
    "Hungarian": "hu",
    "Icelandic": "is",
    "Igbo": "ig",
    "Indonesian": "id",
    "Irish": "ga",
    "Italian": "it",
    "Japanese": "ja",
    "Javanese": "jw",
    "Kannada": "kn",
    "Kazakh": "kk",
    "Khmer": "km",
    "Korean": "ko",
    "Kurdish": "ku",
    "Kyrgyz": "ky",
    "Lao": "lo",
    "Latin": "la",
    "Latvian": "lv",
    "Lithuanian": "lt",
    "Luxembourgish": "lb",
    "Macedonian": "mk",
    "Malagasy": "mg",
    "Malay": "ms",
    "Malayalam": "ml",
    "Maltese": "mt",
    "Maori": "mi",
    "Marathi": "mr",
    "Mongolian": "mn",
    "Myanmar (Burmese)": "my",
    "Nepali": "ne",
    "Norwegian": "no",
    "Odia (Oriya)": "or",
    "Pashto": "ps",
    "Persian": "fa",
    "Polish": "pl",
    "Portuguese": "pt",
    "Punjabi": "pa",
    "Romanian": "ro",
    "Russian": "ru",
    "Samoan": "sm",
    "Scots Gaelic": "gd",
    "Serbian": "sr",
    "Sesotho": "st",
    "Shona": "sn",
    "Sindhi": "sd",
    "Sinhala": "si",
    "Slovak": "sk",
    "Slovenian": "sl",
    "Somali": "so",
    "Spanish": "es",
    "Sundanese": "su",
    "Swahili": "sw",
    "Swedish": "sv",
    "Tajik": "tg",
    "Tamil": "ta",
    "Telugu": "te",
    "Thai": "th",
    "Turkish": "tr",
    "Ukrainian": "uk",
    "Urdu": "ur",
    "Uyghur": "ug",
    "Uzbek": "uz",
    "Vietnamese": "vi",
    "Welsh": "cy",
    "Xhosa": "xh",
    "Yiddish": "yi",
    "Yoruba": "yo",
    "Zulu": "zu",
}

# Reverse lookup dictionary: code -> Language Name
CODE_TO_LANGUAGE: Dict[str, str] = {v: k for k, v in SUPPORTED_LANGUAGES.items()}
# Add common aliases for reverse mapping
CODE_TO_LANGUAGE.update({
    "en": "English",
    "es": "Spanish",
    "fr": "French",
    "de": "German",
    "zh": "Chinese (Simplified)",
    "hi": "Hindi",
    "ar": "Arabic",
    "ru": "Russian",
    "ja": "Japanese",
    "pt": "Portuguese",
})


class TranslationEngine:
    """Handles text translation via Google Translate API and Text-to-Speech synthesis."""

    def __init__(self, timeout: int = 10):
        self.timeout = timeout
        self.endpoint = "https://translate.googleapis.com/translate_a/single"
        self._speech_lock = threading.Lock()

    def translate(
        self, text: str, source_lang: str = "auto", target_lang: str = "en"
    ) -> Tuple[str, str]:
        """
        Translates text from source_lang to target_lang.
        
        Args:
            text: The string to be translated.
            source_lang: Language code or name (e.g., 'auto', 'en', 'English').
            target_lang: Language code or name (e.g., 'es', 'Spanish').

        Returns:
            Tuple of (translated_text, detected_source_language_code)
        """
        cleaned_text = text.strip()
        if not cleaned_text:
            return "", ""

        # Normalize language codes
        source_code = self._resolve_code(source_lang, default="auto")
        target_code = self._resolve_code(target_lang, default="en")

        if source_code == target_code and source_code != "auto":
            return cleaned_text, source_code

        params = {
            "client": "gtx",
            "sl": source_code,
            "tl": target_code,
            "dt": "t",
            "ie": "UTF-8",
            "oe": "UTF-8",
        }
        data = {"q": cleaned_text}
        headers = {
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
            )
        }

        try:
            response = requests.post(
                self.endpoint,
                params=params,
                data=data,
                headers=headers,
                timeout=self.timeout,
            )
            response.raise_for_status()
            res_json = response.json()

            # The response structure from Google Translate API:
            # [[['translated_sentence_1', 'original_1', ...], ['translated_2', ...]], ..., 'detected_lang']
            translated_segments = []
            if isinstance(res_json, list) and len(res_json) > 0 and isinstance(res_json[0], list):
                for item in res_json[0]:
                    if item and isinstance(item, list) and len(item) > 0 and item[0]:
                        translated_segments.append(item[0])

            translated_text = "".join(translated_segments)
            detected_lang = res_json[2] if len(res_json) > 2 and res_json[2] else source_code

            return translated_text, detected_lang

        except requests.exceptions.RequestException as exc:
            raise RuntimeError(f"Network error during translation: {exc}") from exc
        except Exception as exc:
            raise RuntimeError(f"Translation failed: {exc}") from exc

    def _resolve_code(self, lang_identifier: str, default: str = "en") -> str:
        """Resolves language name or code to its valid ISO language code."""
        if not lang_identifier:
            return default
        # If it's already a recognized code
        if lang_identifier.lower() in CODE_TO_LANGUAGE:
            return lang_identifier.lower()
        # If it's a language display name
        if lang_identifier in SUPPORTED_LANGUAGES:
            return SUPPORTED_LANGUAGES[lang_identifier]
        # Case insensitive match on names
        for name, code in SUPPORTED_LANGUAGES.items():
            if name.lower() == lang_identifier.lower():
                return code
        return lang_identifier

    def get_language_name(self, code: str) -> str:
        """Returns the human-readable language name for a given language code."""
        return CODE_TO_LANGUAGE.get(code, code)

    def speak_text(self, text: str, on_complete: Optional[callable] = None) -> None:
        """
        Asynchronously converts text to speech using pyttsx3 in a background thread
        to prevent blocking the user interface.
        """
        if not text or not text.strip():
            return

        def _worker():
            with self._speech_lock:
                try:
                    import pyttsx3
                    engine = pyttsx3.init()
                    engine.setProperty("rate", 150)
                    engine.say(text)
                    engine.runAndWait()
                except Exception as err:
                    print(f"Text-to-speech error: {err}")
                finally:
                    if on_complete:
                        on_complete()

        thread = threading.Thread(target=_worker, daemon=True)
        thread.start()


# Global instance for quick re-use
engine = TranslationEngine()
