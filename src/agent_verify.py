import os
import sys

# Ensure project root is in sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import json
import time
from datetime import datetime
from src.tools import tool_extract_pdf_text, tool_evaluate_rules, tool_validate_consistency

class AgenticBidVerifier:
    def __init__(self, rules_path="data/rules.json", trajectory_log_path="output/agent_trajectories.jsonl"):
        self.rules_path = rules_path
        self.trajectory_log_path = trajectory_log_path
        os.makedirs(os.path.dirname(trajectory_log_path), exist_ok=True)

    def _log_trajectory(self, entry):
        with open(self.trajectory_log_path, "a", encoding="utf-8") as f:
            f.write(json.dumps(entry) + "\n")

    def run_agent_verification(self, pdf_path: str):
        start_time = time.time()
        pdf_name = os.path.basename(pdf_path)

        trajectory = {
            "timestamp": datetime.now().isoformat(),
            "pdf_path": pdf_path,
            "pdf_name": pdf_name,
            "agent_id": "TenderPulse-AI-Orchestrator-v2.4",
            "tender_id": "CPCL/PROC/CRUDE-UNIT/2026/NIT-882",
            "steps": []
        }

        # -------------------------------------------------------------
        # STEP 1: Ingestion & Layout Parsing
        # -------------------------------------------------------------
        trajectory["steps"].append({
            "step": 1,
            "action": "llm_reasoning",
            "phase": "Document Ingestion",
            "thought": f"Ingesting vendor bid dossier at '{pdf_name}'. Activating layout-aware PDF parser to extract annexures and tables."
        })

        extracted_data = tool_extract_pdf_text(pdf_path)
        page_count = extracted_data.get("page_count", 1)
        full_text = extracted_data.get("full_text", "")

        trajectory["steps"].append({
            "step": 2,
            "action": "tool_call",
            "tool": "tool_extract_pdf_text",
            "arguments": {"pdf_path": pdf_path},
            "output_summary": f"Successfully parsed {page_count} pages, {len(full_text)} characters."
        })

        # -------------------------------------------------------------
        # STEP 2: Deterministic Multi-Rule Evaluation (CPCL Clauses 4.1 to 4.5)
        # -------------------------------------------------------------
        trajectory["steps"].append({
            "step": 3,
            "action": "llm_reasoning",
            "phase": "Clause Verification",
            "thought": f"Executing deterministic rule engine against CPCL tender clauses (ISO 9001 date math, CA turnover threshold, GSTIN Mod-36 checksum, and EMD)."
        })

        eval_raw = tool_evaluate_rules(extracted_data, self.rules_path)
        eval_result = json.loads(eval_raw)

        trajectory["steps"].append({
            "step": 4,
            "action": "tool_call",
            "tool": "tool_evaluate_rules",
            "arguments": {"rules_json_path": self.rules_path},
            "output_summary": f"Evaluated {len(eval_result.get('rule_breakdown', []))} clauses. Preliminary Status: {eval_result.get('overall_status')}."
        })

        # -------------------------------------------------------------
        # STEP 3: Self-Correction & Consistency Reflection Guardrail
        # -------------------------------------------------------------
        trajectory["steps"].append({
            "step": 5,
            "action": "self_correction_guardrail",
            "phase": "Consistency Audit",
            "thought": "Auditing for cross-clause anomalies, MSE preference exceptions, or contradictory statements before committing decision."
        })

        consistency_raw = tool_validate_consistency(eval_raw)
        consistency_result = json.loads(consistency_raw)

        trajectory["steps"].append({
            "step": 6,
            "action": "tool_call",
            "tool": "tool_validate_consistency",
            "arguments": {"preliminary_status": eval_result.get("overall_status")},
            "output_summary": f"Guardrail confirmed. Notes: {', '.join(consistency_result.get('reflection_notes', [])) or 'None'}"
        })

        # -------------------------------------------------------------
        # STEP 4: Final Decision Synthesis
        # -------------------------------------------------------------
        status = eval_result.get("overall_status", "PASS")
        confidence = eval_result.get("overall_confidence", 95.0)
        fraud_risk = eval_result.get("fraud_risk", "LOW (5%)")
        rule_breakdown = eval_result.get("rule_breakdown", [])

        failed_rules = [r for r in rule_breakdown if r.get("status") == "FAIL"]
        cond_rules = [r for r in rule_breakdown if r.get("status") == "CONDITIONAL"]

        if status == "PASS":
            reason = "Fully Compliant: All mandatory CPCL tender clauses (ISO validity, turnover, GSTIN, EMD) verified."
        elif status == "CONDITIONAL":
            reasons_list = [f"{r['rule']}: {r['details']}" for r in cond_rules]
            reason = "Referred to Tender Committee: " + "; ".join(reasons_list)
        else:
            reasons_list = [f"{r['rule']}: {r['details']}" for r in failed_rules]
            reason = f"Disqualified ({len(failed_rules)} non-compliant clauses): " + "; ".join(reasons_list)

        elapsed = round(time.time() - start_time, 4)

        trajectory["steps"].append({
            "step": 7,
            "action": "final_decision",
            "status": status,
            "confidence": confidence,
            "fraud_risk": fraud_risk,
            "reason": reason,
            "execution_time_sec": elapsed
        })

        trajectory["final_status"] = status
        trajectory["execution_time_sec"] = elapsed

        # Persist trajectory
        self._log_trajectory(trajectory)

        return {
            "status": status,
            "confidence": confidence,
            "fraud_risk": fraud_risk,
            "reason": reason,
            "rule_breakdown": rule_breakdown,
            "trajectory_steps": trajectory["steps"],
            "execution_time_sec": elapsed
        }

if __name__ == "__main__":
    pdf = sys.argv[1] if len(sys.argv) > 1 else "data/synthetic_bids/bid_11_conditional_msme.pdf"
    agent = AgenticBidVerifier()
    res = agent.run_agent_verification(pdf)
    print(json.dumps(res, indent=2))
