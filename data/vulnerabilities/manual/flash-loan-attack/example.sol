
            // Vulnerable code
            function swap(address token, uint256 amount) public {
                // Using a single price source without time-weighted checks
                uint price = singleSourceOracle.getPrice(token);
                uint returnAmount = amount * price / 1e18;
                
                // Vulnerable to flash loan price manipulation
                token.transferFrom(msg.sender, address(this), amount);
                stablecoin.transfer(msg.sender, returnAmount);
            }
            
            // More resilient code
            function swap(address token, uint256 amount) public {
                // Using time-weighted average price from multiple sources
                uint price = twapOracle.getAveragePrice(token);
                uint returnAmount = amount * price / 1e18;
                
                // Add slippage protection
                require(returnAmount <= maxSwapAmount, "Exceeds max swap");
                
                token.transferFrom(msg.sender, address(this), amount);
                stablecoin.transfer(msg.sender, returnAmount);
            }
        