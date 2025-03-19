"""
Create a dataset of sample contracts for testing the vulnerability detection system.
"""
import json
import os
from pathlib import Path

DATA_DIR = Path(__file__).parent.parent.parent / "data" / "contracts"
SAMPLES_DIR = DATA_DIR / "samples"

# This contains sample contracts with and without vulnerabilities
SAMPLE_CONTRACTS = [
    {
        "id": "simple-token",
        "name": "SimpleToken",
        "description": "A basic ERC20-like token implementation",
        "has_vulnerabilities": False,
        "contract_code": """
            // SPDX-License-Identifier: MIT
            pragma solidity ^0.8.0;
            
            contract SimpleToken {
                string public name = "SimpleToken";
                string public symbol = "SIM";
                uint8 public decimals = 18;
                uint256 public totalSupply = 1000000 * 10**18;
                
                mapping(address => uint256) public balanceOf;
                mapping(address => mapping(address => uint256)) public allowance;
                
                event Transfer(address indexed from, address indexed to, uint256 value);
                event Approval(address indexed owner, address indexed spender, uint256 value);
                
                constructor() {
                    balanceOf[msg.sender] = totalSupply;
                }
                
                function transfer(address to, uint256 value) public returns (bool) {
                    require(to != address(0), "Transfer to zero address");
                    require(balanceOf[msg.sender] >= value, "Insufficient balance");
                    
                    balanceOf[msg.sender] -= value;
                    balanceOf[to] += value;
                    emit Transfer(msg.sender, to, value);
                    return true;
                }
                
                function approve(address spender, uint256 value) public returns (bool) {
                    allowance[msg.sender][spender] = value;
                    emit Approval(msg.sender, spender, value);
                    return true;
                }
                
                function transferFrom(address from, address to, uint256 value) public returns (bool) {
                    require(to != address(0), "Transfer to zero address");
                    require(balanceOf[from] >= value, "Insufficient balance");
                    require(allowance[from][msg.sender] >= value, "Insufficient allowance");
                    
                    balanceOf[from] -= value;
                    balanceOf[to] += value;
                    allowance[from][msg.sender] -= value;
                    emit Transfer(from, to, value);
                    return true;
                }
            }
        """
    },
    {
        "id": "vulnerable-vault",
        "name": "VulnerableVault",
        "description": "A vault contract with a reentrancy vulnerability",
        "has_vulnerabilities": True,
        "vulnerability_types": ["reentrancy"],
        "contract_code": """
            // SPDX-License-Identifier: MIT
            pragma solidity ^0.8.0;
            
            contract VulnerableVault {
                mapping(address => uint256) public balances;
                
                function deposit() public payable {
                    balances[msg.sender] += msg.value;
                }
                
                // This function is vulnerable to reentrancy
                function withdraw(uint256 amount) public {
                    require(balances[msg.sender] >= amount, "Insufficient balance");
                    
                    // Vulnerable: sends ETH before updating the balance
                    (bool success, ) = msg.sender.call{value: amount}("");
                    require(success, "Transfer failed");
                    
                    // State update happens after external call
                    balances[msg.sender] -= amount;
                }
                
                function getBalance() public view returns (uint256) {
                    return balances[msg.sender];
                }
            }
        """
    },
    {
        "id": "insecure-marketplace",
        "name": "InsecureMarketplace",
        "description": "A marketplace contract with access control issues",
        "has_vulnerabilities": True,
        "vulnerability_types": ["access-control"],
        "contract_code": """
            // SPDX-License-Identifier: MIT
            pragma solidity ^0.8.0;
            
            contract InsecureMarketplace {
                address public owner;
                mapping(uint256 => Item) public items;
                uint256 public itemCount;
                
                struct Item {
                    string name;
                    uint256 price;
                    address seller;
                    bool sold;
                }
                
                constructor() {
                    owner = msg.sender;
                }
                
                function addItem(string memory _name, uint256 _price) public {
                    itemCount++;
                    items[itemCount] = Item(_name, _price, msg.sender, false);
                }
                
                // Vulnerable: Missing access control
                function updatePrice(uint256 _itemId, uint256 _newPrice) public {
                    // Should check if msg.sender is the seller but doesn't
                    items[_itemId].price = _newPrice;
                }
                
                function purchaseItem(uint256 _itemId) public payable {
                    Item storage item = items[_itemId];
                    require(!item.sold, "Item already sold");
                    require(msg.value >= item.price, "Insufficient funds");
                    
                    item.sold = true;
                    payable(item.seller).transfer(msg.value);
                }
                
                // Vulnerable: Missing access control
                function withdrawFunds() public {
                    // Should check if msg.sender is the owner but doesn't
                    payable(msg.sender).transfer(address(this).balance);
                }
            }
        """
    },
    {
        "id": "price-oracle",
        "name": "VulnerablePriceOracle",
        "description": "A price oracle vulnerable to flash loan attacks",
        "has_vulnerabilities": True,
        "vulnerability_types": ["flash-loan-attack"],
        "contract_code": """
            // SPDX-License-Identifier: MIT
            pragma solidity ^0.8.0;
            
            interface IERC20 {
                function transferFrom(address sender, address recipient, uint256 amount) external returns (bool);
                function transfer(address recipient, uint256 amount) external returns (bool);
                function balanceOf(address account) external view returns (uint256);
            }
            
            contract VulnerablePriceOracle {
                IERC20 public token;
                IERC20 public stablecoin;
                
                constructor(address _token, address _stablecoin) {
                    token = IERC20(_token);
                    stablecoin = IERC20(_stablecoin);
                }
                
                // Vulnerable to flash loan price manipulation
                function getPrice() public view returns (uint256) {
                    // Simplified price calculation based on pool balances
                    // Vulnerable to manipulation via flash loans
                    return (stablecoin.balanceOf(address(this)) * 1e18) / token.balanceOf(address(this));
                }
                
                function swap(uint256 tokenAmount) public {
                    // Get current price
                    uint256 price = getPrice();
                    uint256 stablecoinAmount = (tokenAmount * price) / 1e18;
                    
                    // Transfer tokens from user to contract
                    require(token.transferFrom(msg.sender, address(this), tokenAmount), "Token transfer failed");
                    
                    // Transfer stablecoins to user
                    require(stablecoin.transfer(msg.sender, stablecoinAmount), "Stablecoin transfer failed");
                }
            }
        """
    },
    {
        "id": "secure-vault",
        "name": "SecureVault",
        "description": "A secure vault contract with reentrancy protection",
        "has_vulnerabilities": False,
        "contract_code": """
            // SPDX-License-Identifier: MIT
            pragma solidity ^0.8.0;
            
            contract SecureVault {
                mapping(address => uint256) public balances;
                bool private locked;
                
                modifier nonReentrant() {
                    require(!locked, "Reentrant call");
                    locked = true;
                    _;
                    locked = false;
                }
                
                function deposit() public payable {
                    balances[msg.sender] += msg.value;
                }
                
                // Secure version with reentrancy protection
                function withdraw(uint256 amount) public nonReentrant {
                    require(balances[msg.sender] >= amount, "Insufficient balance");
                    
                    // Update state before external call
                    balances[msg.sender] -= amount;
                    
                    // External call after state update
                    (bool success, ) = msg.sender.call{value: amount}("");
                    require(success, "Transfer failed");
                }
                
                function getBalance() public view returns (uint256) {
                    return balances[msg.sender];
                }
            }
        """
    }
]

def create_sample_contracts():
    """Create and save sample contracts dataset"""
    os.makedirs(SAMPLES_DIR, exist_ok=True)
    
    # Save the full list
    with open(SAMPLES_DIR / "contracts.json", "w") as f:
        json.dump(SAMPLE_CONTRACTS, f, indent=2)
    
    # Create individual files for each contract
    for contract in SAMPLE_CONTRACTS:
        contract_dir = SAMPLES_DIR / contract["id"]
        os.makedirs(contract_dir, exist_ok=True)
        
        # Save metadata
        metadata = {k: v for k, v in contract.items() if k != "contract_code"}
        with open(contract_dir / "metadata.json", "w") as f:
            json.dump(metadata, f, indent=2)
        
        # Save contract code
        with open(contract_dir / "contract.sol", "w") as f:
            f.write(contract["contract_code"])
    
    print(f"Created sample contracts dataset with {len(SAMPLE_CONTRACTS)} contracts")

if __name__ == "__main__":
    create_sample_contracts()