import subprocess
import os

class OSHandler:
    @staticmethod
    def open_app(path: str):
        try:
            # Using start command to launch app without blocking the server
            subprocess.Popen(['start', '', path], shell=True)
            return True, f"Launched {path}"
        except Exception as e:
            return False, str(e)

    @staticmethod
    def open_url(url: str):
        try:
            # Open URL in default browser
            os.startfile(url)
            return True, f"Opened URL: {url}"
        except Exception as e:
            return False, str(e)

    @staticmethod
    def shutdown_pc(delay_seconds: int = 60):
        try:
            # /s = shutdown, /t = time in seconds
            subprocess.run(['shutdown', '/s', '/t', str(delay_seconds)], check=True)
            return True, f"Shutdown scheduled in {delay_seconds} seconds"
        except Exception as e:
            return False, str(e)

    @staticmethod
    def cancel_shutdown():
        try:
            # /a = abort shutdown
            subprocess.run(['shutdown', '/a'], check=True)
            return True, "Shutdown cancelled"
        except Exception as e:
            return False, str(e)
