def generate_report(data):
    return f"""
============================================================
       OREIL Investment Intelligence Report
============================================================
Asset         : {data['location']}
Type          : {data['type']}
Purchase Price: AED {data['price']:,}
------------------------------------------------------------
Validated Yield  : {data['yield']}%
Projection Gap   : {data['projection_gap']}%
Risk Category    : {data['risk']}
------------------------------------------------------------
Conclusion    : {data['conclusion']}
============================================================
"""
