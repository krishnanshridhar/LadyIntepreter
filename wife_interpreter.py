import streamlit as st
from datetime import datetime
import os

# ─── PAGE CONFIG ─────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="She Said What? 💑",
    page_icon="💑",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─── CUSTOM CSS (with mobile media queries) ───────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700;900&family=DM+Sans:wght@300;400;500;600&display=swap');

html, body, [class*="css"] { font-family: 'DM Sans', sans-serif; }
h1, h2, h3 { font-family: 'Playfair Display', serif; }

/* Dark theme */
.stApp {
    background: linear-gradient(135deg, #1a0a0f 0%, #0d0d1a 50%, #1a0a14 100%);
    color: #f0e6ee;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #1f0a14 0%, #12091a 100%) !important;
    border-right: 1px solid #3d1a2e;
}
section[data-testid="stSidebar"] label { color: #e8c4d8 !important; font-size: 0.88rem; }
section[data-testid="stSidebar"] .stRadio label { color: #e8c4d8 !important; }

/* Inputs */
.stTextArea textarea, .stTextInput input {
    background: rgba(255,255,255,0.05) !important;
    border: 1px solid rgba(255,100,150,0.3) !important;
    border-radius: 12px !important;
    color: #f0e6ee !important;
}
.stTextArea textarea:focus, .stTextInput input:focus {
    border-color: rgba(255,100,150,0.6) !important;
    box-shadow: 0 0 0 2px rgba(194,24,91,0.15) !important;
}
div[data-baseweb="select"] > div {
    background: rgba(255,255,255,0.05) !important;
    border: 1px solid rgba(255,100,150,0.3) !important;
    border-radius: 12px !important;
    color: #f0e6ee !important;
}
div[data-baseweb="select"] span { color: #f0e6ee !important; }

/* Buttons */
.stButton > button {
    background: linear-gradient(135deg, #c2185b, #7b1fa2) !important;
    color: white !important;
    border: none !important;
    border-radius: 50px !important;
    padding: 0.6rem 1.8rem !important;
    font-family: 'DM Sans', sans-serif !important;
    font-weight: 600 !important;
    letter-spacing: 0.5px !important;
    transition: all 0.25s ease !important;
    width: 100%;
}
.stButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 25px rgba(194,24,91,0.4) !important;
}
.stButton > button:active { transform: translateY(0) !important; }

/* Sliders */
.stSlider > div > div > div { background: #c2185b !important; }

/* Multiselect */
.stMultiSelect [data-baseweb="tag"] {
    background: rgba(194,24,91,0.3) !important;
    color: #f48fb1 !important;
}

/* Checkbox */
.stCheckbox label { color: #e8c4d8 !important; }

/* Radio */
.stRadio label { color: #e8c4d8 !important; }

/* Result block */
.result-block {
    background: rgba(194,24,91,0.07);
    border: 1px solid rgba(194,24,91,0.22);
    border-radius: 16px;
    padding: 1.5rem 1.8rem;
    margin-top: 1rem;
    line-height: 1.85;
}
.result-block h3 { color: #f48fb1; margin-top: 1rem; }
.result-block p { color: #f0e6ee; }
.result-block ul, .result-block ol { color: #f0e6ee; }
.result-block strong { color: #fce4ec; }

/* Fancy divider */
.fdiv {
    height: 1px;
    background: linear-gradient(90deg, transparent, rgba(244,143,177,0.4), transparent);
    margin: 1.2rem 0;
}

/* Tabs */
.stTabs [data-baseweb="tab-list"] {
    background: rgba(255,255,255,0.03);
    border-radius: 50px;
    padding: 0.3rem;
}
.stTabs [data-baseweb="tab"] {
    border-radius: 50px !important;
    color: #b088a0 !important;
}
.stTabs [aria-selected="true"] {
    background: linear-gradient(135deg, #c2185b, #7b1fa2) !important;
    color: white !important;
}

/* Expander */
.streamlit-expanderHeader {
    background: rgba(255,255,255,0.04) !important;
    border: 1px solid rgba(255,100,150,0.15) !important;
    border-radius: 10px !important;
    color: #e8c4d8 !important;
}

/* Info/warning/error boxes */
.stAlert { border-radius: 10px !important; }

/* ── MOBILE RESPONSIVE ────────────────────────────────── */
@media (max-width: 768px) {
    /* Stack columns vertically on mobile */
    div[data-testid="column"] {
        width: 100% !important;
        flex: 1 1 100% !important;
        min-width: 100% !important;
    }

    /* Sidebar auto-collapses on mobile (Streamlit default), but tighten it */
    section[data-testid="stSidebar"] {
        min-width: 260px !important;
    }

    /* Smaller headings */
    h1 { font-size: 1.5rem !important; }
    h2 { font-size: 1.2rem !important; }

    /* Full-width result blocks */
    .result-block {
        padding: 1rem 1.1rem;
        font-size: 0.93rem;
    }

    /* Buttons full width on mobile */
    .stButton > button {
        width: 100% !important;
        padding: 0.7rem 1rem !important;
    }

    /* Tighter page padding */
    .block-container {
        padding: 1rem 0.8rem !important;
    }

    /* Phrase buttons: 2 columns on mobile */
    div[data-testid="column"]:nth-child(3) { display: none !important; }
}

@media (max-width: 480px) {
    h1 { font-size: 1.3rem !important; }
    .result-block { padding: 0.8rem; font-size: 0.88rem; }
    section[data-testid="stSidebar"] { min-width: 240px !important; }
}
</style>
""", unsafe_allow_html=True)

# ─── API KEY CHECK ────────────────────────────────────────────────────────────
api_key = os.environ.get("ANTHROPIC_API_KEY", "")
if not api_key:
    st.error(
        "⚠️ **ANTHROPIC_API_KEY not set.**\n\n"
        "Run with: `ANTHROPIC_API_KEY=your_key streamlit run wife_interpreter.py`\n\n"
        "Get your key at [console.anthropic.com](https://console.anthropic.com)"
    )
    st.stop()

import anthropic  # import after key check to give clean error

client = anthropic.Anthropic(api_key=api_key)

# ─── SESSION STATE INIT ───────────────────────────────────────────────────────
for key, default in {
    "history": [],
    "phrase_result": None,
    "phrase_current": None,
    "emoji_quick": "",
}.items():
    if key not in st.session_state:
        st.session_state[key] = default

# ─── HELPERS ─────────────────────────────────────────────────────────────────
def ask_claude(system_prompt: str, user_msg: str, max_tokens: int = 1200) -> str:
    """Call Claude API with full error handling."""
    try:
        resp = client.messages.create(
            model="claude-sonnet-4-5",
            max_tokens=max_tokens,
            system=system_prompt,
            messages=[{"role": "user", "content": user_msg}]
        )
        return resp.content[0].text
    except anthropic.AuthenticationError:
        return "❌ **Authentication error** — check your ANTHROPIC_API_KEY."
    except anthropic.RateLimitError:
        return "❌ **Rate limit hit** — wait a moment and try again."
    except anthropic.APIStatusError as e:
        return f"❌ **API error {e.status_code}** — {e.message}"
    except Exception as e:
        return f"❌ **Unexpected error** — {str(e)}"

def show_result(result: str):
    """Render the AI result in a styled block."""
    st.markdown(f'<div class="result-block">', unsafe_allow_html=True)
    st.markdown(result)
    st.markdown('</div>', unsafe_allow_html=True)

def save_history(feature: str, input_text: str, result: str):
    snippet = input_text[:120] + ("..." if len(input_text) > 120 else "")
    st.session_state.history.insert(0, {
        "feature": feature,
        "input": snippet,
        "result": result,
        "time": datetime.now().strftime("%d %b %H:%M"),
    })
    if len(st.session_state.history) > 30:
        st.session_state.history = st.session_state.history[:30]

def divider():
    st.markdown('<div class="fdiv"></div>', unsafe_allow_html=True)

def validate(text: str, label: str = "This field") -> bool:
    """Show a warning and return False if input is empty."""
    if not text.strip():
        st.warning(f"⚠️ {label} can't be empty.")
        return False
    return True

# ─── SIDEBAR ─────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("<h2 style='color:#f48fb1; font-family:Playfair Display,serif; margin-bottom:2px;'>💑 She Said What?</h2>", unsafe_allow_html=True)
    st.markdown("<p style='color:#8a6070; font-size:0.82rem; margin-top:0;'>Your relationship survival toolkit</p>", unsafe_allow_html=True)
    st.divider()

    st.markdown("**Personalise**")
    her_name = st.text_input("Her name / nickname", value="her", key="her_name_input",
                             help="Used throughout the app to personalise responses")
    your_name = st.text_input("Your name", value="me", key="your_name_input")
    rel_type = st.selectbox("Relationship type", ["Wife", "Girlfriend", "Fiancée", "Partner"])
    years = st.slider("Years together", 0, 30, 2)
    st.divider()

    st.markdown("**Navigate**")
    page = st.radio("", [
        "💬 Message Decoder",
        "📖 Phrase Dictionary",
        "🚨 Danger Meter",
        "💌 Response Crafter",
        "🙏 Apology Forge",
        "😶 Silence Decoder",
        "⚖️ Argument Analyzer",
        "😊 Mood Analyzer",
        "🎁 Gift Oracle",
        "💝 Compliment Generator",
        "📅 Date Night Planner",
        "🔢 Emoji Decoder",
        "🌡️ Relationship Temperature",
        "🗓️ Forgiveness Tracker",
        "📚 Survival Guide",
        "🕑 History",
    ], label_visibility="collapsed")

    st.divider()
    st.markdown(
        f"<p style='color:#5a3050;font-size:0.73rem;text-align:center;'>"
        f"Session: {len(st.session_state.history)} reading(s)<br>"
        f"For entertainment only 😄</p>",
        unsafe_allow_html=True
    )

# Computed label used in feature pages
rel_label = her_name.strip() if her_name.strip() not in ("", "her") else rel_type.lower()

# ═══════════════════════════════════════════════════════════════════════════════
# 💬 MESSAGE DECODER
# ═══════════════════════════════════════════════════════════════════════════════
if page == "💬 Message Decoder":
    st.markdown("<h1 style='color:#f48fb1;'>💬 Message Decoder</h1>", unsafe_allow_html=True)
    st.caption(f"Paste what {rel_label} said — get the real meaning.")

    input_type = st.radio("Input type:", ["Single message", "Full conversation"], horizontal=True)

    if input_type == "Single message":
        msg = st.text_area(f"What did {rel_label} say?", height=100,
                           placeholder='"Fine." / "Do whatever you want." / "I\'m not mad."')
        context = st.text_input("Context (optional)", placeholder="e.g. After I forgot to call")
    else:
        msg = st.text_area("Paste conversation (WhatsApp, iMessage, etc.)", height=220,
                           placeholder="Paste the chat here...")
        context = st.text_input("Any extra context?", placeholder="e.g. This was about weekend plans")

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        go = st.button("🔍 Decode Now", use_container_width=True)

    if go:
        if not validate(msg, "The message"):
            st.stop()
        with st.spinner("Reading between the lines..."):
            system_prompt = f"""You are a witty, warm, and insightful relationship interpreter. The user ({your_name}) is trying to understand their {rel_type.lower()} ({rel_label}), together {years} year(s).

Provide a rich interpretation using these clearly labelled markdown sections:

### 🗣️ What She Said
Quote or summarise the key phrase(s)

### 💭 What She Really Meant
The true underlying message, emotion, or desire — be specific and insightful

### 🌡️ Emotional Temperature
What emotional state is she likely in right now?

### ⚠️ Danger Level
One of: 🟢 All Clear / 🟡 Tread Carefully / 🔴 Abort Mission / ☢️ Nuclear — with a one-line reason

### ✅ What You Should Do RIGHT NOW
3–4 specific, actionable steps. Practical and funny.

### ❌ What You Should NEVER Do
2–3 things that will make this dramatically worse

### 💬 The Perfect Thing To Say
One ideal response sentence they can literally use right now

### 🔮 Likely Outcome
Follow advice vs. ignore it — brief and humorous

Be warm, funny, and genuinely helpful. Refer to her as {rel_label}."""

            prompt = f"Message/conversation: {msg}"
            if context.strip():
                prompt += f"\n\nContext: {context}"

            result = ask_claude(system_prompt, prompt, 1500)
            save_history("💬 Message Decoder", msg, result)

        show_result(result)

# ═══════════════════════════════════════════════════════════════════════════════
# 📖 PHRASE DICTIONARY
# ═══════════════════════════════════════════════════════════════════════════════
elif page == "📖 Phrase Dictionary":
    st.markdown("<h1 style='color:#f48fb1;'>📖 The Sacred Phrase Dictionary</h1>", unsafe_allow_html=True)
    st.caption("Click any classic phrase to decode it instantly.")

    classics = [
        "I'm fine.", "Do whatever you want.", "Nothing's wrong.",
        "We need to talk.", "It's okay.", "If you want to.",
        "I don't care.", "You never listen.", "Must be nice.",
        "Sure, go ahead.", "I'm not angry, I'm disappointed.",
        "Forget it.", "No, don't worry about it.",
        "I just don't want to talk about it right now.",
        "I'm tired.", "You wouldn't understand.",
        "It's not a big deal.", "Whatever.",
    ]

    # 3-column grid of phrase buttons
    cols = st.columns(3)
    for i, phrase in enumerate(classics):
        with cols[i % 3]:
            if st.button(f'"{phrase}"', key=f"phrase_{i}", use_container_width=True):
                with st.spinner("Decoding..."):
                    system_prompt = f"""You are a hilarious and insightful relationship phrase decoder.
Decode this classic phrase that {rel_type.lower()}s say.

### 📌 The Phrase
Quote it back

### 🎭 Surface Translation
What she appears to be saying (the lie)

### 💣 Real Translation
What she actually means (the truth) — specific and funny

### 🌡️ Danger Level
🟢 All Clear / 🟡 Caution / 🔴 Danger / ☢️ Nuclear

### 🧠 Psychology
One insight into WHY she uses this phrase instead of saying what she means

### 💡 How To Handle It
3 specific tips

### 😂 Fun Fact
A funny observation about this phrase in relationships

Warm, funny, relatable."""
                    result = ask_claude(system_prompt, f'Phrase: "{phrase}"')
                    st.session_state.phrase_result = result
                    st.session_state.phrase_current = phrase
                    save_history("📖 Phrase Dictionary", phrase, result)

    # Show persisted result
    if st.session_state.phrase_result:
        divider()
        st.caption(f"📌 Decoded: *\"{st.session_state.phrase_current}\"*")
        show_result(st.session_state.phrase_result)

    divider()
    st.markdown("**🔍 Custom phrase lookup**")
    custom = st.text_input("Type any phrase:", placeholder='e.g. "Why would I be upset?"')
    if st.button("Decode Custom Phrase", use_container_width=True):
        if validate(custom, "Phrase"):
            with st.spinner("Decoding..."):
                system_prompt = f"""You are a hilarious relationship phrase decoder for a {rel_type.lower()}'s phrases.
Decode this phrase: Surface Translation, Real Translation, Danger Level, Psychology, How To Handle It, Fun Fact."""
                result = ask_claude(system_prompt, f'Phrase: "{custom}"')
                st.session_state.phrase_result = result
                st.session_state.phrase_current = custom
                save_history("📖 Phrase Dictionary", custom, result)
                show_result(result)

# ═══════════════════════════════════════════════════════════════════════════════
# 🚨 DANGER METER
# ═══════════════════════════════════════════════════════════════════════════════
elif page == "🚨 Danger Meter":
    st.markdown("<h1 style='color:#f48fb1;'>🚨 Danger Level Meter</h1>", unsafe_allow_html=True)
    st.caption("Describe your situation. Know exactly how worried to be.")

    situation = st.text_area("Describe your situation:", height=140,
        placeholder="e.g. I forgot our anniversary. She said 'It's fine' and went to bed early. This morning she made tea only for herself.")

    col1, col2 = st.columns(2)
    with col1:
        how_long = st.selectbox("How long has this been going on?",
            ["Just happened", "A few hours", "Since yesterday", "2–3 days", "A week+", "I've lost track"])
    with col2:
        prev_incidents = st.selectbox("Recent similar incidents?",
            ["First time", "Once before", "This is a pattern", "I'm always in trouble"])

    red_flags = st.multiselect("Red flags present (select all that apply):", [
        "She's gone quiet 🤐", "One-word answers", "No eye contact",
        "She's been unusually nice 😬", "She called her mum",
        "She's cleaning aggressively 🧹", "She's rearranging furniture",
        "The kids are being updated about 'mummy's feelings'",
        "She's eating alone", "She liked your friend's photo, not yours",
        "She said 'I'm fine' more than once", "She's watching sad movies",
        "No goodnight kiss", "'We need to talk' text received",
    ])

    if st.button("⚡ Assess My Danger Level", use_container_width=True):
        if not validate(situation, "Situation description"):
            st.stop()
        with st.spinner("Calculating survival probability..."):
            system_prompt = f"""You are a brutally honest but funny relationship danger assessor.
The user is in a situation with their {rel_type.lower()} and needs danger level assessment.

### 🌡️ DANGER LEVEL
State clearly: 🟢 SAFE / 🟡 ELEVATED / 🔴 HIGH ALERT / ☢️ DEFCON 1
Include a danger score out of 10 and a one-line headline.

### 🔍 Situation Analysis
What's actually happening — be insightful and specific

### 📊 Contributing Factors
What's making this better or worse

### ⏰ Time Sensitivity
How urgent is action?

### 🛠️ Recovery Protocol
Step-by-step rescue plan (numbered), specific to this exact situation

### 🚫 Avoid At All Costs
What will push this from bad to catastrophic

### 📈 Survival Probability
Humorous percentage with reasoning (e.g. "62% — the tea incident is recoverable but the pattern is concerning")

Be funny, warm, and specific. Show you've read all the details."""

            prompt = f"""Situation: {situation}
Duration: {how_long}
Prior pattern: {prev_incidents}
Red flags: {', '.join(red_flags) if red_flags else 'None selected'}"""

            result = ask_claude(system_prompt, prompt, 1400)
            save_history("🚨 Danger Meter", situation, result)

        show_result(result)

# ═══════════════════════════════════════════════════════════════════════════════
# 💌 RESPONSE CRAFTER
# ═══════════════════════════════════════════════════════════════════════════════
elif page == "💌 Response Crafter":
    st.markdown("<h1 style='color:#f48fb1;'>💌 Response Crafter</h1>", unsafe_allow_html=True)
    st.caption("Get the perfect words to say back.")

    her_msg = st.text_area(f"What did {rel_label} say?", height=110,
        placeholder="What she said or what just happened...")
    situation_ctx = st.text_input("Situation context:", placeholder="e.g. After an argument about the dishes")

    col1, col2, col3 = st.columns(3)
    with col1:
        goal = st.selectbox("Your goal:", [
            "Calm things down", "Apologise sincerely", "Stand my ground (nicely)",
            "Change the subject", "Make her laugh", "Romantic recovery",
            "End the argument", "Get her to open up",
        ])
    with col2:
        tone = st.selectbox("Tone:", ["Sincere", "Humorous", "Romantic", "Practical", "Empathetic"])
    with col3:
        medium = st.selectbox("Medium:", ["In person", "Text message", "WhatsApp", "Phone call"])

    if st.button("✍️ Craft My Response", use_container_width=True):
        if not validate(her_msg, "Her message"):
            st.stop()
        with st.spinner("Crafting the perfect words..."):
            system_prompt = f"""You are an expert relationship communication coach.
The user is {your_name}, with their {rel_type.lower()} ({rel_label}), together {years} year(s).

### 💎 The Perfect Response
3 alternative responses (Option A, B, C) — literal quotes the user can say/send.

### 🎯 Why This Works
Psychology behind the recommended approach

### ⏰ Timing Advice
When and how to deliver this

### 📣 Tone & Delivery Tips
How to say it — body language, voice, pacing

### ⚠️ What NOT To Say
2–3 things that will make this much worse right now

Responses for: {medium}. Goal: {goal}. Tone: {tone}."""

            result = ask_claude(system_prompt, f"Her message: {her_msg}\nContext: {situation_ctx}", 1400)
            save_history("💌 Response Crafter", her_msg, result)

        show_result(result)

# ═══════════════════════════════════════════════════════════════════════════════
# 🙏 APOLOGY FORGE
# ═══════════════════════════════════════════════════════════════════════════════
elif page == "🙏 Apology Forge":
    st.markdown("<h1 style='color:#f48fb1;'>🙏 The Apology Forge</h1>", unsafe_allow_html=True)
    st.caption("Craft an apology that actually works.")

    what_happened = st.text_area("What did you do? (be honest)", height=110,
        placeholder="e.g. Forgot her birthday / Spent too long at cricket / Said 'calm down'")
    her_reaction = st.text_input(f"How did {rel_label} react?",
        placeholder="e.g. She went quiet and said 'fine'")

    col1, col2, col3 = st.columns(3)
    with col1:
        apology_type = st.selectbox("Apology style:", [
            "Sincere & heartfelt", "Grand gesture", "Quick & clean",
            "Humorous but genuine", "Written note/card", "Long-form letter",
        ])
    with col2:
        severity = st.selectbox("How bad was it?", [
            "Minor slip", "Moderate offence", "Significant mistake",
            "Major blunder", "I'm genuinely surprised I'm still here",
        ])
    with col3:
        timing = st.selectbox("When to deliver:", ["Right now", "After she cools down", "Tonight", "Tomorrow morning"])

    # ✅ FIX: initialise apology_how before conditional assignment
    apology_how = ""
    apology_given = st.checkbox("I've already apologised (not well enough)")
    if apology_given:
        apology_how = st.text_input("How did you apologise?", placeholder="e.g. Said sorry quickly, gave flowers")

    if st.button("🔨 Forge My Apology", use_container_width=True):
        if not validate(what_happened, "What happened"):
            st.stop()
        with st.spinner("Forging your redemption arc..."):
            system_prompt = f"""You are a master apology crafter for relationships.
The user is apologising to their {rel_type.lower()} ({rel_label}), together {years} year(s).

### 🔍 What She Actually Needs To Hear
Not what you want to say — what SHE needs to receive emotionally

### 💬 The Apology
Full apology text, {apology_type} style. Genuine and specific, not generic.

### 🎯 Key Elements Included
What makes this apology effective

### 📋 The Action Plan
2–3 concrete things to do beyond words

### ⏰ Delivery Instructions
How and when to deliver for maximum impact

### 🚫 Phrases That Invalidate Apologies
3–4 phrases to NEVER say (e.g. "but you also...", "if you felt hurt...")

### 🔮 Expected Recovery Timeline
Realistic honest assessment given severity: {severity}"""

            apology_context = f"What happened: {what_happened}\nHer reaction: {her_reaction}\nSeverity: {severity}\nTiming: {timing}"
            if apology_given and apology_how:
                apology_context += f"\nPrevious apology attempt: {apology_how}"

            result = ask_claude(system_prompt, apology_context, 1400)
            save_history("🙏 Apology Forge", what_happened, result)

        show_result(result)

# ═══════════════════════════════════════════════════════════════════════════════
# 😶 SILENCE DECODER
# ═══════════════════════════════════════════════════════════════════════════════
elif page == "😶 Silence Decoder":
    st.markdown("<h1 style='color:#f48fb1;'>😶 The Silence Decoder</h1>", unsafe_allow_html=True)
    st.caption("What does this silence REALLY mean?")

    col1, col2 = st.columns(2)
    with col1:
        duration = st.selectbox("How long has she been silent?", [
            "15–30 minutes", "1–2 hours", "Half a day", "Since yesterday",
            "2–3 days", "A week", "I genuinely can't remember when she last spoke to me",
        ])
        last_said = st.text_input("Last thing she said:", placeholder='e.g. "Fine." or nothing at all')
    with col2:
        trigger = st.text_area("What happened just before the silence?", height=100,
            placeholder="e.g. I said I was watching the cricket instead of helping with groceries")

    silence_type = st.multiselect("Describe the silence:", [
        "She's in the same room but not talking",
        "She's moved to another room",
        "One-word text replies only",
        "Read receipts but no reply",
        "Left on delivered",
        "She's talking to everyone else normally",
        "She cried",
        "She's being polite but cold",
        "She's busy on her phone but not with me",
    ])

    if st.button("🔊 Decode The Silence", use_container_width=True):
        with st.spinner("Listening to the silence..."):
            system_prompt = f"""You are a silence decoder and relationship expert. Analyse what the silence means.

### 🔕 Type of Silence
Classify: Processing / Hurt / Punishing / Testing / Exhausted / Other

### 💭 What She's Feeling Right Now
Specific emotional state — not just "upset"

### ⏱️ The Duration Factor
What the duration ({duration}) tells us

### 🔍 Root Cause Analysis
What's this REALLY about?

### 🌡️ Danger Level
🟢 Needs space / 🟡 Needs acknowledgement / 🔴 Needs a serious conversation / ☢️ Intervention required

### 🛠️ How To Break The Silence
Step-by-step — what to do, what to say, what NOT to say

### ❌ Worst Things To Say
3–4 things that will make the silence even louder

### ⏰ Act vs Wait
Should they approach now or give more time?"""

            prompt = f"Duration: {duration}\nLast thing said: {last_said}\nTrigger: {trigger}\nSilence type: {', '.join(silence_type) if silence_type else 'Not specified'}"
            result = ask_claude(system_prompt, prompt, 1300)
            save_history("😶 Silence Decoder", trigger or duration, result)

        show_result(result)

# ═══════════════════════════════════════════════════════════════════════════════
# ⚖️ ARGUMENT ANALYZER
# ═══════════════════════════════════════════════════════════════════════════════
elif page == "⚖️ Argument Analyzer":
    st.markdown("<h1 style='color:#f48fb1;'>⚖️ Argument Analyzer</h1>", unsafe_allow_html=True)
    st.caption("Neutral analysis of who's right and how to resolve it.")
    st.info("⚠️ True neutrality means you might not like the answer.")

    topic = st.text_input("What was the argument about?", placeholder="e.g. Who should have called the plumber")

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("**Your side:**")
        your_side = st.text_area("Your position / what you said", height=130, key="your_side",
            placeholder="My side of the argument...")
    with col2:
        st.markdown(f"**{rel_label.capitalize()}'s side:**")
        her_side = st.text_area(f"{rel_label.capitalize()}'s position / what she said", height=130, key="her_side",
            placeholder="Her side of the argument...")

    want_verdict = st.checkbox("I want a verdict on who's objectively right (might sting)", value=True)

    if st.button("⚖️ Analyse This Argument", use_container_width=True):
        if not validate(topic, "Argument topic"):
            st.stop()
        with st.spinner("Weighing the evidence..."):
            system_prompt = f"""You are a neutral but funny relationship argument analyst. Be genuinely fair.

### 📋 Summary of The Dispute
Neutral 2-sentence summary

### 🔍 What's Really Going On
The underlying issue (often not the surface topic)

### ⚖️ The Verdict
{"Be direct: who has the stronger point and why. Be fair — it might be split." if want_verdict else "Skip the verdict — explore both sides fairly."}

### 💚 Valid Points (His Side)
What he got right

### 💜 Valid Points (Her Side)
What she got right

### 🔥 Escalation Mistakes
What both parties did to make this worse

### 🤝 Resolution Path
Step-by-step: how to actually resolve this specific argument

### 🔮 The Meta-Lesson
What this reveals about a dynamic worth addressing long-term

### 😂 Silver Lining
Something genuinely funny or absurd about the situation

Honest, balanced, specific, funny."""

            result = ask_claude(system_prompt, f"Topic: {topic}\nMy position: {your_side}\n{rel_label}'s position: {her_side}", 1400)
            save_history("⚖️ Argument Analyzer", topic, result)

        show_result(result)

# ═══════════════════════════════════════════════════════════════════════════════
# 😊 MOOD ANALYZER
# ═══════════════════════════════════════════════════════════════════════════════
elif page == "😊 Mood Analyzer":
    st.markdown("<h1 style='color:#f48fb1;'>😊 Mood Analyzer</h1>", unsafe_allow_html=True)
    st.caption("Decode her mood and know exactly how to act.")

    messages = st.text_area("Paste her recent messages or describe her behaviour:", height=160,
        placeholder="e.g. 'okay', 'sure', 'whatever works for you'... or describe what she's doing")

    col1, col2, col3 = st.columns(3)
    with col1:
        body_lang = st.multiselect("Body language:", [
            "Avoiding eye contact", "Smiling a lot", "Quiet", "Sighing frequently",
            "Engaged and chatty", "Giving short answers", "Affectionate", "Keeping distance",
        ])
    with col2:
        context_mood = st.selectbox("Situation:", [
            "Morning", "After work", "Evening", "After a social event",
            "After talking to family", "After bad news", "Weekend mode",
        ])
    with col3:
        your_sense = st.selectbox("Your gut feeling:", [
            "Something's off", "She seems fine", "She's happy",
            "I have no idea", "She might be testing me", "She's stressed about something else",
        ])

    if st.button("🔮 Analyse Her Mood", use_container_width=True):
        if not validate(messages, "Her messages or behaviour"):
            st.stop()
        with st.spinner("Reading the room..."):
            system_prompt = f"""You are an empathetic relationship mood analyst.

### 🎭 Mood Assessment
Primary + secondary mood (e.g. "Primarily tired, with underlying frustration")

### 📊 Confidence Level
How confident in this assessment and why

### 🔍 Key Signals
Which clues are most telling

### 💡 What She Likely Needs Right Now
Specific to her mood

### 🛠️ How To Act
Concrete guide: what to do, what to offer, what to say, what to avoid

### 🎯 Engagement Options
Low-effort, medium-effort, high-effort choices for right now

### ⚡ Mood Forecast
Where this mood is heading in the next few hours if nothing changes

Warm, specific, practical."""

            result = ask_claude(system_prompt, f"Messages/behaviour: {messages}\nBody language: {', '.join(body_lang) if body_lang else 'Not specified'}\nContext: {context_mood}\nMy gut: {your_sense}", 1300)
            save_history("😊 Mood Analyzer", messages[:80], result)

        show_result(result)

# ═══════════════════════════════════════════════════════════════════════════════
# 🎁 GIFT ORACLE
# ═══════════════════════════════════════════════════════════════════════════════
elif page == "🎁 Gift Oracle":
    st.markdown("<h1 style='color:#f48fb1;'>🎁 The Gift Oracle</h1>", unsafe_allow_html=True)
    st.caption("The right gift, for the right reason, at the right time.")

    col1, col2 = st.columns(2)
    with col1:
        occasion = st.selectbox("Occasion:", [
            "Apology / I messed up", "Anniversary", "Birthday",
            "Just because / Surprise", "Valentine's Day", "Milestone",
            "After a tough week for her", "Romantic gesture",
            "Congratulations", "I need to win back points",
        ])
        budget = st.selectbox("Budget:", [
            "Under $50", "$50–150", "$150–300", "$300–500", "$500+", "Money no object",
        ])
    with col2:
        her_interests = st.text_input("Her interests / hobbies:", placeholder="e.g. cooking, yoga, reading, plants")
        situation_gift = st.text_area("Situation context:", height=88,
            placeholder="e.g. She's been stressed with work and I haven't been very present")

    practical = st.checkbox("Include experience gifts (not just physical items)", value=True)

    if st.button("🎁 Reveal Gift Ideas", use_container_width=True):
        with st.spinner("Consulting the oracle..."):
            system_prompt = f"""You are a thoughtful and creative gift advisor.
Relationship: {rel_type.lower()}, {years} year(s). Budget: {budget}. Include experiences: {practical}.

### 🎯 What She Really Wants
What the occasion + context tells us emotionally

### 🏆 Top 3 Gift Recommendations
For each:
- Gift name & description
- Why it's perfect for THIS situation
- Where to find it
- How to present it for maximum impact
- Estimated cost

### 💎 The Grand Gesture Option
One memorable option regardless of budget (label clearly)

### 🪄 The Thoughtful Touch
One low-cost but high-emotional-impact idea

### ❌ Gifts To Avoid
3–4 categories or examples that will backfire for this occasion

### 📦 Presentation Advice
How to give it — timing, wrapping, words to say

Specific, creative, commercially realistic."""

            result = ask_claude(system_prompt, f"Occasion: {occasion}\nBudget: {budget}\nInterests: {her_interests}\nContext: {situation_gift}", 1400)
            save_history("🎁 Gift Oracle", f"{occasion} / {budget}", result)

        show_result(result)

# ═══════════════════════════════════════════════════════════════════════════════
# 💝 COMPLIMENT GENERATOR
# ═══════════════════════════════════════════════════════════════════════════════
elif page == "💝 Compliment Generator":
    st.markdown("<h1 style='color:#f48fb1;'>💝 Compliment Generator</h1>", unsafe_allow_html=True)
    st.caption("The right words, for the right moment.")

    col1, col2 = st.columns(2)
    with col1:
        comp_situation = st.selectbox("Situation:", [
            "She just got dressed / looks nice", "She cooked something",
            "She did something impressive", "She handled a tough situation well",
            "She's been stressed — cheer her up", "Good morning",
            "Good night", "Random act of love", "After an argument — break the tension",
            "She's doubting herself", "Milestone / achievement",
        ])
        comp_style = st.selectbox("Style:", [
            "Sincere & deep", "Funny & playful", "Romantic & poetic",
            "Simple & genuine", "Cheeky", "Over the top",
        ])
    with col2:
        about_her = st.text_area("What specifically to compliment:", height=100,
            placeholder="e.g. how she handled the kids today, her laugh, how hard she works...")
        medium_comp = st.selectbox("Delivery:", ["Say it out loud", "Text her", "Leave a note", "WhatsApp voice note"])

    quantity = st.slider("How many options?", 3, 10, 5)

    if st.button("💝 Generate Compliments", use_container_width=True):
        with st.spinner("Crafting something beautiful..."):
            system_prompt = f"""You are a master of meaningful compliments in relationships.
Generate {quantity} compliments for a {rel_type.lower()} ({rel_label}), together {years} year(s).
Style: {comp_style}. Delivery: {medium_comp}.

Number each one clearly. For each:
- The compliment (literal quote)
- One line on why it works

After all compliments add:
### 💡 Pro Tips
2–3 tips on delivering compliments so they land — not hollow."""

            result = ask_claude(system_prompt, f"Situation: {comp_situation}\nWhat to compliment: {about_her}", 1200)
            save_history("💝 Compliments", comp_situation, result)

        show_result(result)

# ═══════════════════════════════════════════════════════════════════════════════
# 📅 DATE NIGHT PLANNER
# ═══════════════════════════════════════════════════════════════════════════════
elif page == "📅 Date Night Planner":
    st.markdown("<h1 style='color:#f48fb1;'>📅 Date Night Planner</h1>", unsafe_allow_html=True)
    st.caption("Plan a date matched to your relationship temperature.")

    col1, col2, col3 = st.columns(3)
    with col1:
        rel_temp = st.select_slider("Relationship temperature:",
            options=["❄️ Frosty", "🌧️ Tense", "😐 Neutral", "🌤️ Good", "☀️ Great", "🔥 Amazing"])
        location = st.text_input("Your city:", placeholder="e.g. Sydney")
    with col2:
        budget_date = st.selectbox("Budget:", ["Under $50", "$50–150", "$150–300", "$300+"])
        date_time = st.selectbox("When:", ["Tonight", "This weekend", "Weeknight", "Daytime"])
    with col3:
        kids = st.checkbox("Have kids / need babysitter consideration?")
        her_prefs = st.text_input("Her preferences:", placeholder="e.g. loves food, hates loud places")

    if st.button("💫 Plan Our Date", use_container_width=True):
        with st.spinner("Planning your perfect night..."):
            system_prompt = f"""You are a romantic date night planner who tailors plans to the relationship dynamic.
Relationship: {rel_type.lower()}, {years} years. Location: {location or 'Sydney, Australia'}.

### 🎯 Date Strategy
Given temperature ({rel_temp}), what KIND of date is appropriate and why

### 🌟 The Recommended Plan
Full itinerary with timing, specific types of venues, conversation starters, romantic touches. Real, not generic.

### 🔄 Plan B
Alternative if the first doesn't suit

### 💰 Budget Breakdown
Estimated costs

### 💬 How To Invite Her
The exact words — matched to relationship temperature

### 🪄 The Magic Touches
3–5 small upgrades that make it memorable

### ❌ Avoid
Based on preferences and mood — things that will kill the vibe"""

            result = ask_claude(system_prompt, f"Temp: {rel_temp}\nBudget: {budget_date}\nTiming: {date_time}\nKids: {kids}\nPreferences: {her_prefs}", 1400)
            save_history("📅 Date Night", rel_temp, result)

        show_result(result)

# ═══════════════════════════════════════════════════════════════════════════════
# 🔢 EMOJI DECODER
# ═══════════════════════════════════════════════════════════════════════════════
elif page == "🔢 Emoji Decoder":
    st.markdown("<h1 style='color:#f48fb1;'>🔢 Emoji Decoder</h1>", unsafe_allow_html=True)
    st.caption("Decode what that emoji combination REALLY means.")

    # ✅ FIX: quick-decode buttons use session_state so value persists into widget
    quick_emojis = [
        ("🙂", "Dangerous smile"), ("👍", "Cold thumbs up"), ("😶", "Nothing face"),
        ("🙄", "The eye roll"), ("😤", "Frustrated puff"), ("🤔", "Ominous thinking"),
        ("❤️‍🩹", "Hurt heart"), ("🫠", "Melting — help"),
    ]
    st.markdown("**Quick decode — click any:**")
    qcols = st.columns(4)
    for i, (em, label) in enumerate(quick_emojis):
        with qcols[i % 4]:
            if st.button(f"{em} {label}", key=f"emoji_quick_{i}", use_container_width=True):
                st.session_state.emoji_quick = em

    emoji_input = st.text_input("Emoji message to decode:",
        value=st.session_state.emoji_quick,
        placeholder="e.g. 😶 / 👍 / 😤🙄 / ❤️‍🔥",
        key="emoji_input_field")
    emoji_context = st.text_input("Context:", placeholder="e.g. After I said I'd be home late")

    if st.button("🔍 Decode Emojis", use_container_width=True):
        if not validate(emoji_input, "Emoji input"):
            st.stop()
        with st.spinner("Decoding the visual language..."):
            system_prompt = f"""You are a relationship emoji expert who understands how {rel_type.lower()}s use emojis.

### 🎭 Surface Reading
What the emoji technically means

### 💣 The Real Meaning (In Context)
What she actually means by sending THIS in THIS situation

### 🌡️ Emotional Tone
Warm / neutral / passive-aggressive / genuinely happy / testing?

### 🔢 Danger Level
🟢 Safe / 🟡 Caution / 🔴 Alert

### 💬 Ideal Response
How to respond — give an actual suggested reply

### 🤔 The Psychology
Why do {rel_type.lower()}s communicate this way?

Funny and specific. A smiley face is NEVER just a smiley face."""

            result = ask_claude(system_prompt, f"Emoji: {emoji_input}\nContext: {emoji_context}", 900)
            save_history("🔢 Emoji Decoder", emoji_input, result)
            # Reset quick-select after successful decode
            st.session_state.emoji_quick = ""

        show_result(result)

# ═══════════════════════════════════════════════════════════════════════════════
# 🌡️ RELATIONSHIP TEMPERATURE
# ═══════════════════════════════════════════════════════════════════════════════
elif page == "🌡️ Relationship Temperature":
    st.markdown("<h1 style='color:#f48fb1;'>🌡️ Relationship Temperature Check</h1>", unsafe_allow_html=True)
    st.caption("A full health check. Answer honestly — she won't see this 😄")

    q1 = st.slider("Arguments in the last 2 weeks (0 = none, 10 = constantly):", 0, 10, 2)
    q2 = st.slider("Rate your current communication (1–10):", 1, 10, 6)
    q3 = st.slider("How connected do you feel right now? (1–10):", 1, 10, 6)
    q4 = st.slider("How satisfied do you think SHE is right now? (1–10):", 1, 10, 6)
    q5 = st.slider("How satisfied are YOU right now? (1–10):", 1, 10, 7)

    recent_good = st.text_input("Last genuinely good moment together:",
        placeholder="e.g. Laughed together at dinner 3 days ago")
    recent_bad = st.text_input("Last tension point:",
        placeholder="e.g. Argument about house chores")

    col1, col2 = st.columns(2)
    with col1:
        quality_time = st.selectbox("Quality time in last 2 weeks:",
            ["None", "Very little", "Some", "A good amount", "Lots"])
    with col2:
        affection = st.selectbox("Affection levels:",
            ["Very low", "Low", "Normal", "High", "Very high"])

    if st.button("🌡️ Check Our Temperature", use_container_width=True):
        with st.spinner("Running diagnostics..."):
            score = round((q2 + q3 + q4 + q5) / 4 - (q1 * 0.3), 1)
            system_prompt = """You are a relationship health analyst. Give a thorough temperature check.

### 🌡️ Overall Temperature
Clear rating with title (e.g. "Warm — Stable with Minor Friction") and score out of 10.

### 📊 The Breakdown
Analyse each: Communication, Connection, Conflict Level, Mutual Satisfaction, Affection

### 💚 Strengths Right Now
What's working

### 🔧 Areas To Improve
Specific, non-judgmental observations

### 🚀 Action Plan (This Week)
5 specific small things to do THIS WEEK to raise the temperature

### 🔮 Trajectory
Where is this heading in 3 months if current patterns continue?

### 💡 The One Thing
If only one thing — what should it be?

Warm, honest, constructive, specific. Don't sugarcoat but don't be harsh."""

            prompt = f"""Arguments: {q1}/10, Communication: {q2}/10, Connection: {q3}/10
Her satisfaction: {q4}/10, My satisfaction: {q5}/10
Quality time: {quality_time}, Affection: {affection}
Last good moment: {recent_good or 'Not mentioned'}
Last tension: {recent_bad or 'Not mentioned'}"""

            result = ask_claude(system_prompt, prompt, 1400)
            save_history("🌡️ Temperature Check", f"Score: {score}/10", result)

        st.metric("Calculated Score", f"{score}/10", help="Based on your inputs. Treat as indicative, not scientific 😄")
        show_result(result)

# ═══════════════════════════════════════════════════════════════════════════════
# 🗓️ FORGIVENESS TRACKER
# ═══════════════════════════════════════════════════════════════════════════════
elif page == "🗓️ Forgiveness Tracker":
    st.markdown("<h1 style='color:#f48fb1;'>🗓️ The Forgiveness Tracker</h1>", unsafe_allow_html=True)
    st.caption("Am I forgiven yet? Track your path to redemption.")

    incident = st.text_area("What happened:", height=100, placeholder="Describe the incident...")

    col1, col2 = st.columns(2)
    with col1:
        incident_date = st.date_input("When it happened:")
        # ✅ FIX: initialise before conditional assignment
        apology_given_ft = st.checkbox("I've apologised")
        apology_how_ft = ""
        if apology_given_ft:
            apology_how_ft = st.text_input("How did you apologise?",
                placeholder="e.g. Said sorry, bought flowers")
    with col2:
        her_response_ft = st.text_area("Her response / behaviour since:", height=100,
            placeholder="How has she been acting since the incident?")

    positive_steps = st.multiselect("Positive steps taken:", [
        "Genuine verbal apology", "Written apology / note", "Bought a gift",
        "Did something she's been asking you to do", "Quality time together",
        "Listened without defending yourself", "She laughed at something you did",
        "Physical affection restored", "She brought it up again (processing)",
        "She hasn't brought it up since", "She made you food", "Normal conversation resumed",
    ])

    if st.button("📊 Check Forgiveness Status", use_container_width=True):
        if not validate(incident, "Incident description"):
            st.stop()
        with st.spinner("Checking your redemption arc progress..."):
            system_prompt = """You are a relationship recovery tracker.

### 📍 Forgiveness Status
Choose one: ✅ Forgiven / 🔄 In Progress / ⏳ Too Early To Tell / 🔴 Not Yet / ❓ Unclear

### 📊 Recovery Progress
Give a progress percentage and explain why

### 🔍 Positive Signals
Which steps are working in their favour

### ⚠️ Concerning Signs
Signals it might not be as resolved as they think

### ⏰ Estimated Full Recovery
Realistic timeline

### 🛠️ Next Steps
2–3 specific things to do next

### 🔮 Is It Really Forgiven?
Honest assessment of lingering resentment

Honest, warm, specific."""

            apology_note = f"Apology method: {apology_how_ft}" if apology_given_ft and apology_how_ft else "No previous apology"
            prompt = f"Incident: {incident}\nDate: {incident_date}\nApologised: {apology_given_ft}\n{apology_note}\nBehaviour since: {her_response_ft}\nSteps taken: {', '.join(positive_steps) if positive_steps else 'None yet'}"
            result = ask_claude(system_prompt, prompt, 1200)
            save_history("🗓️ Forgiveness Tracker", incident[:80], result)

        show_result(result)

# ═══════════════════════════════════════════════════════════════════════════════
# 📚 SURVIVAL GUIDE
# ═══════════════════════════════════════════════════════════════════════════════
elif page == "📚 Survival Guide":
    st.markdown("<h1 style='color:#f48fb1;'>📚 The Relationship Survival Guide</h1>", unsafe_allow_html=True)
    st.caption("Essential knowledge. Read this before you need it.")

    topic_guide = st.selectbox("Choose a guide:", [
        "The 12 Commandments of Not Getting In Trouble",
        "How To Actually Listen (Not Just Hear)",
        "The Art of the Non-Apology vs Real Apology",
        "Reading the Room: A Field Guide",
        "Why 'Fine' Is Never Fine — The Complete Dictionary",
        "The Things She Wishes You Would Just Know",
        "How To Fight Fair (And Still Win)",
        "When To Talk And When To Shut Up",
        "The 5 Love Languages — Practical Guide",
        "Why She Tests You (And How To Pass)",
        "The Homework: Things To Routinely Do",
        "Understanding PMS vs Actual Upset (Respectfully)",
        "How To Bring Up Something Without Starting An Argument",
        "The Definitive Guide To Not Forgetting Important Dates",
    ])

    if st.button("📖 Read This Guide", use_container_width=True):
        with st.spinner("Compiling wisdom..."):
            system_prompt = f"""You are a warm, funny, and genuinely insightful relationship guide author.
Write for a person in a {rel_type.lower()} relationship ({years} years together).
ACTUALLY useful — not generic. Real examples, numbered rules/tips, humour.
Minimum 600 words. Feel like advice from a wise, funny friend who's seen it all.
Format with clear markdown headers and sections."""
            result = ask_claude(system_prompt, f"Write the guide: '{topic_guide}'", 1500)
            save_history("📚 Survival Guide", topic_guide, result)

        show_result(result)

# ═══════════════════════════════════════════════════════════════════════════════
# 🕑 HISTORY
# ═══════════════════════════════════════════════════════════════════════════════
elif page == "🕑 History":
    st.markdown("<h1 style='color:#f48fb1;'>🕑 Session History</h1>", unsafe_allow_html=True)
    st.caption(f"{len(st.session_state.history)} reading(s) this session.")

    if not st.session_state.history:
        st.info("Nothing yet! Use any feature and your results will appear here.")
    else:
        col1, col2 = st.columns([1, 4])
        with col1:
            if st.button("🗑️ Clear All", use_container_width=True):
                st.session_state.history = []
                st.session_state.phrase_result = None
                st.session_state.phrase_current = None
                st.rerun()

        for i, item in enumerate(st.session_state.history):
            with st.expander(f"{item['feature']}  ·  {item['time']}  ·  \"{item['input']}\""):
                st.markdown(item["result"])
