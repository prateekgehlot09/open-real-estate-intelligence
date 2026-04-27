import csv
from pathlib import Path


def load_from_csv(filepath: str) -> list:
    """
    Load OREIL-standard property data from a local CSV file.

    Args:
        filepath: Path to a CSV file conforming to OREIL Data Standard v0.1.

    Returns:
        List of dicts, one per property row.

    Raises:
        FileNotFoundError: If the file does not exist.
        ValueError: If required columns are missing.
    """
    required_columns = {"location", "type", "price", "rent",
                        "liquidity", "demand", "pricing"}

    path = Path(filepath)
    if not path.exists():
        raise FileNotFoundError(f"Data file not found: {filepath}")

    with open(path, newline="", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        columns = set(reader.fieldnames or [])
        missing = required_columns - columns
        if missing:
            raise ValueError(
                f"CSV missing required OREIL columns: {', '.join(sorted(missing))}"
            )
        return list(reader)


def load_from_dld_export(filepath: str) -> list:
    """
    Parse a Dubai Land Department (DLD) bulk transaction export into
    OREIL Data Standard format.

    DLD exports use different field names — this normalises them.
    Download from: https://dubailand.gov.ae/en/open-data/real-estate-data/

    Note: Risk scores (liquidity, demand, pricing) cannot be derived from
    DLD transaction data alone. They default to 3 (neutral) and should be
    updated by an analyst using market knowledge.

    Args:
        filepath: Path to the DLD export CSV file.

    Returns:
        List of dicts in OREIL Data Standard format.
    """
    path = Path(filepath)
    if not path.exists():
        raise FileNotFoundError(f"DLD export file not found: {filepath}")

    records = []
    with open(path, newline="", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        for i, row in enumerate(reader):
            try:
                price = float(row.get("trans_value", 0) or 0)
                rent = float(row.get("annual_amount", 0) or 0)

                # Skip rows with no price or rent data
                if price <= 0 or rent <= 0:
                    continue

                records.append({
                    "property_id": row.get("transaction_id", str(i)),
                    "location": row.get("area_name_en", "Unknown"),
                    "type": row.get("property_type_en", "Unknown"),
                    "price": price,
                    "rent": rent,
                    # Risk scores default to neutral — update per market knowledge
                    "liquidity": 3,
                    "demand": 3,
                    "pricing": 3,
                })
            except (ValueError, TypeError, KeyError):
                # Skip malformed rows silently
                continue

    return records


def validate_oreil_row(row: dict) -> dict:
    """
    Validate and coerce a single row dict into correct OREIL types.

    Args:
        row: A dict from any OREIL-standard data source.

    Returns:
        A cleaned dict with correct types.

    Raises:
        ValueError: If required fields are missing or invalid.
    """
    try:
        return {
            "property_id": row.get("property_id", ""),
            "location": str(row["location"]).strip(),
            "type": str(row["type"]).strip(),
            "price": float(row["price"]),
            "rent": float(row["rent"]),
            "liquidity": int(row["liquidity"]),
            "demand": int(row["demand"]),
            "pricing": int(row["pricing"]),
        }
    except (KeyError, ValueError, TypeError) as e:
        raise ValueError(f"Invalid OREIL row data: {e}")
