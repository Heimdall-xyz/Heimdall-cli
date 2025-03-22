"""
Reentrancy vulnerability detection pattern.
"""
from typing import Dict, Any, List, Optional
from src.detection.patterns import VulnerabilityPattern

class ReentrancyDetector(VulnerabilityPattern):
    """Detector for reentrancy vulnerabilities."""
    
    def detect(self, code: str, parsed_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Detect reentrancy vulnerabilities in Solidity code.
        
        Args:
            code: Solidity source code
            parsed_data: Parsed data from the Solidity parser
            
        Returns:
            List of detected vulnerabilities
        """
        vulnerabilities = []
        
        # Simple pattern-based detection
        # Look for external calls followed by state changes
        
        # Check for the pattern: external call (call, send, transfer) followed by state change
        lines = code.split("\n")
        for i, line in enumerate(lines):
            # Look for external calls
            if "call{value:" in line or ".call(" in line:
                # Found external call, check if state update happens after this
                call_line_number = i
                
                # Check the next few lines for state updates (simplified)
                for j in range(i+1, min(i+10, len(lines))):
                    if "-=" in lines[j] or "delete" in lines[j]:
                        # Found state update after external call
                        vulnerabilities.append({
                            "type": "Reentrancy",
                            "line": call_line_number + 1,
                            "description": "External call is made before state update, which may allow reentrancy attacks.",
                            "severity": "High",
                            "code_snippet": "\n".join(lines[max(0, i-2):min(len(lines), j+3)])
                        })
                        break
        
        return vulnerabilities