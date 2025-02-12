// SPDX-License-Identifier: MIT
pragma solidity ^0.8.28;

import {Test} from "forge-std/Test.sol";
import {RUSDC} from "../contracts/RUSDC.sol";
import {RUSDCFaucet} from "../contracts/RUSDCFaucet.sol";

contract RUSDCFaucetTest is Test {
    RUSDC public rusdc;
    RUSDCFaucet public faucet;
    address public owner;
    address public user1;
    address public user2;

    function setUp() public {
        owner = address(this);
        user1 = makeAddr("user1");
        user2 = makeAddr("user2");
        
        rusdc = new RUSDC();
        faucet = new RUSDCFaucet(address(rusdc));
        
        // Fund the faucet with initial tokens
        rusdc.transfer(address(faucet), 10000 * 10**6);
    }

    function testRequestTokens() public {
        vm.warp(1 days); // Set initial timestamp
        vm.prank(user1);
        faucet.requestTokens();
        assertEq(rusdc.balanceOf(user1), 1000 * 10**6);
    }

    function testCooldownPeriod() public {
        vm.warp(1 days); // Set initial timestamp
        vm.startPrank(user1);
        faucet.requestTokens();
        
        vm.expectRevert(RUSDCFaucet.CooldownNotExpired.selector);
        faucet.requestTokens();
        vm.stopPrank();
    }

    function testRequestAfterCooldown() public {
        vm.warp(1 days); // Set initial timestamp
        vm.startPrank(user1);
        faucet.requestTokens();
        
        vm.warp(2 days); // Move forward past cooldown
        faucet.requestTokens();
        assertEq(rusdc.balanceOf(user1), 2000 * 10**6);
        vm.stopPrank();
    }

    function testInsufficientFaucetBalance() public {
        vm.warp(1 days); // Set initial timestamp
        
        // Drain the faucet first
        vm.prank(owner);
        faucet.withdrawTokens();
        
        vm.prank(user1);
        vm.expectRevert(RUSDCFaucet.InsufficientFaucetBalance.selector);
        faucet.requestTokens();
    }

    function testWithdrawTokens() public {
        uint256 initialBalance = rusdc.balanceOf(address(faucet));
        
        vm.prank(owner);
        faucet.withdrawTokens();
        
        assertEq(rusdc.balanceOf(owner), 1000000 * 10**6);
        assertEq(rusdc.balanceOf(address(faucet)), 0);
    }

    function testOnlyOwnerCanWithdraw() public {
        vm.prank(user1);
        vm.expectRevert();
        faucet.withdrawTokens();
    }
}
