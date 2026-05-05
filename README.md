# 📋 Policy Summariser & Scenario Generator

A Streamlit web application that uses Google Gemini AI to summarise policy documents and generate tailored scenario-based policy drafts.

---

## ✨ Features

- **PDF & Text Input** — Upload a PDF or paste raw text directly
- **AI-Powered Summarisation** — Extracts main goals, key measures, and overall direction from any policy document
- **Scenario-Based Draft Generation** — Generates up to 5 unique adapted policy drafts, each tailored to a specific sector or context
- **Download Options** — Export the summary and each draft as `.txt` files
- **Multi-Scenario Comparison** — Select multiple scenarios to generate and compare drafts side by side

---

## 🎭 Available Scenarios

| Scenario | Focus Area |
|---|---|
| 🎓 Youth & Education | AI clubs, university programmes, digital literacy |
| 🏥 Healthcare & Public Services | Diagnostics, e-government, patient data governance |
| 🌾 Rural Communities & Agriculture | Crop prediction, mobile AI, market access |
| 🏢 SMEs & Private Sector Growth | Affordable tools, tax incentives, regulatory sandboxes |
| 🌍 Environmental Sustainability & Climate | Green AI, disaster preparedness, environmental monitoring |

---

## 🚀 Getting Started

### Prerequisites

- Python 3.8 or higher
- A free Google Gemini API key

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/your-username/policy-summariser.git
   cd policy-summariser
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the app**
   ```bash
   streamlit run app.py
   ```

4. **Open in browser**
   The app will open automatically at `http://localhost:8501`

---

## 🔑 Getting a Gemini API Key

1. Go to [aistudio.google.com](https://aistudio.google.com)
2. Sign in with your Google account
3. Click **Get API key** → **Create API key**
4. Copy the key and paste it into the app's sidebar

> The free tier is sufficient for typical usage.

---

## 📦 Dependencies

```
streamlit
google-generativeai
PyPDF2
```

Install all at once:
```bash
pip install streamlit google-generativeai PyPDF2
```

---

## 🖥️ How to Use

1. **Enter your Gemini API key** in the sidebar
2. **Input your policy** — upload a PDF or paste the text in the left panel
3. **Click "Generate Summary"** to get a structured 3-section summary
4. **Select scenarios** in the right panel (one or more)
5. **Click "Generate Policy Drafts"** to produce tailored drafts
6. **Download** any summary or draft as a `.txt` file

---

## 🤖 AI Models Used

The app automatically tries the following Gemini models in order, falling back if one is unavailable:

- `gemini-2.0-flash`
- `gemini-2.0-flash-lite`
- `gemini-2.5-flash`
- `gemini-flash-latest`

---

## 📁 Project Structure

```
policy-summariser/
│
├── app.py              # Main Streamlit application
├── requirements.txt    # Python dependencies
└── README.md           # This file
```

---

## ⚠️ Limitations

- PDF text extraction may not work on scanned or image-based PDFs
- Only the first 12,000 characters of a policy document are sent to the API
- API key is entered at runtime and is not stored

---

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

---

<div align="center">
  Built with ❤️ using <a href="https://streamlit.io">Streamlit</a> and <a href="https://aistudio.google.com">Google Gemini AI</a>
</div>
