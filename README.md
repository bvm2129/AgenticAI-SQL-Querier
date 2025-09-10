# AgenticAI-SQL-Querier 🎓🤖

AgenticAI is a Streamlit-based AI-powered assistant that connects to a SQLite database and answers natural language queries using Google Gemini API.  
It enables seamless interaction with structured data — ask questions, get answers, no SQL knowledge required.

---

## 🚀 Features
- Natural language to SQL query generation (powered by Gemini API).
- Easy-to-use **Streamlit web interface**.
- Integration with **SQLite database**.
- Secure key management via `.env` file.
- Extendable for other databases (PostgreSQL, MySQL, etc.).

---

## 🛠️ Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/YOUR_USERNAME/AgenticAI.git
   cd AgenticAI
   ```

2. Create a virtual environment:

   ```bash
   python -m venv venv
   source venv/Scripts/activate   # On Windows
   ```

3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Add your API key:

   * Create a `.env` file in the project root.
   * Add:

     ```
     GOOGLE_API_KEY=your_api_key_here
     ```

---

## ▶️ Usage

Run the Streamlit app:

```bash
streamlit run app.py
```

Open the link in your browser (usually `http://localhost:8501`).

---

## 📂 Project Structure

```
AgenticAI/
│── app.py              # Main Streamlit application
│── sql.py              # Script to create database & tables
│── student.db          # SQLite database (ignored in repo)
│── requirements.txt    # Project dependencies
│── .env                # API key (ignored in repo)
│── .gitignore          # Ignore sensitive/unnecessary files
│── README.md           # Project documentation
```

---

## 🔒 Security

* Never expose your `.env` or `student.db`.
* Add secrets only in deployment platform (e.g., Streamlit Cloud or GCP).

---

## 🤝 Contributing

Pull requests are welcome!
For major changes, open an issue first to discuss what you’d like to improve.

---
