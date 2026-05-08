<!-- 
FILE_TYPE: Project Diagram
CATEGORY: System Design
ENTRIES: 1 Diagram (Mermaid)
DATE_RANGE: 2026-05-08
KEYWORDS: Mermaid, Flowchart, Agentic Loop, WebSocket
SUMMARY: Visual representation of the Agentic Skill Loop and command execution flow for the Remote PC Controller.
-->
# System Flow Diagram - Agentic Remote PC Controller

```mermaid
graph TD
    A[Mobile App] -- "1. Intent (REST)" --> B[FastAPI Webhook]
    B -- "2. Parse Chain/Params" --> C{Skill Registry}
    
    C -- "Exists" --> D[Execute Handler]
    C -- "Not Found" --> E[Skill Generator AI]
    
    E -- "3. Build Skill" --> F[LLM API]
    F -- "4. Python Code" --> G[Sandbox Tester]
    
    G -- "Verified" --> H[Install Skill]
    H --> D
    
    D -- "5. OS Action" --> I[Windows 11]
    
    E -- "Update Status" --> J[WebSocket]
    J -- "6. Live Feedback" --> A
    
    style E fill:#f96,stroke:#333,stroke-width:2px
    style G fill:#bbf,stroke:#333,stroke-width:2px
```

### Flow Highlights:
- **Agentic Loop:** Steps 3-4-5 show how the system builds itself.
- **Feedback:** Step 6 ensures the user isn't left in the dark during the build process.
- **Security:** Sandbox Tester (Step G) acts as the gatekeeper.
