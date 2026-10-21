import re
from datetime import datetime
from typing import Dict, List, Any, Optional

EDUCATIONAL_KNOWLEDGE_BASE = {
    "sql": {
        "title": "SQL Mastery & Relational Databases",
        "tips": [
            "Always visualize tables and their primary/foreign key connections before writing complex multi-table queries.",
            "Remember: WHERE filters records before aggregation, while HAVING filters grouped results after aggregation.",
            "Use EXPLAIN ANALYZE in PostgreSQL to inspect index scans and prevent expensive sequential scans.",
            "Practice writing queries with window functions (ROW_NUMBER(), RANK(), LEAD(), LAG()) for senior-level analytics."
        ],
        "project": "Design a relational schema for a multi-tenant SaaS billing platform with normalized tables, foreign keys, and indexed queries."
    },
    "python": {
        "title": "Python Architecture & Idiomatic Coding",
        "tips": [
            "Use generators and list comprehensions to write memory-efficient code.",
            "Leverage Python 3.10+ match-case and type hints with Pydantic for bulletproof data contracts.",
            "Use virtual environments (venv or uv) to prevent package dependency collisions.",
            "Familiarize yourself with Python's asyncio for high-concurrency network tasks."
        ],
        "project": "Build an asynchronous web scraper or REST API using FastAPI, SQLAlchemy 2.0, and Pydantic."
    },
    "java": {
        "title": "Enterprise Java & Object-Oriented Design",
        "tips": [
            "Master SOLID design principles and standard GoF design patterns (Factory, Strategy, Observer).",
            "Understand the Java Memory Model: Heap vs Stack, Garbage Collection algorithms, and thread safety.",
            "Use Java Streams and Optional API for concise, null-safe functional programming.",
            "Leverage Spring Boot 3 with Spring Data JPA for enterprise microservices."
        ],
        "project": "Develop a Spring Boot microservice with JWT authentication, Docker containerization, and JUnit 5 test coverage."
    },
    "web_dev": {
        "title": "Modern Full-Stack Web Development",
        "tips": [
            "Focus on clean component separation, state immutability, and responsive CSS grid/flexbox.",
            "Keep UI state local when possible; lift state up or use React context only when multiple sibling trees need it.",
            "Optimize web performance: minimize re-renders, use lazy loading for images/routes, and observe Lighthouse metrics.",
            "Prioritize accessibility (a11y): semantic HTML, ARIA labels, and keyboard navigability."
        ],
        "project": "Create a responsive full-stack dashboard featuring real-time charts, dark mode, and optimistic UI updates."
    },
    "data_analytics": {
        "title": "Data Analytics & Insight Extraction",
        "tips": [
            "Always inspect and clean data first: handle null values, detect anomalies, and verify data types.",
            "Master Pandas vectorized operations (avoid looping over DataFrames with iterrows).",
            "Tell a visual story: choose the right chart type (e.g. histograms for distribution, scatter plots for correlation).",
            "Formulate testable business hypotheses before calculating descriptive statistics."
        ],
        "project": "Analyze an e-commerce customer churn dataset: perform cohort analysis, churn prediction, and build an interactive visual dashboard."
    },
    "ml": {
        "title": "Machine Learning & Applied AI",
        "tips": [
            "Prevent data leakage: always split data into train/test sets before fitting scalers or encoders.",
            "Start with simple interpretable baselines (Logistic Regression, Decision Trees) before jumping to neural nets.",
            "Tune hyperparameters systematically using cross-validation (GridSearchCV or Optuna).",
            "Monitor classification metrics beyond accuracy: inspect Precision, Recall, F1-score, and ROC-AUC."
        ],
        "project": "Train an end-to-end classification pipeline with scikit-learn, evaluate metrics, and expose predictions via a FastAPI endpoint."
    }
}

STUDY_HABITS = [
    "Break study sessions into 25-minute Pomodoro intervals followed by 5-minute active recovery breaks.",
    "Implement active recall: summarize what you just learned without looking at the notes.",
    "Practice spaced repetition: review newly acquired concepts at 1-day, 3-day, and 7-day intervals.",
    "Follow the Feynman Technique: explain a complex technical concept in plain terms as if teaching a beginner."
]

def generate_mentor_guidance(
    user_message: str,
    context_skill: Optional[str] = None,
    user_profile: Optional[Dict[str, Any]] = None,
    gaps: Optional[List[Dict[str, Any]]] = None
) -> Dict[str, Any]:
    """
    Intelligent local study mentor. Provides nuanced educational coaching,
    technical explanations, project recommendations, and study action suggestions.
    """
    msg = user_message.lower()
    
    # Check for specific skill mention
    detected_skill = context_skill
    if not detected_skill:
        if "sql" in msg or "database" in msg or "query" in msg or "join" in msg:
            detected_skill = "sql"
        elif "python" in msg or "fastapi" in msg or "django" in msg:
            detected_skill = "python"
        elif "java" in msg or "spring" in msg or "jvm" in msg:
            detected_skill = "java"
        elif "web" in msg or "react" in msg or "frontend" in msg or "javascript" in msg or "css" in msg:
            detected_skill = "web_dev"
        elif "data" in msg or "pandas" in msg or "analytics" in msg:
            detected_skill = "data_analytics"
        elif "ml" in msg or "machine learning" in msg or "ai" in msg or "model" in msg:
            detected_skill = "ml"

    actions = [
        {"label": "Explore Roadmap", "action_type": "navigate", "target": "/pathway"},
        {"label": "Daily Missions", "action_type": "navigate", "target": "/missions"},
        {"label": "Skill Galaxy", "action_type": "navigate", "target": "/galaxy"}
    ]

    # 1. Project recommendations
    if "project" in msg or "portfolio" in msg or "build" in msg:
        skill = detected_skill or "python"
        info = EDUCATIONAL_KNOWLEDGE_BASE.get(skill, EDUCATIONAL_KNOWLEDGE_BASE["python"])
        reply = (
            f"### 🚀 Recommended Hands-on Project for {info['title']}\n\n"
            f"**Project Concept:** {info['project']}\n\n"
            f"**Architecture Highlights:**\n"
            f"- Separate concerns cleanly into data ingestion, business logic, and presentation.\n"
            f"- Implement unit tests and automated linting.\n"
            f"- Document your setup and design decisions in a polished GitHub README.\n\n"
            f"💡 **Mentor Pro-Tip:** Employers love seeing projects deployed with live demo URLs and containerized Docker environments!"
        )
        return {"reply": reply, "suggested_actions": actions, "generated_at": datetime.utcnow()}

    # 2. Knowledge Gap Help
    if "gap" in msg or "weakness" in msg or "improve" in msg or "struggl" in msg:
        gap_summary = ""
        if gaps:
            gap_summary = "\n".join([f"- **{g.get('skill_code', '').title()}**: {g.get('topic', '')} ({g.get('recommendation', '')})" for g in gaps[:3]])
        else:
            gap_summary = "- Identified gaps in complex queries and optimization."

        reply = (
            f"### 🎯 Targeted Remediation Strategy\n\n"
            f"Here is your focused blueprint to turn knowledge gaps into strengths:\n\n"
            f"{gap_summary}\n\n"
            f"**Recommended 3-Step Routine:**\n"
            f"1. **Conceptual Refresh (20 mins):** Consult official documentation or an interactive guide in Resource Explorer.\n"
            f"2. **Isolated Practice (30 mins):** Solve 2-3 focused coding problems addressing the exact missed topic.\n"
            f"3. **Verification Quiz:** Retake the checkpoint diagnostic to validate retention."
        )
        actions.insert(0, {"label": "Take Diagnostic", "action_type": "navigate", "target": "/assessment"})
        actions.insert(1, {"label": "Resource Explorer", "action_type": "navigate", "target": "/resources"})
        return {"reply": reply, "suggested_actions": actions, "generated_at": datetime.utcnow()}

    # 3. Study Plan / Schedule
    if "schedule" in msg or "plan" in msg or "routine" in msg or "hours" in msg or "today" in msg:
        reply = (
            f"### ⏱️ Optimal Daily Learning Rhythm\n\n"
            f"Consistency beats intensity every single time. Here is your structured daily cadence:\n\n"
            f"1. **Warmup (10 mins):** Review yesterday's notes or complete one Daily Mission.\n"
            f"2. **Deep Work Block (45-60 mins):** Work through your active Learning Pathway stage without distractions.\n"
            f"3. **Hands-on Application (30 mins):** Write actual code or build a mini-feature.\n"
            f"4. **Reflection (5 mins):** Log what you learned and mark your progress in SkillVerse.\n\n"
            f"🧠 **Study Habit Recommendation:** {STUDY_HABITS[0]}"
        )
        return {"reply": reply, "suggested_actions": actions, "generated_at": datetime.utcnow()}

    # 4. Specific Technical Topic
    if detected_skill:
        info = EDUCATIONAL_KNOWLEDGE_BASE.get(detected_skill)
        tips_list = "\n".join([f"- {t}" for t in info["tips"]])
        reply = (
            f"### 🌌 Study Guidance: {info['title']}\n\n"
            f"Here are key architectural guidelines and best practices:\n\n"
            f"{tips_list}\n\n"
            f"**Next Step:** Head over to your Interactive Skill Galaxy to see how {info['title']} connects to your broader career trajectory!"
        )
        return {"reply": reply, "suggested_actions": actions, "generated_at": datetime.utcnow()}

    # 5. Default encouraging response
    reply = (
        f"### 🌟 Welcome to SkillVerse AI Study Mentor!\n\n"
        f"I am your dedicated academic advisor and career coach. I can help you:\n\n"
        f"- **Diagnose & close knowledge gaps** across Python, Java, SQL, Data Analytics, Web Dev, and ML.\n"
        f"- **Recommend customized project ideas** that elevate your technical portfolio.\n"
        f"- **Structure daily study routines** tailored to your available hours.\n"
        f"- **Prepare for technical assessments and coding interviews**.\n\n"
        f"What topic, skill, or career goal would you like to explore today?"
    )
    return {"reply": reply, "suggested_actions": actions, "generated_at": datetime.utcnow()}
