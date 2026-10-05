# Kinara AI v2 🚀

**Step-by-step Calculator + Smart Sinhala/English Chat**

Pure frontend — no backend, no API keys. Works offline after first load.

🌐 **Live:** [kinarachamara.github.io/KinaraAI](https://kinarachamara.github.io/KinaraAI/)

---

## What's new in v2

| Feature | Description |
|---------|-------------|
| √ & % math | `sqrt(144)`, `50%`, `2^10` |
| Voice input | 🎤 microphone (Chrome / Edge) |
| Chat history | Saved in browser localStorage |
| Typing indicator | Smooth bot reply animation |
| Copy answers | One-tap copy for calc results |
| More Q&A | Jokes, time, date, help, expanded keywords |
| Clear chat | 🗑️ button in header |
| Better matching | Fuzzy + keyword logic |

---

## Files

```
index.html          → Web app (open in browser)
chatbot.py          → Terminal CLI version
knowledge/
  qa.json           → Questions & answers
  dictionary.json   → Keyword synonyms (Sinhala + English)
  knowledge.json    → Intent-based answers
  logic.json        → Clarification rules
  greetings.json    → Short greetings
```

---

## How to run

### Web
Just open `index.html` in Chrome / Firefox / Edge  
**or** visit the live GitHub Pages link above.

### CLI
```bash
python3 chatbot.py
```

---

## Try these

**Math**
- `111*{1111+234546}`
- `sqrt(144)`
- `(100+200)*3`
- `2^10`
- `50%`

**Chat**
- `ai mokakda?`
- `oya kauda?`
- `oya kohomada?`
- `joke kiyanna`
- `time mokakda?`
- `help`

---

## Add more answers

Edit `knowledge/qa.json`:

```json
"your question": "the answer"
```

Then refresh the page.

---

Made with ❤️ · Kinara AI v2
