"""
Access control vulnerability detection pattern.
"""
from typing import Dict, Any, List, Optional
from src.detection.patterns import VulnerabilityPattern

class AccessControlDetector(VulnerabilityPattern):
    """Detector for access control vulnerabilities."""
    
    def detect(self, code: str, parsed_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Detect access control vulnerabilities in Solidity code.
        
        Args:
            code: Solidity source code
            parsed_data: Parsed data from the Solidity parser
            
        Returns:
            List of detected vulnerabilities
        """
        vulnerabilities = []
        
        # Check for functions that have sensitive operations but lack access control
        sensitive_operations = [
            "selfdestruct", 
            "transfer(", 
            "send(", 
            ".call{value", 
            "delegatecall"
        ]
        
        access_control_patterns = [
            "require(msg.sender ==", 
            "onlyOwner", 
            "require(owner ==", 
            "isOwner", 
            "checkRole",
            "hasRole"
        ]
        
        functions = parsed_data.get("basic_info", {}).get("functions", [])
        lines = code.split("\n")
        
        for function in functions:
            name = function.get("name", "")
            line_num = function.get("line", 0)
            
            # Skip view and pure functions
            if function.get("mutability") in ["view", "pure"]:
                continue
            
            # Skip constructor and internal/private functions (less risk)
            if name == "constructor" or function.get("visibility") in ["internal", "private"]:
                continue
            
            # Check if this function contains sensitive operations
            has_sensitive_op = False
            start_line = max(0, line_num - 1)
            
            # Find function end
            end_line = start_line
            brace_count = 0
            for i in range(start_line, len(lines)):
                line = lines[i]
                brace_count += line.count("{") - line.count("}")
                
                # Check for sensitive operations
                for op in sensitive_operations:
                    if op in line:
                        has_sensitive_op = True
                
                if brace_count == 0 and i > start_line:
                    end_line = i
                    break
            
            # If function has sensitive operations, check for access control
            if has_sensitive_op:
                has_access_control = False
                
                # Check if any access control pattern exists in the function
                function_code = "\n".join(lines[start_line:end_line+1])
                for pattern in access_control_patterns:
                    if pattern in function_code:
                        has_access_control = True
                        break
                
                if not has_access_control:
                    vulnerabilities.append({
                        "type": "Missing Access Control",
                        "line": line_num,
                        "description": f"Function '{name}' performs sensitive operations but lacks access control checks.",
                        "severity": "High",
                        "code_snippet": function_code
                    })
        
        return vulnerabilities