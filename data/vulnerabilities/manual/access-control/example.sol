
            // Vulnerable code
            function withdrawFunds() public {
                // No access control
                payable(msg.sender).transfer(address(this).balance);
            }
            
            // Fixed code
            function withdrawFunds() public {
                // Check that caller is the owner
                require(msg.sender == owner, "Not authorized");
                payable(msg.sender).transfer(address(this).balance);
            }
        