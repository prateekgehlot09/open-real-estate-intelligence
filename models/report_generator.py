def generate_report(data: dict) -> str:
    """
    Generates a formatted OREIL investment intelligence report.

    Args:
        data: Dict with keys: location, type, price, yield, risk,
              projection_gap, conclusion, and optionally yield_grade.
    Returns:
        Formatted multi-line string report.
    """
    grade_line = (
        f"Yield Grade      : {data['yield_grade']}\n"
        if "yield_grade" in data else ""
    )
    return f"""
============================================================
       OREIL Investment Intelligence Report
============================================================
Asset         : {data['location']}
Type          : {data['type']}
Purchase Price: AED {data['price']:,}
------------------------------------------------------------
Validated Yield  : {data['yield']}%
{grade_line}Projection Gap   : {data['projection_gap']}%
Risk Category    : {data['risk']}
------------------------------------------------------------
Conclusion    : {data['conclusion']}
============================================================
"""
