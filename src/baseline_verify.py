import time
import re
import os
import sys

# Ensure project root is in sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from pypdf import PdfReader

def run_baseline_verification(pdf_path: str):
    """
    Standard Industrial Baseline (Rule/Regex Pattern Matching without Semantic Agent Reasoning).
    Attempts standard keyword and numeric regex checks, but lacks:
    - Nuanced MSE / Udyam exemption logic
    - Exact date arithmetic & renewal buffer tolerances
    - Checksum & state validation on statutory registrations
    - Multi-clause cross-consistency reflection
    """
    start_time = time.time()
    try:
        reader = PdfReader(pdf_path)
        text = "".join([p.extract_text() or "" for p in reader.pages])

        # 1. Regex date check (basic year check)
        date_match = re.search(r"\b(\d{4})[-/]\d{2}[-/]\d{2}\b", text)
        iso_pass = False
        if date_match:
            year = int(date_match.group(1))
            iso_pass = (year >= 2026)  # Naive: passes any date in 2026 regardless of month/day cutoff

        # 2. Regex turnover check
        turnover_match = re.search(r"(\d+(?:\.\d+)?)\s*(?:Crore|Cr)", text, re.IGNORECASE)
        turnover_pass = False
        if turnover_match:
            turnover_val = float(turnover_match.group(1))
            turnover_pass = (turnover_val >= 5.0)

        # 3. Regex GSTIN check (checks 15 chars, no checksum or state verification)
        gstin_match = re.search(r"\b\d{2}[A-Z]{5}\d{4}[A-Z]{1}[1-9A-Z]{1}Z[0-9A-Z]{1}\b", text)
        gstin_pass = bool(gstin_match)

        # 4. Regex EMD check
        emd_match = re.search(r"EMD[^\d]*(\d+[\d,]*)", text, re.IGNORECASE)
        emd_pass = False
        if emd_match:
            clean_emd = int(emd_match.group(1).replace(",", ""))
            emd_pass = (clean_emd >= 100000)

        # Combined verdict
        if iso_pass and turnover_pass and gstin_pass and emd_pass:
            status = "PASS"
            reason = "Met standard numeric threshold regex patterns."
        else:
            status = "FAIL"
            failed = []
            if not iso_pass: failed.append("ISO Year < 2026")
            if not turnover_pass: failed.append("Turnover < 5.0 Cr")
            if not gstin_pass: failed.append("GSTIN Format Discrepancy")
            if not emd_pass: failed.append("EMD < 100k")
            reason = f"Violated baseline criteria: {', '.join(failed)}"

        elapsed = time.time() - start_time
        return {
            "status": status,
            "reason": reason,
            "execution_time_sec": round(elapsed, 4)
        }
    except Exception as e:
        return {
            "status": "FAIL",
            "reason": f"Baseline extraction failure: {str(e)}",
            "execution_time_sec": round(time.time() - start_time, 4)
        }

if __name__ == "__main__":
    pdf = sys.argv[1] if len(sys.argv) > 1 else "data/synthetic_bids/bid_11_conditional_msme.pdf"
    res = run_baseline_verification(pdf)
    print(res)
