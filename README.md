# CodeAlpha — Artificial Intelligence Internship
## Task 1: AI Language Translation Tool 🌐

[![Python Version](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://www.python.org/)
[![Internship](https://img.shields.io/badge/CodeAlpha-AI%20Internship-orange.svg)](https://www.codealpha.tech/)
[![Task](https://img.shields.io/badge/Task-Task%201%3A%20Language%20Translation%20Tool-brightgreen.svg)]()
[![License](https://img.shields.io/badge/License-MIT-purple.svg)]()

> A feature-rich AI Language Translation Tool built with Python, Google Translate API, Text-to-Speech (TTS), and dual user interfaces (Modern Desktop GUI & Responsive Web App).

---

## 📌 Project Overview

This project was developed as part of the **CodeAlpha Artificial Intelligence Internship** for **Task 1: Language Translation Tool**.

The application allows users to seamlessly translate text across 100+ languages in real-time. It features automatic source language detection, language swapping, one-click clipboard copying, and voice synthesis (Text-to-Speech).

---

## ✨ Features Implemented

| Requirement | Implementation Detail | Status |
| :--- | :--- | :---: |
| **User Interface** | Intuitive Desktop GUI (`Tkinter`/`TTK`) & Modern Web App (`Flask`, `HTML5`, `CSS3`, `JS`) | ✅ Complete |
| **Translation API** | Google Translate API engine with 105+ supported languages | ✅ Complete |
| **Language Selection** | Source language selector (with Auto-Detect) & Target language selector | ✅ Complete |
| **API Communication** | Asynchronous HTTP requests with background threading (no UI freezing) | ✅ Complete |
| **Output Display** | Dedicated output panel with clean typography and real-time word/character count | ✅ Complete |
| **Copy Button** | One-click copy to clipboard with toast confirmation notification | ✅ Complete |
| **Text-to-Speech (TTS)** | Voice synthesis (`pyttsx3` for Desktop, `Web Speech API` for Web App) | ✅ Complete |
| **Language Swap (⇄)** | Instant swap between source and target languages with text persistence | ✅ Complete |
| **Keyboard Shortcut** | Press `Ctrl + Enter` to immediately translate | ✅ Complete |

---

## 📂 Project Structure

```text
CodeAlpha_LanguageTranslationTool/
│
├── app.py                   # Desktop GUI Application (Tkinter & TTK)
├── web_app.py               # Web Application Server (Flask)
├── translator_engine.py     # Core Translation & TTS Engine
├── requirements.txt         # Project dependencies
├── README.md                # Documentation & instructions
│
├── templates/
│   └── index.html           # Modern glassmorphism frontend for Web App
│
└── static/
    ├── style.css            # Responsive CSS styling
    └── script.js            # Frontend JavaScript (Speech, Copy, Shortcuts)
```

---

## 🚀 Getting Started

### 1. Clone or Download the Repository

```bash
git clone https://github.com/YOUR_USERNAME/CodeAlpha_LanguageTranslationTool.git
cd CodeAlpha_LanguageTranslationTool
```

### 2. Install Dependencies

Ensure you have Python 3.8+ installed. Install the required libraries using pip:

```bash
pip install -r requirements.txt
```

---

## 💻 Running the Application

You can run either the **Desktop GUI** or the **Web Application**:

### Option A: Run the Desktop GUI App (Recommended for Quick Demo)

```bash
python app.py
```
- A native desktop window will open with a modern slate & blue theme.
- Enter text, choose target language, and click **Translate Now** or press `Ctrl + Enter`.
- Click **🔊 Listen** to hear the pronunciation.
- Click **📋 Copy Translation** to copy the translated text to your clipboard.

### Option B: Run the Web Application

```bash
python web_app.py
```
- Open your browser and visit: **`http://127.0.0.1:5000`**
- Features full responsive layout, smooth animations, and audio pronunciation.

---

## 🎥 LinkedIn Video Demonstration Guide

As required by CodeAlpha instructions:
1. **Introduction**: Mention your name, internship role at **@CodeAlpha**, and that this is **Task 1: Language Translation Tool**.
2. **Features Walkthrough**:
   - Show text entry and Auto-Language detection.
   - Show translation into multiple languages (e.g., Spanish, French, Hindi, Japanese).
   - Demonstrate the **Language Swap (⇄)** button.
   - Demonstrate the **Copy to Clipboard** button.
   - Demonstrate the **Text-to-Speech (🔊 Listen)** feature.
3. **Architecture**: Briefly highlight the Python modular architecture (`translator_engine.py`, `app.py`, `web_app.py`).
4. **Post on LinkedIn**:
   - Tag **@CodeAlpha**
   - Include the GitHub repository link: `CodeAlpha_LanguageTranslationTool`
   - Use hashtags: `#CodeAlpha #ArtificialIntelligence #MachineLearning #Python #Internship`

---

## 👨‍💻 Author & Acknowledgements

- **Developer**: CodeAlpha AI Intern
- **Company**: [CodeAlpha](https://www.codealpha.tech/)
- **Domain**: Artificial Intelligence

