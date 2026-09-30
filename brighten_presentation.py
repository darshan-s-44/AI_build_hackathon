import os
import shutil
import zipfile
import numpy as np
import cv2
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor

TEMPLATE_PATH = r"C:\Users\darsh\Downloads\21cdc5d6-726b-4cef-b63b-ea50f9f13a85.pptx"
TARGET_DOWNLOAD = r"C:\Users\darsh\Downloads\TenderPulse_AI_Presentation.pptx"
TARGET_WORKSPACE = r"C:\4th_year\hackathon\AI Build Challenge\TenderPulse_AI_Presentation.pptx"

# Luminous, ultra-readable high-contrast palette
COLOR_WHITE = RGBColor(255, 255, 255)         # Pure bright white for titles & primary values
COLOR_BODY = RGBColor(248, 250, 252)          # Ultra-crisp bright off-white for paragraphs & lists
COLOR_GOLD = RGBColor(255, 215, 120)          # Warm luminous gold (#FFD778) for accents & cards
COLOR_AMBER = RGBColor(245, 185, 55)          # Amber gold (#F5B937) for category badges & tags
COLOR_HEADER = RGBColor(225, 230, 240)        # Crisp silver-white for top navigation & slide numbers
COLOR_PILL_TEXT = RGBColor(20, 20, 20)        # Crisp dark text inside bright yellow button pills

def set_text(shape, text, font_size=None, bold=None, color=COLOR_WHITE):
    """Sets text on a shape and guarantees every paragraph and run receives explicit bright styling."""
    if not shape.has_text_frame:
        return
    tf = shape.text_frame
    tf.word_wrap = True
    
    lines = text.split("\n")
    for i, line in enumerate(lines):
        if i < len(tf.paragraphs):
            p = tf.paragraphs[i]
        else:
            p = tf.add_paragraph()
        p.text = line
        if font_size:
            p.font.size = font_size
        if bold is not None:
            p.font.bold = bold
        if color:
            p.font.color.rgb = color
            
        # Crucial for PowerPoint: explicitly style each run inside the paragraph
        for r in p.runs:
            if font_size:
                r.font.size = font_size
            if bold is not None:
                r.font.bold = bold
            if color:
                r.font.color.rgb = color
            
    # Clear any extra trailing paragraphs
    for extra_p in tf.paragraphs[len(lines):]:
        extra_p.text = ""
        for r in extra_p.runs:
            r.text = ""

def build_brightened_presentation():
    print("Loading official hackathon template...")
    prs = Presentation(TEMPLATE_PATH)
    
    # -------------------------------------------------------------
    # SLIDE 1: Title Slide
    # -------------------------------------------------------------
    s1 = prs.slides[0]
    for s in s1.shapes:
        if not s.has_text_frame: continue
        txt = s.text_frame.text.strip()
        if "[Your idea name]" in txt:
            set_text(s, "TenderPulse AI", font_size=Pt(44), bold=True, color=COLOR_WHITE)
        elif "[One line: what you're building" in txt:
            set_text(s, "Autonomous Technical Bid Compliance Verification & Procurement Decision Engine for CPCL / MoPNG", font_size=Pt(19), bold=False, color=COLOR_GOLD)
        elif "[Team name]" in txt:
            set_text(s, "TeAm AsPirE", font_size=Pt(17), bold=True, color=COLOR_WHITE)
        elif "[PS-0X · Title]" in txt:
            set_text(s, "PS-04 · AI Decision Engine for Business Data", font_size=Pt(17), bold=True, color=COLOR_WHITE)
        elif "[Name, Name, Name]" in txt:
            set_text(s, "Darshan S (Team Lead)", font_size=Pt(17), bold=True, color=COLOR_WHITE)

    # -------------------------------------------------------------
    # SLIDE 2: Architecture & Decision Flow
    # -------------------------------------------------------------
    s2 = prs.slides[1]
    for s in s2.shapes:
        if not s.has_text_frame: continue
        txt = s.text_frame.text.strip()
        if "Read first" in txt:
            set_text(s, "02 · Architecture", font_size=Pt(13), color=COLOR_HEADER)
        elif "DELETE THIS SLIDE" in txt:
            set_text(s, "CORE ARCHITECTURE", font_size=Pt(11), bold=True, color=COLOR_PILL_TEXT)
        elif "BEFORE YOU START" in txt:
            set_text(s, "SYSTEM ARCHITECTURE", font_size=Pt(12), bold=True, color=COLOR_AMBER)
        elif "How to use this template" in txt:
            set_text(s, "Dual-layer decision engine with self-correction guardrails", font_size=Pt(28), bold=True, color=COLOR_WHITE)
        elif "Make your own copy" in txt:
            set_text(s, "1. Ingest & Layout Parse", font_size=Pt(14), bold=True, color=COLOR_GOLD)
        elif "File → Make a copy" in txt:
            set_text(s, "PyMuPDF normalizes multi-page unstructured PDF dossiers and CA tables.", font_size=Pt(12), color=COLOR_BODY)
        elif "Replace every [bracket]" in txt:
            set_text(s, "2. Deterministic Solvers", font_size=Pt(14), bold=True, color=COLOR_GOLD)
        elif "Fill in each slide" in txt:
            set_text(s, "Exact math, ISO expiry dates, Mod-36 GSTIN check, and EMD bank guarantee sums.", font_size=Pt(12), color=COLOR_BODY)
        elif "Keep it to 10 slides" in txt:
            set_text(s, "3. Semantic Agent", font_size=Pt(14), bold=True, color=COLOR_GOLD)
        elif "Add a slide for screens" in txt:
            set_text(s, "Contextual scope-of-work matching, spec equivalence, and UDYAM MSE relief parsing.", font_size=Pt(12), color=COLOR_BODY)
        elif "Export as PDF" in txt:
            set_text(s, "4. Reflection Guardrail", font_size=Pt(14), bold=True, color=COLOR_GOLD)
        elif "File → Download → PDF" in txt:
            set_text(s, "Automated consistency checker eliminates hallucinations & false positives.", font_size=Pt(12), color=COLOR_BODY)
        elif "Post your social card" in txt:
            set_text(s, "5. Clause-Attribution Graph", font_size=Pt(14), bold=True, color=COLOR_GOLD)
        elif "Generate it on buildfastwithai" in txt:
            set_text(s, "100% traceable link connecting verdicts to verbatim quotes and page numbers.", font_size=Pt(12), color=COLOR_BODY)
        elif "Submit on Unstop" in txt:
            set_text(s, "6. CVC Audit Scorecard", font_size=Pt(14), bold=True, color=COLOR_GOLD)
        elif "Upload the PDF and paste" in txt:
            set_text(s, "PASS / CONDITIONAL / REJECT in 1.2s with downloadable vigilance audit PDF.", font_size=Pt(12), color=COLOR_BODY)

    # -------------------------------------------------------------
    # SLIDE 3: Live Prototype & Workspace
    # -------------------------------------------------------------
    s3 = prs.slides[2]
    for s in s3.shapes:
        if not s.has_text_frame: continue
        txt = s.text_frame.text.strip()
        if "Read first" in txt:
            set_text(s, "03 · Live Prototype", font_size=Pt(13), color=COLOR_HEADER)
        elif "DELETE THIS SLIDE" in txt:
            set_text(s, "WORKING PROTOTYPE", font_size=Pt(11), bold=True, color=COLOR_PILL_TEXT)
        elif "YOUR PUBLIC POST" in txt:
            set_text(s, "LIVE WORKSPACE", font_size=Pt(12), bold=True, color=COLOR_AMBER)
        elif "Share your social card" in txt:
            set_text(s, "Three views. One defensible finding.", font_size=Pt(28), bold=True, color=COLOR_WHITE)
        elif "Generate your card" in txt:
            set_text(s, "Review Queue (13 Bids)", font_size=Pt(14), bold=True, color=COLOR_GOLD)
        elif "Your name or team" in txt:
            set_text(s, "Side-by-side queue auditing 13 CPCL packages with live PASS, FAIL, & CONDITIONAL tags.", font_size=Pt(12), color=COLOR_BODY)
        elif "Post it on LinkedIn or X" in txt:
            set_text(s, "Split-Screen Evidence", font_size=Pt(14), bold=True, color=COLOR_GOLD)
        elif "Add a line on what you're building" in txt:
            set_text(s, "PyMuPDF text stream highlighting CA balance sheets, ISO validity, and SBI bank guarantees.", font_size=Pt(12), color=COLOR_BODY)
        elif "Paste the post URL" in txt:
            set_text(s, "Cloud Deployed & Verified", font_size=Pt(14), bold=True, color=COLOR_GOLD)
        elif "In your Unstop submission" in txt:
            set_text(s, "Live on Render (https://ai-build-hackathon.onrender.com) with 1-click PDF audit export.", font_size=Pt(12), color=COLOR_BODY)

    # -------------------------------------------------------------
    # SLIDE 4: The Problem
    # -------------------------------------------------------------
    s4 = prs.slides[3]
    for s in s4.shapes:
        if not s.has_text_frame: continue
        txt = s.text_frame.text.strip()
        if "[PS-0X · Title]" in txt or "[The specific problem" in txt:
            set_text(s, "PS-04 · AI Decision Engine for Business Data\nHigh-Stakes Technical Bid Verification Overhead in Public Procurement (CPCL / MoPNG)", font_size=Pt(13), bold=False, color=COLOR_BODY)
        elif "[The person whose day this makes better" in txt:
            set_text(s, "Technical Evaluation Committees, Vigilance Officers (CVC), and GeM Procurement Executives across CPSEs (CPCL, Indian Oil, ONGC) handling refinery & infrastructure tenders.", font_size=Pt(12), color=COLOR_BODY)
        elif "[Time spent, money lost, errors made" in txt:
            set_text(s, "• 3 to 5 business days spent manually auditing 100+ pages of unstructured scans per vendor.\n• 40%+ disqualification rate due to non-material clerical oversights, unfairly excluding compliant Indian MSMEs.\n• Severe vigilance & legal scrutiny under CVC guidelines from forged GSTINs, expired ISOs, or shell fronting.\n• Standard LLMs hallucinate financial figures and fail to provide clause-verifiable evidence chains.", font_size=Pt(12), color=COLOR_BODY)

    # -------------------------------------------------------------
    # SLIDE 5: Solution Overview
    # -------------------------------------------------------------
    s5 = prs.slides[4]
    for s in s5.shapes:
        if not s.has_text_frame: continue
        txt = s.text_frame.text.strip()
        if "[What your product does, in plain words" in txt:
            set_text(s, "TenderPulse AI is an autonomous, zero-hallucination AI decision engine that ingests scanned multi-page bid dossiers, validates them against official NIT criteria via dual-layer verification, and generates a vigilance-grade audit verdict in 1.2 seconds.", font_size=Pt(13), color=COLOR_BODY)
        elif "[The input: they upload a claim" in txt:
            set_text(s, "The procurement officer selects or uploads a vendor's multi-page technical bid package (PDF) and clicks 'Audit Selected Dossier'.", font_size=Pt(12), color=COLOR_BODY)
        elif "[The output: a ranked list" in txt:
            set_text(s, "An instant, CVC-defensible compliance scorecard (PASS / CONDITIONAL / REJECT) with clause-level citations, reflection traces, and a one-click downloadable PDF audit report.", font_size=Pt(12), color=COLOR_BODY)

    # -------------------------------------------------------------
    # SLIDE 6: Technical Approach
    # -------------------------------------------------------------
    s6 = prs.slides[5]
    for s in s6.shapes:
        if not s.has_text_frame: continue
        txt = s.text_frame.text.strip()
        if "[Which LLMs or models you'll use" in txt:
            set_text(s, "Dual-layer hybrid stack: Deterministic constraint algorithms for statutory math/dates + LiteLLM / Semantic Agent for contextual scope matching, technical spec equivalence, and UDYAM MSE relief analysis.", font_size=Pt(12), color=COLOR_BODY)
        elif "[Agents, RAG, browser use, MCP" in txt:
            set_text(s, "PyMuPDF (layout-normalized parsing), Python 3.11, Mod-36 GSTIN Validator, ReportLab (PDF audit generator), and Docker / Render cloud deployment.", font_size=Pt(12), color=COLOR_BODY)
        elif "[Where your data comes from" in txt:
            set_text(s, "13 benchmark tender dossiers including authentic CPCL Manali Refinery packages (Technip Energies) and targeted edge cases (expired ISO, turnover deficit, EMD shortfall, and UDYAM MSME relief).", font_size=Pt(12), color=COLOR_BODY)
        elif "[Which step waits for a person" in txt:
            set_text(s, "CONDITIONAL verdicts pause for human committee sign-off on borderline MSME exemptions (Clause 4.5) and pending certificate renewals, ensuring complete CVC vigilance compliance.", font_size=Pt(12), color=COLOR_BODY)

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
            set_text(s, feature_names[fn_idx], font_size=Pt(14), bold=True, color=COLOR_GOLD)
            fn_idx += 1
        elif "[What it does for the user, in one line]" in txt and fd_idx < len(feature_descs):
            set_text(s, feature_descs[fd_idx], font_size=Pt(12), color=COLOR_BODY)
            fd_idx += 1

    # -------------------------------------------------------------
    # SLIDE 8: Baseline & Evaluation
    # -------------------------------------------------------------
    s8 = prs.slides[7]
    for s in s8.shapes:
        if not s.has_text_frame: continue
        txt = s.text_frame.text.strip()
        if "[e.g. 30 min → 3 min]" in txt:
            if s.left < Inches(6):
                set_text(s, "3 to 5 Days (50.0% Accuracy)", font_size=Pt(17), bold=True, color=COLOR_WHITE)
            else:
                set_text(s, "1.2 Seconds (100.0% Accuracy)", font_size=Pt(17), bold=True, color=COLOR_GOLD)
        elif "[Time per task, error rate, cost" in txt:
            set_text(s, "Manual committee review takes 3–5 days per tender. Naive keyword baselines score only 50.0% accuracy, missing expired certificates, fake GSTINs, and turnover shortfalls.", font_size=Pt(12), color=COLOR_BODY)
        elif "[The number you're aiming for" in txt:
            set_text(s, "TenderPulse AI cuts review time to 1.2s while achieving 100.0% decision accuracy across all 13 benchmark dossiers (+50.0% gain, zero false positives, 98%+ confidence).", font_size=Pt(12), color=COLOR_BODY)
        elif "[Your test set: how many examples" in txt:
            set_text(s, "Evaluated on 13 diverse bid dossiers: 5 fully compliant passes, 6 failure modes (expired ISO, turnover deficit, invalid GSTIN checksum, EMD shortfall, compound failure), and 2 conditional MSME edge cases.", font_size=Pt(12), color=COLOR_BODY)

    # -------------------------------------------------------------
    # SLIDE 9: Team Slide
    # -------------------------------------------------------------
    s9 = prs.slides[8]
    for s in s9.shapes:
        if not s.has_text_frame: continue
        txt = s.text_frame.text.strip()
        if "[Team name]" in txt:
            set_text(s, "TeAm AsPirE", font_size=Pt(28), bold=True, color=COLOR_WHITE)
        elif "[Full name]" in txt:
            if s.left < Inches(4.5):
                set_text(s, "Darshan S", font_size=Pt(17), bold=True, color=COLOR_GOLD)
            elif s.left < Inches(8.5):
                set_text(s, "AI Decision Agent", font_size=Pt(17), bold=True, color=COLOR_GOLD)
            else:
                set_text(s, "Audit Reflection Guardrail", font_size=Pt(17), bold=True, color=COLOR_GOLD)
        elif "[College name]" in txt:
            if s.left < Inches(4.5):
                set_text(s, "Engineering & Technology", font_size=Pt(12), color=COLOR_BODY)
            elif s.left < Inches(8.5):
                set_text(s, "TenderPulse Core", font_size=Pt(12), color=COLOR_BODY)
            else:
                set_text(s, "CVC Compliance Engine", font_size=Pt(12), color=COLOR_BODY)
        elif "[3rd / final / fresher]" in txt:
            if s.left < Inches(4.5):
                set_text(s, "Final Year (4th Year B.E.)", font_size=Pt(12), color=COLOR_BODY)
            elif s.left < Inches(8.5):
                set_text(s, "Production Layer", font_size=Pt(12), color=COLOR_BODY)
            else:
                set_text(s, "Verification Layer", font_size=Pt(12), color=COLOR_BODY)
        elif "[What you own in this build]" in txt:
            if s.left < Inches(4.5):
                set_text(s, "Full-Stack AI Architecture, Solvers & Dashboard", font_size=Pt(11), color=COLOR_BODY)
            elif s.left < Inches(8.5):
                set_text(s, "Multi-Tool Rule Solvers & Layout Ingestion", font_size=Pt(11), color=COLOR_BODY)
            else:
                set_text(s, "Self-Correction & Trajectory Logging", font_size=Pt(11), color=COLOR_BODY)
        elif "[Profile URL]" in txt:
            if s.left < Inches(4.5):
                set_text(s, "https://github.com/darshan-s-44", font_size=Pt(11), color=COLOR_GOLD)
            else:
                set_text(s, "https://ai-build-hackathon.onrender.com", font_size=Pt(11), color=COLOR_GOLD)

    # -------------------------------------------------------------
    # SLIDE 10: Thank You
    # -------------------------------------------------------------
    s10 = prs.slides[9]
    for s in s10.shapes:
        if not s.has_text_frame: continue
        txt = s.text_frame.text.strip()
        if "[TEAM NAME] · [PS-0X]" in txt:
            set_text(s, "TeAm AsPirE · PS-04 (AI Decision Engine for Business Data)", font_size=Pt(14), bold=True, color=COLOR_AMBER)
        elif "Thank you." in txt:
            set_text(s, "Thank you.\nTenderPulse AI", font_size=Pt(42), bold=True, color=COLOR_WHITE)
        elif "OUR PUBLIC POST" in txt:
            set_text(s, "PROJECT DELIVERABLES & LIVE DEPLOYMENT", font_size=Pt(12), bold=True, color=COLOR_AMBER)
        elif "[Paste your LinkedIn or X post URL]" in txt:
            set_text(s, "Live App: https://ai-build-hackathon.onrender.com/  |  Repo: https://github.com/darshan-s-44/AI_build_hackathon", font_size=Pt(14), color=COLOR_GOLD)

    # -------------------------------------------------------------
    # UNIVERSAL BRIGHTENING & CONTRAST PASS ACROSS ALL SHAPES
    # -------------------------------------------------------------
    print("Running universal brightening pass across all slides and shapes...")
    total_brightened = 0
    for s_idx, slide in enumerate(prs.slides):
        for shp in slide.shapes:
            if not shp.has_text_frame:
                continue
            tf = shp.text_frame
            full_txt = tf.text.strip()
            if not full_txt:
                continue
                
            is_yellow_pill = ("CORE ARCHITECTURE" in full_txt or "WORKING PROTOTYPE" in full_txt)
            
            for p in tf.paragraphs:
                p_clr = getattr(getattr(p.font, 'color', None), 'rgb', None)
                for r in p.runs:
                    txt = r.text.strip()
                    if not txt:
                        continue
                        
                    if is_yellow_pill:
                        r.font.color.rgb = COLOR_PILL_TEXT
                        r.font.bold = True
                        continue
                        
                    r_clr = getattr(getattr(r.font, 'color', None), 'rgb', None)
                    needs_brighten = False
                    if r_clr is None:
                        needs_brighten = True
                    else:
                        lum = 0.299 * r_clr[0] + 0.587 * r_clr[1] + 0.114 * r_clr[2]
                        if lum < 130: # Dim gray, dark brown, or black
                            needs_brighten = True
                            
                    if needs_brighten:
                        total_brightened += 1
                        if p_clr is not None:
                            p_lum = 0.299 * p_clr[0] + 0.587 * p_clr[1] + 0.114 * p_clr[2]
                            if p_lum >= 130:
                                r.font.color.rgb = p_clr
                                continue
                                
                        # Contextual assignment for unassigned runs:
                        if txt in ["01", "02", "03", "04", "05", "06", "1", "2", "3", "4", "5", "6"]:
                            r.font.color.rgb = COLOR_GOLD
                            r.font.bold = True
                        elif txt.isupper() and len(txt) <= 30:
                            r.font.color.rgb = COLOR_AMBER
                            r.font.bold = True
                        elif any(k in txt for k in ["· The problem", "· Solution overview", "· Technical approach", "· Key features", "· Baseline", "· Team", "/ 10", "hackathon"]):
                            r.font.color.rgb = COLOR_HEADER
                        elif s_idx == 0: # Slide 1 items
                            r.font.color.rgb = COLOR_WHITE
                        else:
                            r.font.color.rgb = COLOR_BODY

    print(f"Total runs brightened across all slides: {total_brightened}")

    # Save intermediate presentation
    prs.save("temp_brightened.pptx")
    print("Intermediate presentation saved.")

    # -------------------------------------------------------------
    # 2. BACKGROUND TEXTURE BRIGHTENING
    # -------------------------------------------------------------
    # Smoothly lift the pitch-black background images to a deep luminous studio glow
    temp_dir = "temp_pptx_brighten"
    if os.path.exists(temp_dir):
        shutil.rmtree(temp_dir)
    with zipfile.ZipFile("temp_brightened.pptx", "r") as z:
        z.extractall(temp_dir)

    for img_name in ['image2.png', 'image3.png', 'image4.png', 'image5.png']:
        img_path = os.path.join(temp_dir, 'ppt', 'media', img_name)
        if os.path.exists(img_path):
            img = cv2.imread(img_path)
            # Smoothly lift brightness from pitch black (~13) to deep luminous studio tone (~54):
            # formula: val * 1.5 + 34
            brightened = np.clip(img.astype(float) * 1.5 + 34, 0, 255).astype('uint8')
            cv2.imwrite(img_path, brightened)
            print(f"Brightened {img_name}: mean before={img.mean():.1f} -> after={brightened.mean():.1f}")

    # Re-zip into final PPTX
    def zip_dir(src_dir, output_zip):
        with zipfile.ZipFile(output_zip, 'w', zipfile.ZIP_DEFLATED) as z:
            for root, dirs, files in os.walk(src_dir):
                for file in files:
                    full_path = os.path.join(root, file)
                    rel_path = os.path.relpath(full_path, src_dir)
                    z.write(full_path, rel_path)

    zip_dir(temp_dir, TARGET_DOWNLOAD)
    shutil.copyfile(TARGET_DOWNLOAD, TARGET_WORKSPACE)
    shutil.rmtree(temp_dir)
    if os.path.exists("temp_brightened.pptx"):
        os.remove("temp_brightened.pptx")
    print(f"SUCCESS: Built brightened presentation at {TARGET_DOWNLOAD} and {TARGET_WORKSPACE}")

if __name__ == "__main__":
    build_brightened_presentation()
