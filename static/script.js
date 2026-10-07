// Client-side interactions for CodeAlpha Language Translator

document.addEventListener('DOMContentLoaded', () => {
    const sourceText = document.getElementById('sourceText');
    const targetText = document.getElementById('targetText');
    const sourceLang = document.getElementById('sourceLang');
    const targetLang = document.getElementById('targetLang');
    const translateBtn = document.getElementById('translateBtn');
    const btnSpinner = document.getElementById('btnSpinner');
    const btnText = translateBtn.querySelector('.btn-text');
    const swapBtn = document.getElementById('swapBtn');
    const clearBtn = document.getElementById('clearBtn');
    const copyBtn = document.getElementById('copyBtn');
    const pasteBtn = document.getElementById('pasteBtn');
    const copyToast = document.getElementById('copyToast');
    const sourceStats = document.getElementById('sourceStats');
    const targetStats = document.getElementById('targetStats');
    const statusMessage = document.getElementById('statusMessage');
    const detectionBadge = document.getElementById('detectionBadge');
    const speakSourceBtn = document.getElementById('speakSourceBtn');
    const speakTargetBtn = document.getElementById('speakTargetBtn');

    // Update character and word counts
    function updateCounters() {
        const srcVal = sourceText.value.trim();
        const srcChars = srcVal.length;
        const srcWords = srcVal ? srcVal.split(/\s+/).length : 0;
        sourceStats.textContent = `${srcChars} characters • ${srcWords} words`;

        const tgtVal = targetText.value.trim();
        const tgtChars = tgtVal.length;
        const tgtWords = tgtVal ? tgtVal.split(/\s+/).length : 0;
        targetStats.textContent = `${tgtChars} characters • ${tgtWords} words`;
    }

    sourceText.addEventListener('input', updateCounters);

    // Swap Languages
    swapBtn.addEventListener('click', () => {
        const currentSrc = sourceLang.value;
        const currentTgt = targetLang.value;

        if (currentSrc === 'Auto Detect') {
            sourceLang.value = currentTgt;
            targetLang.value = 'English';
        } else {
            sourceLang.value = currentTgt;
            targetLang.value = currentSrc;
        }

        const srcVal = sourceText.value;
        const tgtVal = targetText.value;
        if (tgtVal) {
            sourceText.value = tgtVal;
            targetText.value = srcVal;
            updateCounters();
        }

        statusMessage.textContent = `Languages swapped: ${sourceLang.value} ⇄ ${targetLang.value}`;
    });

    // Clear All
    clearBtn.addEventListener('click', () => {
        sourceText.value = '';
        targetText.value = '';
        updateCounters();
        detectionBadge.textContent = 'Language: Auto Detect';
        statusMessage.textContent = 'Text cleared';
        sourceText.focus();
    });

    // Copy Translation to Clipboard
    copyBtn.addEventListener('click', async () => {
        const text = targetText.value.trim();
        if (!text) {
            showToast('⚠️ Nothing to copy', false);
            return;
        }

        try {
            await navigator.clipboard.writeText(text);
            showToast('✓ Copied to clipboard!', true);
            statusMessage.textContent = 'Translation copied to clipboard';
        } catch (err) {
            // Fallback
            targetText.select();
            document.execCommand('copy');
            showToast('✓ Copied!', true);
        }
    });

    // Paste into Source
    pasteBtn.addEventListener('click', async () => {
        try {
            const clipText = await navigator.clipboard.readText();
            if (clipText) {
                sourceText.value = clipText;
                updateCounters();
                statusMessage.textContent = 'Pasted text from clipboard';
            }
        } catch (err) {
            alert('Clipboard paste permission denied or unsupported. Please use Ctrl + V.');
        }
    });

    function showToast(msg, isSuccess) {
        copyToast.textContent = msg;
        copyToast.style.color = isSuccess ? '#10b981' : '#ef4444';
        setTimeout(() => {
            copyToast.textContent = '';
        }, 2500);
    }

    // Translation Request
    async function performTranslation() {
        const text = sourceText.value.trim();
        if (!text) {
            statusMessage.textContent = '⚠️ Please enter some text to translate';
            sourceText.focus();
            return;
        }

        // Set Loading State
        translateBtn.disabled = true;
        btnSpinner.style.display = 'inline-block';
        btnText.textContent = 'Translating...';
        statusMessage.textContent = 'Sending request to Google Translate API...';

        try {
            const response = await fetch('/api/translate', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    text: text,
                    source_lang: sourceLang.value,
                    target_lang: targetLang.value
                })
            });

            const data = await response.json();

            if (data.success) {
                targetText.value = data.translated_text;
                updateCounters();
                detectionBadge.textContent = `Detected: ${data.detected_name} (${data.detected_code})`;
                statusMessage.textContent = `✓ Translation complete to ${targetLang.value}!`;
            } else {
                statusMessage.textContent = `❌ Translation error: ${data.error}`;
                alert(`Error: ${data.error}`);
            }
        } catch (err) {
            statusMessage.textContent = '❌ Failed to connect to server. Check connection.';
            console.error(err);
        } finally {
            translateBtn.disabled = false;
            btnSpinner.style.display = 'none';
            btnText.textContent = '🚀 Translate Now';
        }
    }

    translateBtn.addEventListener('click', performTranslation);

    // Keyboard Shortcut: Ctrl + Enter
    document.addEventListener('keydown', (e) => {
        if ((e.ctrlKey || e.metaKey) && e.key === 'Enter') {
            e.preventDefault();
            performTranslation();
        }
    });

    // Text-to-Speech (Web Speech API)
    function speak(text) {
        if (!('speechSynthesis' in window)) {
            alert('Text-to-Speech is not supported in this browser.');
            return;
        }
        if (!text.trim()) return;

        window.speechSynthesis.cancel(); // Stop any active utterance
        const utterance = new SpeechSynthesisUtterance(text);
        utterance.rate = 1.0;
        window.speechSynthesis.speak(utterance);
    }

    speakSourceBtn.addEventListener('click', () => {
        const text = sourceText.value.trim();
        if (text) {
            statusMessage.textContent = '🔊 Playing audio for original text...';
            speak(text);
        }
    });

    speakTargetBtn.addEventListener('click', () => {
        const text = targetText.value.trim();
        if (text) {
            statusMessage.textContent = '🔊 Playing audio for translated text...';
            speak(text);
        }
    });
});
