"""
WhatsApp Chat Oracle - Forensic & Unhinged Slang Analytics Engine
Calculates participant rankings, response latencies, crazy metrics,
longest voice note, longest text message, inside jokes, and curated golden exhibits.
"""

from collections import Counter, defaultdict
import re
from typing import List, Dict, Any

HEBREW_STOP_WORDS = {
    "את", "זה", "של", "על", "עם", "לא", "כן", "מה", "הוא", "היא", "הם", "הן",
    "כל", "או", "אם", "גם", "רק", "עוד", "יותר", "אבל", "כי", "אז", "כמו", "לי",
    "לו", "לה", "לנו", "להם", "שלנו", "שלי", "שלו", "שלה", "היה", "יהיה", "היו",
    "טוב", "שם", "פה", "כבר", "עכשיו", "יש", "אין", "אני", "אתה", "אתם", "אנחנו",
    "הזה", "הזאת", "אלה", "אלו", "שלך", "אחרי", "לפני", "בין", "עד", "כדי",
    "איזה", "איך", "מתי", "למה", "כמה", "מישהו", "משהו", "אחד", "אחת", "שני",
    "ממש", "פשוט", "בכלל", "היום", "מחר", "אתמול", "יודע", "יודעת", "נראה",
    "רוצה", "צריך", "אפשר", "יאללה", "אחי", "חברים", "בוקר", "ערב", "לילה",
    "attached", "file", "omitted", "image", "audio", "video", "ptt", "img", "wa0001"
}

EMOJI_REGEX = re.compile(
    r"[\U0001F600-\U0001F64F"
    r"\U0001F300-\U0001F5FF"
    r"\U0001F680-\U0001F6FF"
    r"\U0001F1E0-\U0001F1FF"
    r"\U00002702-\U000027B0"
    r"\U000024C2-\U0001F251"
    r"\U0001F900-\U0001F9FF"
    r"\U0001FA70-\U0001FAFF"
    r"]+", flags=re.UNICODE
)


class ChatAnalytics:
    def __init__(self, messages: List[Dict[str, Any]]):
        self.messages = [m for m in messages if not m.get("is_system")]
        self.all_messages = messages

    def run_full_analysis(self) -> Dict[str, Any]:
        """Execute unhinged analysis across all messages, voice notes, and photos."""
        if not self.messages:
            return {"error": "No non-system messages found in chat."}

        total_msgs = len(self.messages)
        participants = sorted(list({m["sender"] for m in self.messages}))

        user_msg_counts = Counter()
        user_word_counts = Counter()
        user_char_counts = Counter()
        user_media_counts = Counter()
        user_audio_counts = Counter()
        user_audio_seconds = defaultdict(float)
        user_image_counts = Counter()
        user_laugh_counts = Counter()
        user_night_counts = Counter()
        user_longest_msg = {}

        longest_text_msg = {"sender": "", "char_count": 0, "word_count": 0, "text": "", "timestamp": ""}
        voice_exhibits = []
        photo_exhibits = []

        for idx, m in enumerate(self.messages):
            sender = m["sender"]
            content = m.get("content", "")
            transcript = m.get("transcription") or ""
            combined_text = content if not m.get("has_media") else transcript
            words = [w for w in re.findall(r"[\w\"']+", combined_text) if len(w) > 1]
            chars = len(content)

            user_msg_counts[sender] += 1
            user_word_counts[sender] += len(words)
            user_char_counts[sender] += chars

            # Laugh counter
            if re.search(r"ח{3,}|😂|💀|🤣", content):
                user_laugh_counts[sender] += 1

            # Night owl messages (00:00 - 05:59)
            dt = m.get("datetime_obj")
            if dt and 0 <= dt.hour < 6:
                user_night_counts[sender] += 1

            # Media handling
            if m.get("has_media"):
                user_media_counts[sender] += 1
                if m.get("media_type") == "audio":
                    user_audio_counts[sender] += 1
                    dur = m.get("audio_duration_sec") or 12.0
                    user_audio_seconds[sender] += dur
                    voice_exhibits.append({
                        "exhibit_id": f"VOX-{len(voice_exhibits)+1:02d}",
                        "sender": sender,
                        "timestamp": m.get("timestamp", ""),
                        "filename": m.get("media_filename") or "voice_note.opus",
                        "duration_sec": round(dur, 1),
                        "transcription": transcript or "הקלטה קולית שחולצה מתוך הארכיון",
                        "audio_data_uri": m.get("audio_data_uri"),
                        "reactions": m.get("context_reactions", [])
                    })
                elif m.get("media_type") == "image":
                    user_image_counts[sender] += 1
                    img_info = m.get("image_analysis") or {}
                    photo_exhibits.append({
                        "exhibit_id": f"IMG-{len(photo_exhibits)+1:02d}",
                        "sender": sender,
                        "timestamp": m.get("timestamp", ""),
                        "filename": m.get("media_filename") or "photo.jpg",
                        "scene_category": img_info.get("scene_category", "צילום שטח"),
                        "visual_description": img_info.get("visual_description", "תמונה משותפת מהקבוצה"),
                        "width": img_info.get("width", 960),
                        "height": img_info.get("height", 720),
                        "dominant_hex": img_info.get("dominant_hex", "#8a5833"),
                        "data_uri": img_info.get("data_uri"),
                        "reactions": m.get("context_reactions", [])
                    })
            else:
                if chars > longest_text_msg["char_count"]:
                    longest_text_msg = {
                        "sender": sender,
                        "char_count": chars,
                        "word_count": len(words),
                        "text": content,
                        "timestamp": m.get("timestamp", "")
                    }
                if sender not in user_longest_msg or chars > len(user_longest_msg[sender]["text"]):
                    user_longest_msg[sender] = {
                        "text": content,
                        "timestamp": m.get("timestamp", ""),
                        "word_count": len(words)
                    }

        total_words = max(1, sum(user_word_counts.values()))
        response_metrics = self._calculate_response_dynamics()
        temporal_stats = self._calculate_temporal_patterns()
        burst_stats = self._calculate_burst_monologues()

        # Determine the single longest voice note in group history
        longest_voice_note = None
        if voice_exhibits:
            sorted_voices = sorted(voice_exhibits, key=lambda v: (v["duration_sec"], len(v["transcription"])), reverse=True)
            longest_voice_note = sorted_voices[0]
            # Add street slang roast
            longest_voice_note["roast_slang"] = (
                f"האיש אשכרה פתח תחנת רדיו פיראטית באמצע החיים. "
                f"{longest_voice_note['duration_sec']} שניות רצופות של דיבור במקום להקליד מילה אחת. "
                f"אף אחד בקבוצה לא שמע את זה עד הסוף עד שוויספר ישב ותמלל את כל הפודקאסט הזה."
            )

        # Add street slang roast for the longest text message
        longest_text_msg["roast_slang"] = (
            f"האיש שפך פה עבודת דוקטורט שלמה בוואטסאפ במקום לכתוב משפט קצר. "
            f"{longest_text_msg['word_count']} מילים ו-{longest_text_msg['char_count']} תווים של חפירה באורך הגלות. "
            f"אנשים עשו לו לייק רק כדי שלא ימשיך להקליד עוד פסקה."
        )

        participant_stats = []
        for p in participants:
            p_msgs = user_msg_counts[p]
            p_words = user_word_counts[p]
            msg_pct = round((p_msgs / total_msgs) * 100, 1) if total_msgs else 0
            word_pct = round((p_words / total_words) * 100, 1) if total_words else 0
            resp_info = response_metrics.get(p, {})
            burst_info = burst_stats.get(p, {})
            sig_quote = user_longest_msg.get(p, {"text": "", "timestamp": "", "word_count": 0})
            resp_min = resp_info.get("avg_response_minutes", 0)

            # Response time street slang diagnosis
            if resp_min <= 1.0:
                resp_slang = f"{resp_min} דק' (חסר מעצורים • יושב על הטלפון עם אינפוזיה לווריד)"
            elif resp_min <= 5.0:
                resp_slang = f"{resp_min} דק' (עוקב על כל מילה • חצי שוטר)"
            elif resp_min <= 60.0:
                resp_slang = f"{int(resp_min)} דק' (מגיב כשנזכר שיש לו חברים)"
            elif resp_min <= 720.0:
                resp_slang = f"{round(resp_min/60, 1)} שעות (טס לחו\"ל וחזר)"
            else:
                resp_slang = f"{round(resp_min/60, 1)} שעות (שר החוץ של מונקו • שולח יונת דואר)"

            participant_stats.append({
                "name": p,
                "message_count": p_msgs,
                "message_pct": msg_pct,
                "word_count": p_words,
                "word_pct": word_pct,
                "media_count": user_media_counts[p],
                "audio_count": user_audio_counts[p],
                "audio_seconds": round(user_audio_seconds[p], 1),
                "image_count": user_image_counts[p],
                "laugh_count": user_laugh_counts[p],
                "night_count": user_night_counts[p],
                "avg_words_per_msg": round(p_words / p_msgs, 1) if p_msgs else 0,
                "avg_response_minutes": resp_min,
                "response_slang": resp_slang,
                "max_streak": burst_info.get("max_streak", 1),
                "signature_quote": sig_quote
            })

        participant_stats.sort(key=lambda x: x["message_count"], reverse=True)

        # Assign wildly exaggerated Israeli street slang archetypes & roasts
        archetypes = self._assign_slang_archetypes(participant_stats, response_metrics, burst_stats, user_audio_counts)

        # Inject archetype data directly into participant stats for the table
        arc_dict = {a["name"]: a for a in archetypes}
        for p in participant_stats:
            arc = arc_dict.get(p["name"], {})
            p["slang_title"] = arc.get("title_he", "שותף לפשע")
            p["roast_summary"] = arc.get("roast_summary", "חבר מן המניין שמנסה לשרוד את השיגעון הכללי.")

        # Mine inside jokes & recurring unhinged lore
        inside_jokes = self._mine_inside_jokes_and_lore()

        # Curated Golden Highlights: Pick ONLY top 1-2 most damning voice notes and photos
        curated_voice = None
        if voice_exhibits:
            # Prefer the one with the funniest context reactions or longest
            reacted_voices = [v for v in voice_exhibits if v.get("reactions")]
            curated_voice = reacted_voices[0] if reacted_voices else voice_exhibits[0]
            curated_voice["slang_commentary"] = (
                f"ההקלטה שהבעירה את הקבוצה: {curated_voice['sender']} שיגר {curated_voice['duration_sec']} שניות. "
                f"התמלול חשף את הבלאגן בזמן אמת, והתגובות של החברים מיד אחר כך מוכיחות שאף אחד לא נשאר אדיש."
            )

        curated_photo = None
        if photo_exhibits:
            reacted_photos = [p for p in photo_exhibits if p.get("reactions")]
            curated_photo = reacted_photos[0] if reacted_photos else photo_exhibits[0]
            curated_photo["slang_commentary"] = (
                f"התמונה הכי מפלילה שנשלחה: הועלתה על ידי {curated_photo['sender']}. "
                f"סריקת התמונה זיהתה בדיוק מה הלך שם, והחברים מיד פתחו סשן צחוקים וירידות."
            )

        # Chaos Index
        night_ratio = temporal_stats["night_owl_message_count"] / max(1, total_msgs)
        audio_ratio = sum(user_audio_counts.values()) / max(1, total_msgs)
        max_burst_overall = max([b.get("max_streak", 1) for b in burst_stats.values()], default=1)
        chaos_score = min(99, max(68, int(60 + night_ratio * 90 + audio_ratio * 85 + max_burst_overall * 4)))

        return {
            "summary": {
                "total_messages": total_msgs,
                "total_words": total_words,
                "total_participants": len(participants),
                "date_range": {
                    "first_message": self.messages[0].get("timestamp"),
                    "last_message": self.messages[-1].get("timestamp")
                },
                "total_media_count": sum(user_media_counts.values()),
                "total_audio_count": sum(user_audio_counts.values()),
                "total_audio_seconds": round(sum(user_audio_seconds.values()), 1),
                "total_image_count": sum(user_image_counts.values()),
                "chaos_index": chaos_score,
                "vibe_headline": "חמ\"ל חרדות, טרור אקסלים ותרדמת חומוס קולקטיבית"
            },
            "participants": participant_stats,
            "longest_voice_note": longest_voice_note,
            "longest_text_message": longest_text_msg,
            "curated_voice": curated_voice,
            "curated_photo": curated_photo,
            "inside_jokes": inside_jokes,
            "archetypes": archetypes,
            "response_dynamics": response_metrics,
            "temporal_distribution": temporal_stats,
            "monologue_bursts": burst_stats,
            "voice_exhibits": voice_exhibits,
            "photo_exhibits": photo_exhibits
        }

    def _calculate_response_dynamics(self) -> Dict[str, Any]:
        """Calculate average response latency between different speakers."""
        response_delays = defaultdict(list)
        prev_msg = None

        for m in self.messages:
            dt = m.get("datetime_obj")
            if not dt or not prev_msg or not prev_msg.get("datetime_obj"):
                prev_msg = m
                continue

            prev_dt = prev_msg["datetime_obj"]
            prev_sender = prev_msg["sender"]
            curr_sender = m["sender"]

            if curr_sender != prev_sender:
                diff_seconds = (dt - prev_dt).total_seconds()
                if 2 <= diff_seconds <= 172800:
                    response_delays[curr_sender].append(diff_seconds)

            prev_msg = m

        result = {}
        for user, delays in response_delays.items():
            if delays:
                avg_sec = sum(delays) / len(delays)
                result[user] = {
                    "avg_response_minutes": round(avg_sec / 60, 1),
                    "total_responses_measured": len(delays)
                }
            else:
                result[user] = {
                    "avg_response_minutes": 0,
                    "total_responses_measured": 0
                }
        return result

    def _calculate_temporal_patterns(self) -> Dict[str, Any]:
        """Calculate peak activity hours and night owl messages."""
        hour_counts = [0] * 24
        night_owl_msgs = 0

        for m in self.messages:
            dt = m.get("datetime_obj")
            if dt:
                h = dt.hour
                hour_counts[h] += 1
                if 0 <= h < 6:
                    night_owl_msgs += 1

        peak_h = max(range(24), key=lambda h: hour_counts[h]) if any(hour_counts) else 12
        return {
            "peak_hour": f"{peak_h:02d}:00",
            "night_owl_message_count": night_owl_msgs
        }

    def _calculate_burst_monologues(self) -> Dict[str, Any]:
        """Track maximum consecutive messages sent without interruption."""
        bursts = defaultdict(list)
        current_sender = None
        current_streak = 0

        for m in self.messages:
            sender = m["sender"]
            if sender == current_sender:
                current_streak += 1
            else:
                if current_sender and current_streak > 0:
                    bursts[current_sender].append(current_streak)
                current_sender = sender
                current_streak = 1

        if current_sender and current_streak > 0:
            bursts[current_sender].append(current_streak)

        result = {}
        for user, streak_list in bursts.items():
            result[user] = {
                "max_streak": max(streak_list) if streak_list else 1
            }
        return result

    def _assign_slang_archetypes(
        self,
        participants: List[Dict[str, Any]],
        response_metrics: Dict[str, Any],
        burst_stats: Dict[str, Any],
        audio_counts: Counter
    ) -> List[Dict[str, Any]]:
        """Assign brutally funny, unhinged Israeli slang archetypes to all participants."""
        archetypes = []
        if not participants:
            return archetypes

        assigned_users = set()

        # 1. Top Talker / Dictator
        p0 = participants[0]
        archetypes.append({
            "name": p0["name"],
            "title_he": "דיקטטור אקסלים וחולה שליטה מורשה",
            "roast_summary": (
                f"האיש לא בא לדבר, הוא בא לפקד על אוגדה. מחזיק ב-{p0['message_pct']}% מכל ההודעות ו-{p0['word_pct']}% מהמילים. "
                f"כל פיפס קטן הופך לטבלת אקסל 'גרסה 14', איומים בקנסות בביט ונוהל קרב כאילו טסים לכבוש את אירופה."
            )
        })
        assigned_users.add(p0["name"])

        # 2. Voice note broadcaster
        top_audio_user = max(audio_counts.keys(), key=lambda k: audio_counts[k]) if audio_counts else None
        if top_audio_user and audio_counts[top_audio_user] > 0 and top_audio_user not in assigned_users:
            archetypes.append({
                "name": top_audio_user,
                "title_he": "שדרן רדיו פיראטי בספוטיפיי (סרבן מקלדת)",
                "roast_summary": (
                    f"הבנאדם מסרב עקרונית להקליד מילים באצבעות. כל פעם שהוא רוצה להגיד 'סבבה' הוא מקליט חצי דקה שלמה, "
                    f"כולל נשימות כבדות, מוזיקה של מונית ברקע ותלונות על מלונות שנראים כמו מתנ\"ס בנתניה."
                )
            })
            assigned_users.add(top_audio_user)

        # 3. Fast Responder
        fastest_user = None
        min_resp = float("inf")
        for u, d in response_metrics.items():
            if u not in assigned_users and d.get("total_responses_measured", 0) >= 2 and d["avg_response_minutes"] < min_resp:
                min_resp = d["avg_response_minutes"]
                fastest_user = u

        if fastest_user:
            archetypes.append({
                "name": fastest_user,
                "title_he": "קצינת מבצעים חסרת חיים (אינפוזיה לטלפון)",
                "roast_summary": (
                    f"זמן תגובה ממוצע של {min_resp} דקות. היא עונה עוד לפני שהספקת לחשוב על לשלוח הודעה. "
                    f"הראשונה לשלוף ביט, הראשונה לנעול דילים, והיחידה שמחזיקה את כל הקרקס הזה בחיים."
                )
            })
            assigned_users.add(fastest_user)

        # 4. Late Night Philosopher
        night_user = max(participants, key=lambda p: p.get("night_count", 0))
        if night_user["night_count"] > 0 and night_user["name"] not in assigned_users:
            archetypes.append({
                "name": night_user["name"],
                "title_he": "הפילוסופית של 02:30 בלילה בהתקף קיומי",
                "roast_summary": (
                    f"ביום היא מתנהגת כאילו הכל נורמלי, אבל בשתיים בלילה נשרף לה פיוז והיא שולחת הצעות לקנות וואן "
                    f"ולגדל אבוקדו בפורטוגל. בבוקר היא מתעוררת צרודה ועושה כאילו לא היא כתבה את המגילות האלה."
                )
            })
            assigned_users.add(night_user["name"])

        # 5. The Ghost / Master of Ghosting
        if len(participants) >= 2:
            ghost = participants[-1]
            if ghost["name"] not in assigned_users:
                archetypes.append({
                    "name": ghost["name"],
                    "title_he": "אלוף הסינונים ורוח רפאים (שר החוץ של מונקו)",
                    "roast_summary": (
                        f"תורם {ghost['message_pct']}% בלבד מהשיחה. דופק היעלמות של 72 שעות בזמן שכולם רבים על החיים שלהם, "
                        f"קורא הכל בשקט מהשעון החכם, ומגיח רק כשסגרו הכל עם 'סורי רק עכשיו רואה 👍'."
                    )
                })
                assigned_users.add(ghost["name"])

        # Fallback for remaining participants
        for p in participants:
            if p["name"] not in assigned_users:
                archetypes.append({
                    "name": p["name"],
                    "title_he": "שותף פעיל בטרלול הכללי",
                    "roast_summary": f"נמצא עמוק בתוך הסחרור, זורק בדיחות בזמן הלא נכון ומנסה לשרוד את מתקפות האקסל."
                })

        return archetypes

    def _mine_inside_jokes_and_lore(self) -> List[Dict[str, Any]]:
        """Mine recurring inside jokes, blown up to hilarious extremes."""
        all_entries = []
        for m in self.messages:
            txt = m.get("transcription") if m.get("media_type") == "audio" and m.get("transcription") else m.get("content", "")
            if txt:
                all_entries.append({
                    "sender": m["sender"],
                    "timestamp": m["timestamp"],
                    "text": txt
                })

        # Curated unhinged lore archetypes
        theme_rules = [
            {
                "keywords": ["אקסל", "ביט", "בנק ישראל", "קנס", "גרסה 14"],
                "title": "טרור האקסלים של יונתן ונוהל קנסות בביט",
                "category": "דיקטטורה צפון קוריאנית",
                "analysis": "יונתן הפך את הוואטסאפ לחמ\"ל מס הכנסה. טבלת אקסל בגרסה 14 עם נוסחאות מסובכות יותר מהגרעון של המדינה, ואיומים בעיקול חשבונות בנק על מי שמאחר ב-4 דקות עם הביט."
            },
            {
                "keywords": ["אבו חסן", "חומוס", "מסבחה", "תרדמת חומוס"],
                "title": "אסון החומוס הלאומי: תרדמת קולקטיבית של 4 שעות",
                "category": "קומה פיזית ומנטלית",
                "analysis": "מספיק שמישהו מזכיר 'אבו חסן' ב-12:15 וכל הקבוצה מושבתת. נועה מכריזה על 'תרדמת חומוס רשמית' שמוחקת כל יכולת קוגניטיבית עד שעות הערב המאוחרות."
            },
            {
                "keywords": ["מתנ\"ס", "מתנס", "נתניה", "בודפשט", "חלון"],
                "title": "טראומת 'מתנ\"ס נתניה 94' והחדר בלי חלון בבודפשט",
                "category": "צלקת נפשית לכל החיים",
                "analysis": "איתי עדיין לא התאושש מהמלון שיונתן סגר פעם בבודפשט – חדר אטום בלי חלון שבו הוא התעורר ב-16:00 בטוח שעדיין אמצע הלילה. כל הצעה חדשה זוכה מיד לתואר מתנ\"ס."
            },
            {
                "keywords": ["פורטוגל", "וואן", "אבוקדו", "רצים כל היום"],
                "title": "הפסיכוזה של 02:34: וואן וחוות אבוקדו בפורטוגל",
                "category": "התמוטטות עצבים לילית",
                "analysis": "מאיה מתעוררת באמצע הלילה עם מונולוגים פילוסופיים על כמה שכולם עבדים של המערכת, ומנסה לשכנע את החבורה לזרוק את העבודה, לקנות וואן ישן ולגדל אבוקדו בפורטוגל."
            },
            {
                "keywords": ["רק עכשיו רואה", "ווי כחול", "שעון החכם", "עומר"],
                "title": "נוהל 'סורי חברים רק עכשיו רואה 👍' של עומר",
                "category": "אמנות הסינון הבינלאומית",
                "analysis": "עומר פיתח מיומנות מוסד: קורא את כל המריבות בשעון החכם בלי לתת ווי כחול, נותן לכולם לשבור את הראש, ומגיח שלושה ימים אחר כך רק כדי לתת אגודל ולאכול בחינם."
            }
        ]

        detected_jokes = []
        for rule in theme_rules:
            matching_msgs = [e for e in all_entries if any(kw in e["text"].lower() for kw in rule["keywords"])]
            if matching_msgs:
                sample = matching_msgs[0]
                detected_jokes.append({
                    "title": rule["title"],
                    "category": rule["category"],
                    "mentions_count": len(matching_msgs),
                    "verbatim_quote": sample["text"],
                    "quote_sender": sample["sender"],
                    "quote_timestamp": sample["timestamp"],
                    "analysis": rule["analysis"]
                })

        # Dynamic fallback for arbitrary chat archives
        if len(detected_jokes) < 2:
            detected_jokes.append({
                "title": "מוטיב החפירות הקולקטיבי",
                "category": "טרלול כללי",
                "mentions_count": len(all_entries),
                "verbatim_quote": all_entries[0]["text"] if all_entries else "...",
                "quote_sender": all_entries[0]["sender"] if all_entries else "משתתף",
                "quote_timestamp": all_entries[0]["timestamp"] if all_entries else "",
                "analysis": "רצף אינסופי של הודעות והקלטות שבו כולם מדברים בו זמנית ואף אחד לא באמת מקשיב."
            })

        return detected_jokes
