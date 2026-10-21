# smart-learning-navigator
# 🚀 SkillVerse AI – Smart Learning Pathway Navigator

### AI-Powered Personalized Learning and Career Guidance Platform

SkillVerse AI is a smart web application that helps students explore career opportunities, identify skill gaps, and follow personalized learning pathways based on their career goals.

## 🎯 Problem Statement

Students often struggle to choose the right career, identify required skills, and find suitable learning resources. SkillVerse AI connects career planning, skill analysis, and personalized learning in one platform.

## ✨ Key Features

- 🎯 **Career Selection** – Choose a preferred career based on personal interests.
- 📊 **Skill Gap Analysis** – Compare current skills with career requirements.
- 🗺️ **Personalized Learning Path** – Generate a structured learning roadmap.
- 📚 **Course Recommendations** – Discover relevant courses and learning resources.
- 💻 **Project Suggestions** – Practise skills through hands-on projects.
- 📈 **Progress Tracking** – Monitor completed topics and learning milestones.
- 📝 **Adaptive Assessment** – Evaluate knowledge through skill-based quizzes.
- 🌌 **Interactive Galaxy UI** – Explore learning topics through an engaging interface.

## 🛠️ Technology Stack

| Technology | Purpose |
|---|---|
| React.js + Vite | Frontend development |
| Tailwind CSS | Styling and responsive design |
| Python FastAPI | Backend API |
| PostgreSQL | Database management |
| Python | Skill analysis and recommendation logic |
| Scikit-learn | Machine learning support, if implemented |
| Recharts | Progress charts and analytics |
| REST API | Frontend–backend communication |

## 🏗️ System Architecture

Student → React Frontend → FastAPI Backend → Recommendation Engine → PostgreSQL Database → Dashboard

## 🗄️ Database Design

Main database entities:

- **Users** – Student account information
- **Skills** – Skill names and categories
- **User_Skills** – Student skills and proficiency levels
- **Career_Roles** – Careers and required competencies
- **Courses** – Course information and resource links
- **Learning_Paths** – Personalized learning roadmaps
- **Progress** – Learning completion and milestones

## ⚙️ Installation and Setup

### 1. Clone the repository

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
cd smart-learning-pathway-navigator
```

### 2. Frontend setup

```bash
cd frontend
npm install
npm run dev
```

### 3. Backend setup

Open a new terminal:

```bash
cd backend
python -m venv venv
```

Activate the environment on Windows:

```bash
venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Start FastAPI:

```bash
uvicorn main:app --reload
```

API documentation: `http://127.0.0.1:8000/docs`

### 4. Database setup

Configure the PostgreSQL connection using your local environment variables and existing database configuration. Ensure PostgreSQL is running before starting database-dependent features.

## 🔮 Future Scope

- AI chatbot for learning assistance
- Resume analysis and career readiness evaluation
- Internship and job recommendations
- Integration with external learning platforms
- Adaptive learning pathways
- Gamification with points, badges, and achievements

## 🎓 Project Objective

To help students make informed career decisions by combining skill gap analysis, personalized learning, practical projects, and progress monitoring in a single platform.

## 👩‍💻 Project Status

Academic project under development.

## 📄 License

Choose an appropriate open-source license before distributing this project publicly.
