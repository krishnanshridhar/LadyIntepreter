# 💑 She Said What? — Relationship Interpreter

> A Streamlit app powered by Claude AI that decodes what your wife or girlfriend *really* means — with 16 features covering everything from message decoding to apology crafting, date night planning, and a full relationship health check.

---

## ✨ Features

| Feature | Description |
|---|---|
| 💬 **Message Decoder** | Paste any message or full conversation — get what she really meant, danger level, what to do, and the perfect thing to say |
| 📖 **Phrase Dictionary** | 18 classic phrases decoded instantly (e.g. "I'm fine", "We need to talk") + custom phrase lookup |
| 🚨 **Danger Meter** | Describe your situation, pick your red flags — get a danger score, survival probability, and rescue plan |
| 💌 **Response Crafter** | 3 crafted reply options (A/B/C) tailored to your goal, tone, and medium (text, WhatsApp, in person) |
| 🙏 **Apology Forge** | Full apologies written for you — style, delivery instructions, what phrases to never say |
| 😶 **Silence Decoder** | Decode the silent treatment — type, duration, cause, and how to break it |
| ⚖️ **Argument Analyzer** | Neutral verdict on who's right, root cause, resolution path, and the meta-lesson |
| 😊 **Mood Analyzer** | Decode her mood from messages + body language — and exactly how to act |
| 🎁 **Gift Oracle** | Context-aware gift ideas with presentation tips, what to avoid, and a grand gesture option |
| 💝 **Compliment Generator** | Situation-specific compliments you can literally say or send |
| 📅 **Date Night Planner** | Date matched to your relationship temperature — from frosty to amazing |
| 🔢 **Emoji Decoder** | Decode any emoji sequence — the 🙂 is never just a smiley face |
| 🌡️ **Relationship Temperature** | Full health check with sliders — score, breakdown, action plan, trajectory |
| 🗓️ **Forgiveness Tracker** | Am I forgiven yet? Progress %, recovery timeline, and next steps |
| 📚 **Survival Guide** | 14 deep-dive guides on demand — from active listening to fighting fair |
| 🕑 **History** | All session readings saved and expandable — up to 30 entries |

---

## 🚀 Quick Start

### 1. Clone / download

```bash
git clone <your-repo-url>
cd she-said-what
```

### 2. Install dependencies

```bash
pip install streamlit anthropic
```

### 3. Set your API key

Get your key from [console.anthropic.com](https://console.anthropic.com)

```bash
# Mac / Linux
export ANTHROPIC_API_KEY=sk-ant-...

# Windows Command Prompt
set ANTHROPIC_API_KEY=sk-ant-...

# Windows PowerShell
$env:ANTHROPIC_API_KEY="sk-ant-..."
```

### 4. Run the app

```bash
streamlit run wife_interpreter.py
```

Opens at **http://localhost:8501** in your browser.

---

## 📁 Project Structure

```
she-said-what/
├── wife_interpreter.py   # Main app (single file)
├── requirements.txt      # Python dependencies
└── README.md             # This file
```

No database, no external dependencies beyond `streamlit` and `anthropic`. All state is held in Streamlit session state — nothing persists between sessions.

---

## ⚙️ Configuration

All personalisation is done via the **sidebar** inside the app — no config files needed:

| Setting | Default | Description |
|---|---|---|
| Her name / nickname | `her` | Used throughout all features |
| Your name | `me` | Included in AI prompts |
| Relationship type | `Wife` | Wife / Girlfriend / Fiancée / Partner |
| Years together | `2` | Adjusts advice and tone |

---

## 🔑 API Key & Costs

This app calls the **Anthropic Claude API** (`claude-sonnet-4-5`) on every button click.

- Each feature call uses approximately **500–1,500 tokens** (input + output combined)
- See current pricing at [anthropic.com/pricing](https://www.anthropic.com/pricing)
- For typical personal use (10–20 calls/day) costs are minimal — usually a few cents per day

If the API key is missing, the app shows a clear error on startup and stops — no silent failures.

---

## 🐛 Troubleshooting

| Problem | Fix |
|---|---|
| `ANTHROPIC_API_KEY not set` error on launch | Export the key in your terminal before running |
| App shows an error on button click | Check terminal output — usually a rate limit or auth issue |
| Sidebar not visible | Click the `>` arrow on the left edge of the screen |
| Phrase results disappear after clicking elsewhere | Fixed in v2 — results persist via session state |
| Emoji quick-decode button doesn't update the field | Click the emoji button first, then click **Decode Emojis** |
| Fonts not loading | Check your internet connection — fonts load from Google Fonts CDN |

---

## 📱 Mobile Support

The app is mobile-responsive:

- Columns stack vertically on screens under 768px
- Headings and text scale down on small screens  
- Buttons go full-width on mobile
- Streamlit's sidebar auto-collapses on mobile (tap `>` to open)

Best experienced in **Chrome or Safari** on iOS/Android.

---

## 🔒 Privacy

- **No data is stored** — all inputs and results exist only in your browser session
- Closing the tab clears everything — history is session-only
- Inputs are sent to the Anthropic API to generate responses — see [Anthropic's Privacy Policy](https://www.anthropic.com/privacy)
- Avoid entering sensitive personal information (full names, addresses, financial details)

---

## 🚢 Deployment

### Streamlit Community Cloud (free)

1. Push both files to a **public GitHub repo**
2. Go to [share.streamlit.io](https://share.streamlit.io) and connect your repo
3. Add your key under **Settings → Secrets**:
   ```toml
   ANTHROPIC_API_KEY = "sk-ant-..."
   ```
4. Deploy — you'll get a public shareable URL

### requirements.txt

Create this file alongside the app for cloud deploys:

```
streamlit>=1.32.0
anthropic>=0.25.0
```

### Docker

```bash
docker run -p 8501:8501 \
  -e ANTHROPIC_API_KEY=sk-ant-... \
  -v $(pwd):/app \
  python:3.11-slim \
  bash -c "pip install streamlit anthropic && streamlit run /app/wife_interpreter.py"
```

---

## 🛠️ Developer Notes

### Adding a new feature page

1. Add the page name to the `st.radio()` list in the sidebar
2. Add an `elif page == "🆕 New Feature":` block in the main body
3. Follow this pattern:

```python
elif page == "🆕 New Feature":
    st.markdown("<h1 style='color:#f48fb1;'>🆕 New Feature</h1>", unsafe_allow_html=True)
    st.caption("Short description here.")

    user_input = st.text_area("Input label:", height=100, placeholder="...")

    if st.button("🔍 Run", use_container_width=True):
        if not validate(user_input, "Input"):
            st.stop()
        with st.spinner("Working..."):
            system_prompt = """Your system prompt here."""
            result = ask_claude(system_prompt, user_input, max_tokens=1200)
            save_history("🆕 New Feature", user_input, result)
        show_result(result)
```

### Helper reference

```python
ask_claude(system_prompt, user_msg, max_tokens=1200)
# Calls Claude API with full error handling. Returns a string.

show_result(result)
# Renders AI output in a styled card.

save_history(feature, input_text, result)
# Saves to session_state.history (capped at 30 entries).

validate(text, label)
# Shows st.warning and returns False if input is empty.
# Use: if not validate(text, "Field name"): st.stop()
```

---

## ⚠️ Disclaimer

*For entertainment purposes only. Results are generated by AI and should be taken with a healthy sense of humour. Your actual wife or girlfriend may vary. The app accepts no liability for outcomes of advice followed, gifts purchased, apologies delivered, or arguments started. 😄*

---

## 📄 License

MIT — do whatever you want with it. Just don't show it to her.
