"""
Base classes and utilities for vulnerability detection patterns.
"""
from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional

class VulnerabilityPattern(ABC):
    """
    Base class for all vulnerability detection patterns.
    """
    
    @abstractmethod
    def detect(self, code: str, parsed_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Detect vulnerabilities in the provided smart contract code.
        
        Args:
            code: Solidity source code
            parsed_data: Parsed data from the Solidity parser
            
        Returns:
            List of detected vulnerabilities
        """
        pass