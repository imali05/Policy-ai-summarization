import streamlit as st
import google.generativeai as genai
import PyPDF2
import io

# ── PAGE CONFIG ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Policy Summariser & Scenario Generator",
    layout="wide",
    page_icon="📋"
)

# ── CUSTOM CSS ───────────────────────────────────────────────────────────────
st.markdown("""
<style>
    .main-title {
        text-align: center;
        color: #2c3e50;
        font-size: 2rem;
        font-weight: bold;
        padding: 10px;
    }
    .sub-title {
        text-align: center;
        color: #7f8c8d;
        margin-bottom: 20px;
    }
    .panel-header {
        background: #2980b9;
        color: white;
        padding: 10px 15px;
        border-radius: 8px;
        font-size: 1.05rem;
        font-weight: bold;
        margin-bottom: 12px;
    }
    .summary-box {
        background: #eaf4fb;
        border-left: 5px solid #2980b9;
        padding: 15px;
        border-radius: 6px;
        margin-top: 10px;
    }
    .draft-box {
        background: #eafaf1;
        border-left: 5px solid #27ae60;
        padding: 15px;
        border-radius: 6px;
        margin-top: 10px;
    }
</style>
""", unsafe_allow_html=True)

# ── TITLE ────────────────────────────────────────────────────────────────────
st.markdown('<div class="main-title">📋 Policy Summariser & Scenario Generator</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">Upload or paste a policy → Summarise → Generate scenario-based policy drafts</div>', unsafe_allow_html=True)

# ── SIDEBAR ──────────────────────────────────────────────────────────────────
with st.sidebar:
    st.header("⚙️ Settings")
    api_key = st.text_input(
        "🔑 Gemini API Key",
        type="password",
        placeholder="Paste your Gemini API key here"
    )
    st.markdown("---")
    st.markdown("**Get a FREE API key:**")
    st.markdown("1. Go to [aistudio.google.com](https://aistudio.google.com)")
    st.markdown("2. Sign in with Google")
    st.markdown("3. Click **Get API key** → **Create API key**")
    st.markdown("4. Copy and paste it above")
    st.markdown("---")
    st.markdown("**How to use this app:**")
    st.markdown("1. Enter API key above")
    st.markdown("2. Upload PDF or paste text (left)")
    st.markdown("3. Click **Generate Summary** (left)")
    st.markdown("4. Select scenarios (right)")
    st.markdown("5. Click **Generate Drafts** (right)")


# ── HELPER: Extract text from PDF ────────────────────────────────────────────
def extract_pdf_text(uploaded_file):
    reader = PyPDF2.PdfReader(io.BytesIO(uploaded_file.read()))
    text = ""
    for page in reader.pages:
        extracted = page.extract_text()
        if extracted:
            text += extracted
    return text.strip()


# ── HELPER: Call Gemini API ───────────────────────────────────────────────────
def call_gemini(prompt, api_key):
    genai.configure(api_key=api_key)
    # Try models in order until one works
    models_to_try = [
        "gemini-2.0-flash",
        "gemini-2.0-flash-lite",
        "gemini-2.5-flash",
        "gemini-flash-latest",
    ]
    last_error = None
    for model_name in models_to_try:
        try:
            model = genai.GenerativeModel(model_name)
            response = model.generate_content(prompt)
            return response.text
        except Exception as e:
            last_error = e
            continue
    raise Exception(f"All models failed. Last error: {last_error}")


# ── SCENARIOS ─────────────────────────────────────────────────────────────────
SCENARIOS = {
    "🎓 Scenario 1 – Youth & Education":
        "Adapt this policy specifically for youth aged 15 to 25 and the education sector. "
        "Prioritise AI clubs in schools, university AI degree programmes, "
        "apprenticeships for young engineers, and digital literacy in schools.",

    "🏥 Scenario 2 – Healthcare & Public Services":
        "Adapt this policy for the healthcare sector and public service delivery. "
        "Emphasise AI-powered diagnostics, hospital workflow efficiency, "
        "patient data governance, and AI-driven e-government services.",

    "🌾 Scenario 3 – Rural Communities & Agriculture":
        "Adapt this policy for rural farming communities with limited digital literacy. "
        "Focus on AI tools for crop yield prediction, weather alerts, "
        "market price access, and mobile or offline-friendly AI solutions.",

    "🏢 Scenario 4 – SMEs & Private Sector Growth":
        "Adapt this policy to stimulate AI adoption among small and medium enterprises (SMEs). "
        "Prioritise affordable AI tools, regulatory sandboxes, "
        "tax incentives for AI investment, and export growth programmes.",

    "🌍 Scenario 5 – Environmental Sustainability & Climate":
        "Adapt this policy through an environmental and climate change lens. "
        "Emphasise green AI infrastructure, renewable energy in data centres, "
        "AI for disaster preparedness, and environmental monitoring systems.",
}


# ── SESSION STATE ─────────────────────────────────────────────────────────────
if "summary" not in st.session_state:
    st.session_state.summary = ""
if "drafts" not in st.session_state:
    st.session_state.drafts = {}
if "policy_text" not in st.session_state:
    st.session_state.policy_text = ""


# ── TWO COLUMN LAYOUT ─────────────────────────────────────────────────────────
left_col, right_col = st.columns(2, gap="large")


# ════════════════════════════════════════════════════════════════════════════
# LEFT PANEL — INPUT & SUMMARISE
# ════════════════════════════════════════════════════════════════════════════
with left_col:

    st.markdown('<div class="panel-header">📄 Step 1 — Input Your Policy Document</div>', unsafe_allow_html=True)

    input_method = st.radio(
        "Choose how to input the policy:",
        ["📁 Upload PDF", "📝 Paste Text"],
        horizontal=True
    )

    policy_text = ""

    if input_method == "📁 Upload PDF":
        uploaded_file = st.file_uploader("Upload a PDF file", type=["pdf"])
        if uploaded_file is not None:
            with st.spinner("Reading PDF..."):
                policy_text = extract_pdf_text(uploaded_file)
            if policy_text:
                st.success(f"✅ Successfully extracted {len(policy_text):,} characters from PDF")
                with st.expander("👁️ Preview extracted text"):
                    st.write(policy_text[:1000] + "..." if len(policy_text) > 1000 else policy_text)
            else:
                st.error("❌ Could not extract text from this PDF. Try pasting the text instead.")
    else:
        policy_text = st.text_area(
            "Paste the full policy text here:",
            height=250,
            placeholder="Paste your policy document text here..."
        )

    st.markdown("---")
    st.markdown('<div class="panel-header">🔍 Step 2 — Generate Summary</div>', unsafe_allow_html=True)

    summarise_btn = st.button("✨ Generate Summary", use_container_width=True, type="primary")

    if summarise_btn:
        if not api_key:
            st.error("❌ Please enter your Gemini API key in the left sidebar first.")
        elif not policy_text.strip():
            st.error("❌ Please upload a PDF or paste some policy text above.")
        else:
            summary_prompt = (
                "You are an expert policy analyst. "
                "Carefully read the policy document below and produce a clear, structured summary.\n\n"
                "Your summary MUST have exactly these three sections:\n\n"
                "## Main Goals\n"
                "List 3 to 5 bullet points explaining what this policy is trying to achieve.\n\n"
                "## Key Measures and Strategies\n"
                "List 4 to 6 bullet points describing the specific actions and initiatives proposed.\n\n"
                "## Overall Direction\n"
                "Write one paragraph describing the big-picture vision and approach of this policy.\n\n"
                "Write in clear professional language. Use bullet points for the first two sections.\n\n"
                "--- POLICY DOCUMENT ---\n"
                + policy_text[:12000]
                + "\n--- END OF DOCUMENT ---"
            )
            with st.spinner("Analysing policy with Gemini AI... please wait..."):
                try:
                    st.session_state.summary = call_gemini(summary_prompt, api_key)
                    st.session_state.drafts = {}  # Reset drafts when new summary is made
                    st.success("✅ Summary generated successfully!")
                except Exception as e:
                    st.error(f"❌ Gemini API Error: {e}")

    # Display summary
    if st.session_state.summary:
        st.markdown('<div class="summary-box">', unsafe_allow_html=True)
        st.markdown(st.session_state.summary)
        st.markdown('</div>', unsafe_allow_html=True)
        st.download_button(
            label="⬇️ Download Summary as .txt",
            data=st.session_state.summary,
            file_name="policy_summary.txt",
            mime="text/plain"
        )


# ════════════════════════════════════════════════════════════════════════════
# RIGHT PANEL — SCENARIO GENERATION
# ════════════════════════════════════════════════════════════════════════════
with right_col:

    st.markdown('<div class="panel-header">🎭 Step 3 — Generate Scenario-Based Policy Drafts</div>', unsafe_allow_html=True)

    if not st.session_state.summary:
        st.info("👈 Complete Steps 1 and 2 on the left panel first, then come back here to generate scenario-based drafts.")
    else:
        st.success("✅ Summary is ready! Select your scenarios below and generate drafts.")

        st.markdown("**Select one or more scenarios:**")
        selected_scenarios = st.multiselect(
            "Choose scenarios (select multiple for comparison):",
            options=list(SCENARIOS.keys()),
            default=list(SCENARIOS.keys())[:2],
            help="Each scenario produces a unique policy draft tailored to that context."
        )

        st.markdown("*Each draft will be different — adapted to its specific scenario context.*")

        generate_btn = st.button("🚀 Generate Policy Drafts", use_container_width=True, type="primary")

        if generate_btn:
            if not selected_scenarios:
                st.warning("⚠️ Please select at least one scenario from the list above.")
            else:
                progress_bar = st.progress(0, text="Starting generation...")
                for i, scenario_name in enumerate(selected_scenarios):
                    progress_bar.progress(
                        (i) / len(selected_scenarios),
                        text=f"Generating: {scenario_name}..."
                    )
                    scenario_focus = SCENARIOS[scenario_name]
                    draft_prompt = (
                        "You are a senior government policy advisor with expertise in national AI strategy.\n\n"
                        "Using ONLY the policy summary provided below, write a formal adapted policy draft "
                        "for the specific scenario described.\n\n"
                        f"SCENARIO NAME: {scenario_name}\n"
                        f"SCENARIO FOCUS: {scenario_focus}\n\n"
                        "Your adapted policy draft MUST include ALL of these sections:\n\n"
                        "## [Write a specific title for this scenario-based policy]\n\n"
                        "### Background and Rationale\n"
                        "Write 2 to 3 sentences explaining why this adapted policy is needed.\n\n"
                        "### Vision and Objectives\n"
                        "List 3 to 4 bullet points describing what this adapted policy aims to achieve.\n\n"
                        "### Key Strategic Initiatives\n"
                        "List 4 to 5 bullet points, each with a bold initiative name and a brief description.\n\n"
                        "### Governance and Implementation\n"
                        "Write 2 to 3 sentences on how this policy will be governed and implemented.\n\n"
                        "### Expected Outcomes\n"
                        "List 3 to 4 bullet points describing the expected results by 2028.\n\n"
                        "IMPORTANT RULES:\n"
                        "- Write in formal government policy language\n"
                        "- Make the content SPECIFIC to the scenario — not generic\n"
                        "- This draft must clearly DIFFER from drafts for other scenarios\n"
                        "- Target length: approximately 400 to 500 words\n\n"
                        "--- POLICY SUMMARY ---\n"
                        + st.session_state.summary
                        + "\n--- END OF SUMMARY ---"
                    )
                    try:
                        draft = call_gemini(draft_prompt, api_key)
                        st.session_state.drafts[scenario_name] = draft
                    except Exception as e:
                        st.session_state.drafts[scenario_name] = f"❌ Error generating this draft: {e}"

                progress_bar.progress(1.0, text="All drafts generated!")
                st.success(f"✅ {len(selected_scenarios)} policy draft(s) generated successfully!")

        # ── DISPLAY DRAFTS ────────────────────────────────────────────────────
        if st.session_state.drafts:
            st.markdown("---")
            st.markdown("### 📑 Your Generated Policy Drafts")
            st.markdown(f"*{len(st.session_state.drafts)} draft(s) generated — each tailored to its scenario*")

            for scenario_name, draft_text in st.session_state.drafts.items():
                with st.expander(f"📌 {scenario_name}", expanded=True):
                    st.markdown('<div class="draft-box">', unsafe_allow_html=True)
                    st.markdown(draft_text)
                    st.markdown('</div>', unsafe_allow_html=True)
                    st.download_button(
                        label=f"⬇️ Download this draft",
                        data=draft_text,
                        file_name=f"policy_draft_{scenario_name[:30].replace(' ', '_').replace('–','')}.txt",
                        mime="text/plain",
                        key=f"download_{scenario_name}"
                    )

# ── FOOTER ────────────────────────────────────────────────────────────────────
st.markdown("---")
st.markdown(
    "<div style='text-align:center; color:#95a5a6; font-size:0.85rem;'>"
    "📋 Policy Summariser & Scenario Generator | Powered by Google Gemini AI | Built with Streamlit"
    "</div>",
    unsafe_allow_html=True
)
