import http.server
import socketserver
import json
import os
import sys
import glob
import urllib.parse

# Ensure UTF-8 stdout encoding on Windows
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

# Ensure root directory is in sys.path
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from src.agent_verify import AgenticBidVerifier
from src.baseline_verify import run_baseline_verification
from src.gstin_validator import verify_gstin
from src.export_report import generate_pdf_audit_report
from src.tools import tool_extract_pdf_text

PORT = 8080

class DemoAPIHandler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        super().end_headers()

    def do_OPTIONS(self):
        self.send_response(200)
        self.end_headers()

    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        query = urllib.parse.parse_qs(parsed.query)
        
        # 1. List Available Bids
        if parsed.path == "/api/list_bids":
            bids = sorted(glob.glob("data/synthetic_bids/*.pdf"))
            bid_list = []
            for b in bids:
                fname = os.path.basename(b)
                if "conditional" in fname:
                    expected = "CONDITIONAL"
                elif "pass" in fname or "technip" in fname:
                    expected = "PASS"
                else:
                    expected = "FAIL"
                label = fname.replace(".pdf", "").replace("_", " ").title()
                bid_list.append({"filename": fname, "label": label, "expected": expected})
            
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"bids": bid_list}).encode("utf-8"))
            return

        # 2. Return CPCL Tender Rules
        elif parsed.path == "/api/rules":
            rules_file = "data/rules.json"
            rules_data = {}
            if os.path.exists(rules_file):
                with open(rules_file, "r", encoding="utf-8") as f:
                    rules_data = json.load(f)
            
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(rules_data).encode("utf-8"))
            return

        # 3. Live GSTIN Verification API
        elif parsed.path == "/api/verify_gstin":
            gstin_val = query.get("gstin", ["33AAACT9988P1ZC"])[0]
            res = verify_gstin(gstin_val)
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(res).encode("utf-8"))
            return

        # 4. Extract PDF Text & Clause Metadata for Split-Screen Viewer
        elif parsed.path == "/api/pdf_text":
            fname = query.get("filename", [""])[0]
            pdf_path = os.path.join("data/synthetic_bids", fname)
            if not os.path.exists(pdf_path):
                self.send_response(404)
                self.end_headers()
                self.wfile.write(b'{"error": "File not found"}')
                return
            
            extracted = tool_extract_pdf_text(pdf_path)
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(extracted).encode("utf-8"))
            return

        # 5. One-Click Export PDF Audit Report
        elif parsed.path == "/api/export_pdf_report":
            fname = query.get("filename", [""])[0]
            pdf_path = os.path.join("data/synthetic_bids", fname)
            if not os.path.exists(pdf_path):
                self.send_response(404)
                self.end_headers()
                self.wfile.write(b"Bid dossier not found.")
                return

            verifier = AgenticBidVerifier()
            agent_res = verifier.run_agent_verification(pdf_path)

            eval_summary = {
                "pdf_filename": fname,
                "overall_verdict": agent_res.get("status", "PASS"),
                "overall_confidence": agent_res.get("confidence", 95.0),
                "fraud_risk": agent_res.get("fraud_risk", "LOW (5%)"),
                "rule_breakdown": agent_res.get("rule_breakdown", [])
            }

            report_path = generate_pdf_audit_report(eval_summary)
            if os.path.exists(report_path):
                with open(report_path, "rb") as f:
                    pdf_bytes = f.read()
                self.send_response(200)
                self.send_header("Content-Type", "application/pdf")
                self.send_header("Content-Disposition", f'attachment; filename="Vigilance_Audit_{fname}"')
                self.send_header("Content-Length", str(len(pdf_bytes)))
                self.send_header("Cache-Control", "no-cache, no-store, must-revalidate")
                self.end_headers()
                self.wfile.write(pdf_bytes)
                return
            else:
                self.send_response(500)
                self.end_headers()
                self.wfile.write(b"Failed to generate report PDF")
                return

        # 6. Serve static files from web/
        clean_path = parsed.path
        if clean_path in ["/", "/index.html"]:
            self.path = "/web/index.html"
        elif not clean_path.startswith("/api/"):
            rel_path = clean_path.lstrip("/")
            web_file = os.path.join("web", rel_path)
            if os.path.exists(web_file) and not os.path.isdir(web_file):
                self.path = f"/web/{rel_path}"

        return super().do_GET()

    def do_POST(self):
        parsed = urllib.parse.urlparse(self.path)
        
        if parsed.path == "/api/verify":
            content_len = int(self.headers.get('Content-Length', 0))
            post_body = self.rfile.read(content_len)
            data = json.loads(post_body.decode('utf-8'))
            
            filename = data.get("filename", "")
            pdf_path = os.path.join("data/synthetic_bids", filename)
            
            if not os.path.exists(pdf_path):
                self.send_response(404)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps({"error": f"File {filename} not found"}).encode("utf-8"))
                return

            # Run baseline
            baseline_res = run_baseline_verification(pdf_path)
            
            # Run agent
            verifier = AgenticBidVerifier()
            agent_res = verifier.run_agent_verification(pdf_path)
            
            # Extract PDF text for split screen preview
            extracted_text_data = tool_extract_pdf_text(pdf_path)
            
            # Fetch latest trajectory
            trajectories = agent_res.get("trajectory_steps", [])
            
            # Expected verdict
            if "conditional" in filename:
                expected = "CONDITIONAL"
            elif "pass" in filename or "technip" in filename:
                expected = "PASS"
            else:
                expected = "FAIL"
            
            response_payload = {
                "filename": filename,
                "expected": expected,
                "baseline": baseline_res,
                "agent": agent_res,
                "pdf_preview": extracted_text_data,
                "trajectories": trajectories
            }
            
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(response_payload).encode("utf-8"))
            return

class ReuseTCPServer(socketserver.TCPServer):
    allow_reuse_address = True

def start_server():
    os.makedirs("web", exist_ok=True)
    handler = DemoAPIHandler
    
    env_port = os.environ.get("PORT")
    ports_to_try = [int(env_port)] if env_port else [8080, 8081, 8082, 8090, 9000, 0]
    httpd = None
    actual_port = None

    for port in ports_to_try:
        try:
            httpd = ReuseTCPServer(("", port), handler)
            actual_port = httpd.socket.getsockname()[1]
            break
        except OSError:
            continue

    if not httpd:
        print("Error: Could not find an open port for web server.")
        return

    print(f"\n=========================================================", flush=True)
    print(f" 🚀 TENDERPULSE AI WEB SERVER RUNNING AT: http://localhost:{actual_port}", flush=True)
    print(f" Open http://localhost:{actual_port} in your browser to view the platform!", flush=True)
    print(f"=========================================================\n", flush=True)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nServer stopped.", flush=True)

if __name__ == "__main__":
    start_server()
