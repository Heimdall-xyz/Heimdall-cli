
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
        