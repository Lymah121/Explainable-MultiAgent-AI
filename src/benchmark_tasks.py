"""
Benchmark Tasks — Curated fact-checking tasks for experiments.

12 tasks across 3 difficulty levels (easy, medium, hard) and multiple
domains (history, science, geography, current events) for systematically
evaluating baseline vs. proposed approaches.
"""

BENCHMARK_TASKS = [
    # ── Easy (well-known, easily verifiable facts) ────────────────

    {
        "id": "easy_01",
        "difficulty": "easy",
        "domain": "history",
        "task": (
            "Summarize and fact-check the following: "
            "The Eiffel Tower was built in 1889 for the World's Fair in Paris. "
            "It was designed by Gustave Eiffel and stands 324 meters tall. "
            "It was originally intended to be dismantled after 20 years."
        ),
        "expected_claims": [
            {"claim": "Built in 1889", "expected_status": "verified"},
            {"claim": "For the World's Fair", "expected_status": "verified"},
            {"claim": "Designed by Gustave Eiffel", "expected_status": "verified"},
            {"claim": "324 meters tall", "expected_status": "verified"},
            {"claim": "Intended to be dismantled after 20 years", "expected_status": "verified"},
        ],
    },
    {
        "id": "easy_02",
        "difficulty": "easy",
        "domain": "science",
        "task": (
            "Summarize and fact-check the following: "
            "Water boils at 100 degrees Celsius at standard atmospheric pressure. "
            "It is composed of two hydrogen atoms and one oxygen atom. "
            "The chemical formula for water is H2O."
        ),
        "expected_claims": [
            {"claim": "Boils at 100°C at standard pressure", "expected_status": "verified"},
            {"claim": "Two hydrogen atoms and one oxygen atom", "expected_status": "verified"},
            {"claim": "Chemical formula is H2O", "expected_status": "verified"},
        ],
    },
    {
        "id": "easy_03",
        "difficulty": "easy",
        "domain": "geography",
        "task": (
            "Summarize and fact-check the following: "
            "The Amazon River is the longest river in the world. "
            "It flows through Brazil, Peru, and Colombia. "
            "The Amazon rainforest produces 20% of the world's oxygen."
        ),
        "expected_claims": [
            {"claim": "Amazon is the longest river", "expected_status": "disputed"},
            {"claim": "Flows through Brazil, Peru, and Colombia", "expected_status": "verified"},
            {"claim": "Produces 20% of world's oxygen", "expected_status": "disputed"},
        ],
    },
    {
        "id": "easy_04",
        "difficulty": "easy",
        "domain": "history",
        "task": (
            "Summarize and fact-check the following: "
            "The Great Wall of China was built over many centuries, "
            "beginning in the 7th century BC. It is visible from space "
            "with the naked eye. It stretches over 13,000 miles."
        ),
        "expected_claims": [
            {"claim": "Built beginning in the 7th century BC", "expected_status": "verified"},
            {"claim": "Visible from space with naked eye", "expected_status": "disputed"},
            {"claim": "Stretches over 13,000 miles", "expected_status": "verified"},
        ],
    },

    # ── Medium (mix of accurate and inaccurate claims) ───────────

    {
        "id": "med_01",
        "difficulty": "medium",
        "domain": "science",
        "task": (
            "Summarize and fact-check the following: "
            "Albert Einstein won the Nobel Prize in Physics in 1921 for his "
            "discovery of the theory of relativity. He was born in Germany "
            "and later became a U.S. citizen. He published the special theory "
            "of relativity in 1905."
        ),
        "expected_claims": [
            {"claim": "Won Nobel Prize in 1921", "expected_status": "verified"},
            {"claim": "Nobel Prize for theory of relativity", "expected_status": "disputed"},
            {"claim": "Born in Germany", "expected_status": "verified"},
            {"claim": "Became a U.S. citizen", "expected_status": "verified"},
            {"claim": "Special relativity published in 1905", "expected_status": "verified"},
        ],
    },
    {
        "id": "med_02",
        "difficulty": "medium",
        "domain": "history",
        "task": (
            "Summarize and fact-check the following: "
            "The Titanic sank on its maiden voyage in April 1912 after hitting "
            "an iceberg in the North Atlantic. Over 1,500 people died. The ship "
            "was traveling from Southampton to New York City. It was considered "
            "unsinkable and had enough lifeboats for all passengers."
        ),
        "expected_claims": [
            {"claim": "Sank on maiden voyage April 1912", "expected_status": "verified"},
            {"claim": "Hit an iceberg", "expected_status": "verified"},
            {"claim": "Over 1,500 died", "expected_status": "verified"},
            {"claim": "Southampton to New York", "expected_status": "verified"},
            {"claim": "Had enough lifeboats for all passengers", "expected_status": "disputed"},
        ],
    },
    {
        "id": "med_03",
        "difficulty": "medium",
        "domain": "science",
        "task": (
            "Summarize and fact-check the following: "
            "The human body has 206 bones. Babies are born with approximately "
            "270 bones, many of which fuse together as they grow. The smallest "
            "bone in the body is the stapes in the ear. Humans share 98% of "
            "their DNA with chimpanzees."
        ),
        "expected_claims": [
            {"claim": "206 bones in adult human body", "expected_status": "verified"},
            {"claim": "Babies born with ~270 bones", "expected_status": "verified"},
            {"claim": "Smallest bone is stapes", "expected_status": "verified"},
            {"claim": "98% DNA shared with chimpanzees", "expected_status": "verified"},
        ],
    },
    {
        "id": "med_04",
        "difficulty": "medium",
        "domain": "geography",
        "task": (
            "Summarize and fact-check the following: "
            "Mount Everest is the tallest mountain in the world at 8,849 meters. "
            "It straddles the border between Nepal and Tibet. The first confirmed "
            "ascent was by Edmund Hillary and Tenzing Norgay in 1953. Over 300 "
            "people have died attempting to climb it."
        ),
        "expected_claims": [
            {"claim": "Tallest mountain at 8,849 meters", "expected_status": "verified"},
            {"claim": "Border between Nepal and Tibet", "expected_status": "verified"},
            {"claim": "First ascent by Hillary and Norgay in 1953", "expected_status": "verified"},
            {"claim": "Over 300 deaths", "expected_status": "verified"},
        ],
    },

    # ── Hard (subtle inaccuracies, complex claims) ───────────────

    {
        "id": "hard_01",
        "difficulty": "hard",
        "domain": "science",
        "task": (
            "Summarize and fact-check the following: "
            "CRISPR-Cas9 was discovered by Jennifer Doudna and Feng Zhang in 2012. "
            "It allows scientists to edit genes with unprecedented precision. "
            "The technology has already been used to cure sickle cell disease in "
            "clinical trials. CRISPR stands for Clustered Regularly Interspaced "
            "Short Palindromic Repeats. The 2020 Nobel Prize in Chemistry was "
            "awarded for this technology."
        ),
        "expected_claims": [
            {"claim": "Discovered by Doudna and Zhang in 2012", "expected_status": "disputed"},
            {"claim": "Edits genes with precision", "expected_status": "verified"},
            {"claim": "Used to cure sickle cell in trials", "expected_status": "verified"},
            {"claim": "CRISPR acronym", "expected_status": "verified"},
            {"claim": "2020 Nobel Prize in Chemistry", "expected_status": "verified"},
        ],
    },
    {
        "id": "hard_02",
        "difficulty": "hard",
        "domain": "history",
        "task": (
            "Summarize and fact-check the following: "
            "The United States purchased Alaska from Russia in 1867 for $7.2 million. "
            "At the time, the purchase was widely criticized and called 'Seward's Folly.' "
            "Alaska became the 49th state in 1959. It is the largest U.S. state by area "
            "and has a larger population than Wyoming. The purchase price was approximately "
            "2 cents per acre."
        ),
        "expected_claims": [
            {"claim": "Purchased in 1867 for $7.2 million", "expected_status": "verified"},
            {"claim": "Called Seward's Folly", "expected_status": "verified"},
            {"claim": "49th state in 1959", "expected_status": "verified"},
            {"claim": "Largest state by area", "expected_status": "verified"},
            {"claim": "Larger population than Wyoming", "expected_status": "verified"},
            {"claim": "~2 cents per acre", "expected_status": "verified"},
        ],
    },
    {
        "id": "hard_03",
        "difficulty": "hard",
        "domain": "science",
        "task": (
            "Summarize and fact-check the following: "
            "Quantum computers use qubits instead of classical bits. Unlike classical "
            "bits which can be 0 or 1, qubits can exist in a superposition of both "
            "states simultaneously. Google achieved 'quantum supremacy' in 2019 with "
            "its Sycamore processor, completing a calculation in 200 seconds that would "
            "take a classical supercomputer 10,000 years. IBM disputed this claim, "
            "arguing the classical time estimate was exaggerated."
        ),
        "expected_claims": [
            {"claim": "Qubits vs classical bits", "expected_status": "verified"},
            {"claim": "Superposition of states", "expected_status": "verified"},
            {"claim": "Google quantum supremacy 2019", "expected_status": "verified"},
            {"claim": "200 seconds vs 10,000 years", "expected_status": "disputed"},
            {"claim": "IBM disputed the claim", "expected_status": "verified"},
        ],
    },
    {
        "id": "hard_04",
        "difficulty": "hard",
        "domain": "current_events",
        "task": (
            "Summarize and fact-check the following: "
            "Electric vehicles (EVs) produce zero emissions during operation. "
            "The global EV market share exceeded 15% of new car sales in 2023. "
            "Lithium-ion batteries used in EVs have a typical lifespan of 8-15 years. "
            "Norway has the highest EV adoption rate, with over 80% of new car sales "
            "being electric. The environmental impact of EV battery production is "
            "negligible compared to gasoline vehicle emissions over a car's lifetime."
        ),
        "expected_claims": [
            {"claim": "Zero emissions during operation", "expected_status": "verified"},
            {"claim": "Global market share exceeded 15% in 2023", "expected_status": "verified"},
            {"claim": "Battery lifespan 8-15 years", "expected_status": "verified"},
            {"claim": "Norway 80% EV adoption", "expected_status": "verified"},
            {"claim": "Battery production impact negligible", "expected_status": "disputed"},
        ],
    },
]


def get_tasks_by_difficulty(difficulty: str) -> list[dict]:
    """Get benchmark tasks filtered by difficulty level."""
    return [t for t in BENCHMARK_TASKS if t["difficulty"] == difficulty]


def get_all_tasks() -> list[dict]:
    """Get all benchmark tasks."""
    return BENCHMARK_TASKS


def get_task_by_id(task_id: str) -> dict | None:
    """Get a single benchmark task by its ID."""
    for task in BENCHMARK_TASKS:
        if task["id"] == task_id:
            return task
    return None
