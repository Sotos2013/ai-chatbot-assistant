# AI Chatbot Assistant (Full-Stack Implementation)

Μια ολοκληρωμένη εφαρμογή Chatbot που βασίζεται σε αρχιτεκτονική **client-server**, με δυνατότητα διατήρησης ιστορικού συζητήσεων (**Persistence**). Η εφαρμογή αξιοποιεί σύγχρονες τεχνολογίες cloud για το deployment και τη διαχείριση δεδομένων.

## 🏛️ Αρχιτεκτονική Συστήματος
Το σύστημα αποτελείται από τρία βασικά επίπεδα:

1.  **Frontend (Presentation Layer):** Ανεπτυγμένο σε **React.js**, φιλοξενείται στο **GitHub Pages**. Παρέχει ένα responsive περιβάλλον εργασίας με έμφαση στο UX/UI και το Glassmorphism design.
2.  **Backend (Logic Layer):** REST API ανεπτυγμένο με **FastAPI (Python)**, το οποίο εκτελείται σε περιβάλλον **Docker** μέσω του **Hugging Face Spaces**. Διαχειρίζεται την επικοινωνία με τα LLMs και τη βάση δεδομένων.
3.  **Database (Data Layer):** Σχεσιακή βάση δεδομένων **PostgreSQL** (μέσω της πλατφόρμας **Supabase**) για την ασφαλή αποθήκευση και ανάκτηση του ιστορικού των συζητήσεων.



## 🛠️ Τεχνικό Stack
* **Γλώσσα Προγραμματισμού:** Python 3.10+
* **Web Framework:** FastAPI / Uvicorn
* **Frontend Library:** React.js (Hooks & Functional Components)
* **Βάση Δεδομένων:** PostgreSQL (Supabase)
* **AI Integration:** Hugging Face Inference API (OpenAI-compatible SDK)
* **Containerization:** Docker

## 🚀 Δυνατότητες
* **Conversational Persistence:** Διατήρηση του context της συζήτησης μεταξύ διαφορετικών sessions μέσω της βάσης δεδομένων.
* **Asynchronous Processing:** Χρήση ασύγχρονων κλήσεων (async/await) για βελτιστοποιημένη ταχύτητα απόκρισης.
* **Secure Integration:** Διαχείριση ευαίσθητων δεδομένων (API Keys, Database URIs) μέσω κρυπτογραφημένων περιβαλλόντων (Secrets).
* **Stateful UI:** Αυτόματη φόρτωση ιστορικού κατά την εκκίνηση της εφαρμογής.

## 🔌 API Endpoints
Το Backend εκθέτει τα εξής σημεία επαφής:

| Endpoint | Method | Περιγραφή |
| :--- | :--- | :--- |
| `/` | `GET` | Επιστρέφει το status του server και το ιστορικό μηνυμάτων. |
| `/api/chat` | `POST` | Δέχεται το μήνυμα του χρήστη και επιστρέφει την απάντηση της AI. |
| `/api/clear` | `POST` | Διαγράφει οριστικά το ιστορικό από τη βάση δεδομένων. |

## 📦 Deployment & CI/CD

Η αρχιτεκτονική της εφαρμογής βασίζεται σε πλήρως αυτοματοποιημένες διαδικασίες deployment (CI/CD) για τη διασφάλιση της συνεχούς διαθεσιμότητας.

### Backend (Hugging Face Spaces)
* **Containerization:** Η εφαρμογή είναι "Dockerized", χρησιμοποιώντας ένα ελαφρύ είδωλο βασισμένο στην Python 3.10.
* **Continuous Deployment:** Κάθε αλλαγή στον κώδικα (Push) στο repository του Space πυροδοτεί αυτόματα το build του Docker image και το deployment του νέου container.
* **Infrastructure:** Φιλοξενείται σε Managed Infrastructure, αξιοποιώντας τα secrets του Hugging Face για την ασφαλή διατήρηση των API Keys και των Database Credentials.

### Frontend (GitHub Pages)
* **Static Hosting:** Το περιβάλλον χρήστη (UI) σερβίρεται ως στατικό περιεχόμενο απευθείας από τους servers του GitHub, εξασφαλίζοντας υψηλή ταχύτητα φόρτωσης και μηδενικό downtime.
* **API Integration:** Η επικοινωνία με το backend πραγματοποιείται μέσω ασφαλών HTTPS requests στο production endpoint του Hugging Face Space.



### Secrets Management
Για την ορθή λειτουργία σε περιβάλλον παραγωγής, έχουν οριστεί οι παρακάτω περιβαλλοντικές μεταβλητές:
* `HF_TOKEN`: Για την πρόσβαση στο Inference API.
* `SUPABASE_URL`: Το endpoint της βάσης δεδομένων.
* `SUPABASE_KEY`: Το anon/public key για την επικοινωνία με τη Supabase.