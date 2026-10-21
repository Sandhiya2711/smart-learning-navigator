import numpy as np
from typing import Dict, List, Any, Optional
from sklearn.neighbors import NearestNeighbors
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer

# Canonical Skill Definitions
CANONICAL_SKILLS = ["python", "java", "sql", "data_analytics", "web_dev", "ml"]

# Prerequisite Graph for Rule-Based Baseline
PREREQUISITES_MAP = {
    "python": [],
    "sql": [],
    "java": [],
    "web_dev": ["python", "sql"], # fullstack uses backend + DB
    "data_analytics": ["python", "sql"],
    "ml": ["python", "data_analytics", "sql"]
}

# Career Profiles (Benchmark proficiency weights for 6 skills + study intensity)
# Format: [python, java, sql, data_analytics, web_dev, ml]
CAREER_ARCHETYPES = {
    "AI/ML Engineer": {
        "vector": np.array([0.90, 0.20, 0.70, 0.85, 0.30, 0.95]),
        "primary_skills": ["python", "data_analytics", "ml", "sql"],
        "recommended_title": "AI & Machine Learning Specialist Pathway",
        "weeks": 16
    },
    "Full-Stack Web Developer": {
        "vector": np.array([0.80, 0.30, 0.85, 0.40, 0.95, 0.20]),
        "primary_skills": ["web_dev", "sql", "python"],
        "recommended_title": "Full-Stack Web Architecture Pathway",
        "weeks": 14
    },
    "Data Scientist & Analyst": {
        "vector": np.array([0.85, 0.10, 0.90, 0.95, 0.25, 0.75]),
        "primary_skills": ["data_analytics", "sql", "python", "ml"],
        "recommended_title": "Enterprise Data Science & Analytics Pathway",
        "weeks": 14
    },
    "Backend & Cloud Engineer": {
        "vector": np.array([0.85, 0.85, 0.90, 0.30, 0.60, 0.20]),
        "primary_skills": ["python", "java", "sql", "web_dev"],
        "recommended_title": "Distributed Systems & Cloud Backend Pathway",
        "weeks": 16
    }
}

class SkillVerseRecommender:
    """
    Genuine, explainable recommendation engine combining:
    1. A transparent rule-based prerequisite & gap analyzer.
    2. A trained scikit-learn NearestNeighbors model matching student vectors to target pathways.
    3. A scikit-learn TF-IDF vectorizer + cosine_similarity ranker matching knowledge gaps to educational resources.
    """
    def __init__(self):
        self.career_names = list(CAREER_ARCHETYPES.keys())
        self.archetype_matrix = np.array([CAREER_ARCHETYPES[k]["vector"] for k in self.career_names])
        
        # Fit NearestNeighbors model on archetype matrix
        self.nn_model = NearestNeighbors(n_neighbors=len(self.career_names), metric="cosine")
        self.nn_model.fit(self.archetype_matrix)
        
        # TF-IDF Vectorizer for Content-based Resource Recommendation
        self.tfidf_vectorizer = TfidfVectorizer(stop_words="english")
        self._is_trained = True

    def student_vector(self, skill_scores: Dict[str, float]) -> np.ndarray:
        """Convert a dictionary of skill scores (0-100) into a normalized vector (0.0-1.0)."""
        vec = []
        for s in CANONICAL_SKILLS:
            score = skill_scores.get(s, 0.0)
            vec.append(min(max(score / 100.0, 0.0), 1.0))
        return np.array(vec)

    def identify_gaps(self, skill_scores: Dict[str, float], missed_topics: List[Dict[str, str]]) -> List[Dict[str, Any]]:
        """
        Explainable rule-based gap identification.
        Categorizes gaps based on thresholding & diagnostic results.
        """
        gaps = []
        
        # Skill-level threshold gaps
        for skill in CANONICAL_SKILLS:
            score = skill_scores.get(skill, 0.0)
            if score < 40.0:
                gaps.append({
                    "skill_code": skill,
                    "topic": f"Foundational {skill.replace('_', ' ').title()}",
                    "severity": "High",
                    "recommendation": f"Score is {int(score)}%. Prioritize core syntax, semantics, and standard operations."
                })
            elif score < 70.0:
                gaps.append({
                    "skill_code": skill,
                    "topic": f"Intermediate {skill.replace('_', ' ').title()} Concepts",
                    "severity": "Medium",
                    "recommendation": f"Score is {int(score)}%. Practice real-world application, optimization, and problem-solving."
                })

        # Granular diagnostic missed topics
        for item in missed_topics:
            skill = item.get("skill_code", "python")
            topic = item.get("topic", "Core Concepts")
            # Avoid duplicate topics
            if not any(g["topic"] == topic for g in gaps):
                gaps.append({
                    "skill_code": skill,
                    "topic": topic,
                    "severity": "High" if skill_scores.get(skill, 50) < 50 else "Medium",
                    "recommendation": f"Review dedicated guides and hands-on exercises for {topic}."
                })

        return gaps

    def rank_resources_for_gaps(self, gaps: List[Dict[str, Any]], available_resources: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        scikit-learn TF-IDF + Cosine Similarity ranking.
        Ranks candidate learning resources according to semantic relevance to the student's knowledge gaps.
        """
        if not gaps or not available_resources:
            return available_resources[:10]

        gap_corpus = " ".join([f"{g['skill_code']} {g['topic']} {g['recommendation']}" for g in gaps])
        res_texts = [f"{r.get('skill_code', '')} {r.get('title', '')} {r.get('description', '')} {r.get('category', '')}" for r in available_resources]
        
        all_docs = [gap_corpus] + res_texts
        try:
            tfidf_matrix = self.tfidf_vectorizer.fit_transform(all_docs)
            gap_vec = tfidf_matrix[0:1]
            res_vecs = tfidf_matrix[1:]
            
            sim_scores = cosine_similarity(gap_vec, res_vecs).flatten()
            
            # Rank resources descending by similarity score
            ranked_indices = np.argsort(sim_scores)[::-1]
            ranked_resources = []
            for idx in ranked_indices:
                res = available_resources[idx].copy()
                res["relevance_score"] = float(round(sim_scores[idx], 3))
                ranked_resources.append(res)
            return ranked_resources
        except Exception:
            return available_resources

    def generate_pathway(
        self,
        career_goal: str,
        skill_scores: Dict[str, float],
        gaps: List[Dict[str, Any]],
        daily_study_hours: float = 2.0,
        resources_catalog: Optional[List[Dict[str, Any]]] = None
    ) -> Dict[str, Any]:
        """
        Synthesize customized pathway with scikit-learn archetype matching,
        topological sorting of prerequisites, and personalized stages.
        """
        # 1. Match Career Profile
        matched_career = None
        for key in CAREER_ARCHETYPES:
            if key.lower() in career_goal.lower() or career_goal.lower() in key.lower():
                matched_career = CAREER_ARCHETYPES[key]
                break
        
        if not matched_career:
            # Fallback to NearestNeighbors on student vector
            student_vec = self.student_vector(skill_scores).reshape(1, -1)
            distances, indices = self.nn_model.kneighbors(student_vec)
            best_match_idx = indices[0][0]
            matched_career_name = self.career_names[best_match_idx]
            matched_career = CAREER_ARCHETYPES[matched_career_name]

        target_skills = matched_career["primary_skills"]

        # 2. Sequence skills respecting prerequisite rules
        sequenced_skills = []
        visited = set()

        def visit(skill):
            if skill in visited:
                return
            for prereq in PREREQUISITES_MAP.get(skill, []):
                if prereq in target_skills and prereq not in visited:
                    visit(prereq)
            visited.add(skill)
            sequenced_skills.append(skill)

        for s in target_skills:
            visit(s)

        # 3. Generate Stages & Steps
        steps = []
        total_hours = 0
        order = 1

        for skill in sequenced_skills:
            score = skill_scores.get(skill, 0.0)
            skill_label = skill.replace("_", " ").title()
            
            # Tailor duration based on current proficiency
            if score < 40:
                stage_name = f"Foundations: {skill_label}"
                desc = f"Master fundamental concepts, core syntax, and eliminate critical gaps in {skill_label}."
                duration = 18.0 / max(daily_study_hours, 1.0)
                level = "Beginner"
            elif score < 75:
                stage_name = f"Acceleration: {skill_label}"
                desc = f"Advance to intermediate patterns, optimization, and real-world architectures in {skill_label}."
                duration = 14.0 / max(daily_study_hours, 1.0)
                level = "Intermediate"
            else:
                stage_name = f"Mastery & Capstone: {skill_label}"
                desc = f"High-performance engineering, enterprise patterns, and capstone implementations in {skill_label}."
                duration = 10.0 / max(daily_study_hours, 1.0)
                level = "Advanced"

            # Filter relevant resources
            skill_res = []
            if resources_catalog:
                matched_res = [r for r in resources_catalog if r.get("skill_code") == skill]
                skill_res = self.rank_resources_for_gaps(gaps, matched_res)[:3]

            # Generate learning objectives
            objectives = [
                f"Understand and apply core {skill_label} design principles",
                f"Resolve identified diagnostic gaps in {skill_label} operations",
                f"Implement clean, tested, and idiomatic code modules",
                f"Pass the end-of-stage verification quiz with >= 80% accuracy"
            ]

            tasks = [
                f"Build a mini-project demonstrating {skill_label} problem solving",
                f"Complete 3 algorithmic coding challenges focusing on {skill_label}",
                f"Review official documentation and write unit tests"
            ]

            checkpoint_quiz = [
                {
                    "question": f"Which best practice is vital when developing {skill_label} applications?",
                    "options": ["Adhering to clean architecture and modularity", "Hardcoding database credentials", "Avoiding version control", "Skipping error handling"],
                    "correct": 0
                },
                {
                    "question": f"How should state or resources be managed effectively in {skill_label}?",
                    "options": ["Using context managers, scopes, or proper cleanup", "Leaving files and connections open", "Rebooting the server per request", "Ignoring memory leaks"],
                    "correct": 0
                }
            ]

            steps.append({
                "order_index": order,
                "skill_code": skill,
                "stage_name": stage_name,
                "title": f"{stage_name} ({level})",
                "description": desc,
                "duration_hours": round(duration, 1),
                "learning_objectives": objectives,
                "resources": skill_res,
                "quiz_data": checkpoint_quiz,
                "practical_tasks": tasks,
                "is_completed": False
            })
            total_hours += duration
            order += 1

        total_weeks = max(4, int(np.ceil(total_hours / (daily_study_hours * 7))))

        return {
            "title": matched_career["recommended_title"],
            "career_goal": career_goal,
            "description": f"Tailored curriculum synthesized by SkillVerse AI for {career_goal}, calibrated for {daily_study_hours} hrs/day.",
            "total_duration_weeks": total_weeks,
            "steps": steps
        }

# Global singleton
recommender_engine = SkillVerseRecommender()
