<!-- 
FILE_TYPE: UI/UX Specification
CATEGORY: Mobile App
ENTRIES: 4 Zones, Color Palette, Tech Stack
DATE_RANGE: 2026-05-08
KEYWORDS: Flutter, UI, Hybrid Design, Glassmorphism, PC Stats
SUMMARY: Detailed UI/UX specification for the Remote PC Controller mobile application (v1.0). Defines the Hybrid Layout approved by Trainer G.
-->
# Mobile Interface Specification (v1.0)

## 1. Design Philosophy
- **Theme:** Dark Mode (Deep Navy / Charcoal)
- **Style:** Glassmorphism (Frosted glass effect on cards)
- **Accents:** Neon Blue (#00F2FF) and Cyber Purple (#A020F0)
- **Feedback:** Haptic vibrations on command success.

## 2. Layout Structure (The Hybrid Model)

### Zone 1: PC Health Header (The "Eyes")
- **Components:** 3 Small Horizontal Cards.
- **Data:** CPU %, RAM %, Network Speed (DL/UL).
- **Visual:** Small pulsing progress bars under each stat.
- **Refresh Rate:** 3 seconds (via WebSocket).

### Zone 2: Focus & Work Tracking (The "Body")
- **Component:** Large Central Timer Card.
- **Features:** 
  - Stop-watch style digital clock.
  - Current Task Label (e.g., "📋 Project: PC Automation").
  - Large "START WORK" / "STOP WORK" buttons.

### Zone 3: Action Grid (The "Hands")
- **Component:** 2x2 or 2x3 Grid of Dynamic Buttons.
- **Default Apps:** Chrome, Slack, Gmail, VS Code.
- **Customization:** User can add custom skill buttons from the "Skills" library.
- **Voice Button:** Large Floating Action Button (FAB) at the bottom center.

### Zone 4: AI Brain Feed (The "Thoughts")
- **Component:** Small Terminal Window at the very bottom.
- **Data:** Real-time logs from the `SkillGenerator`.
- **Example:** `> [AI] Intent: open youtube...` -> `> [AI] Searching library...` -> `> [AI] Building new skill... (45%)`

## 3. Technology Stack
- **Framework:** Flutter (3.x)
- **State Management:** Provider or Riverpod
- **Communication:** 
  - `http` package for Webhooks.
  - `web_socket_channel` for live stats and AI logs.
- **Storage:** `shared_preferences` for API Key storage.

## 4. Screen Flow
1. **Splash Screen:** App Identity.
2. **Setup Screen:** API Key & IP Address entry.
3. **Dashboard (Main):** The Hybrid Interface.
4. **Skills Library:** View all auto-generated and manual skills.
5. **Reports Screen:** View work history and session durations.
