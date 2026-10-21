import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from fastapi.testclient import TestClient
from backend.main import app
from backend.services.recommender import recommender_engine

client = TestClient(app)

def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert data["app"] == "SkillVerse AI"

def test_scikit_learn_recommender():
    # Test scikit-learn recommendation engine
    scores = {"python": 85.0, "sql": 35.0, "web_dev": 75.0, "data_analytics": 45.0, "java": 20.0, "ml": 25.0}
    gaps = recommender_engine.identify_gaps(scores, [{"skill_code": "sql", "topic": "JOIN Operations"}])
    assert len(gaps) > 0
    assert any(g["skill_code"] == "sql" for g in gaps)
    
    pathway = recommender_engine.generate_pathway("AI/ML Engineer", scores, gaps, daily_study_hours=2.0)
    assert "steps" in pathway
    assert len(pathway["steps"]) > 0
    assert pathway["total_duration_weeks"] >= 4

def test_auth_login_demo():
    # Test logging in with seeded demo user
    response = client.post("/api/auth/login", json={"email": "demo@skillverse.ai", "password": "Password123!"})
    assert response.status_code == 200
    token_data = response.json()
    assert "access_token" in token_data
    token = token_data["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # Test /students/me
    profile_resp = client.get("/api/students/me", headers=headers)
    assert profile_resp.status_code == 200
    assert profile_resp.json()["career_goal"] == "Full-Stack Web Developer"

    # Test /skills
    skills_resp = client.get("/api/skills", headers=headers)
    assert skills_resp.status_code == 200
    assert len(skills_resp.json()) == 6

    # Test /pathways/me
    pathway_resp = client.get("/api/pathways/me", headers=headers)
    assert pathway_resp.status_code == 200
    assert "steps" in pathway_resp.json()

    # Test /resources
    res_resp = client.get("/api/resources", headers=headers)
    assert res_resp.status_code == 200
    assert len(res_resp.json()) > 0

    # Test /missions/today
    mission_resp = client.get("/api/missions/today", headers=headers)
    assert mission_resp.status_code == 200
    assert len(mission_resp.json()) > 0

    # Test /analytics/me
    analytics_resp = client.get("/api/analytics/me", headers=headers)
    assert analytics_resp.status_code == 200
    assert "skill_scores" in analytics_resp.json()

    # Test /mentor/recommend
    mentor_resp = client.post("/api/mentor/recommend", json={"message": "How do I fix my SQL gaps?"}, headers=headers)
    assert mentor_resp.status_code == 200
    assert "reply" in mentor_resp.json()

if __name__ == "__main__":
    print("[RUNNING TESTS]")
    test_health()
    print("[PASS] /health")
    test_scikit_learn_recommender()
    print("[PASS] scikit-learn recommendation engine")
    test_auth_login_demo()
    print("[PASS] Auth, Students, Skills, Pathways, Resources, Missions, Analytics, Mentor Endpoints")
    print("[ALL BACKEND TESTS PASSED]")
