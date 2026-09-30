import asyncio
import os
import subprocess
import soundfile as sf
import numpy as np
import edge_tts

# Video Metadata
VIDEO_INPUT = r"C:\Users\darsh\Downloads\demo.mp4"
VIDEO_OUTPUT = r"C:\Users\darsh\Downloads\demo_with_voiceover.mp4"
TOTAL_DURATION = 139.4333  # seconds
SAMPLE_RATE = 48000
VOICE = "en-US-ChristopherNeural"
RATE = "+8%"

SEGMENTS = [
    {
        "id": 1,
        "start": 0.5,
        "speech": "Welcome to TenderPulse AI, the autonomous bid compliance engine for CPCL under the Ministry of Petroleum and Natural Gas. Our live vigilance terminal audits technical dossiers against official NIT rules in real time.",
        "captions": [
            (0.5, 5.0, "Welcome to TenderPulse AI, the autonomous bid compliance engine"),
            (5.0, 9.2, "built for CPCL under the Ministry of Petroleum & Natural Gas."),
            (9.2, 14.3, "Our live vigilance terminal audits technical dossiers against official NIT rules in real time.")
        ]
    },
    {
        "id": 2,
        "start": 16.0,
        "speech": "Entering the Review Workspace. Notice bid zero-one: all four statutory clauses pass with CVC-grade defensibility, benchmarking vendor eligibility with zero hallucination.",
        "captions": [
            (16.0, 19.8, "Entering the Review Workspace with unified dossier and evidence views."),
            (19.8, 24.0, "Notice bid 01: all four statutory clauses pass with CVC-grade defensibility,"),
            (24.0, 27.8, "benchmarking vendor eligibility with zero hallucination.")
        ]
    },
    {
        "id": 3,
        "start": 29.0,
        "speech": "Selecting bid zero-five. The Bid Dossier tab displays normalized PyMuPDF extraction, verifying fifteen crore turnover, ISO validity, and the SBI bank guarantee.",
        "captions": [
            (29.0, 32.8, "Selecting bid 05 from the review queue."),
            (32.8, 37.0, "The Bid Dossier tab displays our normalized PyMuPDF extraction stream,"),
            (37.0, 41.3, "verifying ₹15 Cr turnover, ISO validity, and SBI bank guarantee.")
        ]
    },
    {
        "id": 4,
        "start": 42.6,
        "speech": "For bid zero-six, our deterministic date solver instantly flags an expired ISO certificate from June 2025 against CPCL's December 2026 cutoff—preventing costly manual review errors.",
        "captions": [
            (42.6, 46.8, "For bid 06, our deterministic date solver detects a statutory failure:"),
            (46.8, 51.2, "the ISO certificate expired in June 2025 against CPCL's Dec 2026 cutoff,"),
            (51.2, 55.4, "eliminating costly clerical oversights that plague manual audits.")
        ]
    },
    {
        "id": 5,
        "start": 56.5,
        "speech": "Now observe bid eleven. While naive baselines falsely reject this vendor, TenderPulse flags it as CONDITIONAL. The semantic engine recognizes their valid UDYAM certificate, applying MSME turnover relaxation under Clause 4.5 to protect compliant suppliers.",
        "captions": [
            (56.5, 60.8, "Now observe bid 11. While naive baselines falsely reject this vendor,"),
            (60.8, 65.0, "TenderPulse AI correctly flags it as CONDITIONAL."),
            (65.0, 69.5, "The semantic engine recognizes their valid UDYAM certificate,"),
            (69.5, 74.0, "applying MSME turnover relaxation under Clause 4.5 to protect compliant suppliers.")
        ]
    },
    {
        "id": 6,
        "start": 75.5,
        "speech": "Reviewers can toggle high-contrast dark mode for intensive vigilance sessions. Auditing bid zero-nine instantly catches a missing EMD bank guarantee, safeguarding public funds from non-serious bidders before tenders are opened.",
        "captions": [
            (75.5, 79.8, "Reviewers can toggle high-contrast dark mode for intensive audit sessions."),
            (79.8, 84.2, "Auditing bid 09 instantly catches a missing EMD bank guarantee,"),
            (84.2, 89.1, "safeguarding public funds from non-serious bidders before tender opening.")
        ]
    },
    {
        "id": 7,
        "start": 93.2,
        "speech": "In the References section, our decision workflow aligns with the Government of India eProcurement portal, SAP Ariba, and Coupa—integrating proven enterprise procurement patterns while ensuring all bid evidence remains strictly local and air-gapped.",
        "captions": [
            (93.2, 97.5, "In the References section, our decision workflow aligns with"),
            (97.5, 102.2, "Government of India eProcurement (GeM / CPPP), SAP Ariba, and Coupa—"),
            (102.2, 106.9, "integrating enterprise standards while keeping all bid data strictly local and secure.")
        ]
    },
    {
        "id": 8,
        "start": 114.8,
        "speech": "The interface emphasizes clarity over spectacle—combining semantic color hierarchy, keyboard accessibility, and full transparency on verified evidence.",
        "captions": [
            (114.8, 119.5, "The interface emphasizes cognitive clarity over spectacle—"),
            (119.5, 124.5, "combining semantic color hierarchy, accessibility, and verifiable evidence.")
        ]
    },
    {
        "id": 9,
        "start": 126.0,
        "speech": "Returning to the Overview. Across all thirteen benchmark dossiers, TenderPulse achieves one hundred percent accuracy—slashing evaluation cycles from five days to seconds with total vigilance transparency.",
        "captions": [
            (126.0, 130.2, "Returning to the Overview summary."),
            (130.2, 134.5, "Across all thirteen benchmark dossiers, TenderPulse achieves 100% accuracy—"),
            (134.5, 138.8, "slashing evaluation cycles from five days to seconds with total vigilance transparency.")
        ]
    }
]

def format_ass_time(sec):
    h = int(sec // 3600)
    m = int((sec % 3600) // 60)
    s = sec % 60
    return f"{h}:{m:02d}:{s:05.2f}"

def generate_ass_file(filename="tenderpulse_captions.ass"):
    header = """[Script Info]
Title: TenderPulse AI Screen Recording Voiceover
ScriptType: v4.00+
WrapStyle: 0
ScaledBorderAndShadow: yes
YCbCr Matrix: TV.601
PlayResX: 1918
PlayResY: 1032

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: CleanSub,Segoe UI,15,&H00FFFFFF,&H000000FF,&H00000000,&HB00F172A,1,0,0,0,100,100,0.3,0,3,1.0,0,2,30,30,8,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
    lines = [header]
    for seg in SEGMENTS:
        for c_start, c_end, text in seg["captions"]:
            t_s = format_ass_time(c_start)
            t_e = format_ass_time(c_end)
            lines.append(f"Dialogue: 0,{t_s},{t_e},CleanSub,,0,0,0,,{text}\n")
    
    with open(filename, "w", encoding="utf-8") as f:
        f.writelines(lines)
    print(f"Generated ASS subtitles: {filename}")

async def generate_speech_audio():
    total_samples = int(TOTAL_DURATION * SAMPLE_RATE)
    # Master audio buffer: 2 channels (stereo), 48kHz float32
    master_audio = np.zeros((total_samples, 2), dtype=np.float32)

    for seg in SEGMENTS:
        mp3_name = f"seg_{seg['id']}.mp3"
        wav_name = f"seg_{seg['id']}.wav"
        
        print(f"Synthesizing Segment {seg['id']}...")
        comm = edge_tts.Communicate(seg["speech"], VOICE, rate=RATE)
        await comm.save(mp3_name)
        
        # Convert MP3 to 48kHz stereo WAV using ffmpeg for perfect resampling
        cmd = ["ffmpeg", "-y", "-i", mp3_name, "-ar", str(SAMPLE_RATE), "-ac", "2", wav_name]
        subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
        
        # Read WAV
        audio_data, sr = sf.read(wav_name)
        assert sr == SAMPLE_RATE
        
        start_sample = int(seg["start"] * SAMPLE_RATE)
        end_sample = start_sample + len(audio_data)
        
        print(f"  Segment {seg['id']}: placed at {seg['start']}s -> {(end_sample/SAMPLE_RATE):.2f}s ({len(audio_data)/SAMPLE_RATE:.2f}s duration)")
        if end_sample > total_samples:
            end_sample = total_samples
            audio_data = audio_data[:(end_sample - start_sample)]
            
        master_audio[start_sample:end_sample, :] += audio_data
        
    master_wav = "master_voiceover.wav"
    sf.write(master_wav, master_audio, SAMPLE_RATE)
    print(f"Master audio generated: {master_wav} (duration: {len(master_audio)/SAMPLE_RATE:.2f}s)")
    return master_wav

def remux_video(master_wav, ass_file):
    print("Muxing video with voiceover and burning in non-distracting subtitles...")
    cmd = [
        "ffmpeg", "-y",
        "-i", VIDEO_INPUT,
        "-i", master_wav,
        "-vf", f"ass={ass_file}",
        "-map", "0:v:0",
        "-map", "1:a:0",
        "-c:v", "libx264",
        "-preset", "medium",
        "-crf", "18",
        "-pix_fmt", "yuv420p",
        "-c:a", "aac",
        "-b:a", "256k",
        "-ar", "48000",
        "-shortest",
        VIDEO_OUTPUT
    ]
    print("Running command:", " ".join(cmd))
    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode != 0:
        print("FFmpeg error:", res.stderr)
        raise RuntimeError("FFmpeg encoding failed!")
    print(f"SUCCESS: Rendered complete dubbed video to: {VIDEO_OUTPUT}")

async def main():
    generate_ass_file("tenderpulse_captions.ass")
    master_wav = await generate_speech_audio()
    remux_video(master_wav, "tenderpulse_captions.ass")

if __name__ == "__main__":
    asyncio.run(main())
