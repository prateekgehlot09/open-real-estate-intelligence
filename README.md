## Run Locally

Requires Python 3.8+.

```bash
# Clone the repo
git clone https://github.com/prateekgehlot09/open-real-estate-intelligence.git
cd open-real-estate-intelligence

# Install dependencies
pip install -r requirements.txt

# Run CLI — with AI analysis (requires Anthropic API key)
export ANTHROPIC_API_KEY=your_key_here
python main.py

# Run CLI — without AI (no API key needed)
python main.py --no-ai

# Filter by market
python main.py --market "Business Bay" --no-ai

# Save report to file
python main.py --output reports/dubai_analysis.txt

# Run the intelligence dashboard
streamlit run dashboard/app.py

# Run the REST API
uvicorn api.main:app --reload
# Interactive docs: http://localhost:8000/docs

# Run tests
pytest tests/ -v
```
