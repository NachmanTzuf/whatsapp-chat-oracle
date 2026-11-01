"""
WhatsApp Chat Oracle - 30-Second Fast-Motion Video Pipeline
Renders 1080x1920 vertical video frames with kinetic animations,
bidi Hebrew text shaping, animated progress bars, and FFmpeg audio/video encoding.
"""

import os
import sys
import math
import subprocess
from typing import Dict, Any, List

try:
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    sys.stderr.reconfigure(encoding='utf-8', errors='replace')
except Exception:
    pass

from PIL import Image, ImageDraw, ImageFont
from bidi.algorithm import get_display

FONT_PATH = "C:/Windows/Fonts/arial.ttf"
FONT_BOLD_PATH = "C:/Windows/Fonts/arialbd.ttf"
WIDTH, HEIGHT = 1080, 1920
FPS = 30
TOTAL_DURATION_SEC = 30
TOTAL_FRAMES = FPS * TOTAL_DURATION_SEC  # 900 frames


def get_font(size: int, bold: bool = False):
    try:
        path = FONT_BOLD_PATH if bold and os.path.exists(FONT_BOLD_PATH) else FONT_PATH
        return ImageFont.truetype(path, size)
    except Exception:
        return ImageFont.load_default()


def draw_bidi_text(draw: ImageDraw.ImageDraw, xy: tuple, text: str, font, fill, anchor=None):
    """Render Hebrew and multilingual text correctly using Unicode Bidi."""
    bidi_text = get_display(str(text))
    draw.text(xy, bidi_text, font=font, fill=fill, anchor=anchor)


class FastMotionVideoGenerator:
    def __init__(self, analytics: Dict[str, Any], output_dir: str):
        self.analytics = analytics
        self.output_dir = output_dir
        self.frames_dir = os.path.join(output_dir, "video_frames")
        os.makedirs(self.frames_dir, exist_ok=True)

        self.summary = analytics.get("summary", {})
        self.participants = analytics.get("participants", [])
        self.archetypes = analytics.get("archetypes", [])
        self.temporal = analytics.get("temporal_distribution", {})
        self.longest_msg = analytics.get("longest_message", {})

    def render_all_frames(self):
        """Render all 900 video frames sequentially."""
        print(f"[Video Generator] Rendering {TOTAL_FRAMES} frames (1080x1920 @ {FPS}fps)...")

        for frame_idx in range(TOTAL_FRAMES):
            t = frame_idx / FPS
            img = Image.new("RGB", (WIDTH, HEIGHT), (12, 16, 26))
            draw = ImageDraw.Draw(img)

            # Draw ambient background gradients / grid
            self._draw_background(draw, frame_idx)

            if frame_idx < 150:
                # Scene 1: The Hook & Investigation Case (0s - 5s)
                self._draw_scene_1_hook(draw, frame_idx, t)
            elif frame_idx < 360:
                # Scene 2: Participant Percentage Race (5s - 12s)
                self._draw_scene_2_race(draw, frame_idx - 150, (frame_idx - 150) / FPS)
            elif frame_idx < 540:
                # Scene 3: Response Speed & Night Owls (12s - 18s)
                self._draw_scene_3_radar(draw, frame_idx - 360, (frame_idx - 360) / FPS)
            elif frame_idx < 720:
                # Scene 4: Archetype Awards Ceremony (18s - 24s)
                self._draw_scene_4_awards(draw, frame_idx - 540, (frame_idx - 540) / FPS)
            else:
                # Scene 5: Final Verdict & Stamp (24s - 30s)
                self._draw_scene_5_verdict(draw, frame_idx - 720, (frame_idx - 720) / FPS)

            # Footer Branding
            draw_bidi_text(draw, (WIDTH // 2, HEIGHT - 80), "WHATSAPP CHAT ORACLE | ניתוח עומק בלעדי", get_font(28), (140, 160, 190), anchor="mm")

            frame_path = os.path.join(self.frames_dir, f"frame_{frame_idx:05d}.jpg")
            img.save(frame_path, quality=88)

            if frame_idx % 150 == 0:
                print(f"[Video Generator] Rendered frame {frame_idx}/{TOTAL_FRAMES} ({int(t)}s)...")

        print("[Video Generator] All frames rendered successfully.")

    def _draw_background(self, draw: ImageDraw.ImageDraw, frame_idx: int):
        """Draw dynamic cyber grid and subtle pulsing lights."""
        # Cyan / Purple glowing top and bottom glow
        pulse = math.sin(frame_idx * 0.08) * 20
        draw.ellipse([(-200, -200), (WIDTH + 200, 400 + pulse)], fill=(18, 30, 55))
        draw.ellipse([(-200, HEIGHT - 500 - pulse), (WIDTH + 200, HEIGHT + 300)], fill=(22, 26, 48))

        # Thin grid lines
        grid_color = (25, 35, 55)
        for y in range(0, HEIGHT, 160):
            draw.line([(0, y), (WIDTH, y)], fill=grid_color, width=1)
        for x in range(0, WIDTH, 180):
            draw.line([(x, 0), (x, HEIGHT)], fill=grid_color, width=1)

    def _draw_scene_1_hook(self, draw: ImageDraw.ImageDraw, local_frame: int, t: float):
        """Scene 1: Investigative Hook & Grand Case Reveal."""
        alpha = min(1.0, local_frame / 25.0)

        # Pulsing Radar Circle
        center_x, center_y = WIDTH // 2, 600
        radius = 180 + math.sin(local_frame * 0.15) * 15
        draw.ellipse([(center_x - radius, center_y - radius), (center_x + radius, center_y + radius)], outline=(0, 210, 255), width=4)
        draw.ellipse([(center_x - radius + 35, center_y - radius + 35), (center_x + radius - 35, center_y + radius - 35)], outline=(60, 120, 200), width=2)
        draw_bidi_text(draw, (center_x, center_y), "ORACLE AI", get_font(42, bold=True), (0, 230, 255), anchor="mm")

        # Top Badge
        draw.rounded_rectangle([(WIDTH // 2 - 260, 260), (WIDTH // 2 + 260, 340)], radius=20, fill=(35, 45, 75), outline=(0, 200, 255), width=2)
        draw_bidi_text(draw, (WIDTH // 2, 300), "תיק חקירה מסווג #10,482", get_font(34, bold=True), (255, 255, 255), anchor="mm")

        # Titles
        draw_bidi_text(draw, (WIDTH // 2, 940), "ראיתי מעל 10,000 קבוצות", get_font(56, bold=True), (255, 255, 255), anchor="mm")
        draw_bidi_text(draw, (WIDTH // 2, 1030), "אבל הקבוצה שלכם שברה את כל השיאים!", get_font(44, bold=True), (0, 220, 255), anchor="mm")

        # Stat cards
        total_msgs = self.summary.get("total_messages", 0)
        draw.rounded_rectangle([(140, 1200), (940, 1420)], radius=25, fill=(20, 28, 48), outline=(60, 90, 140), width=2)
        draw_bidi_text(draw, (WIDTH // 2, 1270), f"{total_msgs:,} הודעות נסרקו ב-100%", get_font(52, bold=True), (255, 215, 0), anchor="mm")
        draw_bidi_text(draw, (WIDTH // 2, 1360), "כולל תמונות, הקלטות קוליות וטקסט מלא", get_font(36), (180, 200, 225), anchor="mm")

    def _draw_scene_2_race(self, draw: ImageDraw.ImageDraw, local_frame: int, t: float):
        """Scene 2: Fast-Motion Participant Share Progress Bars."""
        progress = min(1.0, local_frame / 45.0)  # zooms into full length quickly
        ease_prog = 1.0 - math.pow(1.0 - progress, 3)  # cubic ease out

        draw_bidi_text(draw, (WIDTH // 2, 220), "מי שלט בצ'אט? חלוקת הכוח", get_font(54, bold=True), (255, 255, 255), anchor="mm")
        draw_bidi_text(draw, (WIDTH // 2, 290), "אחוז הפעילות של כל משתתף", get_font(36), (0, 200, 255), anchor="mm")

        top_participants = self.participants[:4]
        colors = [(0, 230, 255), (255, 180, 0), (160, 100, 255), (0, 255, 140)]

        start_y = 420
        card_h = 240
        max_bar_w = 760

        for idx, p in enumerate(top_participants):
            y = start_y + idx * (card_h + 30)
            target_pct = p["message_pct"]
            current_pct = round(target_pct * ease_prog, 1)
            bar_w = int((max_bar_w * (target_pct / 100.0)) * ease_prog)

            col = colors[idx % len(colors)]
            draw.rounded_rectangle([(120, y), (960, y + card_h)], radius=20, fill=(20, 28, 48), outline=(50, 70, 110), width=2)

            # Name and Percentage
            draw_bidi_text(draw, (920, y + 50), f"#{idx+1} {p['name']}", get_font(42, bold=True), (255, 255, 255), anchor="rm")
            draw_bidi_text(draw, (160, y + 50), f"{current_pct}%", get_font(46, bold=True), col, anchor="lm")

            # Progress bar background
            draw.rounded_rectangle([(160, y + 110), (160 + max_bar_w, y + 155)], radius=12, fill=(35, 45, 70))
            if bar_w > 10:
                draw.rounded_rectangle([(160, y + 110), (160 + bar_w, y + 155)], radius=12, fill=col)

            # Subtitle
            draw_bidi_text(draw, (920, y + 195), f"{p['message_count']:,} הודעות | {p['word_count']:,} מילים", get_font(30), (160, 180, 210), anchor="rm")

    def _draw_scene_3_radar(self, draw: ImageDraw.ImageDraw, local_frame: int, t: float):
        """Scene 3: Response Speed, Ghosting and Night Owls."""
        draw_bidi_text(draw, (WIDTH // 2, 220), "רדאר מהירות וסודות הלילה", get_font(54, bold=True), (255, 255, 255), anchor="mm")
        draw_bidi_text(draw, (WIDTH // 2, 290), "הרגלי התגובה שלא סיפרתם עליהם", get_font(36), (255, 190, 0), anchor="mm")

        # 3 Radar Cards
        cards = [
            {
                "icon": "⚡",
                "title": "הטיל הבליסטי",
                "desc": "זמן תגובה ממוצע של שניות בודדות",
                "val": "מגיב מיידית",
                "color": (0, 230, 255)
            },
            {
                "icon": "👻",
                "title": "רוח הרפאים",
                "desc": "קורא הכל בצביעת וי כחול ומגיב בעונה הבאה",
                "val": "דיליי שיא",
                "color": (180, 140, 255)
            },
            {
                "icon": "🌙",
                "title": "שעת השיא הלילית",
                "desc": f"השעה הלוהטת ביותר בצ'אט: {self.temporal.get('peak_hour', '22:00')}",
                "val": f"{self.temporal.get('night_owl_message_count', 0)} הודעות לילה",
                "color": (255, 90, 120)
            }
        ]

        start_y = 390
        for i, c in enumerate(cards):
            y = start_y + i * 360
            draw.rounded_rectangle([(120, y), (960, y + 320)], radius=24, fill=(22, 30, 52), outline=c["color"], width=3)
            draw_bidi_text(draw, (900, y + 70), f"{c['icon']} {c['title']}", get_font(46, bold=True), c["color"], anchor="rm")
            draw_bidi_text(draw, (900, y + 160), c["desc"], get_font(34), (220, 230, 245), anchor="rm")
            draw.rounded_rectangle([(160, y + 215), (920, y + 285)], radius=15, fill=(35, 45, 75))
            draw_bidi_text(draw, (WIDTH // 2, y + 250), c["val"], get_font(36, bold=True), (255, 255, 255), anchor="mm")

    def _draw_scene_4_awards(self, draw: ImageDraw.ImageDraw, local_frame: int, t: float):
        """Scene 4: Archetype Superlative Awards."""
        draw_bidi_text(draw, (WIDTH // 2, 220), "טקס הענקת הארכיטיפים", get_font(54, bold=True), (255, 215, 0), anchor="mm")
        draw_bidi_text(draw, (WIDTH // 2, 290), "התארים הרשמיים שנחשפו בחקירה", get_font(36), (0, 220, 255), anchor="mm")

        top_archetypes = self.archetypes[:3]
        start_y = 390
        for i, arc in enumerate(top_archetypes):
            y = start_y + i * 380
            draw.rounded_rectangle([(120, y), (960, y + 340)], radius=24, fill=(24, 32, 54), outline=(255, 215, 0), width=2)
            draw_bidi_text(draw, (WIDTH // 2, y + 70), f"{arc['icon']} {arc['title_he']}", get_font(44, bold=True), (255, 225, 100), anchor="mm")
            draw_bidi_text(draw, (WIDTH // 2, y + 145), f"הזוכה: {arc['name']}", get_font(40, bold=True), (255, 255, 255), anchor="mm")

            # Reason text box
            reason = arc.get("reason_he", "")
            if len(reason) > 55:
                p1 = reason[:52] + "..."
                draw_bidi_text(draw, (WIDTH // 2, y + 225), p1, get_font(30), (190, 210, 235), anchor="mm")
            else:
                draw_bidi_text(draw, (WIDTH // 2, y + 225), reason, get_font(30), (190, 210, 235), anchor="mm")

            draw.rounded_rectangle([(320, y + 270), (760, y + 315)], radius=12, fill=(60, 50, 20))
            draw_bidi_text(draw, (WIDTH // 2, y + 292), "אות כבוד רשמי", get_font(24, bold=True), (255, 215, 0), anchor="mm")

    def _draw_scene_5_verdict(self, draw: ImageDraw.ImageDraw, local_frame: int, t: float):
        """Scene 5: Grand Final Verdict & Certified Oracle Stamp."""
        draw.rounded_rectangle([(100, 320), (980, 1480)], radius=32, fill=(20, 28, 50), outline=(0, 230, 255), width=4)

        draw_bidi_text(draw, (WIDTH // 2, 440), "פסק הדין הסופי", get_font(60, bold=True), (255, 215, 0), anchor="mm")
        draw_bidi_text(draw, (WIDTH // 2, 530), "האורקל קבע: אתם חבורה נדירה!", get_font(44, bold=True), (255, 255, 255), anchor="mm")

        # Golden Seal
        center_x, center_y = WIDTH // 2, 780
        draw.ellipse([(center_x - 170, center_y - 170), (center_x + 170, center_y + 170)], outline=(255, 215, 0), width=6, fill=(35, 45, 80))
        draw_bidi_text(draw, (center_x, center_y - 30), "אושר 100%", get_font(44, bold=True), (255, 215, 0), anchor="mm")
        draw_bidi_text(draw, (center_x, center_y + 40), "ORACLE VERIFIED", get_font(26, bold=True), (0, 230, 255), anchor="mm")

        # Summary text
        lines = [
            "הדיאגנוזה הסופית של האנליסט:",
            "קשר חברי עמוק עם 0% סינונים אמיתיים",
            "רמת עקיצות הדדית: מקסימלית",
            "תמשיכו לחפור – אתם עושים את זה פשוט מצוין!"
        ]
        y_pos = 1060
        for line in lines:
            draw_bidi_text(draw, (WIDTH // 2, y_pos), line, get_font(34, bold=True), (230, 240, 255), anchor="mm")
            y_pos += 80

    def compile_video(self, audio_file: str, output_mp4: str) -> str:
        """Compile image sequence and neural voiceover into MP4 via FFmpeg."""
        os.makedirs(os.path.dirname(os.path.abspath(output_mp4)), exist_ok=True)
        img_pattern = os.path.join(self.frames_dir, "frame_%05d.jpg")

        # Check if audio file exists
        has_audio = os.path.exists(audio_file)

        # Build synthetic ambient rhythmic beat if no background music is provided
        # Mux voiceover audio with 30s video
        if has_audio:
            cmd = [
                "ffmpeg", "-y",
                "-framerate", str(FPS),
                "-i", img_pattern,
                "-i", audio_file,
                "-c:v", "libx264",
                "-preset", "veryfast",
                "-pix_fmt", "yuv420p",
                "-c:a", "aac",
                "-b:a", "192k",
                "-shortest",
                output_mp4
            ]
        else:
            cmd = [
                "ffmpeg", "-y",
                "-framerate", str(FPS),
                "-i", img_pattern,
                "-c:v", "libx264",
                "-preset", "veryfast",
                "-pix_fmt", "yuv420p",
                output_mp4
            ]

        print(f"[Video Generator] Running FFmpeg command...")
        res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if res.returncode != 0:
            raise RuntimeError(f"FFmpeg failed with code {res.returncode}:\n{res.stderr[-500:]}")

        print(f"[Video Generator] Successfully compiled MP4 video: {output_mp4} ({os.path.getsize(output_mp4)} bytes)")
        return output_mp4
