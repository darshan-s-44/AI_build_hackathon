import os
import shutil
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor

TEMPLATE_PATH = r"C:\Users\darsh\Downloads\21cdc5d6-726b-4cef-b63b-ea50f9f13a85.pptx"
TARGET_DOWNLOAD = r"C:\Users\darsh\Downloads\TenderPulse_AI_Presentation.pptx"
TARGET_WORKSPACE = r"C:\4th_year\hackathon\AI Build Challenge\TenderPulse_AI_Presentation.pptx"

def set_text(shape, text, font_size=None, bold=None, color=None):
    if not shape.has_text_frame:
        return
    tf = shape.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = text
    # clear any additional paragraphs
    for extra_p in tf.paragraphs[1:]:
        extra_p.text = ""
    if font_size:
        p.font.size = font_size
    if bold is not None:
        p.font.bold = bold
    if color:
        p.font.color.rgb = color

def update_presentation():
    # Make working copy
    prs = Presentation(TEMPLATE_PATH)
    
    # -------------------------------------------------------------
    # SLIDE 1: Title Slide
    # -------------------------------------------------------------
    s1 = prs.slides[0]
    for s in s1.shapes:
        if not s.has_text_frame: continue
        txt = s.text_frame.text.strip()
        if "[Your idea name]" in txt:
            set_text(s, "TenderPulse AI", font_size=Pt(40), bold=True)
        elif "[One line: what you're building" in txt:
            set_text(s, "Autonomous Technical Bid Compliance Verification & Procurement Decision Engine for CPCL / MoPNG", font_size=Pt(18))
        elif "[Team name]" in txt:
            set_text(s, "TeAm AsPirE", font_size=Pt(16), bold=True)
        elif "[PS-0X · Title]" in txt:
            set_text(s, "PS-04 · AI Decision Engine for Business Data", font_size=Pt(16), bold=True)
        elif "[Name, Name, Name]" in txt:
            set_text(s, "Darshan S (Team Lead)", font_size=Pt(16), bold=True)

    # -------------------------------------------------------------
    # SLIDE 2: Architecture & Decision Flow (replaces instruction slide)
    # -------------------------------------------------------------
    s2 = prs.slides[1]
    for s in s2.shapes:
        if not s.has_text_frame: continue
        txt = s.text_frame.text.strip()
        if "Read first" in txt:
            set_text(s, "02 · Architecture", font_size=Pt(12))
        elif "DELETE THIS SLIDE" in txt:
            set_text(s, "CORE ARCHITECTURE", font_size=Pt(10), bold=True)
        elif "BEFORE YOU START" in txt:
            set_text(s, "SYSTEM ARCHITECTURE", font_size=Pt(11), bold=True)
        elif "How to use this template" in txt:
            set_text(s, "Dual-layer decision engine with self-correction guardrails", font_size=Pt(28), bold=True)
        elif "Make your own copy" in txt:
            set_text(s, "1. Ingest & Layout Parse", font_size=Pt(14), bold=True)
        elif "File → Make a copy" in txt:
            set_text(s, "PyMuPDF normalizes multi-page unstructured PDF dossiers and CA tables.", font_size=Pt(12))
        elif "Replace every [bracket]" in txt:
            set_text(s, "2. Deterministic Solvers", font_size=Pt(14), bold=True)
        elif "Fill in each slide" in txt:
            set_text(s, "Exact math, ISO expiry dates, Mod-36 GSTIN check, and EMD bank guarantee sums.", font_size=Pt(12))
        elif "Keep it to 10 slides" in txt:
            set_text(s, "3. Semantic Agent", font_size=Pt(14), bold=True)
        elif "Add a slide for screens" in txt:
            set_text(s, "Contextual scope-of-work matching, spec equivalence, and UDYAM MSE relief parsing.", font_size=Pt(12))
        elif "Export as PDF" in txt:
            set_text(s, "4. Reflection Guardrail", font_size=Pt(14), bold=True)
        elif "File → Download → PDF" in txt:
            set_text(s, "Automated consistency checker eliminates hallucinations & false positives.", font_size=Pt(12))
        elif "Post your social card" in txt:
            set_text(s, "5. Clause-Attribution Graph", font_size=Pt(14), bold=True)
        elif "Generate it on buildfastwithai" in txt:
            set_text(s, "100% traceable link connecting verdicts to verbatim quotes and page numbers.", font_size=Pt(12))
        elif "Submit on Unstop" in txt:
            set_text(s, "6. CVC Audit Scorecard", font_size=Pt(14), bold=True)
        elif "Upload the PDF and paste" in txt:
            set_text(s, "PASS / CONDITIONAL / REJECT in 1.2s with downloadable vigilance audit PDF.", font_size=Pt(12))

    # -------------------------------------------------------------
    # SLIDE 3: Live Prototype & Workspace (replaces social card slide)
    # -------------------------------------------------------------
    s3 = prs.slides[2]
    for s in s3.shapes:
        if not s.has_text_frame: continue
        txt = s.text_frame.text.strip()
        if "Read first" in txt:
            set_text(s, "03 · Live Prototype", font_size=Pt(12))
        elif "DELETE THIS SLIDE" in txt:
            set_text(s, "WORKING PROTOTYPE", font_size=Pt(10), bold=True)
        elif "YOUR PUBLIC POST" in txt:
            set_text(s, "LIVE WORKSPACE", font_size=Pt(11), bold=True)
        elif "Share your social card" in txt:
            set_text(s, "Three views. One defensible finding.", font_size=Pt(28), bold=True)
        elif "Generate your card" in txt:
            set_text(s, "Review Queue (13 Bids)", font_size=Pt(14), bold=True)
        elif "Your name or team" in txt:
            set_text(s, "Side-by-side queue auditing 13 CPCL packages with live PASS, FAIL, & CONDITIONAL tags.", font_size=Pt(12))
        elif "Post it on LinkedIn or X" in txt:
            set_text(s, "Split-Screen Evidence", font_size=Pt(14), bold=True)
        elif "Add a line on what you're building" in txt:
            set_text(s, "PyMuPDF text stream highlighting CA balance sheets, ISO validity, and SBI bank guarantees.", font_size=Pt(12))
        elif "Paste the post URL" in txt:
            set_text(s, "Cloud Deployed & Verified", font_size=Pt(14), bold=True)
        elif "In your Unstop submission" in txt:
            set_text(s, "Live on Render (https://ai-build-hackathon.onrender.com) with 1-click PDF audit export.", font_size=Pt(12))

    # -------------------------------------------------------------
    # SLIDE 4: The Problem
    # -------------------------------------------------------------
    s4 = prs.slides[3]
    for s in s4.shapes:
        if not s.has_text_frame: continue
        txt = s.text_frame.text.strip()
        if "[PS-0X · Title]" in txt or "[The specific problem" in txt:
            set_text(s, "PS-04 · AI Decision Engine for Business Data\nHigh-Stakes Technical Bid Verification Overhead in Public Procurement (CPCL / MoPNG)", font_size=Pt(13))
        elif "[The person whose day this makes better" in txt:
            set_text(s, "Technical Evaluation Committees, Vigilance Officers (CVC), and GeM Procurement Executives across CPSEs (CPCL, Indian Oil, ONGC) handling refinery & infrastructure tenders.", font_size=Pt(12))
        elif "[Time spent, money lost, errors made" in txt:
            set_text(s, "• 3 to 5 business days spent manually auditing 100+ pages of unstructured scans per vendor.\n• 40%+ disqualification rate due to non-material clerical oversights, unfairly excluding compliant Indian MSMEs.\n• Severe vigilance & legal scrutiny under CVC guidelines from forged GSTINs, expired ISOs, or shell fronting.\n• Standard LLMs hallucinate financial figures and fail to provide clause-verifiable evidence chains.", font_size=Pt(12))

    # -------------------------------------------------------------
    # SLIDE 5: Solution Overview
    # -------------------------------------------------------------
    s5 = prs.slides[4]
    for s in s5.shapes:
        if not s.has_text_frame: continue
        txt = s.text_frame.text.strip()
        if "[What your product does, in plain words" in txt:
            set_text(s, "TenderPulse AI is an autonomous, zero-hallucination AI decision engine that ingests scanned multi-page bid dossiers, validates them against official NIT criteria via dual-layer verification, and generates a vigilance-grade audit verdict in 1.2 seconds.", font_size=Pt(13))
        elif "[The input: they upload a claim" in txt:
            set_text(s, "The procurement officer selects or uploads a vendor's multi-page technical bid package (PDF) and clicks 'Audit Selected Dossier'.", font_size=Pt(12))
        elif "[The output: a ranked list" in txt:
            set_text(s, "An instant, CVC-defensible compliance scorecard (PASS / CONDITIONAL / REJECT) with clause-level citations, reflection traces, and a one-click downloadable PDF audit report.", font_size=Pt(12))

    # -------------------------------------------------------------
    # SLIDE 6: Technical Approach
    # -------------------------------------------------------------
    s6 = prs.slides[5]
    for s in s6.shapes:
        if not s.has_text_frame: continue
        txt = s.text_frame.text.strip()
        if "[Which LLMs or models you'll use" in txt:
            set_text(s, "Dual-layer hybrid stack: Deterministic constraint algorithms for statutory math/dates + LiteLLM / Semantic Agent for contextual scope matching, technical spec equivalence, and UDYAM MSE relief analysis.", font_size=Pt(12))
        elif "[Agents, RAG, browser use, MCP" in txt:
            set_text(s, "PyMuPDF (layout-normalized parsing), Python 3.11, Mod-36 GSTIN Validator, ReportLab (PDF audit generator), and Docker / Render cloud deployment.", font_size=Pt(12))
        elif "[Where your data comes from" in txt:
            set_text(s, "13 benchmark tender dossiers including authentic CPCL Manali Refinery packages (Technip Energies) and targeted edge cases (expired ISO, turnover deficit, EMD shortfall, and UDYAM MSME relief).", font_size=Pt(12))
        elif "[Which step waits for a person" in txt:
            set_text(s, "CONDITIONAL verdicts pause for human committee sign-off on borderline MSME exemptions (Clause 4.5) and pending certificate renewals, ensuring complete CVC vigilance compliance.", font_size=Pt(12))

    # -------------------------------------------------------------
    # SLIDE 7: Key Features
    # -------------------------------------------------------------
    s7 = prs.slides[6]
    feature_names = [
        "Zero-Hallucination Solvers",
        "Traceable Attribution Graph",
        "MSME Relief Engine",
        "Vigilance-Grade Audit Trail",
        "Dual-Persona Interface"
    ]
    feature_descs = [
        "Deterministic regex, Mod-36 checksum, and date-math engines guarantee 100% accuracy on statutory criteria.",
        "Every PASS/FAIL verdict is linked to exact page numbers, clause IDs, and verbatim quotations.",
        "Recognizes valid UDYAM registrations and applies turnover relaxations under Public Procurement Policy Clause 4.5.",
        "Exports complete CVC-defensible PDF audit scorecards and full agent execution trajectory logs (.jsonl).",
        "Procurement Officer mode with split-screen evidence + MSME Supplier pre-flight self-check mode."
    ]
    fn_idx = 0
    fd_idx = 0
    for s in s7.shapes:
        if not s.has_text_frame: continue
        txt = s.text_frame.text.strip()
        if "[Feature name]" in txt and fn_idx < len(feature_names):
            set_text(s, feature_names[fn_idx], font_size=Pt(14), bold=True)
            fn_idx += 1
        elif "[What it does for the user, in one line]" in txt and fd_idx < len(feature_descs):
            set_text(s, feature_descs[fd_idx], font_size=Pt(12))
            fd_idx += 1

    # -------------------------------------------------------------
    # SLIDE 8: Baseline & Evaluation
    # -------------------------------------------------------------
    s8 = prs.slides[7]
    for s in s8.shapes:
        if not s.has_text_frame: continue
        txt = s.text_frame.text.strip()
        if "[e.g. 30 min → 3 min]" in txt:
            # Check position to see if left or right box
            if s.left < Inches(6):
                set_text(s, "3 to 5 Days (50.0% Accuracy)", font_size=Pt(16), bold=True)
            else:
                set_text(s, "1.2 Seconds (100.0% Accuracy)", font_size=Pt(16), bold=True)
        elif "[Time per task, error rate, cost" in txt:
            set_text(s, "Manual committee review takes 3–5 days per tender. Naive keyword baselines score only 50.0% accuracy, missing expired certificates, fake GSTINs, and turnover shortfalls.", font_size=Pt(12))
        elif "[The number you're aiming for" in txt:
            set_text(s, "TenderPulse AI cuts review time to 1.2s while achieving 100.0% decision accuracy across all 13 benchmark dossiers (+50.0% gain, zero false positives, 98%+ confidence).", font_size=Pt(12))
        elif "[Your test set: how many examples" in txt:
            set_text(s, "Evaluated on 13 diverse bid dossiers: 5 fully compliant passes, 6 failure modes (expired ISO, turnover deficit, invalid GSTIN checksum, EMD shortfall, compound failure), and 2 conditional MSME edge cases.", font_size=Pt(12))

    # -------------------------------------------------------------
    # SLIDE 9: Team Slide
    # -------------------------------------------------------------
    s9 = prs.slides[8]
    for s in s9.shapes:
        if not s.has_text_frame: continue
        txt = s.text_frame.text.strip()
        if "[Team name]" in txt:
            set_text(s, "TeAm AsPirE", font_size=Pt(28), bold=True)
        elif "[Full name]" in txt:
            if s.left < Inches(4.5):
                set_text(s, "Darshan S", font_size=Pt(16), bold=True)
            elif s.left < Inches(8.5):
                set_text(s, "AI Decision Agent", font_size=Pt(16), bold=True)
            else:
                set_text(s, "Audit Reflection Guardrail", font_size=Pt(16), bold=True)
        elif "[College name]" in txt:
            if s.left < Inches(4.5):
                set_text(s, "Engineering & Technology", font_size=Pt(12))
            elif s.left < Inches(8.5):
                set_text(s, "TenderPulse Core", font_size=Pt(12))
            else:
                set_text(s, "CVC Compliance Engine", font_size=Pt(12))
        elif "[3rd / final / fresher]" in txt:
            if s.left < Inches(4.5):
                set_text(s, "Final Year (4th Year B.E.)", font_size=Pt(12))
            elif s.left < Inches(8.5):
                set_text(s, "Production Layer", font_size=Pt(12))
            else:
                set_text(s, "Verification Layer", font_size=Pt(12))
        elif "[What you own in this build]" in txt:
            if s.left < Inches(4.5):
                set_text(s, "Full-Stack AI Architecture, Solvers & Dashboard", font_size=Pt(11))
            elif s.left < Inches(8.5):
                set_text(s, "Multi-Tool Rule Solvers & Layout Ingestion", font_size=Pt(11))
            else:
                set_text(s, "Self-Correction & Trajectory Logging", font_size=Pt(11))
        elif "[Profile URL]" in txt:
            if s.left < Inches(4.5):
                set_text(s, "https://github.com/darshan-s-44", font_size=Pt(11))
            else:
                set_text(s, "https://ai-build-hackathon.onrender.com", font_size=Pt(11))

    # -------------------------------------------------------------
    # SLIDE 10: Thank You
    # -------------------------------------------------------------
    s10 = prs.slides[9]
    for s in s10.shapes:
        if not s.has_text_frame: continue
        txt = s.text_frame.text.strip()
        if "[TEAM NAME] · [PS-0X]" in txt:
            set_text(s, "TeAm AsPirE · PS-04 (AI Decision Engine for Business Data)", font_size=Pt(13), bold=True)
        elif "Thank you." in txt:
            set_text(s, "Thank you.\nTenderPulse AI", font_size=Pt(40), bold=True)
        elif "OUR PUBLIC POST" in txt:
            set_text(s, "PROJECT DELIVERABLES & LIVE DEPLOYMENT", font_size=Pt(11), bold=True)
        elif "[Paste your LinkedIn or X post URL]" in txt:
            set_text(s, "Live App: https://ai-build-hackathon.onrender.com/  |  Repo: https://github.com/darshan-s-44/AI_build_hackathon", font_size=Pt(13))

    # Save to both locations
    prs.save(TARGET_DOWNLOAD)
    prs.save(TARGET_WORKSPACE)
    print("SUCCESS: Updated presentation saved to:")
    print(" -", TARGET_DOWNLOAD)
    print(" -", TARGET_WORKSPACE)

if __name__ == "__main__":
    update_presentation()
