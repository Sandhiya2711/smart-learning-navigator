from typing import Dict, List, Any
from datetime import datetime

# Avatar Evolution Tiers based on overall score and cleared steps
AVATAR_TIERS = [
    {
        "tier": 1,
        "name": "Stardust Initiate",
        "title": "Cosmic Trainee",
        "min_score": 0,
        "min_steps": 0,
        "aura_color": "#94a3b8",
        "glow_class": "shadow-slate-500/30",
        "description": "Just embarking on the cosmic voyage. Basic spacesuit and standard navigation beacon."
    },
    {
        "tier": 2,
        "name": "Orbital Voyager",
        "title": "Planetary Scout",
        "min_score": 35,
        "min_steps": 1,
        "aura_color": "#38bdf8",
        "glow_class": "shadow-cyan-500/50",
        "description": "Ascending into planetary orbit. Equipped with Cybernetic HUD Visor and thruster stabilization."
    },
    {
        "tier": 3,
        "name": "Nebula Commander",
        "title": "Systems Architect",
        "min_score": 55,
        "min_steps": 2,
        "aura_color": "#a855f7",
        "glow_class": "shadow-purple-500/60",
        "description": "Harnessing deep space energy. Unlocked Quantum Core Gauntlet and high-density ion shielding."
    },
    {
        "tier": 4,
        "name": "Supernova Master",
        "title": "Quantum Polymath",
        "min_score": 75,
        "min_steps": 3,
        "aura_color": "#ec4899",
        "glow_class": "shadow-pink-500/70",
        "description": "Radiating stellar power. Unlocked Solar Flare Cape, Neural Tensor Matrix, and gravity distortion field."
    },
    {
        "tier": 5,
        "name": "Celestial Sovereign",
        "title": "Master of the Skill Galaxy",
        "min_score": 90,
        "min_steps": 4,
        "aura_color": "#f59e0b",
        "glow_class": "shadow-amber-500/80",
        "description": "Supreme architect of the cosmic curriculum. Bends spacetime and unlocks all galaxy powers."
    }
]

# Accessories and Gear unlocked by specific skill thresholds
AVATAR_ACCESSORIES_CATALOG = [
    {
        "id": "item_sql_gauntlet",
        "name": "Relational Query Gauntlet",
        "slot": "arms",
        "required_skill": "sql",
        "required_score": 40,
        "icon": "Shield",
        "effect": "+25% Query Optimization Focus",
        "description": "Infused with PostgreSQL transaction locks. Eliminates dirty reads and phantom mutations."
    },
    {
        "id": "item_python_core",
        "name": "Async Core Engine",
        "slot": "chest",
        "required_skill": "python",
        "required_score": 60,
        "icon": "Cpu",
        "effect": "+30% Concurrency Processing",
        "description": "Powers simultaneous coroutine execution and memory-efficient generator iterators."
    },
    {
        "id": "item_web_visor",
        "name": "DOM Holographic Visor",
        "slot": "head",
        "required_skill": "web_dev",
        "required_score": 50,
        "icon": "Eye",
        "effect": "Instant Virtual DOM Reconciliation",
        "description": "Projects responsive UI layouts and component trees directly into visual field."
    },
    {
        "id": "item_ml_matrix",
        "name": "Neural Tensor Wings",
        "slot": "wings",
        "required_skill": "ml",
        "required_score": 30,
        "icon": "Sparkles",
        "effect": "Gradient Descent Warp Speed",
        "description": "Aerodynamic plasma wings optimized with scikit-learn loss function convergence."
    },
    {
        "id": "item_data_orb",
        "name": "Pandas Telemetric Companion Drone",
        "slot": "companion",
        "required_skill": "data_analytics",
        "required_score": 45,
        "icon": "Bot",
        "effect": "Automated Missing Value Imputation",
        "description": "Autonomous hovering drone that scans dataset distributions and flags outlier anomalies."
    }
]

# Galaxy Powers unlocked as student advances
GALAXY_POWERS_CATALOG = [
    {
        "power_id": "pwr_syntax_surge",
        "name": "Syntax Surge",
        "unlocked_at_level": 1,
        "aura_effect": "Electric Blue Corona",
        "cooldown": "Passive",
        "description": "Boosts daily quiz retention and code readability across all programming languages."
    },
    {
        "power_id": "pwr_schema_shield",
        "name": "ACID Schema Shield",
        "unlocked_at_level": 2,
        "aura_effect": "Neon Cyan Hexagonal Grid",
        "cooldown": "Passive",
        "description": "Guarantees transactional consistency and prevents mental fatigue during complex JOINs."
    },
    {
        "power_id": "pwr_neural_singularity",
        "name": "Neural Singularity",
        "unlocked_at_level": 3,
        "aura_effect": "Cosmic Violet Shockwave",
        "cooldown": "Active Burst",
        "description": "Instantly maps multi-dimensional feature matrices and synthesizes optimal ML hyperparameters."
    }
]

def calculate_avatar_state(skill_scores: Dict[str, float], completed_steps: int = 1) -> Dict[str, Any]:
    scores = list(skill_scores.values()) if skill_scores else [30]
    avg_score = sum(scores) / max(len(scores), 1)

    # Determine Tier
    current_tier = AVATAR_TIERS[0]
    for t in AVATAR_TIERS:
        if avg_score >= t["min_score"] and completed_steps >= t["min_steps"]:
            current_tier = t

    # Next Tier
    next_tier = None
    for t in AVATAR_TIERS:
        if t["tier"] > current_tier["tier"]:
            next_tier = t
            break

    # Progress to next tier
    progress_to_next = 100
    if next_tier:
        score_diff = next_tier["min_score"] - current_tier["min_score"]
        curr_progress = avg_score - current_tier["min_score"]
        progress_to_next = min(100, max(5, int((curr_progress / max(score_diff, 1)) * 100)))

    # Evaluate Unlocked Gear & Accessories
    gear = []
    unlocked_count = 0
    for item in AVATAR_ACCESSORIES_CATALOG:
        score = skill_scores.get(item["required_skill"], 0)
        is_unlocked = score >= item["required_score"]
        if is_unlocked:
            unlocked_count += 1
        gear.append({
            **item,
            "current_score": score,
            "is_unlocked": is_unlocked
        })

    # Powers unlocked
    powers = []
    for p in GALAXY_POWERS_CATALOG:
        powers.append({
            **p,
            "is_unlocked": current_tier["tier"] >= p["unlocked_at_level"]
        })

    return {
        "current_tier": current_tier,
        "next_tier": next_tier,
        "progress_to_next": progress_to_next,
        "power_level": int(avg_score * 12 + completed_steps * 85),
        "unlocked_gear": gear,
        "unlocked_count": unlocked_count,
        "total_gear_count": len(gear),
        "galaxy_powers": powers
    }
