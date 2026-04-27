# Contributing to OREIL

OREIL is an open framework. Contributions that expand its intelligence,
data coverage, or analytical depth are welcome.

---

## What We Need Most

| Area | Examples |
|---|---|
| **Market datasets** | Transaction CSVs for Abu Dhabi, Riyadh, London, Singapore |
| **Risk model improvements** | Better scoring frameworks, volatility-adjusted weights |
| **Core model expansion** | Net yield (after fees/tax), capital growth metrics |
| **AI prompt refinement** | Improved Claude prompt templates in `docs/claude_prompt.md` |
| **Test coverage** | Additional edge cases in `tests/` |
| **Documentation** | Market-specific data guides, usage tutorials |

---

## How to Contribute

```bash
# 1. Fork the repository on GitHub

# 2. Clone your fork
git clone https://github.com/YOUR_USERNAME/open-real-estate-intelligence.git
cd open-real-estate-intelligence

# 3. Create a feature branch
git checkout -b feature/your-feature-name

# 4. Install dependencies
pip install -r requirements.txt

# 5. Make your changes

# 6. Run tests before submitting
pytest tests/ -v

# 7. Commit with a clear message
git commit -m "Add Abu Dhabi sample dataset (OREIL Data Standard v0.1)"

# 8. Push and open a Pull Request
git push origin feature/your-feature-name
```

---

## Adding a New Market Dataset

1. Create a CSV in `data/` conforming to `docs/data_standard.md`
2. Include at minimum 5 properties from different sub-markets
3. Add a corresponding example report in `examples/`
4. Update `docs/data_standard.md` if you introduce optional fields

---

## Code Standards

- Python 3.8+ compatible
- Type hints on all function signatures
- Docstrings on all classes and public methods
- New logic must have corresponding tests in `tests/`
- No external dependencies in `core/` — keep it offline-capable

---

## Goal

To build the open standard for real estate investment intelligence —
a framework that any analyst, developer, or institution can adopt,
extend, and contribute to.
