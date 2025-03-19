
            // Vulnerable code
            function buyTokens() public payable {
                // Price is determined at execution time
                uint256 price = getCurrentPrice();
                uint256 tokenAmount = msg.value / price;
                
                // Vulnerable to front-running
                balances[msg.sender] += tokenAmount;
            }
            
            // More resistant code
            function buyTokens(uint256 maxPrice) public payable {
                uint256 price = getCurrentPrice();
                // Buyer specifies maximum price they're willing to pay
                require(price <= maxPrice, "Price too high");
                uint256 tokenAmount = msg.value / price;
                balances[msg.sender] += tokenAmount;
            }
        