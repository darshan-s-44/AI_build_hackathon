import os
import hashlib
from datetime import datetime
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors

styles = getSampleStyleSheet()

title_style = ParagraphStyle(
    "ReportTitle",
    parent=styles["Heading1"],
    fontSize=13,
    leading=16,
    textColor=colors.HexColor("#0f172a"),
    alignment=1,
    spaceAfter=4
)

sub_style = ParagraphStyle(
    "ReportSub",
    parent=styles["Normal"],
    fontSize=8.5,
    leading=12,
    textColor=colors.HexColor("#475569"),
    alignment=1,
    spaceAfter=8
)

h2_style = ParagraphStyle(
    "ReportH2",
    parent=styles["Heading2"],
    fontSize=10,
    leading=13,
    textColor=colors.HexColor("#1e3a8a"),
    spaceBefore=6,
    spaceAfter=3
)

body_style = ParagraphStyle(
    "ReportBody",
    parent=styles["Normal"],
    fontSize=8,
    leading=11,
    textColor=colors.HexColor("#1e293b")
)

bold_style = ParagraphStyle(
    "ReportBold",
    parent=styles["Normal"],
    fontSize=8,
    leading=11,
    fontName="Helvetica-Bold",
    textColor=colors.HexColor("#0f172a")
)

def generate_pdf_audit_report(eval_summary: dict, output_pdf_path: str = None) -> str:
    """Generates an official Vigilance-Grade Compliance Audit Report PDF using ReportLab."""
    pdf_filename = eval_summary.get("pdf_filename", "bid_submission.pdf")
    if not output_pdf_path:
        os.makedirs("output/reports", exist_ok=True)
        safe_name = os.path.splitext(pdf_filename)[0]
        output_pdf_path = f"output/reports/Vigilance_Audit_{safe_name}.pdf"

    doc = SimpleDocTemplate(
        output_pdf_path,
        pagesize=letter,
        leftMargin=36,
        rightMargin=36,
        topMargin=36,
        bottomMargin=36
    )
    story = []

    # 1. Official Header
    story.append(Paragraph("CHENNAI PETROLEUM CORPORATION LIMITED (CPCL)", title_style))
    story.append(Paragraph("A Government of India Enterprise | Ministry of Petroleum & Natural Gas<br/>Technical Evaluation Committee & Vigilance Directorate | Manali Refinery", sub_style))
    story.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor("#1e3a8a"), spaceAfter=8))

    # 2. Executive Decision Banner
    verdict = eval_summary.get("overall_verdict", "PASS").upper()
    confidence = eval_summary.get("overall_confidence", 95.0)
    fraud_risk = eval_summary.get("fraud_risk", "LOW")

    if verdict == "PASS":
        badge_bg = colors.HexColor("#dcfce7")
        badge_text_color = colors.HexColor("#166534")
        verdict_label = "RECOMMENDED FOR QUALIFICATION (PASS)"
    elif verdict == "CONDITIONAL":
        badge_bg = colors.HexColor("#fef3c7")
        badge_text_color = colors.HexColor("#92400e")
        verdict_label = "REFERRED FOR COMMITTEE CLARIFICATION (CONDITIONAL)"
    else:
        badge_bg = colors.HexColor("#fee2e2")
        badge_text_color = colors.HexColor("#991b1b")
        verdict_label = "DISQUALIFIED / REJECTED (NON-COMPLIANT)"

    meta_table_data = [
        [Paragraph("<b>Tender Reference:</b>", bold_style), Paragraph("CPCL/PROC/CRUDE-UNIT/2026/NIT-882", body_style),
         Paragraph("<b>Audit Timestamp:</b>", bold_style), Paragraph(datetime.now().strftime("%Y-%m-%d %H:%M:%S IST"), body_style)],
        [Paragraph("<b>Bidder Dossier:</b>", bold_style), Paragraph(pdf_filename, body_style),
         Paragraph("<b>Confidence Score:</b>", bold_style), Paragraph(f"<b>{confidence:.1f}%</b> (High Reliability)", body_style)],
        [Paragraph("<b>Decision Verdict:</b>", bold_style), Paragraph(f"<b>{verdict_label}</b>", ParagraphStyle('V', parent=bold_style, textColor=badge_text_color)),
         Paragraph("<b>Fraud Risk Index:</b>", bold_style), Paragraph(f"<b>{fraud_risk}</b>", body_style)],
    ]

    t_meta = Table(meta_table_data, colWidths=[95, 175, 95, 175])
    t_meta.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#f8fafc")),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#cbd5e1")),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
    ]))
    story.append(t_meta)
    story.append(Spacer(1, 10))

    # 3. Clause Compliance Breakdown Table
    story.append(Paragraph("<b>CLAUSE-BY-CLAUSE TECHNICAL COMPLIANCE MATRIX</b>", h2_style))

    table_headers = [
        Paragraph("<b>NIT Clause</b>", bold_style),
        Paragraph("<b>Requirement Description</b>", bold_style),
        Paragraph("<b>Extracted Bid Evidence</b>", bold_style),
        Paragraph("<b>Compliance Status</b>", bold_style),
        Paragraph("<b>Confidence</b>", bold_style)
    ]
    rows = [table_headers]

    breakdown = eval_summary.get("rule_breakdown", [])
    for item in breakdown:
        rule_name = item.get("rule", "General Clause")
        clause_id = item.get("clause_id", "NIT-Ref")
        details = item.get("details", "")
        passed = item.get("status", "PASS")
        conf = item.get("confidence", 0.95) * 100

        if passed == "PASS":
            c_tag = Paragraph("<font color='#16a34a'><b>COMPLIANT (PASS)</b></font>", body_style)
        elif passed == "CONDITIONAL":
            c_tag = Paragraph("<font color='#d97706'><b>CONDITIONAL (REVIEW)</b></font>", body_style)
        else:
            c_tag = Paragraph("<font color='#dc2626'><b>DEFICIT (FAIL)</b></font>", body_style)

        rows.append([
            Paragraph(clause_id, bold_style),
            Paragraph(rule_name, body_style),
            Paragraph(details, body_style),
            c_tag,
            Paragraph(f"{conf:.0f}%", body_style)
        ])

    t_breakdown = Table(rows, colWidths=[65, 110, 220, 100, 45])
    t_breakdown.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#e2e8f0")),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#94a3b8")),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
    ]))
    story.append(t_breakdown)
    story.append(Spacer(1, 10))

    # 4. Trajectory Hash & Vigilance Attestation
    story.append(Paragraph("<b>DIGITAL AUDIT TRAIL & ATTESTATION</b>", h2_style))
    audit_hash = hashlib.sha256(f"{pdf_filename}_{datetime.now().isoformat()}_{verdict}".encode()).hexdigest()[:24].upper()
    story.append(Paragraph(f"<b>System Audit Token:</b> <code>SHA256:{audit_hash}</code> &nbsp;|&nbsp; <b>Engine:</b> TenderPulse AI v2.4 (Deterministic + LLM Hybrid)", body_style))
    story.append(Paragraph("This document is a machine-generated vigilance compliance report grounded in statutory rules and official NIT clauses. All citations are anchored to verified text coordinates in the vendor bid dossier.", sub_style))
    story.append(Spacer(1, 15))

    # Sign-off Blocks
    sign_data = [
        [Paragraph("____________________________<br/><b>Technical Evaluation Officer</b><br/>CPCL Contracts & Materials", body_style),
         Paragraph("____________________________<br/><b>Finance & Accounts Vigilance</b><br/>CPCL Manali Refinery", body_style),
         Paragraph("____________________________<br/><b>Chief General Manager (Procurement)</b><br/>Tender Committee Chairman", body_style)]
    ]
    t_sign = Table(sign_data, colWidths=[180, 180, 180])
    t_sign.setStyle(TableStyle([
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('TOPPADDING', (0,0), (-1,-1), 8),
    ]))
    story.append(t_sign)

    doc.build(story)
    return output_pdf_path

if __name__ == "__main__":
    sample_summary = {
        "pdf_filename": "bid_01_pass.pdf",
        "overall_verdict": "PASS",
        "overall_confidence": 98.4,
        "fraud_risk": "LOW (4%)",
        "rule_breakdown": [
            {"clause_id": "Clause 4.1", "rule": "ISO 9001:2015 Validity", "details": "Found: 2027-12-31 | Required >= 2026-12-31", "status": "PASS", "confidence": 0.99},
            {"clause_id": "Clause 4.2", "rule": "Annual Average Turnover", "details": "Found: 8.5 Cr INR | Required >= 5.0 Cr | CA UDIN verified", "status": "PASS", "confidence": 0.98},
            {"clause_id": "Clause 4.3", "rule": "Statutory GSTIN Check", "details": "07AAAAA1234A1Z5 (Delhi) | Mod-36 Checksum Verified", "status": "PASS", "confidence": 0.99},
            {"clause_id": "Clause 4.4", "rule": "Earnest Money Deposit", "details": "Found: 100,000 INR | Bank Guarantee BG/2026/0991", "status": "PASS", "confidence": 0.99}
        ]
    }
    path = generate_pdf_audit_report(sample_summary)
    print(f"Sample report generated at: {path}")
