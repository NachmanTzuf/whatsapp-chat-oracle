"""
WhatsApp Chat Oracle - Unhinged Slang Narrative & Rapid-Fire Interview Engine
Constructs hyper-exaggerated group lore, punchy roasts, and a street-fluent
comedic confrontation between the investigator and the chat members.
"""

from typing import Dict, Any, List


class InterviewerEngine:
    def __init__(self, analytics_data: Dict[str, Any]):
        self.data = analytics_data
        self.summary = analytics_data.get("summary", {})
        self.participants = analytics_data.get("participants", [])
        self.longest_text = analytics_data.get("longest_text_message", {})
        self.longest_voice = analytics_data.get("longest_voice_note", {})
        self.inside_jokes = analytics_data.get("inside_jokes", [])
        self.curated_voice = analytics_data.get("curated_voice")
        self.curated_photo = analytics_data.get("curated_photo")

    def generate_full_interviewer_script(self) -> Dict[str, Any]:
        """Generate short, punchy, unhinged Israeli street slang narrative and dialogue."""
        if not self.participants:
            return {"error": "Insufficient participant data to build script."}

        p1 = self.participants[0]
        p2 = self.participants[1] if len(self.participants) > 1 else p1
        p_last = self.participants[-1]
        total_msgs = self.summary.get("total_messages", 0)
        total_words = self.summary.get("total_words", 0)
        total_audio = self.summary.get("total_audio_count", 0)
        total_images = self.summary.get("total_image_count", 0)

        # 1. Collective Madness Lore: Blown-up hilarious incidents
        collective_lore = self._build_unhinged_lore(p1, p2, p_last)

        # 2. Rapid-fire comedic interview Q&A
        interview_dialogue = self._build_rapid_interview(p1, p2, p_last)

        # 3. 30-Second Fast-Motion Video Script (Spoken street Hebrew)
        video_30s_script = (
            f"סרקתי מעל עשרת אלפים קבוצות וואטסאפ, אבל הקבוצה הזו היא אשפוז דחוף. "
            f"מתוך {total_msgs:,} הודעות, {p1['name']} משליט דיקטטורת אקסלים עם {p1['message_pct']}% מהדיבור, "
            f"בזמן ש-{p2['name']} עונה תוך שניות כמו חמ\"ל מבצעים. "
            f"פיענחנו {total_audio} הקלטות קוליות של פודקאסטים פיראטיים, {total_images} תמונות שטח מפלילות, "
            f"תרדמת חומוס קולקטיבית והתמוטטות עצבים בארבע לפנות בוקר על וואן בפורטוגל. "
            f"המסקנה: אתם שרוטים על כל הראש, אבל אין סיכוי שתתפרקו."
        )

        return {
            "title": "תיק החקירה המטורלל: הדו\"ח הסודי של הקבוצה",
            "subtitle": f"סריקה מלאה של {total_msgs:,} הודעות, {total_words:,} מילים, {total_audio} הקלטות קוליות ו-{total_images} תמונות שחשפה שהקבוצה הזו רחוקה מלהיות שפויה",
            "vibe_headline": "חמ\"ל חרדות, טרור אקסלים ותרדמת חומוס קולקטיבית",
            "host_persona": "החוקר הראשי | ארכיון 10,000 הקבוצות",
            "collective_lore": collective_lore,
            "interview_dialogue": interview_dialogue,
            "video_30s_script_he": video_30s_script
        }

    def _build_unhinged_lore(self, p1: dict, p2: dict, p_last: dict) -> List[Dict[str, Any]]:
        """Build 4 ultra-exaggerated, hilarious collective incidents."""
        return [
            {
                "id": "LORE-01",
                "tag": "דיקטטורה צפון קוריאנית",
                "title": f"טרור האקסלים של {p1['name']} ונוהל קנסות בביט",
                "story": (
                    f"האיש לא מנהל שיחה של חברים, הוא מנהל מחנה צבאי סגור. "
                    f"במקום לכתוב 'מתי נוסעים?', הוא הנחית על הקבוצה קובץ אקסל ב'גרסה 14' עם יותר נוסחאות, עמודות וסעיפים מהתקציב של משרד הביטחון. "
                    f"מי שלא העביר מקדמה בביט בתוך 12 דקות זכה לאזהרות עיקול חשבונות ולחפירה של 150 מילים ברצף."
                ),
                "punchline": "החברים הודו בסתר שהם עשו לו לייק רק כדי שלא יפתח גרסה 15 של האקסל."
            },
            {
                "id": "LORE-02",
                "tag": "קומה פיזית ומנטלית",
                "title": "אסון החומוס הלאומי: תרדמת קולקטיבית שהשביתה את המשק",
                "story": (
                    "בשעה 12:15 מישהו זרק את המילה 'אבו חסן' בצ'אט. תוך 40 שניות כל משימות העבודה ננטשו, פגישות זום בוטלו בתירוצים הזויים, "
                    "וכל החבורה התייצבה על צלחת מסבחה. "
                    "התוצאה: הכרזה על 'תרדמת חומוס רשמית' ומחיקה מוחלטת של כל יכולת קוגניטיבית בין 13:00 ל-15:30. "
                    "אף הודעה לא נענתה, ואף משימה לא התקדמה."
                ),
                "punchline": "המשק הישראלי הפסיד שעות עבודה יקרות רק כי המסבחה הייתה חמה מדי."
            },
            {
                "id": "LORE-03",
                "tag": "התמוטטות עצבים לילית",
                "title": "הפסיכוזה של 02:34: וואן וחוות אבוקדו בפורטוגל",
                "story": (
                    "באמצע הלילה, כשכל בנאדם נורמלי ישן, נפתחה בקבוצה סדרת הודעות היסטרית. "
                    "מונולוג שלם על כמה שהחיים הם מרוץ עכברים, כמה שהמשרד והמצגות חונקים, והצעה רצינית לחלוטין למכור את הדירות, "
                    "לקנות וואן מתפרק ולגדל אבוקדו בפורטוגל. "
                    "בבוקר שאחרי, כולם התעוררו עם כאב ראש ועשו כאילו שום דבר לא קרה."
                ),
                "punchline": "בבדיקת מעבדה נמצא שפורטוגל הוזכרה 4 פעמים בלילה ו-0 פעמים באור יום."
            },
            {
                "id": "LORE-04",
                "tag": "אמנות הסינון של שר החוץ",
                "title": f"נוהל 'סורי חברים רק עכשיו רואה 👍' של {p_last['name']}",
                "story": (
                    f"{p_last['name']} פיתח טכניקת הישרדות ברמת מוסד: הוא רואה את כל המריבות, ההקלטות והאקסלים מהתצוגה של השעון החכם "
                    f"כדי לא להשאיר ווי כחול מחייב. "
                    f"במשך 72 שעות כולם צועקים את השם שלו, והוא בדממת אלחוט מוחלטת. "
                    f"רק כשהכל כבר סגור, מוזמן ושולם, הוא מגיח עם תגובה של שתי שניות."
                ),
                "punchline": "האיש חי כאילו הוא שר החוץ של מונקו – שולח יונת דואר פעם בחודש."
            }
        ]

    def _build_rapid_interview(self, p1: dict, p2: dict, p_last: dict) -> List[Dict[str, Any]]:
        """Rapid-fire, hilarious street slang interrogation with chat members."""
        dialogue = [
            {
                "speaker": "החוקר",
                "role": "ראש ארכיון 10,000 הקבוצות",
                "text": f"תגיד לי {p1['name']}, ראיתי אלפי קבוצות בחיים שלי, אבל למה לעזאזל לנהל חברים עם טבלת אקסל שיש בה יותר סעיפים מהגרעון של המדינה?!"
            },
            {
                "speaker": p1["name"],
                "role": "מנכ\"ל הטבלאות וחולה שליטה",
                "text": "כי אם אני לא מוציא אקסל בגרסה 14 ומאיים עליהם בקנסות בביט, כולנו נתקעים עד היום בנתניה ומתווכחים שלוש שעות על מי מזמין מונית. מישהו פה חייב להיות המבוגר האחראי!"
            },
            {
                "speaker": "החוקר",
                "role": "ראש ארכיון 10,000 הקבוצות",
                "text": f"ואתה איתי, יש פה הקלטות קוליות של חצי דקה שבהן אתה רק מתנשף וצועק על מתנ\"ס משנת 94. מה נסגר? אין לך מקלדת בטלפון?"
            },
            {
                "speaker": "איתי",
                "role": "שדרן הפודקאסט הפיראטי",
                "text": "אחי, אני לא מקליד כשאני נסער! יש לי טראומה מבודפשט שיונתן שם אותנו בחדר בלי חלון, קמתי בארבע אחרי הצהריים בחושך וחשבתי שהגיע סוף העולם. אין מצב אני ישן במתנ\"ס שוב."
            },
            {
                "speaker": "החוקר",
                "role": "ראש ארכיון 10,000 הקבוצות",
                "text": f"{p2['name']}, את עונה לכל הודעה תוך 36 שניות. את מחוברת לטלפון באינפוזיה לווריד או שאין לך עבודה?!"
            },
            {
                "speaker": p2["name"],
                "role": "קצינת המבצעים המיידית",
                "text": "מישהו פה צריך לסגור כרטיסים לפני שהמחיר קופץ ב-400 שקל! חוץ מזה בין אחת לשלוש אני בתרדמת חומוס אטומה, אז אם לא עניתי בבוקר הלך על כולנו."
            },
            {
                "speaker": "החוקר",
                "role": "ראש ארכיון 10,000 הקבוצות",
                "text": f"ו-{p_last['name']}... אלוף הסינונים. שלושה ימים של דממת אלחוט, כולם צועקים איפה אתה, ואז אתה מגיח כמו שר החוץ של מונקו עם אגודל לקוני?"
            },
            {
                "speaker": p_last["name"],
                "role": "רוח רפאים",
                "text": "סורי אחי, רק עכשיו רואה... הייתי בישיבה. נשמע מעולה אני בפנים 👍"
            },
            {
                "speaker": "החוקר",
                "role": "פסק הדין הסופי",
                "text": "המסקנה שלי ברורה: הקבוצה הזו היא שילוב מוחלט של דיקטטורה, חרדות, עצלנות והתקפי חומוס. במילים אחרות: אתם החברים הכי טובים שיש."
            }
        ]
        return dialogue
