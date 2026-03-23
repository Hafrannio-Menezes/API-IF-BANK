import json
from pathlib import Path

from django.conf import settings

from apps.investments.models import InvestmentProduct


REFERENCE_PRODUCTS_FILE = Path(settings.BASE_DIR) / "data" / "reference" / "investment_products.json"


def _load_products_payload(data_file: Path | None = None) -> list[dict]:
    file_path = data_file or REFERENCE_PRODUCTS_FILE
    with file_path.open(encoding="utf-8") as file_handler:
        return json.load(file_handler)


def sync_investment_products(*, data_file: Path | None = None) -> dict:
    summary = {
        "created": 0,
        "updated": 0,
        "total": 0,
    }

    for product_payload in _load_products_payload(data_file=data_file):
        _, created = InvestmentProduct.objects.update_or_create(
            name=product_payload["name"],
            defaults=product_payload,
        )
        if created:
            summary["created"] += 1
        else:
            summary["updated"] += 1

    summary["total"] = summary["created"] + summary["updated"]
    return summary
