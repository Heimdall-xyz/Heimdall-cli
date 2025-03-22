"""
Arithmetic vulnerability detection pattern.
"""
from typing import Dict, Any, List, Optional
from src.detection.patterns import VulnerabilityPattern

class ArithmeticDetector(VulnerabilityPattern):
    """Detector for arithmetic vulnerabilities like overflow/underflow."""
    
    def detect(self, code: str, parsed_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Detect arithmetic vulnerabilities in Solidity code.
        
        Args:
            code: Solidity source code
            parsed_data: Parsed data from the Solidity parser
            
        Returns:
            List of detected vulnerabilities
        """
        vulnerabilities = []
        
        # Extract pragma to check Solidity version
        pragma = parsed_data.get("basic_info", {}).get("pragma", "")
        
        # Check if using Solidity < 0.8.0 (which doesn't have automatic overflow checking)
        old_solidity = False
        if "pragma solidity" in pragma:
            version_str = pragma.split("pragma solidity")[1].strip()
            
            # Simple check - if 0.8 is not mentioned, it's likely older
            if "0.8" not in version_str and "^0.8" not in version_str:
                old_solidity = True
        
        # For older Solidity versions, check for arithmetic operations without SafeMath
        if old_solidity:
            lines = code.split("\n")
            
            # Check if using SafeMath
            using_safe_math = "using SafeMath " in code
            
            if not using_safe_math:
                # Look for arithmetic operations
                for i, line in enumerate(lines):
                    stripped = line.strip()
                    
                    # Check for arithmetic operations that might overflow/underflow
                    if "++" in stripped or "--" in stripped or "+=" in stripped or "-=" in stripped:
                        if "require(" not in stripped and "assert(" not in stripped:
                            vulnerabilities.append({
                                "type": "Arithmetic Overflow/Underflow",
                                "line": i + 1,
                                "description": "Arithmetic operation without overflow check in Solidity < 0.8.0",
                                "severity": "Medium",
                                "code_snippet": lines[max(0, i-1):min(len(lines), i+2)]
                            })
                    
                    # Check for multiplication/division that might overflow
                    if "*" in stripped or "/" in stripped:
                        if "require(" not in stripped and "assert(" not in stripped:
                            vulnerabilities.append({
                                "type": "Arithmetic Overflow/Underflow",
                                "line": i + 1,
                                "description": "Multiplication/division without overflow check in Solidity < 0.8.0",
                                "severity": "Medium",
                                "code_snippet": lines[max(0, i-1):min(len(lines), i+2)]
                            })
        
        return vulnerabilities