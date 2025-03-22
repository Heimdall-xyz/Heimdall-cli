"""
Flash loan vulnerability detection pattern.
"""
from typing import Dict, Any, List, Optional
from src.detection.patterns import VulnerabilityPattern

class FlashLoanDetector(VulnerabilityPattern):
    """Detector for flash loan vulnerabilities."""
    
    def detect(self, code: str, parsed_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Detect flash loan vulnerabilities in Solidity code.
        
        Args:
            code: Solidity source code
            parsed_data: Parsed data from the Solidity parser
            
        Returns:
            List of detected vulnerabilities
        """
        vulnerabilities = []
        
        # Check for price calculations based on current balances (vulnerable to manipulation)
        lines = code.split("\n")
        
        for i, line in enumerate(lines):
            # Look for potential price calculations
            if ("price" in line.lower() or "getPrice" in line or "calculatePrice" in line):
                
                # Check nearby lines for potential balance-based calculations
                start_idx = max(0, i - 5)
                end_idx = min(len(lines), i + 5)
                
                snippet = "\n".join(lines[start_idx:end_idx])
                
                # Check for balance-based calculations
                if ("balanceOf" in snippet and "price" in snippet.lower()):
                    vulnerabilities.append({
                        "type": "Flash Loan Vulnerability",
                        "line": i + 1,
                        "description": "Price calculation based on current balances, which may be manipulated by flash loans.",
                        "severity": "Critical",
                        "code_snippet": snippet
                    })
                
                # Check for single-block oracle usage
                if ("blockNumber" in snippet and "price" in snippet.lower() and "require" not in snippet):
                    vulnerabilities.append({
                        "type": "Oracle Manipulation Vulnerability",
                        "line": i + 1,
                        "description": "Price oracle lacks manipulation protection. Consider using a TWAP oracle.",
                        "severity": "High",
                        "code_snippet": snippet
                    })
        
        return vulnerabilities