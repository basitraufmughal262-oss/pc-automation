import logging
import asyncio
from google import genai
from ..config import get_settings
from .sandbox_tester import SandboxTester

class SkillGenerator:
    def __init__(self, websocket_manager=None):
        self.settings = get_settings()
        self.ws = websocket_manager
        self.MAX_RETRIES = 3
        
        # REQ-SEC-02: API key from .env only
        self.client = genai.Client(api_key=self.settings.gemini_api_key)
        self.model_id = "gemini-2.0-flash"

    async def _broadcast(self, status: str, message: str, intent: str):
        if self.ws:
            await self.ws.broadcast({
                "status": status,
                "message": message,
                "intent": intent
            })

    async def build_skill(self, intent: str):
        """
        REQ-AI-01: Orchestrates full skill generation loop using google-genai SDK.
        """
        # REQ-AI-05: Check Privacy Mode from Settings
        if self.settings.privacy_mode:
            logging.warning("Privacy Mode is ACTIVE. Autonomous Skill Generation is blocked.")
            await self._broadcast("BLOCKED", "Privacy Mode is ON. Auto-Build disabled.", intent)
            return False, "Privacy Mode is ON."

        logging.info(f"[*] Auto-Build initiated for: {intent}")
        await self._broadcast("BUILDING", f"Skill '{intent}' not found. Building with AI...", intent)

        # REQ-AI-04: Retry Logic (max 3 attempts)
        for attempt in range(1, self.MAX_RETRIES + 1):
            try:
                await self._broadcast(
                    "GENERATING",
                    f"Generating code... (Attempt {attempt}/{self.MAX_RETRIES})",
                    intent
                )

                # REQ-AI-02: Generate code via LLM
                code = await self._call_gemini(intent)

                await self._broadcast("TESTING", "Testing generated code in Sandbox...", intent)

                # REQ-AI-03: Sandbox Verification
                passed, reason = SandboxTester.verify_code(code)
                if not passed:
                    logging.warning(f"Sandbox failed (attempt {attempt}): {reason}")
                    if attempt == self.MAX_RETRIES:
                        await self._broadcast("FAILED", f"Skill failed after {self.MAX_RETRIES} attempts: {reason}", intent)
                        return False, reason
                    continue

                # Success!
                await self._broadcast("READY", f"Skill '{intent}' is ready! Executing...", intent)
                logging.info(f"[+] Skill built successfully: {intent}")
                return True, code

            except Exception as e:
                logging.error(f"Generation error (attempt {attempt}): {e}")
                if attempt == self.MAX_RETRIES:
                    await self._broadcast("FAILED", f"Error: {str(e)}", intent)
                    return False, str(e)
                await asyncio.sleep(1)

        return False, "Max retries reached."

    async def _call_gemini(self, intent: str) -> str:
        """REQ-AI-02: Calls Gemini API using the new google-genai SDK."""
        prompt = self._generate_prompt(intent)
        
        # Use asyncio.to_thread for the synchronous SDK call
        response = await asyncio.to_thread(
            self.client.models.generate_content,
            model=self.model_id,
            contents=prompt
        )
        
        raw = response.text

        # Extract code block if Gemini wraps it in ```python
        if "```python" in raw:
            raw = raw.split("```python")[1].split("```")[0].strip()
        elif "```" in raw:
            raw = raw.split("```")[1].split("```")[0].strip()

        return raw

    def _generate_prompt(self, intent: str) -> str:
        """Builds a safe, constrained prompt for Windows 11 automation."""
        return f"""
You are a Windows 11 Python automation expert.
Write a Python function named 'execute_skill(params: dict)' for this task:

TASK: {intent}

RULES:
1. Use ONLY: pyautogui, webbrowser, subprocess, os, time
2. NO file deletions, NO system format commands
3. Add time.sleep(0.5) between UI actions for stability
4. Return a dict: {{"status": "success", "message": "..."}}
5. Return ONLY valid Python code. No explanation or markdown outside the code.
"""
