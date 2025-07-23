import re

def parse_query(query: str) -> dict:
    age_match = re.search(r'(\d{1,2})[- ]?year[- ]?old', query)
    gender_match = re.search(r'\b(male|female|m|f)\b', query, re.IGNORECASE)
    procedure_match = re.search(r'(surgery|operation|procedure) (on|for)? ([a-zA-Z ]+)', query)
    location_match = re.search(r'in ([A-Za-z ]+)', query)
    policy_duration_match = re.search(r'(\d+)[ -]?month[- ]?(old)?', query)

    return {
        "age": age_match.group(1) if age_match else None,
        "gender": gender_match.group(1).lower() if gender_match else None,
        "procedure": procedure_match.group(3).strip() if procedure_match else None,
        "location": location_match.group(1).strip() if location_match else None,
        "policy_duration": policy_duration_match.group(1) + " months" if policy_duration_match else None
    }
