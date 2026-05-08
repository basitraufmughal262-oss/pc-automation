<!-- 
FILE_TYPE: Project Governance (Change Log)
CATEGORY: Project Management
ENTRIES: 3 Major Revisions
DATE_RANGE: 2026-05-07
KEYWORDS: History, Versions, Approvals, Baselines
SUMMARY: Chronological record of all project requirement changes and client approvals for the Remote PC Controller.
-->
# Change Log - Remote PC Controller

All requirement changes and project approvals are recorded here.

| Date | Version | Change Description | Approval Status |
|------|---------|--------------------|-----------------|
| 2026-05-07 | 1.0.0 | Initial Project Discovery & Draft SRS | Drafted |
| 2026-05-07 | 1.1.0 | Finalized SRS with SQLite, Native Voice, and Win11 specifics | **APPROVED ✅** |
| 2026-05-07 | 1.1.1 | Refined Database Schema with audit columns and SQL DDL | Validated |
| 2026-05-07 | 1.2.0 | Finalized SRS & API Design with Versioning, Rate Limits, and Error IDs | **BASELINED ✅** |
| 2026-05-08 | 2.0.0 | **Major Evolution:** Added Self-Building (Agentic) capability, UI Automation engine, and WebSocket real-time feedback. Transitioned from static controller to autonomous assistant. | APPROVED ✅ |
| 2026-05-08 | 2.0.1 | **Schema Update:** Refined DB tables to support versions, privacy mode, and auto-generated scripts. | **APPROVED ✅** |
| 2026-05-08 | 2.1.0 | **Schema Fix:** Added `retry_count`, `skill_id`, and `RETRYING` status to `command_logs` (Trainer's recommendation). | **APPROVED ✅** |
| 2026-05-08 | 2.1.1 | **PROJECT POSTPONED:** Backend 70% done. Pending: LLM Integration + Mobile App. Full details in HANDOFF.md | ⏸️ PAUSED |
