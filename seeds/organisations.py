"""
Sample fictional organisations for security posture assessments.
"""


def get_sample_organisations():
    """Return three fictional small organisation profiles."""
    return [
        {
            "name": "Maple Leaf Bakery",
            "industry": "Food Retail",
            "size": "15 employees",
            "description": (
                "A family-owned bakery with two locations. Uses a POS system, "
                "basic website, and email. Minimal IT infrastructure — one shared "
                "office PC, Wi-Fi for credit card processing. No dedicated IT staff."
            ),
        },
        {
            "name": "TechStart Solutions",
            "industry": "Software Development",
            "size": "30 employees",
            "description": (
                "A startup developing SaaS tools for small businesses. Cloud-native "
                "architecture (AWS), remote-first team. Strong technical capabilities "
                "but immature governance and incident response. Fast-moving, security "
                "often an afterthought."
            ),
        },
        {
            "name": "Greenfield Medical Clinic",
            "industry": "Healthcare",
            "size": "25 employees (5 doctors, 20 support staff)",
            "description": (
                "A primary care clinic managing sensitive patient records. Uses an "
                "Electronic Health Records (EHR) system (cloud-hosted). Subject to "
                "healthcare regulations. Moderate IT maturity, some awareness of "
                "privacy obligations, but limited security monitoring and response."
            ),
        },
    ]
