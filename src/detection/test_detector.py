"""
Test script for the vulnerability detector.
"""
import json
import sys
from pathlib import Path
from typing import Dict, Any

# Add the project root to the Python path
project_root = Path(__file__).parent.parent.parent
sys.path.append(str(project_root))

# Then import your modules (only need to do this once)
from src.detection.detector import VulnerabilityDetector

def test_vulnerable_contracts():
    """Test the detector on sample vulnerable contracts."""
    detector = VulnerabilityDetector()
    
    # Get the sample contracts directory
    samples_dir = Path(__file__).parent.parent.parent / "data" / "contracts" / "samples"
    
    # Test each contract
    for contract_dir in samples_dir.iterdir():
        if contract_dir.is_dir():
            contract_file = contract_dir / "contract.sol"
            metadata_file = contract_dir / "metadata.json"
            
            if contract_file.exists() and metadata_file.exists():
                print(f"\nAnalyzing contract: {contract_dir.name}")
                
                # Load metadata to check if vulnerabilities are expected
                with open(metadata_file, "r") as f:
                    metadata = json.load(f)
                
                has_vulnerabilities = metadata.get("has_vulnerabilities", False)
                expected_types = metadata.get("vulnerability_types", [])
                
                # Analyze the contract
                with open(contract_file, "r") as f:
                    contract_code = f.read()
                
                results = detector.detect_vulnerabilities(contract_code)
                
                # Print results
                if "error" in results:
                    print(f"Error: {results['error']}")
                    continue
                
                vulnerabilities = results["contract_analysis"]["vulnerabilities_found"]
                print(f"Found {len(vulnerabilities)} vulnerabilities.")
                
                # Check if results match expectations
                if has_vulnerabilities and not vulnerabilities:
                    print("❌ Failed: Expected vulnerabilities but found none.")
                elif not has_vulnerabilities and vulnerabilities:
                    print("❌ Failed: Found unexpected vulnerabilities.")
                else:
                    print("✅ Success: Results match expectations.")
                
                # Print found vulnerabilities
                for vuln in vulnerabilities:
                    print(f"  - {vuln['type']} (Line {vuln['line']}): {vuln['severity']}")
                    
                    # Check if this vulnerability type was expected
                    if vuln['type'].lower() in [t.lower() for t in expected_types]:
                        print("    ✅ Expected vulnerability type")
                    else:
                        print("    ❌ Unexpected vulnerability type")

if __name__ == "__main__":
    test_vulnerable_contracts()