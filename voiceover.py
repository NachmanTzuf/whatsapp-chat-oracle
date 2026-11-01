"""
WhatsApp Chat Oracle - Neural Voiceover Engine
Synthesizes high-fidelity spoken Hebrew / English narration using Edge Neural TTS.
"""

import asyncio
import os
from typing import Optional
import edge_tts

DEFAULT_VOICE_HE = "he-IL-AvriNeural"  # Professional male radio interviewer voice
ALTERNATIVE_VOICE_HE = "he-IL-HilaNeural"  # Professional female interviewer voice
DEFAULT_VOICE_EN = "en-US-AndrewNeural"


class VoiceoverSynthesizer:
    def __init__(self, voice: str = DEFAULT_VOICE_HE, rate: str = "+0%"):
        self.voice = voice
        self.rate = rate

    async def synthesize_async(self, text: str, output_path: str):
        """Synthesize text into MP3 audio file asynchronously."""
        os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
        communicate = edge_tts.Communicate(text, self.voice, rate=self.rate)
        await communicate.save(output_path)
        return output_path

    def synthesize(self, text: str, output_path: str) -> str:
        """Synchronous wrapper for text-to-speech synthesis."""
        return asyncio.run(self.synthesize_async(text, output_path))


def generate_audio_deliverables(scripts_data: dict, output_dir: str) -> dict:
    """Generate both the full podcast interview and the 30s fast-motion voiceovers."""
    synthesizer_normal = VoiceoverSynthesizer(voice=DEFAULT_VOICE_HE, rate="+2%")
    # For 30s video, slightly faster cadence (+15%) to match energetic pacing
    synthesizer_fast = VoiceoverSynthesizer(voice=DEFAULT_VOICE_HE, rate="+15%")

    os.makedirs(output_dir, exist_ok=True)
    full_audio_path = os.path.join(output_dir, "interviewer_full_podcast.mp3")
    video_30s_audio_path = os.path.join(output_dir, "video_30s_narration.mp3")

    full_script = scripts_data.get("full_script_he", "")
    video_script = scripts_data.get("video_30s_script_he", "")

    synthesizer_normal.synthesize(full_script, full_audio_path)
    synthesizer_fast.synthesize(video_script, video_30s_audio_path)

    return {
        "full_podcast_audio": full_audio_path,
        "video_30s_audio": video_30s_audio_path
    }
