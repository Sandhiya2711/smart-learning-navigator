from datetime import datetime
from typing import Dict, List, Any, Optional
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from backend.services.recommender import CANONICAL_SKILLS, PREREQUISITES_MAP

# ----------------------------------------------------
# 1. PARALLEL UNIVERSE LEARNING SIMULATOR
# ----------------------------------------------------
PARALLEL_ROUTES_CATALOG = {
    "Full-Stack Web Developer": [
        {
            "universe_id": "alpha_python_first",
            "name": "Universe Alpha: Python & API First",
            "tagline": "Back-of-the-Napkin to Production API",
            "sequence": ["python", "sql", "web_dev"],
            "difficulty_curve": "Moderate Start, Smooth Scaling",
            "focus": "Backend Architecture, Data Modeling, then React Frontend Integration",
            "estimated_weeks": 12,
            "weights": np.array([0.9, 0.2, 0.8, 0.4, 0.9, 0.2]),
            "pros": ["Faster grasp of backend logic and clean OOP", "Seamless database migrations with ORM"],
            "cons": ["Frontend visual components introduced later in Stage 3"]
        },
        {
            "universe_id": "beta_web_first",
            "name": "Universe Beta: Frontend Visual First",
            "tagline": "Pixel-Perfect UI to Database Core",
            "sequence": ["web_dev", "sql", "python"],
            "difficulty_curve": "Immediate Visual Gratification, Steeper Backend Transition",
            "focus": "React State Management, UI/UX Components, then SQL & Python Backends",
            "estimated_weeks": 13,
            "weights": np.array([0.7, 0.2, 0.8, 0.3, 0.95, 0.2]),
            "pros": ["Immediate deployable frontend prototypes", "Higher initial visual feedback"],
            "cons": ["Requires mock APIs before backend integration is learned"]
        }
    ],
    "Data Scientist & Analyst": [
        {
            "universe_id": "alpha_sql_first",
            "name": "Universe Alpha: SQL & Query Architecture",
            "tagline": "Relational Data Heavyweights",
            "sequence": ["sql", "data_analytics", "python", "ml"],
            "difficulty_curve": "Low Friction Start, High Industry Demand",
            "focus": "Data Aggregations, Window Functions, then Pandas and Scikit-Learn",
            "estimated_weeks": 14,
            "weights": np.array([0.8, 0.1, 0.95, 0.9, 0.2, 0.7]),
            "pros": ["Immediate mastery of enterprise database querying", "Matches 90% of business analyst job listings"],
            "cons": ["Algorithmic scripting introduced after SQL data fundamentals"]
        },
        {
            "universe_id": "beta_python_first",
            "name": "Universe Beta: Python Algorithmic Science",
            "tagline": "Matrix Computation & Machine Learning",
            "sequence": ["python", "data_analytics", "sql", "ml"],
            "difficulty_curve": "Linear Algorithmic Progression",
            "focus": "NumPy Vectorization, Pandas DataFrames, followed by SQL and Scikit-learn",
            "estimated_weeks": 15,
            "weights": np.array([0.9, 0.1, 0.8, 0.95, 0.2, 0.85]),
            "pros": ["Strong foundation in computational programming", "Faster transition into Machine Learning"],
            "cons": ["Database joins deferred until after exploratory analytics"]
        }
    ],
    "AI/ML Engineer": [
        {
            "universe_id": "alpha_ml_engineering",
            "name": "Universe Alpha: Production ML & Pipelines",
            "tagline": "From Scikit-Learn to Deployed REST Inference",
            "sequence": ["python", "sql", "data_analytics", "ml"],
            "difficulty_curve": "Continuous High-Yield Engineering",
            "focus": "FastAPI REST API, Database Storage, Data Pipelines, and Model Deployment",
            "estimated_weeks": 16,
            "weights": np.array([0.9, 0.2, 0.75, 0.85, 0.3, 0.95]),
            "pros": ["Builds portfolio-ready deployed AI endpoints", "End-to-end data ingestion to inference"],
            "cons": ["Demands disciplined weekly consistency"]
        },
        {
            "universe_id": "beta_data_centric",
            "name": "Universe Beta: Data-Centric AI",
            "tagline": "Feature Engineering & Anomaly Detection",
            "sequence": ["python", "data_analytics", "sql", "ml"],
            "difficulty_curve": "Exploratory & Statistical Immersion",
            "focus": "Statistical Distributions, Missing Data Imputation, Model Evaluation Metrics",
            "estimated_weeks": 15,
            "weights": np.array([0.85, 0.1, 0.85, 0.95, 0.2, 0.9]),
            "pros": ["Eliminates common machine learning pitfalls like data leakage", "Strong metrics evaluation skills"],
            "cons": ["API serving learned in final phase"]
        }
    ]
}

def simulate_parallel_universes(career_goal: str, student_scores: Dict[str, float]) -> List[Dict[str, Any]]:
    # Match candidate universes
    routes = PARALLEL_ROUTES_CATALOG.get(career_goal)
    if not routes:
        # Default to Full-Stack Web Developer routes
        routes = PARALLEL_ROUTES_CATALOG["Full-Stack Web Developer"]

    # Student vector [python, java, sql, data_analytics, web_dev, ml]
    student_vec = np.array([student_scores.get(s, 0.0) / 100.0 for s in CANONICAL_SKILLS]).reshape(1, -1)

    evaluated_routes = []
    for r in routes:
        route_vec = r["weights"].reshape(1, -1)
        sim = float(cosine_similarity(student_vec, route_vec)[0][0])
        match_percentage = round(max(30.0, sim * 100.0), 1)

        # Check prerequisite friction
        friction = "Low" if match_percentage >= 65 else ("Moderate" if match_percentage >= 45 else "Steep")

        evaluated_routes.append({
            "universe_id": r["universe_id"],
            "name": r["name"],
            "tagline": r["tagline"],
            "sequence": r["sequence"],
            "difficulty_curve": r["difficulty_curve"],
            "focus": r["focus"],
            "estimated_weeks": r["estimated_weeks"],
            "match_score": match_percentage,
            "cognitive_friction": friction,
            "pros": r["pros"],
            "cons": r["cons"],
            "is_recommended": False
        })

    # Mark highest match score as recommended
    if evaluated_routes:
        best_route = max(evaluated_routes, key=lambda x: x["match_score"])
        best_route["is_recommended"] = True

    return evaluated_routes


# ----------------------------------------------------
# 2. MISTAKE DNA: REPEATED ERROR GENOME ANALYZER
# ----------------------------------------------------
MISTAKE_GENOME_DATABASE = [
    {
        "dna_id": "dna_sql_having_filter",
        "skill_code": "sql",
        "title": "WHERE vs HAVING Misconception",
        "pattern": "Attempting to filter aggregated functions (e.g. COUNT(*)) inside WHERE clauses",
        "root_misunderstanding": "Misunderstanding the SQL logical query processing order. WHERE executes *before* GROUP BY row aggregation, while HAVING executes *after* grouping.",
        "frequency_score": "High (Occurred in 3 attempts)",
        "diagnostic_trigger": "Aggregation & Filtering Conditions",
        "targeted_challenge": {
            "title": "Fix the E-Commerce High-Value Customer Query",
            "scenario": "Select customer_id and total order sum for customers who spent more than $500.",
            "code_snippet": "-- ❌ BROKEN QUERY:\nSELECT customer_id, SUM(price) \nFROM orders \nWHERE SUM(price) > 500 \nGROUP BY customer_id;\n\n-- ✅ CORRECT QUERY:\nSELECT customer_id, SUM(price) \nFROM orders \nGROUP BY customer_id \nHAVING SUM(price) > 500;",
            "key_takeaway": "WHERE operates on individual rows; HAVING operates on aggregated buckets."
        }
    },
    {
        "dna_id": "dna_python_mutable_defaults",
        "skill_code": "python",
        "title": "Mutable Default Arguments Mutation",
        "pattern": "Using `def append_to(item, target_list=[])` leading to unexpected state leakage across calls",
        "root_misunderstanding": "Python function default arguments are evaluated only once at definition time, not every time the function is invoked.",
        "frequency_score": "Medium (Occurred in 2 attempts)",
        "diagnostic_trigger": "Variable Scope & Closures",
        "targeted_challenge": {
            "title": "Safe Sentinel Default Pattern",
            "scenario": "Ensure each function call receives an isolated new list when no argument is supplied.",
            "code_snippet": "# ❌ DANGEROUS MUTABLE DEFAULT:\ndef add_item(val, items=[]):\n    items.append(val)\n    return items\n\n# ✅ SAFE SENTINEL IDIOM:\ndef add_item(val, items=None):\n    if items is None:\n        items = []\n    items.append(val)\n    return items",
            "key_takeaway": "Always use None as default sentinel for mutable containers (lists, dicts, sets)."
        }
    },
    {
        "dna_id": "dna_web_direct_state_mutation",
        "skill_code": "web_dev",
        "title": "Direct React State Mutation",
        "pattern": "Writing `user.profile.name = 'New'` instead of functional setter updates",
        "root_misunderstanding": "React relies on shallow object reference inequality (`prev !== next`) to trigger Virtual DOM diffing. Mutating the object in-place bypasses re-rendering.",
        "frequency_score": "High (Occurred in 3 attempts)",
        "diagnostic_trigger": "React Component State & Hooks",
        "targeted_challenge": {
            "title": "Immutable Spread State Update",
            "scenario": "Update nested user age inside state without modifying the existing object.",
            "code_snippet": "// ❌ DIRECT MUTATION:\nuser.age = 25;\nsetUser(user); // Will NOT re-render!\n\n// ✅ IMMUTABLE SHALLOW COPY:\nsetUser(prev => ({ ...prev, age: 25 }));",
            "key_takeaway": "Treat state as strictly read-only. Always return fresh object references."
        }
    },
    {
        "dna_id": "dna_ml_data_leakage",
        "skill_code": "ml",
        "title": "Pre-Split Scaler Fitting Data Leakage",
        "pattern": "Fitting StandardScaler on entire dataset before running train_test_split",
        "root_misunderstanding": "Computing mean and variance on the combined dataset injects information from the test evaluation set directly into training, causing unrealistically optimistic validation metrics.",
        "frequency_score": "Medium (Occurred in 2 attempts)",
        "diagnostic_trigger": "Feature Preprocessing & Scaling",
        "targeted_challenge": {
            "title": "Pipeline Encapsulation Drill",
            "scenario": "Ensure preprocessors only fit on X_train and transform X_test.",
            "code_snippet": "# ✅ BULLETPROOF LEAK-FREE PIPELINE:\nfrom sklearn.pipeline import Pipeline\nfrom sklearn.preprocessing import StandardScaler\nfrom sklearn.linear_model import LogisticRegression\n\nmodel = Pipeline([\n    ('scaler', StandardScaler()),\n    ('clf', LogisticRegression())\n])\nmodel.fit(X_train, y_train)\nscore = model.score(X_test, y_test)",
            "key_takeaway": "Never call fit() on test data. Wrap scalers and models inside a Scikit-Learn Pipeline."
        }
    }
]

def analyze_mistake_dna(user_gaps: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Match student diagnostic knowledge gaps against the Mistake DNA taxonomy."""
    results = []
    gap_skills = {g.get("skill_code") for g in user_gaps} if user_gaps else {"sql", "python", "web_dev"}

    for item in MISTAKE_GENOME_DATABASE:
        if item["skill_code"] in gap_skills:
            results.append(item)

    if not results:
        results = MISTAKE_GENOME_DATABASE[:2]
    return results


# ----------------------------------------------------
# 3. SKILL RIPPLE EFFECT ENGINE
# ----------------------------------------------------
SKILL_RIPPLE_CATALOG = {
    "sql": {
        "skill_name": "SQL & Relational Databases",
        "ripple_radius": 85,
        "unlocked_skills": [
            {"code": "data_analytics", "name": "Data Analytics", "influence": "Enables complex aggregation, ETL pipelines, and window analytics."},
            {"code": "web_dev", "name": "Full-Stack Web APIs", "influence": "Powers relational ORMs, ACID migrations, and PostgreSQL persistence."}
        ],
        "unlocked_projects": [
            {"title": "Multi-Tenant SaaS Billing Schema", "difficulty": "Intermediate", "impact": "+35% Backend Portfolio Readiness"},
            {"title": "Real-Time Financial Fraud Query Engine", "difficulty": "Advanced", "impact": "+40% Data Engineering Readiness"}
        ],
        "career_impact": {
            "Full-Stack Web Developer": "+30%",
            "Data Scientist & Analyst": "+45%",
            "Backend & Cloud Engineer": "+40%"
        }
    },
    "python": {
        "skill_name": "Python Programming",
        "ripple_radius": 95,
        "unlocked_skills": [
            {"code": "ml", "name": "Machine Learning", "influence": "Direct engine for NumPy tensors, Scikit-learn, and PyTorch models."},
            {"code": "data_analytics", "name": "Data Science", "influence": "Automates tabular wrangling with Pandas and statistical distributions."},
            {"code": "web_dev", "name": "FastAPI Web Services", "influence": "Enables asynchronous microservices with Pydantic validation."}
        ],
        "unlocked_projects": [
            {"title": "Autonomous Web Scraper & Data Pipeline", "difficulty": "Beginner", "impact": "+25% Scripting Mastery"},
            {"title": "FastAPI Asynchronous Microservice Gateway", "difficulty": "Intermediate", "impact": "+35% API Design Readiness"}
        ],
        "career_impact": {
            "Full-Stack Web Developer": "+35%",
            "AI/ML Engineer": "+50%",
            "Data Scientist & Analyst": "+40%"
        }
    },
    "web_dev": {
        "skill_name": "Modern Web Development",
        "ripple_radius": 90,
        "unlocked_skills": [
            {"code": "fullstack", "name": "Full-Stack Architecture", "influence": "Seamless end-to-end user state and REST API consumption."}
        ],
        "unlocked_projects": [
            {"title": "Interactive Celestial Dashboard", "difficulty": "Advanced", "impact": "+45% UI/UX & Frontend Mastery"},
            {"title": "Real-Time Collaborative Workspace", "difficulty": "Advanced", "impact": "+50% Production Readiness"}
        ],
        "career_impact": {
            "Full-Stack Web Developer": "+55%",
            "Backend & Cloud Engineer": "+20%"
        }
    },
    "data_analytics": {
        "skill_name": "Data Analytics",
        "ripple_radius": 88,
        "unlocked_skills": [
            {"code": "ml", "name": "Machine Learning", "influence": "Fundamental exploratory data analysis, outlier trimming, and feature synthesis."}
        ],
        "unlocked_projects": [
            {"title": "E-Commerce Customer Churn Cohort Engine", "difficulty": "Intermediate", "impact": "+40% Business Analytics Readiness"},
            {"title": "Dynamic Executive KPI Telemetry", "difficulty": "Intermediate", "impact": "+35% Data Storytelling"}
        ],
        "career_impact": {
            "Data Scientist & Analyst": "+50%",
            "AI/ML Engineer": "+35%"
        }
    },
    "ml": {
        "skill_name": "Machine Learning",
        "ripple_radius": 98,
        "unlocked_skills": [
            {"code": "deep_learning", "name": "Deep Learning & LLM Integration", "influence": "Foundation for neural architectures, embeddings, and transformer models."}
        ],
        "unlocked_projects": [
            {"title": "End-to-End Predictive Recommendation Pipeline", "difficulty": "Advanced", "impact": "+60% Applied AI Readiness"},
            {"title": "Automated Anomaly Detection Engine", "difficulty": "Advanced", "impact": "+50% ML Systems Architecture"}
        ],
        "career_impact": {
            "AI/ML Engineer": "+60%",
            "Data Scientist & Analyst": "+40%"
        }
    },
    "java": {
        "skill_name": "Java Enterprise",
        "ripple_radius": 80,
        "unlocked_skills": [
            {"code": "spring_boot", "name": "Spring Boot Cloud Microservices", "influence": "Powers enterprise scale, multithreaded systems, and resilient JVM services."}
        ],
        "unlocked_projects": [
            {"title": "Distributed Banking Transaction Service", "difficulty": "Advanced", "impact": "+50% Enterprise Readiness"}
        ],
        "career_impact": {
            "Backend & Cloud Engineer": "+50%",
            "Full-Stack Web Developer": "+25%"
        }
    }
}

def get_skill_ripple(skill_code: str) -> Dict[str, Any]:
    return SKILL_RIPPLE_CATALOG.get(skill_code, SKILL_RIPPLE_CATALOG["python"])

def get_all_ripples() -> Dict[str, Any]:
    return SKILL_RIPPLE_CATALOG
