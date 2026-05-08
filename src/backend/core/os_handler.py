import subprocess
import os
import pyautogui
import time
import webbrowser

class OSHandler:
    @staticmethod
    def open_app(path: str):
        try:
            subprocess.Popen(['start', '', path], shell=True)
            return True, f"Launched {path}"
        except Exception as e:
            return False, str(e)

    @staticmethod
    def perform_search(target: str, query: str):
        """
        REQ-CMD-02 & REQ-CMD-03: UI Automation Search.
        Example: search youtube for 'lofi music'
        """
        try:
            if target.lower() == "youtube":
                url = f"https://www.youtube.com/results?search_query={query.replace(' ', '+')}"
                webbrowser.open(url)
                return True, f"Searching YouTube for: {query}"
            
            elif target.lower() == "google":
                url = f"https://www.google.com/search?q={query.replace(' ', '+')}"
                webbrowser.open(url)
                return True, f"Searching Google for: {query}"
            
            return False, f"Search target '{target}' not supported yet."
        except Exception as e:
            return False, str(e)

    @staticmethod
    def type_text(text: str):
        """Simulates keyboard typing."""
        try:
            pyautogui.write(text, interval=0.1)
            pyautogui.press('enter')
            return True, "Typed text successfully"
        except Exception as e:
            return False, str(e)
