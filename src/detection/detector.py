"""
Core vulnerability detection system for smart contracts.
"""
import json
import os
from pathlib import Path
from typing import Dict, Any, List, Optional

from src.preprocessing.solidity_parser import SolidityParser

class VulnerabilityDetector:
    """
    Detector for smart contract vulnerabilities using pattern-based analysis.
    """
    
    def __init__(self, solc_version: str = "0.8.29"):
        """Initialize the detector."""
        self.parser = SolidityParser(solc_version=solc_version)
        self.patterns = {}
        self._load_patterns()
    
    def _load_patterns(self):
        """
        Load all vulnerability detection patterns.
        """
        # Import patterns here to avoid circular imports
        from src.detection.patterns.reentrancy import ReentrancyDetector
        from src.detection.patterns.access_control import AccessControlDetector
        from src.detection.patterns.arithmetic import ArithmeticDetector
        from src.detection.patterns.flash_loan import FlashLoanDetector
        
        # Register each pattern
        self.patterns["reentrancy"] = ReentrancyDetector()
        self.patterns["access_control"] = AccessControlDetector()
        self.patterns["arithmetic"] = ArithmeticDetector()
        self.patterns["flash_loan"] = FlashLoanDetector()
    
    def detect_vulnerabilities(self, code: str) -> Dict[str, Any]:
        """
        Detect vulnerabilities in the provided smart contract code.
        
        Args:
            code: Solidity source code to analyze
            
        Returns:
            Dictionary with detected vulnerabilities and analysis results
        """
        # Parse the code
        parsed_data = self.parser.parse_code(code)
        
        # If parsing failed, return error
        if "error" in parsed_data:
            return {"error": parsed_data["error"]}
        
        # Run each detection pattern
        vulnerabilities = []
        
        for pattern_name, detector in self.patterns.items():
            results = detector.detect(code, parsed_data)
            if results:
                for result in results:
                    result["pattern"] = pattern_name
                    vulnerabilities.append(result)
        
        # Calculate severity statistics
        severity_counts = {
            "Critical": 0,
            "High": 0,
            "Medium": 0,
            "Low": 0,
            "Informational": 0
        }
        
        for vuln in vulnerabilities:
            severity = vuln.get("severity", "Informational")
            if severity in severity_counts:
                severity_counts[severity] += 1
        
        # Prepare the result
        return {
            "contract_analysis": {
                "vulnerabilities_found": vulnerabilities,
                "vulnerability_count": len(vulnerabilities),
                "severity_distribution": severity_counts,
                "analysis_summary": f"Found {len(vulnerabilities)} potential vulnerabilities.",
                "confidence_score": 0.85 if vulnerabilities else 0.9
            }
        }
    
    def analyze_file(self, file_path: str) -> Dict[str, Any]:
        """
        Analyze a Solidity file for vulnerabilities.
        
        Args:
            file_path: Path to the Solidity file
            
        Returns:
            Dictionary with detected vulnerabilities and analysis results
        """
        try:
            with open(file_path, "r") as f:
                code = f.read()
            
            return self.detect_vulnerabilities(code)
            
        except Exception as e:
            return {"error": f"Error analyzing file: {str(e)}"}