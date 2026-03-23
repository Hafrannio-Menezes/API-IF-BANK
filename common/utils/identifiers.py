import random
import uuid


def generate_agency_number() -> str:
    return "0001"


def generate_account_number() -> str:
    return f"{random.randint(100000, 999999)}-{random.randint(0, 9)}"


def generate_reference_code(prefix: str) -> str:
    return f"{prefix}-{uuid.uuid4().hex[:12].upper()}"
