
            // Vulnerable code (pre-Solidity 0.8.0)
            function transfer(address to, uint256 amount) public {
                require(balances[msg.sender] >= amount, "Insufficient balance");
                balances[msg.sender] -= amount;
                balances[to] += amount; // Potential overflow
            }
            
            // Fixed code for pre-0.8.0
            function transfer(address to, uint256 amount) public {
                require(balances[msg.sender] >= amount, "Insufficient balance");
                balances[msg.sender] -= amount;
                require(balances[to] + amount >= balances[to], "Overflow check");
                balances[to] += amount;
            }
        