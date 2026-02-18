# 🤖 Full-Stack AI Chatbot Assistant

Μια σύγχρονη εφαρμογή Chatbot που συνδυάζει **FastAPI** και **React**, χρησιμοποιώντας το **Gemini 1.5 Flash API** της Google. Το project εστιάζει στην καθαρή αρχιτεκτονική και την άμεση εμπειρία χρήστη (UX).

## ✨ Χαρακτηριστικά
- **Real-time AI Responses:** Ενσωμάτωση με το μοντέλο Gemini για φυσική γλώσσα.
- **Conversational Memory:** Το backend διατηρεί το context της συζήτησης.
- **Modern UX:** - Typewriter effect για τις απαντήσεις του bot.
  - Auto-scroll στο τελευταίο μήνυμα.
  - Δυνατότητα καθαρισμού ιστορικού (Memory Reset).
- **Security:** Διαχείριση API Keys μέσω `.env` αρχείων.

## 🛠️ Τεχνικό Stack
- **Backend:** Python 3.10+, FastAPI, Uvicorn, Google GenAI SDK.
- **Frontend:** React.js (Hooks, Functional Components), CSS3 Flexbox.
- **API:** RESTful επικοινωνία με CORS middleware.

## 🚀 Οδηγίες Εγκατάστασης
1. Κλωνοποιήστε το repository.
2. Στο φάκελο `backend/`, δημιουργήστε ένα αρχείο `.env` και προσθέστε:  
   `GEMINI_API_KEY=το_κλειδί_σας`
3. Εγκαταστήστε τις εξαρτήσεις:  
   `pip install -r backend/requirements.txt`
4. Εκκινήστε το backend:  
   `python -m uvicorn main:app --reload`
5. Ανοίξτε το `frontend/index.html` στον browser σας.