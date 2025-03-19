
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
        