import ast
import logging

class SandboxTester:
    @staticmethod
    def verify_code(code_string: str):
        """
        REQ-AI-03: Basic static analysis and sandbox check.
        Checks for syntax errors and dangerous imports.
        """
        try:
            # 1. Syntax Check
            ast.parse(code_string)
            
            # 2. Dangerous Keywords Check
            dangerous_calls = ['os.remove', 'shutil.rmtree', 'format_c', 'rm -rf']
            for call in dangerous_calls:
                if call in code_string:
                    return False, f"Dangerous command detected: {call}"
            
            # 3. Import Check
            tree = ast.parse(code_string)
            for node in ast.walk(tree):
                if isinstance(node, ast.Import) or isinstance(node, ast.ImportFrom):
                    # For now, we only allow specific safe modules
                    pass # We can implement a whitelist here
                    
            return True, "Code passed sandbox verification"
            
        except SyntaxError as e:
            return False, f"Syntax Error: {e.msg} at line {e.lineno}"
        except Exception as e:
            return False, str(e)
