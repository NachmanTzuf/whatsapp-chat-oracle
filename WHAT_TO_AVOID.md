# WHAT TO AVOID — WHATSAPP CHAT ORACLE
# Negative Example Archival Ledger (Constitutional Rule 2.6)

## Critique Entry 1 (2026-11-01)
- **Archived Snapshot:** `what_to_avoid_reference/index_v2_rejected.html`
- **User Critique:**
  1. **Visual Aesthetic Failure ("נראה עדיין כמו איזה שהוא אתר AI מחורבן, הכל מרובע, הכל אותו צבעים, הכל זה פשוט נראה כמו דבר ש-AI הכין"):**
     - Using repetitive dark slate Tailwind boxes (`#0d1320`, `#090d16`) with uniform 1px borders (`border-slate-800`) and uniform boxy cards screams generic AI boilerplate.
     - Never build "by eye" using generic dark-mode dashboard grids. Must use an Awwwards-winning editorial/luxury or warm tactile publication design (such as OKLCH warm editorial paper/ink or high-contrast asymmetric magazine typography with fluid `clamp()` scales, organic whitespace, and zero repetitive boxy containers).
  2. **UI Clutter & Missing Primary Action ("לא הרבה כפתורים, אבל למעלה כפתור איך לעשות upload לכל הדבר. לכפתור אחד שלוחצים עליו וזה מדפיס את הדוח המלא בלחיצת כפתור, כפתור מאוד ברור"):**
     - Too many scattered small buttons and fake inputs (like a group link box that just pops up an alert).
     - Must have a clean, focused top area: a clear way to Upload the full WhatsApp `.zip` (with concise instructions on how to export), and ONE unmistakable, prominent primary button to Print / Export the Full Report in a single click.
  3. **Shallow / Fake Static Report ("הדוח צריך להיות הרבה יותר מפורט, מעבר לאנליזה שזה נותן ממש כאילו לבנות את כל הסיפור מאחורי הקבוצה. הדוח ממש מפורט צריך להיות עם כל מיני בדיחות פנימיות, צחוקים"):**
     - In `index_v2_rejected.html`, uploading a file only updated 4 numbers and the table, leaving the 5 chapters of text hardcoded to the demo names ("יונתן כהן", "נועה לוי")! That is unacceptable.
     - The report generator must dynamically construct a massive, deeply detailed, hilarious multi-chapter narrative from the *actual* uploaded chat (and for the default showcase), extracting real verbatim quotes, real inside jokes, real awkward moments, late-night meltdowns, consecutive message spams, media habits, and turning the entire history of the group into a rich, comedic, investigative story.
  4. **Inability to Read Images & Voice Notes ("תעתיק את זה בצורה שזה באמת יכול לקרוא תמונות ולקרוא הודעות קוליות, כי כרגע זה ממש לא יכול"):**
     - A static client-side-only HTML file using only regex on `.txt` ignores the actual `.opus`/`.ogg` voice recordings and `.jpg`/`.png` photos inside the `.zip`!
     - We must run a real backend server (Python HTTP + API server on `localhost:8089`) so when a `.zip` (or folder/files) is uploaded in the browser, the backend genuinely unpacks all `.opus`/`.ogg`/`.mp3`/`.m4a` voice recordings, transcribes them into Hebrew text using `faster-whisper`, analyzes all `.jpg`/`.png`/`.webp` images (extracting EXIF/visual features, dominant colors, aspect ratios, OCR/vision descriptions, and displaying the actual photos inline as visual exhibits in the report!), and weaves the transcribed voice notes and actual photos directly into the story and timeline!

## Critique Entry 2 (2026-11-01)
* **Archived Snapshot:** `what_to_avoid_reference/index_v3_rejected_academic_dump.html`
* **User Critique:**
  1. **Academic High Register Failure:** The previous report used formal, journalistic, high register Hebrew ("ניתוח פורנזי", "חמ\"ל מבצעים", "מאזן כוחות"). The user wants authentic Israeli street slang ("חופר ברמות", "שרוט לגמרי", "פודקאסט לא מורשה", "סינונים", "טרלול מוחלט", "עבריין מקלדת").
  2. **Lack of Wild Exaggeration:** The text treated the chat too seriously or moderately. It must be wildly exaggerated and unhinged, depicting the group as an absolute madhouse, a cult, or a mental asylum rather than a normal group of friends.
  3. **Exhaustive Evidence Dump:** Dumping every single voice note and photo creates clutter. All analysis, transcription, and vision scanning must happen behind the scenes, and the report should only curate and spotlight the top 1 or 2 most unhinged voice notes and photos with maximum reactions and brutal roasts.
  4. **Too Long / Missing Immediate Punchy Metrics:** The report was too dense with long essays before presenting simple metrics. The user demands a clear sequence:
     * First: A clean, punchy table showing message counts, word shares, and average response times plus 2 or 3 fun metrics per person.
     * Second: The absolute longest voice note (who, how long, transcript, and roast) and longest text message (who, word count, exact quote, and roast).
     * Third: High-level unhinged lore and exaggerated recurring themes across the group.
     * Fourth: Curated spotlights on the wildest evidence only.
  5. **Mobile Responsiveness Optimization:** The previous layout was desktop-centric. The mobile layout must be flawless with zero horizontal overflow, thumb-friendly tap targets, readable fluid typography, and stacked responsive tables.
