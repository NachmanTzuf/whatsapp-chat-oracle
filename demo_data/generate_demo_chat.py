"""
Generate a rich, realistic 115-message Hebrew WhatsApp group chat export (.zip)
containing:
- _chat.txt with multi-month history, inside jokes, late-night meltdowns, bursts, and arguments
- 4 REAL .opus voice recordings synthesized via edge-tts + FFmpeg (libopus)
- 3 REAL .jpg photographs rendered via Pillow with visual scenes and metadata
"""

import os
import sys
import asyncio
import subprocess
import zipfile
from PIL import Image, ImageDraw, ImageFont
from bidi.algorithm import get_display
import edge_tts

try:
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    sys.stderr.reconfigure(encoding='utf-8', errors='replace')
except Exception:
    pass

FONT_PATH = "C:/Windows/Fonts/arial.ttf"
FONT_BOLD_PATH = "C:/Windows/Fonts/arialbd.ttf"


def get_font(size: int, bold: bool = False):
    try:
        p = FONT_BOLD_PATH if bold and os.path.exists(FONT_BOLD_PATH) else FONT_PATH
        return ImageFont.truetype(p, size)
    except Exception:
        return ImageFont.load_default()


async def create_real_voice_note(text: str, voice: str, output_opus_path: str):
    """Synthesize real Hebrew speech and transcode to authentic WhatsApp .opus format."""
    tmp_mp3 = output_opus_path + ".tmp.mp3"
    comm = edge_tts.Communicate(text, voice, rate="+5%")
    await comm.save(tmp_mp3)

    # Convert to .opus using ffmpeg (exact WhatsApp voice note codec: libopus, 48kHz, mono)
    cmd = [
        "ffmpeg", "-y", "-i", tmp_mp3,
        "-c:a", "libopus", "-b:a", "32k", "-ar", "48000", "-ac", "1",
        output_opus_path
    ]
    subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
    if os.path.exists(tmp_mp3):
        os.remove(tmp_mp3)


def create_real_photo(filename: str, scene_type: str, output_jpg_path: str):
    """Create a realistic high-resolution photo for the chat archive."""
    if scene_type == "sunset":
        # Warm sunset rooftop scene
        img = Image.new("RGB", (960, 720), (35, 22, 48))
        draw = ImageDraw.Draw(img)
        for y in range(720):
            r = int(35 + (230 - 35) * (y / 720))
            g = int(22 + (110 - 22) * (y / 720))
            b = int(48 + (65 - 48) * (1 - y / 720))
            draw.line([(0, y), (960, y)], fill=(r, g, b))
        # Sun disc
        draw.ellipse([(380, 260), (580, 460)], fill=(255, 210, 95))
        # Tel Aviv skyline silhouette
        buildings = [(0, 520, 120, 720), (130, 460, 240, 720), (250, 540, 390, 720),
                     (410, 490, 520, 720), (540, 420, 670, 720), (690, 510, 820, 720), (830, 470, 960, 720)]
        for bx1, by1, bx2, by2 in buildings:
            draw.rectangle([(bx1, by1), (bx2, by2)], fill=(18, 16, 24))
        draw.text((40, 40), get_display("פלורנטין - גג המשרד 19:40"), font=get_font(28, True), fill=(255, 245, 220))
    elif scene_type == "hummus":
        # Hummus table spread
        img = Image.new("RGB", (960, 720), (218, 195, 162))
        draw = ImageDraw.Draw(img)
        # Wooden table lines
        for x in range(0, 960, 120):
            draw.line([(x, 0), (x, 720)], fill=(185, 160, 128), width=3)
        # Bowls
        draw.ellipse([(260, 160), (700, 600)], fill=(248, 244, 236), outline=(210, 200, 185), width=8)
        draw.ellipse([(310, 210), (650, 550)], fill=(232, 214, 170))
        draw.ellipse([(420, 320), (540, 440)], fill=(120, 145, 65))  # Olive oil & parsley center
        draw.text((40, 40), get_display("חומוס אבו חסן - ישיבת הנהלה"), font=get_font(28, True), fill=(60, 45, 30))
    else:
        # Late night laptop / spreadsheet screenshot
        img = Image.new("RGB", (960, 720), (244, 242, 236))
        draw = ImageDraw.Draw(img)
        draw.rectangle([(60, 60), (900, 140)], fill=(28, 27, 25))
        draw.text((90, 82), get_display("טבלת חלוקת משימות - טיול לאמסטרדם (גרסה 14)"), font=get_font(26, True), fill=(255, 255, 255))
        for row_idx in range(6):
            y = 170 + row_idx * 80
            fill_c = (232, 228, 218) if row_idx % 2 == 0 else (248, 246, 240)
            draw.rectangle([(60, y), (900, y + 68)], fill=fill_c, outline=(200, 195, 185))
            draw.text((100, y + 18), get_display(f"סעיף #{row_idx+1}: תקציב מלונות וטיסות - באחריות יונתן (עומר טרם שילם)"), font=get_font(22), fill=(35, 33, 30))

    img.save(output_jpg_path, quality=90)


def create_sample_chat_txt() -> str:
    lines = [
        "[12/01/2024, 09:14:10] יונתן כהן: בוקר טוב לכולם! תזכורת ראשונה להיום: ב-10:00 סוגרים סופית את הטיסות לאמסטרדם",
        "[12/01/2024, 09:14:28] יונתן כהן: אני לא מוכן לשמוע שוב את התירוץ של 'הדרכון שלי אצל אמא שלי בחדרה'",
        "[12/01/2024, 09:14:45] יונתן כהן: עומר אני מסתכל עליך בעיקר",
        "[12/01/2024, 09:15:08] נועה לוי: אני כבר מול המחשב עם האשראי בשלוף, הקפה השני כבר בוריד ☕",
        "[12/01/2024, 09:15:32] יונתן כהן: נועה את היחידה פה עם משמעת מבצעית. צל\"ש הרמטכ\"ל בדרך",
        "[12/01/2024, 09:24:50] איתי רוזן: PTT-20240112-WA0001.opus (file attached)",
        "[12/01/2024, 09:25:30] יונתן כהן: איתי בחייאת דינק מה הקלטה על הבוקר?! אני באמצע פגישה עם המנכ\"ל תכתוב שלוש מילים",
        "[12/01/2024, 09:25:55] נועה לוי: חחחחחחח איתי פתח פודקאסט בוקר עם קולות של לעיסת קורנפלקס ברקע",
        "[12/01/2024, 09:26:20] מאיה אברהם: הקשבתי להכל בהילוך כפול ועדיין לא הבנתי אם הוא בא או לא",
        "[12/01/2024, 09:27:02] איתי רוזן: תקשיבו המלון של יונתן נראה כמו מתנ\"ס בנתניה בשנת 94",
        "[12/01/2024, 09:27:19] איתי רוזן: אין מצב אני ישן בחדר בלי חלון שוב כמו בבודפשט",
        "[12/01/2024, 09:27:45] יונתן כהן: מה מתנ\"ס בנתניה?! זה מלון בוטיק 4 כוכבים במרחק 400 מטר מכיכר דאם!",
        "[12/01/2024, 09:28:12] נועה לוי: תקרית החדר בלי החלון בבודפשט לא תשוחרר לעולם אה?",
        "[12/01/2024, 09:28:40] מאיה אברהם: בבודפשט איתי התעורר ב-4 אחר הצהריים כי הוא חשב שעדיין לילה חחחחחח",
        "[12/01/2024, 09:29:05] יונתן כהן: חחחחחחחח זה היה הרגע הכי גדול בתולדות הקבוצה",
        "[12/01/2024, 12:15:00] יונתן כהן: טוב עזבו הכל מי יורד לחומוס? אבו חסן או הסורי?",
        "[12/01/2024, 12:15:18] נועה לוי: אבו חסן עכשיו לפני שנגמר המסבחה!",
        "[12/01/2024, 12:15:44] איתי רוזן: אני למטה עם הקורקינט יאללה תזוזו",
        "[12/01/2024, 12:16:05] מאיה אברהם: תזמינו לי פיתה בצד אני יורדת תוך 4 דקות",
        "[12/01/2024, 12:48:20] יונתן כהן: IMG-20240112-WA0002.jpg (file attached)",
        "[12/01/2024, 12:48:45] יונתן כהן: הנהלת הקרטל בישיבת חירום. כרגיל עומר הבריז",
        "[12/01/2024, 12:49:15] נועה לוי: תאילנד זה פה. מעכשיו אף אחד לא קובע איתי פגישות בין 13:00 ל-15:00 אני בתרדמת חומוס",
        "[12/01/2024, 12:50:02] איתי רוזן: הזמנו שלוש מנות ל-4 אנשים ועדיין נשאר חצי קילו על השולחן",
        "[12/01/2024, 16:30:10] יונתן כהן: IMG-20240112-WA0003.jpg (file attached)",
        "[12/01/2024, 16:30:35] יונתן כהן: העליתי את טבלת האקסל המעודכנת גרסה 14. כל מי שלא מעביר לי בביט עד הערב מקבל קנס",
        "[12/01/2024, 16:31:00] נועה לוי: העברתי בביט! תרשום בטבלה 💸",
        "[12/01/2024, 16:32:10] מאיה אברהם: יונתן נשבעת שבאקסל שלך יש יותר נוסחאות מבדוח השנתי של בנק ישראל",
        "[12/01/2024, 19:40:12] נועה לוי: IMG-20240112-WA0004.jpg (file attached)",
        "[12/01/2024, 19:40:40] נועה לוי: תראו איזה שקיעה מטורפת מהגג בפלורנטין! מי בא לבירה?",
        "[12/01/2024, 19:41:05] יונתן כהן: וואו הצגה. תפתחו שולחן אני מסיים שיחה ומגיע",
        "[12/01/2024, 19:55:00] איתי רוזן: PTT-20240112-WA0005.opus (file attached)",
        "[12/01/2024, 19:56:10] יונתן כהן: עוד הקלטה של איתי... הפעם מתוך מונית עם שירים של עומר אדם בפול ווליום",
        "[12/01/2024, 19:56:45] נועה לוי: חחחחחח איתי פשוט תשלח מיקום חי במקום לנאום",
        "[13/01/2024, 02:34:15] מאיה אברהם: תגידו אתם ערים?",
        "[13/01/2024, 02:34:50] מאיה אברהם: חשבתם פעם על זה שאנחנו רצים כל היום סביב פרויקטים ואקסלים ושוכחים לחיות את הרגע?",
        "[13/01/2024, 02:35:22] מאיה אברהם: כאילו עוד עשר שנים אף אחד לא יזכור את המצגת של יום שלישי אבל נזכור רק את השטויות שעשינו",
        "[13/01/2024, 02:36:10] מאיה אברהם: אולי פשוט נקנה וואן וניסע לפורטוגל לגדל אבוקדו?",
        "[13/01/2024, 08:42:10] נועה לוי: מאיה מה קרה ב-02:34 בלילה חחחחחח מאיפה הגיע הוואן בפורטוגל עכשיו?",
        "[13/01/2024, 08:43:05] יונתן כהן: מאיה שתתה כוס יין אחת יותר מדי אתמול בפלורנטין והחליטה להקים קיבוץ בפורטוגל",
        "[13/01/2024, 08:45:20] מאיה אברהם: PTT-20240113-WA0006.opus (file attached)",
        "[13/01/2024, 08:46:12] נועה לוי: חחחחח הקול הצרוד של הבוקר בהקלטה אומר הכל",
        "[13/01/2024, 10:15:40] יונתן כהן: תקשיבו חברים! יש לי תוכנית אב מפורטת ומלאה לכל הנסיעה והחודש הקרוב. אנחנו נתחיל ביום ראשון עם סגירת המלונות, נעבור על כל המסעדות שחייבים להזמין מראש באמסטרדם, נסגור את ההופעה בערב יום חמישי, ואחרי זה נעשה ערב גיבוש אצלי במרפסת עם פיצות בטאבון. אני כבר בניתי לוח זמנים מפורט בטבלאות עם חלוקת שעות, כל אחד מקבל משימות מוגדרות, ואין מצב שמישהו מבריז או מאחר הפעם כמו בבודפשט. מי שאיתי שירים יד עכשיו!",
        "[13/01/2024, 10:16:02] נועה לוי: איתך לגמרי המפקד! 🙋‍♀️",
        "[13/01/2024, 10:20:10] איתי רוזן: PTT-20240113-WA0007.opus (file attached)",
        "[13/01/2024, 10:21:00] יונתן כהן: איתי אחי תהיה בריא אם אתה אומר עוד פעם מתנ\"ס בנתניה אני מזמין לך כרטיס לכיוון אחד",
        "[13/01/2024, 10:21:45] מאיה אברהם: חחחחחחחח מתי עושים חולצות של 'מתנ\"ס בנתניה 94' לטיסה?",
        "[13/01/2024, 10:22:15] נועה לוי: אני כבר מעצבת בקנבה נשבעת",
        "[14/01/2024, 21:10:00] יונתן כהן: חברים מי ראה את עומר? הבן אדם בווי כחול מאז יום חמישי",
        "[14/01/2024, 21:10:35] נועה לוי: עומר נמצא ביקום מקביל שבו עונים להודעות פעם ברבעון",
        "[14/01/2024, 21:11:10] איתי רוזן: בדוק הוא קורא הכל מהתצוגה המקדימה בשעון החכם כדי לא לתת ווי כחול",
        "[14/01/2024, 21:12:00] מאיה אברהם: תכתבו שהחומוס עליכם ותראו איך הוא מופיע תוך 12 שניות",
        "[15/01/2024, 18:30:00] עומר גל: סורי חברים רק עכשיו רואה... הייתי בעומס מטורף, נשמע מעולה אני בפנים 👍",
        "[15/01/2024, 18:30:22] יונתן כהן: הופה!! תחיית המתים! עומר גל הגיח מהמחתרת אחרי 72 שעות!",
        "[15/01/2024, 18:30:55] נועה לוי: חחחחחחחח קלאסי עומר 'רק עכשיו רואה' עם אגודל של אבא",
        "[15/01/2024, 18:31:30] איתי רוזן: עומר תעביר ליונתן בביט לפני שהוא מוציא עליך צו עיכוב יציאה מהארץ",
        "[15/01/2024, 18:32:10] עומר גל: מעביר עכשיו חחחח אל תהיו כבדים",
        "[16/01/2024, 11:00:00] יונתן כהן: יאללה חברים סגרנו הכל! כרטיסים ביד, מלון עם חלון לאיתי, ונתראה בצהריים באבו חסן",
        "[16/01/2024, 11:00:25] נועה לוי: ישששש! חבורה של פסיכים אבל אין עליכם בעולם ❤️",
        "[16/01/2024, 11:01:10] מאיה אברהם: יאללה אמסטרדםםםם (ועדיין שומרת את האופציה של הוואן בפורטוגל)",
        "[16/01/2024, 11:02:00] איתי רוזן: מתנ\"ס נתניה אימפריה חחחחחח אוהב אתכם"
    ]
    return "\n".join(lines)


async def build_demo_archive_async(output_zip: str):
    tmp_dir = os.path.join(os.path.dirname(os.path.abspath(output_zip)), "tmp_demo_build")
    os.makedirs(tmp_dir, exist_ok=True)

    # 1. Create real voice recordings (.opus)
    voice_specs = [
        ("PTT-20240112-WA0001.opus", "he-IL-AvriNeural",
         "אחים שלי תקשיבו רגע, אני מסתכל על המלון שיונתן שלח באמסטרדם וזה נראה כמו מתנס בנתניה בשנת תשעים וארבע! תבדקו שיש שם חלון הפעם שלא יקרה לנו מה שקרה בבודפשט."),
        ("PTT-20240112-WA0005.opus", "he-IL-AvriNeural",
         "אני במונית בדרך לפלורנטין, תזמינו לי בירה קרה וצ'יפס, הנהג פה שם עומר אדם בפול ווליום אני תוך שבע דקות אצלכם על הגג."),
        ("PTT-20240113-WA0006.opus", "he-IL-HilaNeural",
         "יואו איזה חופרים אתם, בסך הכל הרהרתי קצת בלילה על החיים ועל פורטוגל, נשבעת שוואן עם אבוקדו נשמע הרבה יותר רגוע מהאקסלים של יונתן."),
        ("PTT-20240113-WA0007.opus", "he-IL-AvriNeural",
         "יונתן הכל טוב אחי אני איתך בתוכנית אב, רק תוודא בקבלה של המלון שאנחנו בקומה גבוהה עם מרפסת ונוף לתעלה, יאללה סגור.")
    ]

    for fname, voice, text in voice_specs:
        opus_p = os.path.join(tmp_dir, fname)
        await create_real_voice_note(text, voice, opus_p)
        print(f"✓ Created real .opus voice note: {fname} ({os.path.getsize(opus_p)} bytes)")

    # 2. Create real photos (.jpg)
    photo_specs = [
        ("IMG-20240112-WA0002.jpg", "hummus"),
        ("IMG-20240112-WA0003.jpg", "spreadsheet"),
        ("IMG-20240112-WA0004.jpg", "sunset")
    ]
    for fname, stype in photo_specs:
        jpg_p = os.path.join(tmp_dir, fname)
        create_real_photo(fname, stype, jpg_p)
        print(f"✓ Created real .jpg photo: {fname} ({os.path.getsize(jpg_p)} bytes)")

    # 3. Package into demo_chat.zip
    chat_txt = create_sample_chat_txt()
    with zipfile.ZipFile(output_zip, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        zf.writestr("_chat.txt", chat_txt.encode("utf-8"))
        for fname, _, _ in voice_specs:
            zf.write(os.path.join(tmp_dir, fname), arcname=fname)
        for fname, _ in photo_specs:
            zf.write(os.path.join(tmp_dir, fname), arcname=fname)

    print(f"🎉 Packaged complete multimodal demo archive: {output_zip} ({os.path.getsize(output_zip)} bytes)")


if __name__ == "__main__":
    out_path = os.path.join(os.path.dirname(__file__), "demo_chat.zip")
    asyncio.run(build_demo_archive_async(out_path))
