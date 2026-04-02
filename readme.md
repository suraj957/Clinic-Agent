# 🏥 AI Clinic Assistant

An intelligent appointment booking system powered by **AutoGen multi-agent framework**, **Azure OpenAI (GPT-4o)**, **FastAPI**, and **Streamlit**. Patients can book clinic appointments through a natural language chat interface — no forms, no phone calls.

---

## 🎥 Demo

> _"Hi, I'm Suraj. Book appointment tomorrow at 6pm"_
> 
> ✅ **"Hi Suraj, your appointment for tomorrow at 6pm has been successfully booked!"**

---

## 🧠 How It Works

The system uses a **multi-agent pipeline** where each agent has a specific role:

```
User Message
     │
     ▼
┌─────────────────┐
│  Receptionist   │  → Extracts name, date, time from natural language
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│   Scheduler     │  → Checks slot availability in the database
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│   Data Agent    │  → Saves appointment & confirms in friendly language
└─────────────────┘
```

---

## 🏗️ Architecture

```
project/
├── app.py               # Streamlit frontend (chat UI)
├── .env                 # Azure OpenAI credentials
└── backend/
    ├── __init__.py
    ├── main.py          # FastAPI server (/book endpoint)
    ├── agents.py        # AutoGen multi-agent setup
    └── tools.py         # SQLite tools (check_availability, save_to_db)
```

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| LLM | Azure OpenAI (GPT-4o) |
| Agent Framework | AutoGen (ag2) |
| Backend API | FastAPI + Uvicorn |
| Frontend | Streamlit |
| Database | SQLite |

---

## ⚙️ Setup & Installation

### 1. Clone the repository

```bash
git clone https://github.com/your-username/ai-clinic-assistant.git
cd ai-clinic-assistant
```

### 2. Install dependencies

```bash
pip install autogen-agentchat streamlit fastapi uvicorn python-dotenv requests openai
```

### 3. Configure environment variables

Create a `.env` file in the project root:

```env
AZURE_OPENAI_API_KEY=your_api_key_here
AZURE_OPENAI_DEPLOYMENT=gpt-4o
AZURE_OPENAI_BASE_URL=https://your-resource-name.openai.azure.com/
AZURE_OPENAI_API_VERSION=2024-08-01-preview
```

> ⚠️ Never commit your `.env` file. Add it to `.gitignore`.

### 4. Run the app

Open **two terminals**:

**Terminal 1 — FastAPI backend:**
```bash
uvicorn backend.main:app --host 127.0.0.1 --port 8001 --reload
```

**Terminal 2 — Streamlit frontend:**
```bash
streamlit run app.py
```

Visit **http://localhost:8501** in your browser.

---

## 💬 Example Usage

| User Message | Bot Response |
|---|---|
| "Hi I'm Priya, book me an appointment on April 5th at 10am" | "Hi Priya, your appointment for April 5th at 10am has been successfully booked!" |
| "I'm John, I need a slot tomorrow at 3pm" | "Hi John, your appointment for tomorrow at 3pm has been successfully booked!" |
| _(slot already taken)_ | "Sorry, that slot is not available. Please choose another time." |

---

## 🗂️ Key Files Explained

### `agents.py`
Sets up three AutoGen `AssistantAgent`s and one `UserProxyAgent` in a `GroupChat`. Each agent has a focused role and tools are registered using AutoGen's `register_function` API with proper type annotations.

### `tools.py`
Two SQLite-backed tools exposed to the agents:
- `check_availability(date: str, time: str) -> bool` — returns `True` if the slot is free
- `save_to_db(name: str, date: str, time: str) -> str` — inserts the appointment and confirms

### `main.py`
A single FastAPI POST endpoint `/book` that accepts a natural language message and returns the agent's response.

### `app.py`
A Streamlit chat interface that maintains conversation history and calls the FastAPI backend.

---

## 🚧 Known Limitations & Future Improvements

- [ ] Dates are stored as strings (e.g. "tomorrow") — add date parsing with `dateparser`
- [ ] No appointment cancellation or rescheduling flow yet
- [ ] No patient authentication
- [ ] Could be extended to support multiple doctors/rooms
- [ ] Add email/SMS confirmation via Twilio or SendGrid

---

## 📄 License

MIT License — feel free to use and build on this project.

---

## 🙋 Author

Built with ❤️ using AutoGen + Azure OpenAI.  
Feel free to connect and share feedback!