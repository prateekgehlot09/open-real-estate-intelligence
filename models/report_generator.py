def generate_report(data):
    return f"""
OREIL Investment Intelligence Report

Location: {data['location']}
Type: {data['type']}
Price: AED {data['price']}

Yield: {data['yield']}%
Risk: {data['risk']}

Conclusion:
{data['conclusion']}
"""
