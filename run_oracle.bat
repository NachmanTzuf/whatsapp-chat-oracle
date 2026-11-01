@echo off
chcp 65001 >nul
echo ============================================================================
echo   WHATSAPP CHAT ORACLE : MULTIMODAL UNHINGED REPORT (PORT 8090)
echo ============================================================================
cd /d "C:\Users\Hp\.gemini\antigravity\scratch\whatsapp_chat_oracle"
start "" "http://localhost:8090/"
python "C:\Users\Hp\.gemini\antigravity\scratch\whatsapp_chat_oracle\server.py" 8090
pause
