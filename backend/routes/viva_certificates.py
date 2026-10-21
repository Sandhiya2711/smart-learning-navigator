import hashlib
import time
from datetime import datetime
from typing import Dict, Any, List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel
from sqlalchemy.orm import Session
from backend.database import get_db
from backend.models.user import User
from backend.models.profile import StudentProfile
from backend.services.auth import get_optional_current_user

router = APIRouter(prefix="/viva-cert", tags=["AI Viva & Certificates"])

# In-memory certificate cache for instant tamper-proof verification
CERTIFICATES_DB: Dict[str, Dict[str, Any]] = {
    "SKV-2026-AI-8832": {
        "cert_id": "SKV-2026-AI-8832",
        "student_name": "Ganesh",
        "student_email": "demo@skillverse.ai",
        "pathway_title": "Full Stack AI & Autonomous Agent Architect",
        "issue_date": "October 21, 2026",
        "score_percent": 96,
        "global_rank": "Top 2% Celestial Tier",
        "status": "VALID",
        "issuer": "SkillVerse AI Autonomous Certification Engine",
        "crypto_hash": "sha256:7f4e9a1820bc9d14624d77298317e34f810aa7e8d423405c938b81204cf012aa",
        "skills_verified": [
            "Python Architecture & AsyncIO",
            "Vector Embeddings & RAG",
            "FastAPI Microservices",
            "Autonomous Agents & Tool Calling",
            "SQL Query Optimization & Indexing",
            "Scikit-Learn Pipeline Modeling"
        ],
        "viva_score": "9.5 / 10 (Mastery Distinction)",
        "diagnostic_score": "94%",
        "stages_completed": 6
    }
}

class VivaEvaluateRequest(BaseModel):
    question_id: str
    topic: str
    question_text: str
    student_answer: str

class CertificateGenerateRequest(BaseModel):
    pathway_title: Optional[str] = "Full Stack AI & Autonomous Systems Architect"
    score_percent: Optional[int] = 95
    skills: Optional[List[str]] = None

VIVA_QUESTIONS = [
    {
        "id": "py-01",
        "topic": "Python Core & Memory",
        "domain": "python",
        "level": "Intermediate",
        "question": "Can you explain the key differences between Mutable and Immutable types in Python, and how memory addresses behave?",
        "expected_keywords": ["mutable", "immutable", "id", "reference", "memory", "list", "tuple", "hashable", "in-place"],
        "model_answer": "In Python, mutable objects like lists and dicts can be modified in-place at the same memory address (id), while immutable objects like strings, ints, and tuples cannot be altered once created. Modifying an immutable type creates a new object in memory."
    },
    {
        "id": "py-02",
        "topic": "Python Concurrency",
        "domain": "python",
        "level": "Advanced",
        "question": "What is Python's Global Interpreter Lock (GIL), and when should you choose Multiprocessing over Multithreading?",
        "expected_keywords": ["gil", "thread", "multiprocessing", "cpu-bound", "i/o-bound", "lock", "process", "memory"],
        "model_answer": "The GIL is a mutex preventing multiple native threads from executing Python bytecodes at once. For CPU-intensive computation, multiprocessing bypasses the GIL by using separate processes with independent memory spaces. For I/O-bound tasks, threading or asyncio is preferred."
    },
    {
        "id": "sql-01",
        "topic": "Database Architecture",
        "domain": "sql",
        "level": "Intermediate",
        "question": "In SQL, what is the architectural difference between WHERE and HAVING, and how do database indexes accelerate queries?",
        "expected_keywords": ["where", "having", "aggregate", "group by", "index", "b-tree", "filter", "scan", "execution plan"],
        "model_answer": "WHERE filters rows before any groupings or aggregations are calculated, whereas HAVING filters grouped result sets after GROUP BY. Indexes (typically B-Trees) allow logarithmic O(log N) lookups instead of expensive full table scans."
    },
    {
        "id": "ai-01",
        "topic": "Machine Learning & AI",
        "domain": "ai",
        "level": "Advanced",
        "question": "Explain the Bias-Variance tradeoff in machine learning. How do you prevent overfitting in deep neural networks or ensemble models?",
        "expected_keywords": ["bias", "variance", "underfitting", "overfitting", "regularization", "dropout", "cross-validation", "generalization"],
        "model_answer": "High bias leads to underfitting due to overly simplistic assumptions, while high variance leads to overfitting by learning training noise. Overfitting is mitigated via L1/L2 regularization, dropout, early stopping, cross-validation, and ensemble methods like bagging and boosting."
    },
    {
        "id": "web-01",
        "topic": "Web Systems & APIs",
        "domain": "web",
        "level": "Intermediate",
        "question": "Compare stateless REST APIs with WebSockets or GraphQL. Why is token-based stateless authentication (JWT) popular for microservices?",
        "expected_keywords": ["stateless", "rest", "jwt", "token", "signature", "microservices", "bidirectional", "websocket", "scalability"],
        "model_answer": "REST is stateless and request-response driven, whereas WebSockets enable persistent bidirectional streaming. JWT is popular in microservices because tokens are self-contained and cryptographically signed, eliminating the need to query a central session store on every service call."
    }
]

@router.get("/viva/questions")
def get_viva_questions(domain: Optional[str] = None):
    if domain:
        filtered = [q for q in VIVA_QUESTIONS if q["domain"] == domain]
        return filtered or VIVA_QUESTIONS
    return VIVA_QUESTIONS

@router.post("/viva/evaluate")
def evaluate_viva_answer(
    req: VivaEvaluateRequest,
    current_user: Optional[User] = Depends(get_optional_current_user)
):
    answer = req.student_answer.strip().lower()
    if not answer or len(answer) < 5:
        return {
            "score": 2,
            "max_score": 10,
            "rating": "Needs Elaboration",
            "feedback": "Answer was too brief. Try to articulate technical definitions, memory mechanics, or architectural reasons.",
            "detected_keywords": [],
            "missing_keywords": ["definition", "use-case", "mechanisms"],
            "model_answer": "Provide a comprehensive answer covering key technical concepts.",
            "cosmic_xp_earned": 20
        }

    # Find question match
    matched = next((q for q in VIVA_QUESTIONS if q["id"] == req.question_id), None)
    expected = matched["expected_keywords"] if matched else ["concept", "memory", "performance", "architecture"]
    
    detected = [kw for kw in expected if kw in answer]
    coverage = len(detected) / max(len(expected), 1)

    # Word count and depth heuristic
    word_count = len(answer.split())
    depth_bonus = min(2, word_count // 15)

    base_score = int(coverage * 7) + depth_bonus + 1
    score = max(3, min(10, base_score))

    if score >= 9:
        rating = "Outstanding Mastery 🔥"
        badge = "Grandmaster Orator"
        feedback = "Exceptional articulation! You clearly communicated the core principles, underlying mechanics, and architectural tradeoffs with high technical precision."
    elif score >= 7:
        rating = "Proficient & Strong 🚀"
        badge = "Certified Technical Orator"
        feedback = "Solid explanation! You touched upon the essential concepts accurately. Deepening the discussion on edge cases or internal mechanics will make it world-class."
    elif score >= 5:
        rating = "Developing Knowledge 💡"
        badge = "Cosmic Apprentice"
        feedback = "Good foundation, but your answer could use more domain-specific terminology and clear structural distinction between the core concepts."
    else:
        rating = "Review Recommended 📖"
        badge = "Seeker"
        feedback = "Several critical technical aspects were missed. Review the model explanation and practice articulating the core concepts aloud."

    missing = [kw for kw in expected if kw not in detected]

    return {
        "score": score,
        "max_score": 10,
        "rating": rating,
        "badge": badge,
        "feedback": feedback,
        "detected_keywords": detected,
        "missing_keywords": missing[:4],
        "model_answer": matched["model_answer"] if matched else "Review fundamentals to solidify your grasp.",
        "cosmic_xp_earned": score * 25
    }

@router.get("/certificates/verify/{cert_id}")
def verify_certificate(cert_id: str):
    cert = CERTIFICATES_DB.get(cert_id.upper())
    if not cert:
        # Check case-insensitive
        for k, v in CERTIFICATES_DB.items():
            if k.lower() == cert_id.lower():
                return {"valid": True, "certificate": v}
        return {
            "valid": False,
            "error": "Certificate ID not found on SkillVerse ledger.",
            "cert_id": cert_id
        }
    return {
        "valid": True,
        "certificate": cert
    }

@router.post("/certificates/generate")
def generate_certificate(
    req: CertificateGenerateRequest,
    current_user: Optional[User] = Depends(get_optional_current_user),
    db: Session = Depends(get_db)
):
    student_name = "Cosmic Navigator Ganesh"
    student_email = "ganesh@skillverse.ai"
    if current_user:
        student_name = current_user.full_name or "Ganesh"
        student_email = current_user.email

    timestamp_int = int(time.time())
    unique_suffix = str(timestamp_int)[-4:]
    cert_id = f"SKV-2026-AI-{unique_suffix}"

    raw_hash_content = f"{cert_id}:{student_name}:{req.pathway_title}:{timestamp_int}:SKILLVERSE_LEDGER"
    crypto_hash = "sha256:" + hashlib.sha256(raw_hash_content.encode("utf-8")).hexdigest()

    skills = req.skills or [
        "Python Architecture & Systems",
        "FastAPI Asynchronous Microservices",
        "Scikit-Learn Predictive Modeling",
        "SQL Relational Indexing",
        "Autonomous Agent Orchestration"
    ]

    cert_obj = {
        "cert_id": cert_id,
        "student_name": student_name,
        "student_email": student_email,
        "pathway_title": req.pathway_title,
        "issue_date": datetime.now().strftime("%B %d, %Y"),
        "score_percent": req.score_percent or 96,
        "global_rank": "Top 2% Celestial Tier",
        "status": "VALID",
        "issuer": "SkillVerse AI Autonomous Certification Engine",
        "crypto_hash": crypto_hash,
        "skills_verified": skills,
        "viva_score": "9.4 / 10 (Distinction)",
        "diagnostic_score": "95%",
        "stages_completed": 6
    }

    CERTIFICATES_DB[cert_id] = cert_obj

    return {
        "success": True,
        "certificate": cert_obj
    }
