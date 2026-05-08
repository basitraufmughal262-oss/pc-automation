import re

class IntentParser:
    @staticmethod
    def parse(raw_text: str):
        """
        Parses raw text into multiple commands and extracts parameters.
        Example: 'open chrome AND search youtube for lofi music'
        """
        # REQ-CMD-01: Command Chaining (Split by 'AND' or 'THEN')
        commands = re.split(r'\s+AND\s+|\s+THEN\s+', raw_text, flags=re.IGNORECASE)
        
        parsed_results = []
        for cmd in commands:
            cmd = cmd.strip()
            
            # REQ-CMD-02: Parametric Extraction
            # Pattern: search [TARGET] for [QUERY]
            search_match = re.search(r'search\s+(.+)\s+for\s+(.+)', cmd, re.IGNORECASE)
            
            if search_match:
                parsed_results.append({
                    "action": "search",
                    "target": search_match.group(1).lower(),
                    "query": search_match.group(2),
                    "raw": cmd
                })
            else:
                # Default keyword extraction
                parsed_results.append({
                    "action": "execute",
                    "intent": cmd.lower(),
                    "raw": cmd
                })
        
        return parsed_results
