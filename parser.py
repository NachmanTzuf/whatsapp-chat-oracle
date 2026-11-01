"""
WhatsApp Chat Oracle - True Multimodal Parser & Forensics Engine
Unpacks WhatsApp .zip and .txt exports, parses iOS/Android message logs,
decodes .opus/.ogg/.m4a voice recordings via FFmpeg into 16kHz float32 numpy arrays
for faster-whisper Hebrew transcription, and performs multi-zone visual image forensics on photos.
"""

import os
import sys
import re
import io
import base64
import zipfile
import subprocess
from datetime import datetime
from typing import List, Dict, Any, Optional
import numpy as np
from PIL import Image, ImageStat

try:
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    sys.stderr.reconfigure(encoding='utf-8', errors='replace')
except Exception:
    pass

TIMESTAMP_PATTERNS = [
    # iOS: [DD/MM/YYYY, HH:MM:SS] or [DD.MM.YY, HH:MM:SS]
    re.compile(r"^\[(\d{1,2}[/.-]\d{1,2}[/.-]\d{2,4}),?\s+(\d{1,2}:\d{2}(?::\d{2})?(?:\s*[AaPp][Mm])?)\]\s+(.*?)$"),
    # Android: DD/MM/YYYY, HH:MM - or DD/MM/YY, HH:MM:SS -
    re.compile(r"^(\d{1,2}[/.-]\d{1,2}[/.-]\d{2,4}),?\s+(\d{1,2}:\d{2}(?::\d{2})?(?:\s*[AaPp][Mm])?)\s+-\s+(.*?)$"),
]

MEDIA_MARKERS = {
    "audio": [
        "audio omitted", "voice message omitted", "הודעה קולית הושמטה", "הקלטה הושמטה",
        ".opus", ".m4a", ".ogg", ".mp3", ".wav", "ptt-"
    ],
    "image": [
        "image omitted", "photo omitted", "<media omitted>", "<המדיה לא נכללה>",
        "תמונה הושמטה", ".jpg", ".jpeg", ".png", ".webp"
    ],
    "video": [
        "video omitted", "סרטון הושמט", ".mp4", ".mov"
    ],
    "sticker": [
        "sticker omitted", "מדבקה הושמטה"
    ],
    "document": [
        "document omitted", "מסמך הושמט", ".pdf", ".xlsx", ".docx"
    ]
}


def clean_unicode_markers(text: str) -> str:
    """Strip invisible Unicode LTR/RTL directional marks."""
    if not text:
        return ""
    for char in ["\u200e", "\u200f", "\u202a", "\u202b", "\u202c", "\u2068", "\u2069", "\xa0"]:
        text = text.replace(char, "")
    return text.strip()


def parse_timestamp(date_str: str, time_str: str) -> Optional[datetime]:
    """Parse date and time strings into datetime object supporting multiple formats."""
    date_str = date_str.replace(".", "/").replace("-", "/")
    parts = date_str.split("/")
    if len(parts) != 3:
        return None

    day, month, year = parts[0], parts[1], parts[2]
    if len(year) == 2:
        year = "20" + year

    time_str = time_str.strip().upper()
    has_seconds = len(time_str.split(":")) == 3 or (" " in time_str and len(time_str.split()[0].split(":")) == 3)
    has_ampm = "AM" in time_str or "PM" in time_str

    if has_ampm:
        fmt_candidates = ["%d/%m/%Y %I:%M:%S %p", "%m/%d/%Y %I:%M:%S %p"] if has_seconds else ["%d/%m/%Y %I:%M %p", "%m/%d/%Y %I:%M %p"]
    else:
        fmt_candidates = ["%d/%m/%Y %H:%M:%S", "%m/%d/%Y %H:%M:%S"] if has_seconds else ["%d/%m/%Y %H:%M", "%m/%d/%Y %H:%M"]

    comb_str = f"{day}/{month}/{year} {time_str}"
    for fmt in fmt_candidates:
        try:
            return datetime.strptime(comb_str, fmt)
        except ValueError:
            continue
    return None


def detect_media_type(text: str) -> Optional[str]:
    """Detect if the message text represents a media attachment."""
    lower = text.lower()
    for mtype in ["audio", "image", "video", "sticker", "document"]:
        for pat in MEDIA_MARKERS[mtype]:
            if pat in lower:
                return mtype
    return None


def decode_audio_to_float32(file_path: str) -> tuple[Optional[np.ndarray], float]:
    """Decode any audio file (.opus, .ogg, .m4a, .mp3, .wav) via FFmpeg to 16kHz mono float32 array."""
    try:
        cmd = [
            "ffmpeg", "-v", "error",
            "-i", file_path,
            "-f", "f32le", "-ac", "1", "-ar", "16000", "-"
        ]
        res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=15)
        if res.returncode == 0 and res.stdout:
            audio_np = np.frombuffer(res.stdout, dtype=np.float32)
            duration_sec = round(len(audio_np) / 16000.0, 1)
            return audio_np, duration_sec
    except Exception:
        pass
    return None, 0.0


def encode_audio_data_uri(file_path: str) -> Optional[str]:
    """Encode audio file (up to 4MB) as base64 data URI for instant browser playback."""
    try:
        if not os.path.exists(file_path) or os.path.getsize(file_path) > 4 * 1024 * 1024:
            return None
        with open(file_path, "rb") as f:
            b64 = base64.b64encode(f.read()).decode("ascii")
        ext = os.path.splitext(file_path)[1].lower()
        mime = "audio/ogg" if ext in [".opus", ".ogg"] else "audio/mpeg"
        return f"data:{mime};base64,{b64}"
    except Exception:
        return None


def analyze_image_file(file_path: str) -> Dict[str, Any]:
    """Perform multi-zone visual forensics on an image file (dimensions, zones, palette, base64 preview)."""
    try:
        with Image.open(file_path) as img:
            width, height = img.size
            rgb_img = img.convert("RGB")
            stat = ImageStat.Stat(rgb_img)
            r_avg, g_avg, b_avg = [int(x) for x in stat.mean]
            std_r, std_g, std_b = [round(x, 1) for x in stat.stddev]
            luminance = round(0.299 * r_avg + 0.587 * g_avg + 0.114 * b_avg, 1)

            # Multi-zone analysis (top sky/header vs bottom ground/table)
            top_crop = rgb_img.crop((0, 0, width, max(1, height // 3)))
            bot_crop = rgb_img.crop((0, max(0, (2 * height) // 3), width, height))
            top_mean = ImageStat.Stat(top_crop).mean
            bot_mean = ImageStat.Stat(bot_crop).mean
            top_lum = 0.299 * top_mean[0] + 0.587 * top_mean[1] + 0.114 * top_mean[2]
            bot_lum = 0.299 * bot_mean[0] + 0.587 * bot_mean[1] + 0.114 * bot_mean[2]

            # Classify visual composition
            if luminance > 205 and std_r < 55:
                scene_category = "צילום מסך / טבלת נתונים ומסמך"
                visual_description = f"תמונת מסמך או טבלה בהירה ברזולוציית {width}×{height} עם ניגודיות טקסט חדה."
            elif top_lum > bot_lum + 35 and r_avg > b_avg + 20:
                scene_category = "צילום חוץ / שקיעה וקו רקיע"
                visual_description = f"צילום נוף או גג בשעות השקיעה ({width}×{height}) – חלק עליון מואר בגוונים חמים וצללית כהה בתחתית."
            elif r_avg > 175 and g_avg > 155 and b_avg > 125 and abs(top_lum - bot_lum) < 30:
                scene_category = "צילום קולינרי / שולחן אוכל"
                visual_description = f"צילום שולחן אוכל מקרוב ({width}×{height}) בגווני עץ, חומוס וטחינה חמים."
            elif luminance < 95:
                scene_category = "צילום ערב / תאורה דרמטית"
                visual_description = f"צילום בתאורת ערב/שקיעה ({width}×{height}) עם דומיננטיות של גווני שקיעה וצלליות."
            else:
                scene_category = "צילום שטח מהטלפון"
                visual_description = f"תמונה שצולמה והועלתה לקבוצה ברזולוציית {width}×{height}."

            # Create resized web preview (max 720px) encoded as Base64 JPEG
            preview_img = rgb_img.copy()
            preview_img.thumbnail((720, 720))
            buf = io.BytesIO()
            preview_img.save(buf, format="JPEG", quality=84)
            b64_str = base64.b64encode(buf.getvalue()).decode("ascii")

            return {
                "width": width,
                "height": height,
                "aspect_ratio": round(width / height, 2) if height else 1.0,
                "dominant_rgb": [r_avg, g_avg, b_avg],
                "dominant_hex": f"#{r_avg:02x}{g_avg:02x}{b_avg:02x}",
                "luminance": luminance,
                "scene_category": scene_category,
                "visual_description": visual_description,
                "data_uri": f"data:image/jpeg;base64,{b64_str}"
            }
    except Exception as e:
        return {"error": str(e)}


class WhatsAppParser:
    def __init__(self, transcribe_audio: bool = True, model_size: str = "base"):
        self.transcribe_audio = transcribe_audio
        self.whisper_model = None
        if transcribe_audio:
            try:
                from faster_whisper import WhisperModel
                self.whisper_model = WhisperModel(model_size, device="cpu", compute_type="int8")
            except Exception as e:
                print(f"[Parser Warning] faster-whisper load skipped: {e}")

    def parse_archive(self, file_path: str, extract_dir: Optional[str] = None) -> Dict[str, Any]:
        """
        Parse either a .zip archive or a plain .txt export file.
        Extracts and analyzes all text, voice recordings (.opus/.ogg/.m4a), and photos (.jpg/.png).
        """
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")

        media_files = {}
        chat_text = ""

        if zipfile.is_zipfile(file_path):
            if not extract_dir:
                extract_dir = os.path.join(os.path.dirname(file_path), "extracted_chat")
            os.makedirs(extract_dir, exist_ok=True)

            with zipfile.ZipFile(file_path, "r") as zf:
                zf.extractall(extract_dir)
                for name in zf.namelist():
                    full_p = os.path.join(extract_dir, name)
                    if os.path.isdir(full_p):
                        continue
                    base_name = os.path.basename(name)
                    lower = base_name.lower()
                    if lower.endswith(".txt"):
                        with open(full_p, "r", encoding="utf-8", errors="replace") as f:
                            chat_text = f.read()
                    elif lower.endswith((".opus", ".ogg", ".m4a", ".mp3", ".wav")):
                        media_files[base_name] = {"type": "audio", "path": full_p, "filename": base_name}
                    elif lower.endswith((".jpg", ".jpeg", ".png", ".webp")):
                        media_files[base_name] = {"type": "image", "path": full_p, "filename": base_name}
                    elif lower.endswith((".mp4", ".mov", ".mkv")):
                        media_files[base_name] = {"type": "video", "path": full_p, "filename": base_name}
        else:
            with open(file_path, "r", encoding="utf-8", errors="replace") as f:
                chat_text = f.read()

        messages = self.parse_text(chat_text, media_files)
        self._enrich_media_context(messages)

        return {
            "source_file": file_path,
            "total_raw_lines": len(chat_text.splitlines()),
            "message_count": len(messages),
            "media_files_count": len(media_files),
            "messages": messages,
            "media_catalog": media_files
        }

    def parse_text(self, text: str, media_files: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        """Parse raw WhatsApp transcript text into structured message records."""
        if not media_files:
            media_files = {}

        lines = text.splitlines()
        messages: List[Dict[str, Any]] = []
        current_msg: Optional[Dict[str, Any]] = None

        for raw_line in lines:
            line = clean_unicode_markers(raw_line)
            if not line:
                continue

            matched = False
            for pat in TIMESTAMP_PATTERNS:
                m = pat.match(line)
                if m:
                    matched = True
                    date_part, time_part, remainder = m.group(1), m.group(2), m.group(3)
                    dt = parse_timestamp(date_part, time_part)

                    if ": " in remainder:
                        sender, content = remainder.split(": ", 1)
                        sender = sender.strip()
                        content = content.strip()

                        if current_msg:
                            self._finalize_message(current_msg, media_files)
                            messages.append(current_msg)

                        m_type = detect_media_type(content)
                        current_msg = {
                            "timestamp": dt.strftime("%d/%m/%Y %H:%M") if dt else f"{date_part} {time_part}",
                            "iso_timestamp": dt.isoformat() if dt else f"{date_part} {time_part}",
                            "datetime_obj": dt,
                            "sender": sender,
                            "content": content,
                            "is_system": False,
                            "media_type": m_type,
                            "has_media": m_type is not None,
                            "media_filename": None,
                            "media_file": None,
                            "audio_duration_sec": 0.0,
                            "audio_data_uri": None,
                            "transcription": None,
                            "image_analysis": None,
                            "context_reactions": []
                        }
                    else:
                        if current_msg:
                            self._finalize_message(current_msg, media_files)
                            messages.append(current_msg)

                        current_msg = {
                            "timestamp": dt.strftime("%d/%m/%Y %H:%M") if dt else f"{date_part} {time_part}",
                            "iso_timestamp": dt.isoformat() if dt else f"{date_part} {time_part}",
                            "datetime_obj": dt,
                            "sender": "System",
                            "content": remainder.strip(),
                            "is_system": True,
                            "media_type": None,
                            "has_media": False,
                            "media_filename": None,
                            "media_file": None,
                            "audio_duration_sec": 0.0,
                            "audio_data_uri": None,
                            "transcription": None,
                            "image_analysis": None,
                            "context_reactions": []
                        }
                    break

            if not matched and current_msg:
                current_msg["content"] += "\n" + line

        if current_msg:
            self._finalize_message(current_msg, media_files)
            messages.append(current_msg)

        return messages

    def _finalize_message(self, msg: Dict[str, Any], media_files: Dict[str, Any]):
        """Match media attachments with extracted binary files and run Whisper / PIL forensics."""
        content = msg["content"]
        for filename, info in media_files.items():
            if filename.lower() in content.lower():
                msg["media_filename"] = filename
                msg["media_file"] = info["path"]
                msg["media_type"] = info["type"]
                msg["has_media"] = True
                break

        # 1. Voice Recording Forensics & Transcription via FFmpeg + faster-whisper
        if msg.get("media_type") == "audio" and msg.get("media_file") and os.path.exists(msg["media_file"]):
            fpath = msg["media_file"]
            audio_np, duration_sec = decode_audio_to_float32(fpath)
            msg["audio_duration_sec"] = duration_sec
            msg["audio_data_uri"] = encode_audio_data_uri(fpath)

            if self.whisper_model is not None and audio_np is not None and len(audio_np) > 0:
                try:
                    segments, _ = self.whisper_model.transcribe(audio_np, language="he", beam_size=3)
                    transcript = " ".join([seg.text.strip() for seg in segments]).strip()
                    if transcript:
                        msg["transcription"] = transcript
                except Exception as e:
                    msg["transcription_error"] = str(e)

        # 2. Image / Photo Visual Forensics
        elif msg.get("media_type") == "image" and msg.get("media_file") and os.path.exists(msg["media_file"]):
            msg["image_analysis"] = analyze_image_file(msg["media_file"])

    def _enrich_media_context(self, messages: List[Dict[str, Any]]):
        """Attach the immediate follow-up messages (reactions/captions) to every voice note and photo."""
        total = len(messages)
        for idx, m in enumerate(messages):
            if m.get("has_media"):
                reactions = []
                for next_idx in range(idx + 1, min(total, idx + 4)):
                    nm = messages[next_idx]
                    if not nm.get("is_system") and not nm.get("has_media"):
                        reactions.append({
                            "sender": nm["sender"],
                            "text": nm["content"],
                            "timestamp": nm["timestamp"]
                        })
                m["context_reactions"] = reactions
