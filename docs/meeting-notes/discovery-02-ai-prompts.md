<!-- 
FILE_TYPE: Domain Discovery
CATEGORY: AI Prompt Engineering
ENTRIES: 3 Prompt Templates
DATE_RANGE: 2026-05-08
KEYWORDS: Prompt Engineering, LLM, Code Generation, Windows Automation
SUMMARY: Discovery notes for AI code generation logic. Defines the context, constraints, and templates for the Skill Generator.
-->
# Discovery 02 - AI Prompt Engineering Strategy

## 1. Context Injection
For the LLM to write accurate code, we must provide the system context:
- **OS:** Windows 11
- **Available Libraries:** `pyautogui`, `webbrowser`, `os`, `subprocess`, `time`
- **Execution Environment:** Python 3.14 (Backend Server)

## 2. Constraints (Safety)
Prompts must enforce:
- No deletion of system files.
- No network requests outside of authorized domains.
- No endless loops.
- Use of `time.sleep()` between UI actions for stability.

## 3. Skill Generation Prompt Template
```text
SYSTEM ROLE: Senior Python Automation Engineer
TASK: Generate a single Python function 'execute_skill(params)' for the following intent.

INTENT: {user_intent}
PARAMS: {extracted_params}

CONSTRAINTS:
1. Use 'pyautogui' for UI interactions.
2. Use 'webbrowser' for URL tasks.
3. Return ONLY the code block.
4. Add comments for each step.
```

## 4. Testing Strategy
- Code will be parsed by `SandboxTester`.
- Syntax will be verified with `ast.parse`.
- Trial run will be performed on a non-destructive command first.
