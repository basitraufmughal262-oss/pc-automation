# Discovery Session 01: Remote PC Controller (Structured Interview)

**Date:** 2026-05-07
**Project:** Remote PC Controller
**Status:** INTERVIEW IN PROGRESS

## 🎤 Interview Log (Step-by-Step)

| # | Question | Answer | Status |
|---|----------|--------|--------|
| 1 | What is the Operating System (OS) of the PC we are controlling? (e.g., Windows 10/11, Linux) | Windows 11 | Done |
| 2 | Do you require Authentication (API Key/Password) for the WiFi communication? | Yes (API Key required) | Done |
| 3 | Besides websites, what specific Desktop Apps (e.g., Slack, VS Code) should be launchable? | Dynamic/Configurable mapping (Add apps/paths as needed) | Done |
| 4 | If the server restarts, should the timer resume the last session or reset? | Yes (Resume last session) | Done |
| **Note** | **Core Concept** | Intent-based: Voice, Type, or Click to trigger PC commands. | - |
| 5 | What should be the default 'Grace Period' (in seconds) for Shutdown cancellation? | 60 seconds | Done |
| 6 | Are there any specific reports you want from the SQLite database later? | Yes (Weekly summary, App usage frequency, 24h Activity Log) | Done |

## 📐 Final Technical Decisions
- **Q1 (Storage):** App mappings/paths will be stored in **SQLite Database** (not JSON).
- **Q2 (Voice):** Voice-to-Text will be handled by **Mobile Native Engines** (Android/iOS).
- **Q3 (Auth):** Initial implementation will use a **Single API Key**.
- **Q4 (Platforms):** Deployment targeted for **Both Android & iOS**.

---
**Status:** INTERVIEW COMPLETE ✅
