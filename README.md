# 🌌 SkillVerse AI — Smart Learning Pathway Navigator

SkillVerse AI is a full-stack, hackathon-ready intelligent educational platform that guides students across their technical journey. It diagnoses competencies across 6 core pillars (**Python, Java, SQL, Data Analytics, Web Development, and Machine Learning**), detects granular knowledge gaps, and uses an explainable **scikit-learn** recommendation engine to synthesize custom learning pathways with an interactive planetary galaxy visualization, daily missions, curated resources, and progress analytics.

---

## 🚀 Key Functional Modules

1. **Galaxy UI & Design**:
   - Deep cosmic dark mode with animated starfield canvas, glowing celestial bodies, and glassmorphism cards.
   - Designed with accessible contrast, modern typography (Outfit & Inter), and micro-animations.
2. **Student Authentication**:
   - Registration, Login, and JWT Bearer authorization.
   - Secure password hashing with `bcrypt` (never stored in plaintext).
   - **1-Click Hackathon Demo Student Access** (`demo@skillverse.ai` / `Password123!`).
3. **Student Profile**:
   - Tracks education level, engineering branch, career target (Full-Stack, AI/ML, Data Science, Cloud Backend), preferred learning style, daily study commitment hours, and target completion dates.
4. **Skill Assessment**:
   - 30+ interactive diagnostic questions covering syntax, data structures, multi-table JOINs, asynchronous execution, and model evaluation metrics.
   - Automatic domain scoring, mastery level assignment, and granular knowledge gap identification.
5. **AI Learning Pathway Generator**:
   - Genuine, explainable Python recommendation engine.
   - Rule-based prerequisite topological sort combined with **scikit-learn `NearestNeighbors` and TF-IDF `cosine_similarity`** to rank resources and tailor stage durations.
   - Interactive stage completion tracking with celebratory confetti.
6. **Interactive Skill Galaxy**:
   - Skills rendered as orbiting planets around a central Career Goal Sun.
   - **Planet Diameter**: Reflects student proficiency score (38px to 76px).
   - **Planet Color & Aura**: Cyan for mastered, violet for in-progress, red/amber pulsing alert for knowledge gaps.
   - **Orbital Links**: Shows prerequisite dependencies between skills.
   - **Clickable Planet HUD**: Inspect metrics, prerequisite checklist, and jump straight to corresponding roadmap stages.
7. **Daily Missions & Quests**:
   - Daily activities (code challenges, quizzes, reading tasks) yielding XP rewards.
   - Active streak tracker with fire multiplier animation.
8. **Resource Explorer**:
   - Searchable directory of verified official documentation (Python.org, MDN, PostgreSQL docs, Oracle, Kaggle, Scikit-learn).
   - Filter by skill, category, and difficulty level.
   - PostgreSQL-backed 1-click bookmarking.
9. **Progress Analytics**:
   - **Recharts Radar Chart**: Multi-axis comparison of student score vs. career benchmark archetype.
   - **Recharts Bar Chart**: Weekly study distribution across 7 days.
   - KPI metrics: Total learning hours, completed stages, streak counter, and priority gap remediation pipeline.
10. **Study Mentor (Cosmic AI)**:
    - Chat-style study companion powered by local educational guidance and pattern matching.
    - Zero paid API keys required; optional OpenAI API key support.
    - Fast prompt chips and 1-click suggested actions.

---

## 🛠️ Mandatory Tech Stack

| Layer | Technologies |
|---|---|
| **Frontend** | React 18, Vite, Tailwind CSS, Framer Motion, Recharts, Lucide React, Canvas Confetti |
| **Backend** | Python 3.11, FastAPI, SQLAlchemy 2.0, Alembic, Pydantic v2 |
| **Recommendation Engine** | Python, scikit-learn (`NearestNeighbors`, `TfidfVectorizer`, `cosine_similarity`), NumPy |
| **Database** | PostgreSQL (Docker Compose container) with resilient local SQLite zero-config fallback |
| **Authentication** | JWT (JSON Web Tokens) with `bcrypt` salt & hash encryption |
| **API Architecture** | RESTful API with Pydantic validation, CORS middleware, and complete test suites |

---

## 📁 Project Structure

```
smart learning/
├── docker-compose.yml              # Local PostgreSQL container configuration
├── alembic.ini                     # Alembic database migration config
├── .env.example                    # Environment variables template
├── requirements.txt                # Python backend dependencies
├── package.json                    # Root npm workspace commands
│
├── backend/
│   ├── config.py                   # Pydantic BaseSettings & JWT configuration
│   ├── database.py                 # SQLAlchemy engine, session maker & connection fallback
│   ├── main.py                     # FastAPI application entrypoint & lifespan events
│   ├── test_api.py                 # Automated backend test suite
│   ├── models/                     # SQLAlchemy Models
│   │   ├── user.py                 # Users table
│   │   ├── profile.py              # Student profiles table
│   │   ├── skill.py                # Skills table
│   │   ├── assessment.py           # Assessments, questions, submissions, answers
│   │   ├── pathway.py              # Learning pathways and steps
│   │   ├── resource.py             # Learning resources
│   │   ├── mission.py              # Daily missions
│   │   ├── progress.py             # Student skill progress
│   │   ├── quiz.py                 # Quiz results
│   │   └── bookmark.py             # User resource bookmarks
│   ├── schemas/                    # Pydantic v2 schemas
│   ├── services/
│   │   ├── auth.py                 # Bcrypt password hashing & JWT tokens
│   │   ├── recommender.py          # scikit-learn + rule-based recommendation engine
│   │   ├── mentor.py               # AI study mentor guidance engine
│   │   └── seed.py                 # Rich seed database script
│   ├── routes/                     # FastAPI API routers
│   └── alembic/                    # Database migrations
│
└── frontend/                       # React + Vite application
    ├── package.json
    ├── vite.config.js              # Dev proxy configuration
    ├── tailwind.config.js          # Galaxy color tokens & animation keyframes
    ├── index.html                  # SEO tags & app title
    └── src/
        ├── App.jsx                 # Master layout & tab navigation
        ├── index.css               # Glassmorphism, neon glows & scrollbars
        ├── services/api.js         # API client with token management
        ├── components/
        │   ├── CosmicBackground.jsx # Canvas twinkling starfield
        │   ├── Navbar.jsx          # Futuristic header & mobile subnav
        │   ├── AuthModal.jsx       # Login/Register modal with 1-click Demo Student
        │   └── StudyMentorDrawer.jsx # Cosmic AI chat drawer with prompt chips
        └── pages/
            ├── LandingPage.jsx     # Hero section & galaxy teaser
            ├── GalaxyPage.jsx      # Planetary skill galaxy orbit view
            ├── PathwayPage.jsx     # AI customized learning roadmap
            ├── AssessmentPage.jsx  # Technical diagnostic quiz & gap modal
            ├── MissionsPage.jsx    # Daily quests, streak tracker & XP
            ├── ResourcesPage.jsx   # Curated free tutorials & bookmarks
            ├── AnalyticsPage.jsx   # Recharts radar & bar charts
            └── ProfilePage.jsx     # Student profile & study hours settings
```

---

## ⚡ Quick Start (Windows PowerShell)

### Prerequisites
- Python 3.10+ installed and on PATH
- Node.js v18+ and npm installed

### 1. Database Setup with Docker Compose (PostgreSQL)
To run the local PostgreSQL database using Docker:
```powershell
# Start PostgreSQL container in background
docker compose up -d

# Verify container health
docker compose ps
```
> **Note:** If Docker is not installed on your machine, SkillVerse AI will **automatically fall back to a local SQLite database (`skillverse.db`)** so you can develop and evaluate immediately with zero barriers!

### 2. Backend Setup & Seeding
In your PowerShell terminal:
```powershell
# 1. Install backend dependencies
pip install -r requirements.txt

# 2. Run database migrations
alembic upgrade head

# 3. Seed initial canonical skills, questions, and demo student
python -m backend.services.seed

# 4. Run automated test suite to verify endpoints
python backend/test_api.py

# 5. Start FastAPI backend dev server
python -m uvicorn backend.main:app --host 127.0.0.1 --port 8000 --reload
```
The FastAPI interactive Swagger documentation is available at:
👉 `http://127.0.0.1:8000/docs`

### 3. Frontend Setup
In a second PowerShell window:
```powershell
cd frontend

# 1. Install dependencies
npm install

# 2. Start Vite dev server
npm run dev
```
Open your browser at:
👉 **`http://127.0.0.1:5173/`**

---

## 🧪 Hackathon Demonstration Walkthrough

1. **Landing Page**:
   - Navigate to `http://127.0.0.1:5173/`.
   - Admire the interactive animated cosmic starfield, neon violet and electric blue highlights.
2. **Instant 1-Click Login**:
   - Click the **"Demo Student"** button on the navbar.
   - Instantly logged in as `Alex Mercer (Demo Student)` (`demo@skillverse.ai`).
3. **Interactive Skill Galaxy**:
   - Observe skills orbiting the central **Career Core** (`Full-Stack Web Developer`).
   - Notice the varying planet sizes (reflecting current proficiency) and the red/amber alert beacon on the SQL planet highlighting a knowledge gap.
   - Click on the **SQL** or **Python** planet to open the planetary HUD modal and inspect prerequisites.
4. **AI Learning Pathway**:
   - Click **"AI Pathway"** in the top navigation.
   - Review personalized stages with estimated hours, verified learning resources, and practical tasks.
   - Click **"Complete This Stage"** on any stage to see instant progress updates and celebratory confetti.
5. **Skill Assessment & Gap Detection**:
   - Click **"Diagnostic"** in the navigation.
   - Use the **"Autofill Sample Answers"** button for quick demonstration or answer the interactive multiple-choice questions.
   - Click **"Submit Diagnostic"** to trigger the explainable engine and view the knowledge gaps analysis.
6. **Daily Missions & Streak XP**:
   - Click **"Missions"** to view daily quests and the active streak counter with flame animation.
   - Click **"Claim XP"** to complete an activity and increment the streak.
7. **Progress Analytics**:
   - Click **"Analytics"** to view the **Recharts Radar Chart** comparing the student's current proficiency vs target industry benchmarks, along with the weekly study hours bar chart.
8. **Study Mentor Assistant**:
   - Click **"Ask Mentor"** in the top right navbar.
   - Click the prompt chip **"How do I fix my SQL knowledge gap?"** to see tailored remediation guidance and 1-click navigation links.

---

## 🔒 Security & Data Integrity
- **Password Protection**: Passwords are encrypted using salted `bcrypt` algorithms before saving to the database.
- **Token Security**: Stateless JWTs with HMAC SHA-256 signature verification and expiration handling.
- **Pydantic Validation**: Strict input and output schemas across all REST API endpoints.

---

## 📜 License
MIT License. Created for collegiate and open-source hackathons.
