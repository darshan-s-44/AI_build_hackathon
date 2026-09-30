import asyncio
import os
import edge_tts
import subprocess

SEGMENTS = [
    {
        "id": 1,
        "start": 0.5,
        "window_end": 15.5,
        "text": "Welcome to TenderPulse AI, the autonomous bid compliance engine for CPCL under the Ministry of Petroleum and Natural Gas. Our live vigilance terminal verifies multi-page technical dossiers against official NIT rules in real time."
    },
    {
        "id": 2,
        "start": 16.0,
        "window_end": 28.0,
        "text": "Entering the Review Workspace. Notice bid zero-one: all four statutory clauses pass with complete CVC-grade defensibility, benchmarking vendor eligibility with zero hallucination."
    },
    {
        "id": 3,
        "start": 29.0,
        "window_end": 41.8,
        "text": "Selecting bid zero-five. The Bid Dossier tab displays our normalized PyMuPDF extraction stream, directly verifying fifteen crore turnover, ISO validity, and the SBI bank guarantee."
    },
    {
        "id": 4,
        "start": 42.6,
        "window_end": 55.5,
        "text": "For bid zero-six, our deterministic date solver instantly flags an expired ISO certificate from June 2025 against CPCL's December 2026 cutoff—preventing costly manual review errors."
    },
    {
        "id": 5,
        "start": 56.5,
        "window_end": 74.5,
        "text": "Now observe bid eleven. While naive baselines falsely reject this vendor, TenderPulse flags it as CONDITIONAL. The semantic engine recognizes their valid UDYAM certificate, applying MSME turnover relaxation under Clause 4.5 to protect compliant suppliers."
    },
    {
        "id": 6,
        "start": 75.5,
        "window_end": 92.0,
        "text": "Reviewers can toggle high-contrast dark mode for intensive vigilance sessions. Auditing bid zero-nine instantly catches a missing EMD bank guarantee, safeguarding public funds from non-serious bidders before tenders are opened."
    },
    {
        "id": 7,
        "start": 93.2,
        "window_end": 113.8,
        "text": "In the References section, our decision workflow aligns with the Government of India eProcurement portal, SAP Ariba, and Coupa—integrating proven enterprise procurement patterns while ensuring all bid evidence remains strictly local and air-gapped."
    },
    {
        "id": 8,
        "start": 114.8,
        "window_end": 125.0,
        "text": "The interface emphasizes clarity over spectacle—combining semantic color hierarchy, keyboard accessibility, and transparent separation between verified local extraction and proposed integrations."
    },
    {
        "id": 9,
        "start": 126.0,
        "window_end": 139.0,
        "text": "Returning to the Overview. Across all thirteen benchmark dossiers, TenderPulse achieves one hundred percent accuracy—slashing evaluation cycles from five days to seconds with total vigilance transparency."
    }
]

VOICE = "en-US-ChristopherNeural"
RATE = "+8%"

async def generate_segment(seg):
    filename = f"audio_seg_{seg['id']}.mp3"
    comm = edge_tts.Communicate(seg['text'], VOICE, rate=RATE)
    await comm.save(filename)
    cmd = [
        "ffprobe", "-v", "error", "-show_entries", "format=duration",
        "-of", "default=noprint_wrappers=1:nokey=1", filename
    ]
    res = subprocess.run(cmd, capture_output=True, text=True)
    dur = float(res.stdout.strip())
    seg["duration"] = dur
    seg["end"] = seg["start"] + dur
    seg["file"] = filename
    buffer = seg['window_end'] - seg['end']
    print(f"Seg {seg['id']}: start={seg['start']:5.1f}s | dur={dur:4.1f}s | end={seg['end']:5.1f}s | window_end={seg['window_end']:5.1f}s | buffer=+{buffer:4.1f}s")

async def main():
    for seg in SEGMENTS:
        await generate_segment(seg)

if __name__ == "__main__":
    asyncio.run(main())
