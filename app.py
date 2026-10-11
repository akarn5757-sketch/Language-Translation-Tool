"""
CodeAlpha AI Internship - Task 1: Language Translation Tool
Desktop GUI Application using Python Tkinter, TTK, and Google Translate API.

Features:
- Source & Target language selection (100+ languages with Auto-Detection)
- Swap Languages button (⇄)
- Real-time character & word counter
- Copy to Clipboard with visual feedback
- Text-to-Speech (TTS) audio playback using pyttsx3
- Background threading to prevent GUI freezing
- Keyboard shortcut: Ctrl + Enter to Translate
- Clean, modern, responsive user interface
"""

import sys
import threading
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import pyperclip

from translator_engine import (
    SUPPORTED_LANGUAGES,
    CODE_TO_LANGUAGE,
    TranslationEngine,
)


class LanguageTranslatorApp:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("CodeAlpha — AI Language Translation Tool")
        self.root.geometry("1020x720")
        self.root.minsize(860, 600)
        self.root.configure(bg="#F1F5F9")

        # Translation engine instance
        self.engine = TranslationEngine()
        self.is_translating = False
        self.is_speaking = False

        # Configure modern TTK styles
        self._setup_styles()

        # Build UI layout
        self._create_header()
        self._create_language_selector()
        self._create_text_areas()
        self._create_action_bar()
        self._create_status_bar()

        # Keyboard shortcuts
        self.root.bind("<Control-Return>", lambda event: self.translate_text())
        self.root.bind("<Control-Shift-C>", lambda event: self.copy_translation())

        # Initialize focus
        self.source_text.focus_set()

    def _setup_styles(self):
        """Configure modern clean TTK styles and color palette."""
        style = ttk.Style()
        try:
            style.theme_use("clam")
        except Exception:
            pass

        # Color palette
        self.COLOR_BG = "#F8FAFC"
        self.COLOR_SURFACE = "#FFFFFF"
        self.COLOR_PRIMARY = "#2563EB"       # Modern Royal Blue
        self.COLOR_PRIMARY_HOVER = "#1D4ED8"
        self.COLOR_SECONDARY = "#0F172A"     # Dark Slate
        self.COLOR_BORDER = "#E2E8F0"
        self.COLOR_TEXT_MAIN = "#1E293B"
        self.COLOR_TEXT_MUTED = "#64748B"
        self.COLOR_ACCENT = "#10B981"        # Emerald Green for Success
        self.COLOR_DANGER = "#EF4444"

        # Combobox styling
        style.configure(
            "Custom.TCombobox",
            fieldbackground="#FFFFFF",
            background="#FFFFFF",
            foreground="#1E293B",
            font=("Segoe UI", 10),
            padding=5,
        )

        # Primary Button
        style.configure(
            "Primary.TButton",
            font=("Segoe UI", 11, "bold"),
            background=self.COLOR_PRIMARY,
            foreground="#FFFFFF",
            padding=(18, 9),
            borderwidth=0,
        )
        style.map(
            "Primary.TButton",
            background=[("active", self.COLOR_PRIMARY_HOVER), ("disabled", "#94A3B8")],
            foreground=[("disabled", "#E2E8F0")],
        )

        # Secondary Button
        style.configure(
            "Secondary.TButton",
            font=("Segoe UI", 9),
            background="#E2E8F0",
            foreground="#1E293B",
            padding=(10, 5),
            borderwidth=0,
        )
        style.map(
            "Secondary.TButton",
            background=[("active", "#CBD5E1")],
        )

        # Swap Button
        style.configure(
            "Swap.TButton",
            font=("Segoe UI", 12, "bold"),
            background="#EEF2F6",
            foreground=self.COLOR_PRIMARY,
            padding=(10, 4),
        )
        style.map(
            "Swap.TButton",
            background=[("active", "#DBEAFE")],
        )

    def _create_header(self):
        """Header banner with title, branding, and subtitle."""
        header_frame = tk.Frame(self.root, bg="#1E293B", height=85)
        header_frame.pack(fill="x", side="top")
        header_frame.pack_propagate(False)

        inner_header = tk.Frame(header_frame, bg="#1E293B")
        inner_header.pack(fill="both", expand=True, padx=30, pady=12)

        # Left title section
        title_frame = tk.Frame(inner_header, bg="#1E293B")
        title_frame.pack(side="left", fill="y")

        lbl_title = tk.Label(
            title_frame,
            text="🌐 CodeAlpha Language Translation Tool",
            font=("Segoe UI", 16, "bold"),
            bg="#1E293B",
            fg="#FFFFFF",
        )
        lbl_title.pack(anchor="w")

        lbl_subtitle = tk.Label(
            title_frame,
            text="AI-powered Multilingual Translation • Real-Time Detection • Text-To-Speech",
            font=("Segoe UI", 9),
            bg="#1E293B",
            fg="#94A3B8",
        )
        lbl_subtitle.pack(anchor="w", pady=(2, 0))

        # Right badge
        badge_frame = tk.Frame(inner_header, bg="#1E293B")
        badge_frame.pack(side="right", fill="y")

        lbl_badge = tk.Label(
            badge_frame,
            text="Task 1 • CodeAlpha AI",
            font=("Segoe UI", 9, "bold"),
            bg="#3B82F6",
            fg="#FFFFFF",
            padx=12,
            pady=4,
        )
        lbl_badge.pack(anchor="e", pady=8)

    def _create_language_selector(self):
        """Language dropdowns with Swap button."""
        selector_card = tk.Frame(self.root, bg="#FFFFFF", bd=1, relief="flat", highlightbackground="#E2E8F0", highlightthickness=1)
        selector_card.pack(fill="x", padx=30, pady=(20, 10))

        inner = tk.Frame(selector_card, bg="#FFFFFF", padx=20, pady=14)
        inner.pack(fill="x")

        # Source language
        source_frame = tk.Frame(inner, bg="#FFFFFF")
        source_frame.pack(side="left", fill="x", expand=True)

        lbl_source = tk.Label(
            source_frame,
            text="SOURCE LANGUAGE",
            font=("Segoe UI", 8, "bold"),
            fg="#64748B",
            bg="#FFFFFF",
        )
        lbl_source.pack(anchor="w", pady=(0, 4))

        languages_list = list(SUPPORTED_LANGUAGES.keys())
        self.source_combo = ttk.Combobox(
            source_frame,
            values=languages_list,
            style="Custom.TCombobox",
            state="readonly",
            height=15,
        )
        self.source_combo.set("Auto Detect")
        self.source_combo.pack(fill="x")
        self.source_combo.bind("<<ComboboxSelected>>", lambda e: self._on_language_changed())

        # Swap button in the center
        swap_container = tk.Frame(inner, bg="#FFFFFF", padx=20)
        swap_container.pack(side="left")

        btn_swap = ttk.Button(
            swap_container,
            text="⇄ Swap",
            style="Swap.TButton",
            command=self.swap_languages,
        )
        btn_swap.pack(pady=(15, 0))

        # Target language
        target_frame = tk.Frame(inner, bg="#FFFFFF")
        target_frame.pack(side="right", fill="x", expand=True)

        lbl_target = tk.Label(
            target_frame,
            text="TARGET LANGUAGE",
            font=("Segoe UI", 8, "bold"),
            fg="#64748B",
            bg="#FFFFFF",
        )
        lbl_target.pack(anchor="w", pady=(0, 4))

        target_langs = [k for k in languages_list if k != "Auto Detect"]
        self.target_combo = ttk.Combobox(
            target_frame,
            values=target_langs,
            style="Custom.TCombobox",
            state="readonly",
            height=15,
        )
        self.target_combo.set("Spanish")
        self.target_combo.pack(fill="x")
        self.target_combo.bind("<<ComboboxSelected>>", lambda e: self._on_language_changed())

    def _create_text_areas(self):
        """Creates side-by-side input and translation output text panels."""
        panels_frame = tk.Frame(self.root, bg="#F1F5F9")
        panels_frame.pack(fill="both", expand=True, padx=30, pady=10)

        # Configure equal grid column weights
        panels_frame.grid_columnconfigure(0, weight=1, uniform="col")
        panels_frame.grid_columnconfigure(1, weight=1, uniform="col")
        panels_frame.grid_rowconfigure(0, weight=1)

        # ------------------ LEFT PANEL: Source Input ------------------
        left_card = tk.Frame(panels_frame, bg="#FFFFFF", bd=1, relief="flat", highlightbackground="#E2E8F0", highlightthickness=1)
        left_card.grid(row=0, column=0, sticky="nsew", padx=(0, 8))

        # Header of Left Card
        left_hdr = tk.Frame(left_card, bg="#FFFFFF", padx=16, pady=10)
        left_hdr.pack(fill="x")

        tk.Label(
            left_hdr,
            text="Original Text",
            font=("Segoe UI", 11, "bold"),
            fg="#1E293B",
            bg="#FFFFFF",
        ).pack(side="left")

        self.lbl_source_count = tk.Label(
            left_hdr,
            text="0 characters • 0 words",
            font=("Segoe UI", 8),
            fg="#94A3B8",
            bg="#FFFFFF",
        )
        self.lbl_source_count.pack(side="right")

        # Source Text Box
        text_container_left = tk.Frame(left_card, bg="#FFFFFF", padx=14, pady=0)
        text_container_left.pack(fill="both", expand=True)

        self.source_text = scrolledtext.ScrolledText(
            text_container_left,
            wrap=tk.WORD,
            font=("Segoe UI", 11),
            bg="#F8FAFC",
            fg="#0F172A",
            insertbackground="#0F172A",
            relief="flat",
            bd=0,
            highlightthickness=1,
            highlightbackground="#CBD5E1",
            highlightcolor="#3B82F6",
            padx=12,
            pady=12,
        )
        self.source_text.pack(fill="both", expand=True)
        self.source_text.bind("<KeyRelease>", self._on_source_text_change)

        # Source Action Toolbar
        left_actions = tk.Frame(left_card, bg="#FFFFFF", padx=14, pady=10)
        left_actions.pack(fill="x")

        self.btn_speak_source = tk.Button(
            left_actions,
            text="🔊 Listen",
            font=("Segoe UI", 9),
            bg="#F1F5F9",
            fg="#1E293B",
            activebackground="#E2E8F0",
            relief="flat",
            padx=10,
            pady=4,
            cursor="hand2",
            command=self.speak_source_text,
        )
        self.btn_speak_source.pack(side="left", padx=(0, 6))

        btn_paste = tk.Button(
            left_actions,
            text="📋 Paste",
            font=("Segoe UI", 9),
            bg="#F1F5F9",
            fg="#1E293B",
            activebackground="#E2E8F0",
            relief="flat",
            padx=10,
            pady=4,
            cursor="hand2",
            command=self.paste_to_source,
        )
        btn_paste.pack(side="left", padx=(0, 6))

        btn_clear = tk.Button(
            left_actions,
            text="🗑️ Clear",
            font=("Segoe UI", 9),
            bg="#FEE2E2",
            fg="#991B1B",
            activebackground="#FECACA",
            relief="flat",
            padx=10,
            pady=4,
            cursor="hand2",
            command=self.clear_all,
        )
        btn_clear.pack(side="right")

        # ------------------ RIGHT PANEL: Translated Output ------------------
        right_card = tk.Frame(panels_frame, bg="#FFFFFF", bd=1, relief="flat", highlightbackground="#E2E8F0", highlightthickness=1)
        right_card.grid(row=0, column=1, sticky="nsew", padx=(8, 0))

        # Header of Right Card
        right_hdr = tk.Frame(right_card, bg="#FFFFFF", padx=16, pady=10)
        right_hdr.pack(fill="x")

        tk.Label(
            right_hdr,
            text="Translated Text",
            font=("Segoe UI", 11, "bold"),
            fg="#1E293B",
            bg="#FFFFFF",
        ).pack(side="left")

        self.lbl_target_count = tk.Label(
            right_hdr,
            text="0 characters • 0 words",
            font=("Segoe UI", 8),
            fg="#94A3B8",
            bg="#FFFFFF",
        )
        self.lbl_target_count.pack(side="right")

        # Target Text Box
        text_container_right = tk.Frame(right_card, bg="#FFFFFF", padx=14, pady=0)
        text_container_right.pack(fill="both", expand=True)

        self.target_text = scrolledtext.ScrolledText(
            text_container_right,
            wrap=tk.WORD,
            font=("Segoe UI", 11),
            bg="#F8FAFC",
            fg="#0F172A",
            insertbackground="#0F172A",
            relief="flat",
            bd=0,
            highlightthickness=1,
            highlightbackground="#CBD5E1",
            highlightcolor="#10B981",
            padx=12,
            pady=12,
        )
        self.target_text.pack(fill="both", expand=True)

        # Target Action Toolbar
        right_actions = tk.Frame(right_card, bg="#FFFFFF", padx=14, pady=10)
        right_actions.pack(fill="x")

        self.btn_speak_target = tk.Button(
            right_actions,
            text="🔊 Listen",
            font=("Segoe UI", 9),
            bg="#F1F5F9",
            fg="#1E293B",
            activebackground="#E2E8F0",
            relief="flat",
            padx=10,
            pady=4,
            cursor="hand2",
            command=self.speak_target_text,
        )
        self.btn_speak_target.pack(side="left", padx=(0, 6))

        self.btn_copy = tk.Button(
            right_actions,
            text="📋 Copy Translation",
            font=("Segoe UI", 9, "bold"),
            bg="#DCFCE7",
            fg="#166534",
            activebackground="#BBF7D0",
            relief="flat",
            padx=12,
            pady=4,
            cursor="hand2",
            command=self.copy_translation,
        )
        self.btn_copy.pack(side="left", padx=(0, 6))

        self.lbl_copy_toast = tk.Label(
            right_actions,
            text="",
            font=("Segoe UI", 9, "bold"),
            fg="#16A34A",
            bg="#FFFFFF",
        )
        self.lbl_copy_toast.pack(side="left", padx=6)

    def _create_action_bar(self):
        """Action bar with the primary Translate Button."""
        action_frame = tk.Frame(self.root, bg="#F1F5F9")
        action_frame.pack(fill="x", padx=30, pady=(5, 12))

        self.btn_translate = ttk.Button(
            action_frame,
            text="🚀 Translate Now (Ctrl + Enter)",
            style="Primary.TButton",
            command=self.translate_text,
        )
        self.btn_translate.pack(side="right")

        # Quick tip label on left
        lbl_tip = tk.Label(
            action_frame,
            text="💡 Tip: Press Ctrl + Enter to quickly translate • Select Auto Detect for auto-sensing",
            font=("Segoe UI", 8),
            fg="#64748B",
            bg="#F1F5F9",
        )
        lbl_tip.pack(side="left", pady=8)

    def _create_status_bar(self):
        """Footer status bar showing current status and detected language."""
        status_frame = tk.Frame(self.root, bg="#E2E8F0", height=30)
        status_frame.pack(fill="x", side="bottom")

        self.lbl_status = tk.Label(
            status_frame,
            text="Ready • Enter text and click Translate",
            font=("Segoe UI", 8),
            fg="#475569",
            bg="#E2E8F0",
            anchor="w",
            padx=15,
        )
        self.lbl_status.pack(side="left", fill="y")

        self.lbl_detected = tk.Label(
            status_frame,
            text="Detected: —",
            font=("Segoe UI", 8, "bold"),
            fg="#2563EB",
            bg="#E2E8F0",
            anchor="e",
            padx=15,
        )
        self.lbl_detected.pack(side="right", fill="y")

    # ------------------ EVENT HANDLERS & LOGIC ------------------

    def _on_source_text_change(self, event=None):
        """Updates live character and word counters for source text."""
        content = self.source_text.get("1.0", tk.END).strip()
        chars = len(content)
        words = len(content.split()) if content else 0
        self.lbl_source_count.config(text=f"{chars} characters • {words} words")

    def _update_target_count(self, text: str):
        """Updates character and word counters for target text."""
        chars = len(text.strip())
        words = len(text.strip().split()) if chars else 0
        self.lbl_target_count.config(text=f"{chars} characters • {words} words")

    def _on_language_changed(self):
        """Clear detected indicator on language change."""
        self.lbl_status.config(text="Ready • Ready to translate")

    def swap_languages(self):
        """Swaps source and target languages smoothly."""
        current_source = self.source_combo.get()
        current_target = self.target_combo.get()

        # If source is Auto Detect, swap target to source and set target to English
        if current_source == "Auto Detect":
            self.source_combo.set(current_target)
            self.target_combo.set("English")
        else:
            self.source_combo.set(current_target)
            self.target_combo.set(current_source)

        # Also swap the texts if target has content
        source_content = self.source_text.get("1.0", tk.END).strip()
        target_content = self.target_text.get("1.0", tk.END).strip()

        if target_content:
            self.source_text.delete("1.0", tk.END)
            self.source_text.insert(tk.END, target_content)

            self.target_text.delete("1.0", tk.END)
            self.target_text.insert(tk.END, source_content)

            self._on_source_text_change()
            self._update_target_count(source_content)

        self.lbl_status.config(text=f"Languages swapped: {self.source_combo.get()} ⇄ {self.target_combo.get()}")

    def paste_to_source(self):
        """Pastes text from clipboard into the source input."""
        try:
            clipboard_text = self.root.clipboard_get()
            if clipboard_text:
                self.source_text.insert(tk.INSERT, clipboard_text)
                self._on_source_text_change()
                self.lbl_status.config(text="Pasted text from clipboard")
        except Exception:
            try:
                clip_text = pyperclip.paste()
                if clip_text:
                    self.source_text.insert(tk.INSERT, clip_text)
                    self._on_source_text_change()
                    self.lbl_status.config(text="Pasted text from clipboard")
            except Exception as e:
                messagebox.showwarning("Clipboard", f"Could not paste clipboard content: {e}")

    def copy_translation(self):
        """Copies translated text to system clipboard with animated toast notification."""
        translation = self.target_text.get("1.0", tk.END).strip()
        if not translation:
            messagebox.showinfo("Copy", "There is no translated text to copy.")
            return

        try:
            pyperclip.copy(translation)
            self.root.clipboard_clear()
            self.root.clipboard_append(translation)

            # Show visual toast
            self.lbl_copy_toast.config(text="✓ Copied to Clipboard!")
            self.lbl_status.config(text="Translation copied to clipboard successfully")
            self.root.after(2500, lambda: self.lbl_copy_toast.config(text=""))
        except Exception as e:
            messagebox.showerror("Error", f"Failed to copy text: {e}")

    def clear_all(self):
        """Clears both text boxes and resets counters."""
        self.source_text.delete("1.0", tk.END)
        self.target_text.delete("1.0", tk.END)
        self._on_source_text_change()
        self._update_target_count("")
        self.lbl_detected.config(text="Detected: —")
        self.lbl_status.config(text="Cleared all text")
        self.source_text.focus_set()

    def translate_text(self):
        """Initiates translation in a separate background thread to keep GUI responsive."""
        if self.is_translating:
            return

        text = self.source_text.get("1.0", tk.END).strip()
        if not text:
            messagebox.showwarning("Input Required", "Please enter some text to translate.")
            self.source_text.focus_set()
            return

        source_lang = self.source_combo.get()
        target_lang = self.target_combo.get()

        # Update UI to loading state
        self.is_translating = True
        self.btn_translate.state(["disabled"])
        self.lbl_status.config(text="Translating text... Please wait...")

        def _worker():
            try:
                translated, detected = self.engine.translate(
                    text=text,
                    source_lang=source_lang,
                    target_lang=target_lang,
                )
                self.root.after(0, self._on_translation_success, translated, detected)
            except Exception as exc:
                self.root.after(0, self._on_translation_error, str(exc))

        thread = threading.Thread(target=_worker, daemon=True)
        thread.start()

    def _on_translation_success(self, translated: str, detected_code: str):
        """Callback when translation successfully completes."""
        self.target_text.delete("1.0", tk.END)
        self.target_text.insert(tk.END, translated)
        self._update_target_count(translated)

        detected_name = self.engine.get_language_name(detected_code)
        self.lbl_detected.config(text=f"Detected: {detected_name} ({detected_code})")
        self.lbl_status.config(text=f"✓ Translated successfully to {self.target_combo.get()}")

        self.btn_translate.state(["!disabled"])
        self.is_translating = False

    def _on_translation_error(self, error_msg: str):
        """Callback when an error occurs during translation."""
        self.btn_translate.state(["!disabled"])
        self.is_translating = False
        self.lbl_status.config(text=f"❌ Translation failed: {error_msg}")
        messagebox.showerror(
            "Translation Error",
            f"An error occurred while communicating with the translation API:\n\n{error_msg}\n\nPlease check your internet connection and try again.",
        )

    def speak_source_text(self):
        """Reads aloud the source text using TTS."""
        text = self.source_text.get("1.0", tk.END).strip()
        if not text:
            messagebox.showinfo("Speech", "No source text to read aloud.")
            return

        self.btn_speak_source.config(text="🔊 Speaking...", state="disabled")
        self.lbl_status.config(text="Playing audio for source text...")

        def _finished():
            self.root.after(0, lambda: self.btn_speak_source.config(text="🔊 Listen", state="normal"))
            self.root.after(0, lambda: self.lbl_status.config(text="Audio playback finished"))

        self.engine.speak_text(text, on_complete=_finished)

    def speak_target_text(self):
        """Reads aloud the translated text using TTS."""
        text = self.target_text.get("1.0", tk.END).strip()
        if not text:
            messagebox.showinfo("Speech", "No translated text to read aloud.")
            return

        self.btn_speak_target.config(text="🔊 Speaking...", state="disabled")
        self.lbl_status.config(text="Playing audio for translated text...")

        def _finished():
            self.root.after(0, lambda: self.btn_speak_target.config(text="🔊 Listen", state="normal"))
            self.root.after(0, lambda: self.lbl_status.config(text="Audio playback finished"))

        self.engine.speak_text(text, on_complete=_finished)


def main():
    root = tk.Tk()
    app = LanguageTranslatorApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()

