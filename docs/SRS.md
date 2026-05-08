<!-- 
FILE_TYPE: Project Documentation (SRS)
CATEGORY: Requirements Engineering
ENTRIES: 6 Sections (v2.0.0)
DATE_RANGE: 2026-05-08
KEYWORDS: Agentic, Self-Building, WebSocket, UI Automation, LLM, Python
SUMMARY: Major upgrade to v2.0.0. Added autonomous skill generation, command chaining, and real-time feedback via WebSockets.
-->
# SRS v2.0 - AI-Powered Remote PC Controller with Self-Building Capability

**Version:** 2.0.0
**Status:** DRAFT (Awaiting Approval)
**Standard:** IEEE 830-1998 Compliance

---

## 1. Introduction

### 1.1 Purpose
This document specifies the requirements for the **AI-Powered Remote PC Controller (v2.0)**. Unlike static controllers, this version introduces **Agentic Self-Building** capabilities, allowing the system to autonomously generate and install new automation scripts (Skills) when a user request exceeds current capabilities.

### 1.2 Scope
The system provides a Windows 11 remote control interface via a mobile app. Key innovations include:
- **Autonomous Skill Generation:** The agent writes its own code to handle new tasks.
- **UI Automation:** Deep integration with Windows UI (typing, clicking, searching).
- **Real-time Feedback:** Live status of AI "thinking" and "building" processes via WebSockets.

---

## 2. Overall Description

### 2.1 Product Perspective (Agentic System)
The system operates as a stateless FastAPI server on Windows 11, connected to a SQLite database. It leverages an external LLM (e.g., OpenAI/Gemini) as a "Coder" to generate automation logic on-the-fly.

### 2.2 Product Functions (Self-Building Flow)
1. **Request Received:** Mobile sends "Open YouTube and search X".
2. **Skill Check:** System checks if "YouTube Search" skill exists.
3. **Auto-Build:** If missing, system backups handlers, generates a Python automation script using LLM, and tests it.
4. **Execution:** Once verified, the new skill is executed and saved permanently.

### 2.3 User Classes
- **End User:** Controls PC via voice/text from mobile.
- **Admin:** Manages the Skill Database and API keys.

---

## 3. Functional Requirements (UPDATED)

### 3.1 Command Management
- **REQ-CMD-01 (Command Chaining):** System MUST support multiple actions in one intent string using separators (e.g., "AND", "THEN").
- **REQ-CMD-02 (Parametric Commands):** System MUST extract variables from intents (e.g., "Search [X] on [Y]").
- **REQ-CMD-03 (UI Automation):** System MUST support mouse clicks, keyboard typing, and scrolling using `pyautogui` and native Windows APIs.

### 3.2 Agentic Self-Building (AI Layer)
- **REQ-AI-01 (Skill Detection):** System MUST identify "Missing Skills" and initiate the Auto-Build process.
- **REQ-AI-02 (Code Generation):** System MUST interface with an LLM to generate Python automation scripts for missing tasks.
- **REQ-AI-03 (Sandbox Testing):** System MUST run generated code in a restricted environment to verify no syntax errors before final installation.
- **REQ-AI-04 (Retry Logic):** If code generation or testing fails, the system MUST retry a maximum of 3 times before reporting an error to the user.
- **REQ-AI-05 (Privacy Mode):** The user MUST have the option to disable the Auto-Build (Agentic) capability. If disabled, the system will only use existing skills.
- **REQ-RT-01 (Real-time Status):** System MUST send live updates to mobile via **WebSockets** during the building process (e.g., "⚠️ Skill not found. Building...", "✅ Skill ready!").

### 3.3 Data & Security
- **REQ-DATA-01 (Skill Database):** Every successfully generated skill must be stored as a reusable mapping in SQLite.
- **REQ-DATA-03 (Rollback Support):** Every skill MUST have a version number. The system MUST support rolling back to a previous version if a new skill causes instability.
- **REQ-SEC-01 (Integrity Guard):** System MUST perform an automated backup of the `handlers/` directory before installing any auto-generated code.
- **REQ-SEC-02 (API Key Security):** All LLM API keys MUST be stored securely in a `.env` file and never hardcoded in the source code.

---

## 4. External Interface Requirements

### 4.1 Mobile to Server
- **Protocol:** HTTP REST for standard commands, **WebSocket (WS)** for real-time status and logs.

### 4.2 Server to OS (Automation Engine)
- **Engine:** Python `subprocess` + `pyautogui` + `selenium` (for web-specific tasks).

### 4.3 AI Interface
- **Provider:** OpenAI GPT-4o or Google Gemini Pro API for code generation.

---

## 5. Non-Functional Requirements

### 5.1 Performance
- **REQ-NFR-01 (Skill Gen Time):** Skill generation and testing MUST complete within 15 seconds.
- **REQ-NFR-02 (Execution Latency):** Commands with existing skills must execute within 1 second.

### 5.2 Security
- **REQ-NFR-03 (Isolation):** Auto-generated code must not have access to sensitive system paths outside the project directory.

---

## 6. Approvals

| Role | Name | Status | Date |
|------|------|--------|------|
| **Stakeholder** | Specialist (Trainer G) | PENDING | - |
| **Architect** | Basit | APPROVED | 2026-05-08 |
| **User** | Boss | PENDING | - |
