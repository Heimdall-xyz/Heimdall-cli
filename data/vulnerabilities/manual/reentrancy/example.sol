
            // Vulnerable code
            function withdraw(uint256 amount) public {
                require(balances[msg.sender] >= amount, "Insufficient balance");
                
                // Send funds before updating state
                (bool success, ) = msg.sender.call{value: amount}("");
                require(success, "Transfer failed");
                
                // State update happens after external call
                balances[msg.sender] -= amount;
            }
            
            // Fixed code
            function withdraw(uint256 amount) public {
                require(balances[msg.sender] >= amount, "Insufficient balance");
                
                // Update state before external call
                balances[msg.sender] -= amount;
                
                // Send funds after updating state
                (bool success, ) = msg.sender.call{value: amount}("");
                require(success, "Transfer failed");
            }
        