// SPDX-License-Identifier: MIT
pragma solidity ^0.8.28;

import "@openzeppelin/contracts/token/ERC20/ERC20.sol";
import "@openzeppelin/contracts/access/Ownable.sol";

contract RUSDC is ERC20, Ownable {
    uint8 private constant DECIMALS = 6;

    constructor() ERC20("Rika Usdc", "RUSDC") Ownable(msg.sender) {
        _mint(msg.sender, 1000000 * 10**DECIMALS); // Initial supply of 1M USDC
    }

    function decimals() public pure override returns (uint8) {
        return DECIMALS;
    }

    function mint(address to, uint256 amount) external onlyOwner {
        _mint(to, amount);
        _approve(to, to, type(uint256).max);
    }
}
