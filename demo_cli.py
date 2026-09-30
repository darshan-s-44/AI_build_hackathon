import os
import sys
import time
import glob
import json

# Ensure UTF-8 stdout encoding on Windows
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

# Ensure root directory is on PYTHONPATH
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from src.baseline_verify import run_baseline_verification
from src.agent_verify import AgenticBidVerifier
from src.export_report import generate_pdf_audit_report

def print_header(title):
    print("\n" + "=" * 75)
    print(f"  {title}")
    print("=" * 75 + "\n")

def run_interactive_demo():
    pdf_files = sorted(glob.glob("data/synthetic_bids/*.pdf"))
    if not pdf_files:
        print("Error: No test PDFs found. Running generate_test_data.py...")
        import generate_test_data
        generate_test_data.generate_all()
        pdf_files = sorted(glob.glob("data/synthetic_bids/*.pdf"))

    print_header("TENDERPULSE AI — AUTONOMOUS BID COMPLIANCE VERIFICATION DEMO\n  Sponsoring Partner: Ministry of Petroleum & Natural Gas / CPCL")
    
    print("Available CPCL Tender Bid Packages:")
    for idx, pdf in enumerate(pdf_files, 1):
        fname = os.path.basename(pdf)
        if "conditional" in fname:
            expected = "CONDITIONAL"
        elif "pass" in fname or "technip" in fname:
            expected = "PASS"
        else:
            expected = "FAIL"
        print(f" [{idx:2d}] {fname:<32} (Target Outcome: {expected:<11})")

    print("\nSelect an option:")
    print("  [1-13] Pick a specific PDF to watch live Agent verification & tool traces")
    print("  [ A ]  Run FULL benchmark (Baseline vs Agent on all 13 PDFs)")
    print("  [ Q ]  Quit")
    
    try:
        choice = input("\nEnter selection (default: 11 - conditional_msme): ").strip().upper()
    except EOFError:
        choice = "11"

    if not choice:
        choice = "11"

    if choice == "Q":
        return

    if choice == "A":
        print("\nLaunching Full Benchmark Suite...")
        from src.evaluate import run_benchmark
        run_benchmark()
        return

    try:
        idx = int(choice) - 1
        selected_pdf = pdf_files[idx]
    except Exception:
        selected_pdf = pdf_files[10] # default bid_11_conditional_msme.pdf

    filename = os.path.basename(selected_pdf)
    if "conditional" in filename:
        expected = "CONDITIONAL"
    elif "pass" in filename or "technip" in filename:
        expected = "PASS"
    else:
        expected = "FAIL"

    print_header(f"DEMONSTRATING AUDIT VERIFICATION FOR: {filename}")
    print(f"-> Target Expected Outcome : {expected}\n")

    # Step 1: Run Naive Baseline
    print("---------------------------------------------------------------------------")
    print(" 1. RUNNING INDUSTRIAL BASELINE (Numeric Regex Matching)...")
    print("---------------------------------------------------------------------------")
    time.sleep(0.2)
    base_res = run_baseline_verification(selected_pdf)
    print(f"    * Baseline Result        : {base_res['status']}")
    print(f"    * Baseline Reason        : {base_res['reason']}")
    base_correct = (base_res['status'] == expected)
    print(f"    * Baseline Accuracy Check: {'[CORRECT]' if base_correct else '[FAILED / LIMITATION DEMONSTRATED]'}\n")
    time.sleep(0.3)

    # Step 2: Run Agentic Workflow
    print("---------------------------------------------------------------------------")
    print(" 2. RUNNING TENDERPULSE AI (Deterministic + LLM + Reflection Guardrail)...")
    print("---------------------------------------------------------------------------")
    
    verifier = AgenticBidVerifier()
    agent_res = verifier.run_agent_verification(selected_pdf)

    # Display Trajectory Steps Live
    steps = agent_res.get("trajectory_steps", [])
    if steps:
        print("\n[STEP-BY-STEP AGENT EXECUTION TRAJECTORY]")
        for s in steps:
            time.sleep(0.15)
            print(f"  * Step {s['step']}: [{s.get('phase', s['action'])}]")
            if s.get("thought"):
                print(f"      Thought : {s['thought']}")
            if s.get("tool"):
                print(f"      Tool    : {s['tool']}({json.dumps(s.get('arguments', {}))})")
            if s.get("output_summary"):
                print(f"      Output  : {s['output_summary']}")

    time.sleep(0.2)
    print("\n" + "=" * 75)
    print(f" FINAL VERDICT        : {agent_res['status']}")
    print(f" CONFIDENCE RATING    : {agent_res.get('confidence', 95):.1f}% (High Reliability)")
    print(f" FRAUD RISK INDEX     : {agent_res.get('fraud_risk', 'LOW')}")
    print(f" CLAUSE REASONING     : {agent_res['reason']}")
    agent_correct = (agent_res['status'] == expected)
    print(f" EVALUATION OUTCOME   : {'[ACCURATE & VERIFIED]' if agent_correct else '[INACCURATE]'}")

    # Generate PDF Report
    eval_summary = {
        "pdf_filename": filename,
        "overall_verdict": agent_res["status"],
        "overall_confidence": agent_res.get("confidence", 95.0),
        "fraud_risk": agent_res.get("fraud_risk", "LOW"),
        "rule_breakdown": agent_res.get("rule_breakdown", [])
    }
    report_file = generate_pdf_audit_report(eval_summary)
    print(f" VIGILANCE PDF REPORT : Exported to '{report_file}'")
    print("=" * 75 + "\n")

if __name__ == "__main__":
    run_interactive_demo()
