// SPDX-License-Identifier: MIT
pragma solidity ^0.8.28;

import {Test} from "forge-std/Test.sol";
import {RUSDC} from "../contracts/RUSDC.sol";

contract RUSDCTest is Test {
    RUSDC public rusdc;
    address public owner;
    address public user1;

    function setUp() public {
        owner = address(this);
        user1 = makeAddr("user1");
        rusdc = new RUSDC();
    }

    function testInitialSupply() public {
        assertEq(rusdc.totalSupply(), 1000000 * 10**6);
        assertEq(rusdc.balanceOf(owner), 1000000 * 10**6);
    }

    function testDecimals() public {
        assertEq(rusdc.decimals(), 6); // RUSDC uses 6 decimals
    }

    function testName() public {
        assertEq(rusdc.name(), "Rika Usdc");
        assertEq(rusdc.symbol(), "RUSDC");
    }

    function testMint() public {
        uint256 mintAmount = 1000 * 10**6;
        rusdc.mint(user1, mintAmount);
        assertEq(rusdc.balanceOf(user1), mintAmount);
    }

    function testOnlyOwnerCanMint() public {
        vm.prank(user1);
        vm.expectRevert();
        rusdc.mint(user1, 1000 * 10**6);
    }

    function testTotalSupplyAfterMint() public {
        uint256 initialSupply = rusdc.totalSupply();
        uint256 mintAmount = 1000 * 10**6;
        
        rusdc.mint(user1, mintAmount);
        assertEq(rusdc.totalSupply(), initialSupply + mintAmount);
    }
}
