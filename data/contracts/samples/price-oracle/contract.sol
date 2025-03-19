
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
        