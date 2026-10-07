"""
CodeAlpha AI Internship - Task 1: Language Translation Tool
Web Application built with Flask.
Provides a modern REST API and responsive web frontend for translation.
"""

from flask import Flask, render_template, request, jsonify
from translator_engine import TranslationEngine, SUPPORTED_LANGUAGES

app = Flask(__name__)
engine = TranslationEngine()


@app.route("/")
def index():
    """Renders the main translation tool web interface."""
    return render_template(
        "index.html",
        languages=SUPPORTED_LANGUAGES,
    )


@app.route("/api/translate", methods=["POST"])
def translate_api():
    """
    API endpoint for text translation.
    Request JSON payload:
      {
         "text": "Hello world",
         "source_lang": "Auto Detect",
         "target_lang": "Spanish"
      }
    """
    try:
        data = request.get_json(force=True)
        text = data.get("text", "").strip()
        source_lang = data.get("source_lang", "Auto Detect")
        target_lang = data.get("target_lang", "Spanish")

        if not text:
            return jsonify({
                "success": False,
                "error": "Please enter some text to translate."
            }), 400

        translated_text, detected_code = engine.translate(
            text=text,
            source_lang=source_lang,
            target_lang=target_lang,
        )

        detected_name = engine.get_language_name(detected_code)

        return jsonify({
            "success": True,
            "translated_text": translated_text,
            "detected_code": detected_code,
            "detected_name": detected_name,
            "char_count": len(translated_text),
            "word_count": len(translated_text.split()) if translated_text else 0,
        })

    except Exception as exc:
        return jsonify({
            "success": False,
            "error": str(exc),
        }), 500


if __name__ == "__main__":
    print("Starting CodeAlpha Language Translation Tool Web App...")
    print("Open your browser and navigate to: http://127.0.0.1:5000")
    app.run(debug=True, host="127.0.0.1", port=5000)
