


SKILL_ALIASES = {
    "python": [
        "python"
    ],

    "java": [
        "java"
    ],

    "c++": [
        "c++",
        "cpp"
    ],

    "sql": [
        "sql"
    ],

    "pandas": [
        "pandas"
    ],

    "numpy": [
        "numpy"
    ],

    "matplotlib": [
        "matplotlib"
    ],

    "seaborn": [
        "seaborn"
    ],

    "scikit-learn": [
        "scikit-learn",
        "scikit learn",
        "sklearn"
    ],

    "machine learning": [
        "machine learning",
        "machine-learning",
        "ml"
    ],

    "deep learning": [
        "deep learning",
        "deep-learning",
        "dl"
    ],

    "tensorflow": [
        "tensorflow"
    ],

    "pytorch": [
        "pytorch",
        "py torch"
    ],

    "nlp": [
        "nlp",
        "natural language processing"
    ],

    "git": [
        "git"
    ],

    "github": [
        "github",
        "git hub"
    ],

    "docker": [
        "docker"
    ],

    "aws": [
        "aws",
        "amazon web services"
    ],

    "azure": [
        "azure",
        "microsoft azure"
    ],

    "streamlit": [
        "streamlit"
    ]
}




def extract_skills(text):
    """Return canonical skills whose aliases occur in *text*."""
    text = text.lower()
    found_skills = []

    for skill, aliases in SKILL_ALIASES.items():
        if any(alias in text for alias in aliases):
            found_skills.append(skill)

    return found_skills
