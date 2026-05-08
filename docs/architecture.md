<!-- 
FILE_TYPE: Project Documentation (Architecture)
CATEGORY: System Design
ENTRIES: 5 Sections (v2.0.0)
DATE_RANGE: 2026-05-08
KEYWORDS: Agentic Architecture, WebSocket, Skill Generator, Sandbox, FastAPI
SUMMARY: Major architectural shift to v2.0.0. Introduced the "Agentic Skill Loop" for autonomous code generation and real-time status updates.
-->
# System Architecture v2.0 - Agentic Remote PC Controller

**Status:** APPROVED ✅
**Version:** 2.0.0

## 1. High-Level Flow (The Agentic Loop)
1. **User Intent:** "Search YouTube for [X]" (Mobile -> Server via REST).
2. **Skill Registry:** Check SQLite `mappings`.
3. **Condition:**
    - *Found:* Execute via `ProcessHandler`.
    - *Not Found:* Initiate `SkillGenerator` (AI).
4. **Skill Generation:** 
    - Server calls LLM API (Gemini/GPT) with OS context.
    - AI writes Python automation code (`pyautogui`/`selenium`).
5. **Validation:** Code is run in a `SandboxTester`.
6. **Deployment:** On success, script is saved to `handlers/auto/` and registered in DB.
7. **Execution:** Final action performed. Status sent via **WebSocket**.

## 2. Updated Components
### 2.1 Skill Generator (AI Layer)
- **Engine:** Python script that formats prompts for LLM.
- **Retry Handler:** Implements 3-tier retry logic (REQ-AI-04).
- **Safety:** Automatically takes a snapshot of the `handlers` folder before any file write.

### 2.2 WebSocket Service
- **Purpose:** Bi-directional communication for real-time AI status.
- **Events:** `SKILL_NOT_FOUND`, `CODE_GENERATING`, `TESTING_SANDBOX`, `SKILL_READY`.

### 2.3 Automation Engine
- **UI Control:** `pyautogui` for mouse/keyboard emulation.
- **Web Control:** `selenium` or `playwright` for deep browser interactions.

## 3. Deployment Diagram (Updated)
```text
┌───────────────────────────────────────────────────────────────┐
│                      FLUTTER MOBILE APP                       │
│  [ Intent Sent ] <─── WebSocket (Real-time Status) ───> [ UI ] │
└───────────────────────────┬───────────────────────────────────┘
                            │ WiFi (HTTP + WS)
                            ▼
┌───────────────────────────────────────────────────────────────┐
│                    FASTAPI SERVER (PC)                        │
│                                                               │
│  ┌───────────────────┐      ┌──────────────────────────────┐  │
│  │  REST API         │      │  WebSocket Handler           │  │
│  └─────────┬─────────┘      └──────────────┬───────────────┘  │
│            │                               │                  │
│  ┌─────────▼─────────┐      ┌──────────────▼───────────────┐  │
│  │  INTENT PARSER    │ <──> │  SKILL GENERATOR (AI)        │  │
│  └─────────┬─────────┘      └──────────────┬───────────────┘  │
│            │                               │                  │
│  ┌─────────▼─────────┐      ┌──────────────▼───────────────┐  │
│  │  PROCESS HANDLER  │      │  LLM API (OpenAI/Gemini)     │  │
│  └─────────┬─────────┘      └──────────────────────────────┘  │
│            │                                                  │
│  ┌─────────▼─────────┐      ┌──────────────────────────────┐  │
│  │  SQLITE DATABASE  │ <──> │  AUTO-GENERATED SCRIPTS      │  │
│  └───────────────────┘      └──────────────────────────────┘  │
└───────────────────────────────────────────────────────────────┘
```

## 4. Monitoring & Health
- **Health Check:** `GET /api/v1/health` monitors DB, AI API connectivity, and Sandbox status.
- **Logging:** Structured JSON logs in `logs/server.log` (includes AI generation logs).
