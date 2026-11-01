"""
WhatsApp Chat Oracle - Master Processing Pipeline
Coordinates parsing, forensic analytics, scriptwriting, voiceover synthesis,
fast-motion video generation, and web bundle packaging.
"""

import os
import sys
import json
import argparse
import shutil
from typing import Optional

# Reconfigure stdout/stderr for Unicode in Windows terminals
try:
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    sys.stderr.reconfigure(encoding='utf-8', errors='replace')
except Exception:
    pass

from parser import WhatsAppParser
from analytics import ChatAnalytics
from interviewer import InterviewerEngine
from voiceover import generate_audio_deliverables
from video_generator import FastMotionVideoGenerator


def run_pipeline(input_path: str, output_dir: str, skip_video: bool = False, skip_audio: bool = False) -> dict:
    """Execute complete end-to-end processing pipeline."""
    os.makedirs(output_dir, exist_ok=True)
    print(f"\n==================================================")
    print(f"🚀 WHATSAPP CHAT ORACLE: PROCESSING PIPELINE")
    print(f"==================================================")
    print(f"• Input:  {input_path}")
    print(f"• Output: {output_dir}")

    # Step 1: Parse WhatsApp Export (including faster-whisper audio transcription & PIL image forensics)
    print(f"\n[Step 1/5] Ingesting & Parsing WhatsApp Data (Text + Voice Notes + Photos)...")
    parser = WhatsAppParser(transcribe_audio=True, model_size="base")
    extract_dir = os.path.join(output_dir, "extracted_assets")
    parsed_data = parser.parse_archive(input_path, extract_dir=extract_dir)
    print(f"✓ Parsed {parsed_data['message_count']} messages, {parsed_data['media_files_count']} media files.")

    # Step 2: Forensic Statistical Analytics
    print(f"\n[Step 2/5] Running Forensic Statistical Analytics...")
    analytics = ChatAnalytics(parsed_data["messages"])
    analysis_results = analytics.run_full_analysis()
    print(f"✓ Total participants: {analysis_results['summary']['total_participants']}")
    print(f"✓ Total words analyzed: {analysis_results['summary']['total_words']:,}")
    print(f"✓ Archetypes identified: {len(analysis_results['archetypes'])}")

    # Step 3: The Interviewer Script Generation
    print(f"\n[Step 3/5] Synthesizing Interviewer Podcast Script...")
    interviewer = InterviewerEngine(analysis_results)
    script_data = interviewer.generate_full_interviewer_script()
    print(f"✓ Generated 5-section investigative documentary script in Hebrew.")

    # Step 4: Neural Voiceover Audio Synthesis
    audio_paths = {}
    if not skip_audio:
        print(f"\n[Step 4/5] Synthesizing Neural Voiceovers (edge-tts / he-IL-AvriNeural)...")
        audio_dir = os.path.join(output_dir, "audio")
        audio_paths = generate_audio_deliverables(script_data, audio_dir)
        print(f"✓ Generated full podcast audio: {audio_paths['full_podcast_audio']}")
        print(f"✓ Generated 30s video voiceover: {audio_paths['video_30s_audio']}")
    else:
        print(f"\n[Step 4/5] Audio synthesis skipped.")

    # Step 5: 30-Second Fast-Motion Video Generation
    video_mp4_path = None
    if not skip_video:
        print(f"\n[Step 5/5] Generating 30-Second Fast-Motion Video...")
        video_gen = FastMotionVideoGenerator(analysis_results, output_dir)
        video_gen.render_all_frames()
        target_mp4 = os.path.join(output_dir, "whatsapp_oracle_recap_30s.mp4")
        audio_src = audio_paths.get("video_30s_audio", "")
        video_mp4_path = video_gen.compile_video(audio_src, target_mp4)
        print(f"✓ Video compiled successfully: {video_mp4_path}")
    else:
        print(f"\n[Step 5/5] Video generation skipped.")

    # Final Bundle Assembly
    bundle_data = {
        "source": input_path,
        "analytics": analysis_results,
        "interviewer_script": script_data,
        "audio_files": audio_paths,
        "video_file": video_mp4_path
    }

    results_json_path = os.path.join(output_dir, "chat_oracle_results.json")
    with open(results_json_path, "w", encoding="utf-8") as f:
        json.dump(bundle_data, f, ensure_ascii=False, indent=2)

    # Sync into web/ for immediate standalone viewing
    web_dir = os.path.join(os.path.dirname(__file__), "web")
    if os.path.exists(web_dir):
        web_data_json = os.path.join(web_dir, "data.json")
        with open(web_data_json, "w", encoding="utf-8") as f:
            json.dump(bundle_data, f, ensure_ascii=False, indent=2)

        # Copy audio & video to web/media if present
        web_media_dir = os.path.join(web_dir, "media")
        os.makedirs(web_media_dir, exist_ok=True)
        if audio_paths.get("full_podcast_audio") and os.path.exists(audio_paths["full_podcast_audio"]):
            shutil.copy(audio_paths["full_podcast_audio"], os.path.join(web_media_dir, "podcast.mp3"))
        if video_mp4_path and os.path.exists(video_mp4_path):
            shutil.copy(video_mp4_path, os.path.join(web_media_dir, "recap_30s.mp4"))

    print(f"\n==================================================")
    print(f"🎉 WHATSAPP CHAT ORACLE: PROCESSING COMPLETE")
    print(f"==================================================")
    print(f"• Results JSON: {results_json_path}")
    if video_mp4_path:
        print(f"• 30s Video:   {video_mp4_path}")
    print(f"• Web App:     {os.path.join(web_dir, 'index.html')}")

    return bundle_data


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="WhatsApp Chat Oracle Master Pipeline")
    parser.add_argument("--input", "-i", type=str, default="", help="Path to WhatsApp .zip or .txt export")
    parser.add_argument("--output", "-o", type=str, default="", help="Output directory")
    parser.add_argument("--skip-video", action="store_true", help="Skip video frame rendering and FFmpeg compilation")
    parser.add_argument("--skip-audio", action="store_true", help="Skip TTS audio generation")

    args = parser.parse_args()

    default_base = os.path.dirname(os.path.abspath(__file__))
    input_file = args.input if args.input else os.path.join(default_base, "demo_data", "demo_chat.zip")
    output_directory = args.output if args.output else os.path.join(default_base, "output")

    run_pipeline(input_file, output_directory, skip_video=args.skip_video, skip_audio=args.skip_audio)
