// SPDX-License-Identifier: MIT
pragma solidity ^0.8.28;

import "@openzeppelin/contracts/access/Ownable.sol";
import "@openzeppelin/contracts/token/ERC20/IERC20.sol";

contract RUSDCFaucet is Ownable {
    IERC20 public usdc;
    uint256 public constant FAUCET_AMOUNT = 1000 * 10**6; // 1000 USDC
    mapping(address => uint256) public lastFaucetTime;
    uint256 public constant FAUCET_COOLDOWN = 24 hours;

    error CooldownNotExpired();
    error InsufficientFaucetBalance();
    error TransferFailed();

    event TokensRequested(address indexed user, uint256 amount);
    event TokensWithdrawn(address indexed owner, uint256 amount);

    constructor(address _usdc) Ownable(msg.sender) {
        usdc = IERC20(_usdc);
    }

    function requestTokens() external {
        // Checks
        if (block.timestamp < lastFaucetTime[msg.sender] + FAUCET_COOLDOWN)
            revert CooldownNotExpired();
        if (usdc.balanceOf(address(this)) < FAUCET_AMOUNT)
            revert InsufficientFaucetBalance();

        // Effects
        lastFaucetTime[msg.sender] = block.timestamp;
        emit TokensRequested(msg.sender, FAUCET_AMOUNT);

        // Interactions
        bool success = usdc.transfer(msg.sender, FAUCET_AMOUNT);
        if (!success) revert TransferFailed();
    }

    function withdrawTokens() external onlyOwner {
        // Checks
        uint256 balance = usdc.balanceOf(address(this));

        // Effects
        emit TokensWithdrawn(owner(), balance);

        // Interactions
        bool success = usdc.transfer(owner(), balance);
        if (!success) revert TransferFailed();
    }
}
