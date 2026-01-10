## IG_TRACKER — Instagram Message Analyzer

A lightweight analyzer for Instagram messages and enquiries. IG_TRACKER extracts detected products, categorizes question types, evaluates sentiment, and assigns urgency and lead-segmentation tags. It produces reports under `reports/` and writes logs to `logs/`.

Contents
- `app.py` — Streamlit frontend (entrypoint)
- `config.py` — Configuration and constants
- `daily_analyzer.py` — Batch analysis driver for daily reports
- `product_detector.py` — Product matching and detection logic
- `question_analyzer.py` — Question classification and intent detection
- `sentiment_analyzer.py` — Sentiment scoring and simple heuristics
- `requirements.txt` — Python dependencies
- `setup.py` — Packaging / helper tasks

Quick Start
1. Create a virtual environment and install dependencies:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

2. Run the Streamlit app locally:

```powershell
streamlit run app.py
```

3. To run the daily analyzer manually:

```powershell
python daily_analyzer.py
```

Configuration
- Edit `config.py` to set input paths, API keys, or thresholds (urgency, sentiment cutoffs).

Input & Output
- Input: expects an Excel/CSV file formatted same as original ingestion (customer message, timestamp, user id).
- Output: reports are written to `reports/` with subfolders `daily/`, `weekly/`, and `priority/`. Processed files move to `archive/processed/`.

Core Features
- Product detection: extensive product list matching (brand + model heuristics).
- Question classification: maps messages into predefined question categories.
- Sentiment analysis: simple polarity scoring to flag negative/positive messages.
- Urgency scoring: numeric scale used to prioritize responses.
- Lead segmentation: tags messages as Hot/Warm/Cold/VIP for follow-up.

How to extend
- Add new products or keywords in `product_detector.py` (follow existing patterns).
- Add new categories in `question_analyzer.py` and update mapping tables.
- Replace `sentiment_analyzer.py` with a model-backed approach if higher accuracy is needed.

Recommended Workflow
1. Place input file in the project root or configure path in `config.py`.
2. Run `python daily_analyzer.py` to process and generate reports.
3. Review outputs in `reports/daily/` and check `logs/` for processing details.

Testing
- There is no dedicated test suite in this repo. To validate changes manually, run `daily_analyzer.py` against a small sample of messages and inspect generated reports.

Contributing
- Fork the repo, create a feature branch, and open a PR with a clear description of the changes.

License
- This project has no license file. Add `LICENSE` if you plan to open-source it.

Contact
- For questions about the implementation, inspect `app.py` and `daily_analyzer.py` or open an issue in the project tracker.

----

Notes
- This README is intentionally concise and targeted at getting you running quickly. If you want the older, extended documentation index restored, tell me and I will add a `docs/` folder with the longer markdown files.


Coverage: 100% of changes documented
```

---

## 🏁 GET STARTED

### 1. Quick Overview (5 min)
→ Read: **[IMPROVEMENTS_SUMMARY.md](IMPROVEMENTS_SUMMARY.md)**

### 2. Try It Out (2 min)
→ Upload Excel and analyze (improvements are automatic!)

### 3. Learn Details (15 min)
→ Read: **[QUICK_REFERENCE.md](QUICK_REFERENCE.md)**

### 4. Validate (30 min)
→ Follow: **[TESTING_GUIDE.md](TESTING_GUIDE.md)**

### 5. Go Live! ✨
→ All improvements ready to use!

---

**Version:** 2.0 (Enhanced)  
**Status:** ✅ Production Ready  
**Updated:** January 9, 2026

**Welcome to your upgraded analyzer!** 🚀
