
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
        