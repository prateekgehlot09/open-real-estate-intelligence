import csv
import json
import urllib.request
from pathlib import Path


def load_from_csv(filepath: str) -> list[dict]:
    """Load OREIL-standard data from a local CSV file."""
    with open(filepath, newline="") as f:
        return list(csv.DictReader(f))


def load_from_dld_export(filepath: str) -> list[dict]:
    """
    Parse a DLD bulk transaction export file into OREIL Data Standard format.

    DLD exports use different field names — this normalises them.
    Download from: https://dubailand.gov.ae/en/open-data/real-estate-data/

    Note: Risk scores (liquidity, demand, pricing) cannot be derived from
    DLD data alone — they must be assigned by an analyst or derived from
    a separate market scoring model.
    """
    raw_data = []
    with open(filepath, newline="", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                raw_data.append({
                    "property_id": row.get("transaction_id", ""),
                    "location": row.get("area_name_en", ""),
                    "type": row.get("property_type_en", ""),
                    "price": float(row.get("trans_value", 0)),
                    "rent": float(row.get("annual_amount", 0)),
                    # Risk scores must be assigned externally
                    "liquidity": 3,
                    "demand": 3,
                    "pricing": 3,
                })
            except (ValueError, KeyError):
                continue
    return raw_data
