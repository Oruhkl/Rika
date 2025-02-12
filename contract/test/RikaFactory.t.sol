// SPDX-License-Identifier: MIT
pragma solidity ^0.8.28;

import {Test, console2} from "forge-std/Test.sol";
import {Pausable} from "@openzeppelin/contracts/utils/Pausable.sol";

import {RikaFactory} from "../contracts/RikaFactory.sol";
import {RikaManagement} from "../contracts/RikaManagement.sol";
import {RUSDC} from "../contracts/RUSDC.sol";

contract RikaFactoryTest is Test {
    RikaFactory public factory;
    RikaManagement public implementation;
    RUSDC public usdc;
    
    address public admin = address(1);
    address public employer1 = address(2);
    address public employer2 = address(3);
    address public aiAgent = address(4);
    address public tesla = address(0x1);
    address public apple = address(0x2);
    address public microsoft = address(0x3);
    address public amazon = address(0x4);
    address public google = address(0x5);

    event PayrollContractCreated(address indexed employer, address indexed payrollContract);
    event AiAgentAdded(address indexed agent);
    event AiAgentRemoved(address indexed agent);

    function setUp() public {
        vm.startPrank(admin);
        usdc = new RUSDC();
        implementation = new RikaManagement();
        factory = new RikaFactory(address(implementation), address(usdc));
        // Mint USDC to employers
        usdc.mint(address(0x1), 10000000e6); // Tesla
        usdc.mint(address(0x2), 10000000e6); // Apple
        usdc.mint(address(0x3), 10000000e6); // Microsoft
        usdc.mint(address(0x4), 10000000e6); // Amazon
        usdc.mint(address(0x5), 10000000e6); // Google
        vm.stopPrank();
    }

    function testInitialState() public {
        assertEq(factory.implementationContract(), address(implementation));
        assertEq(factory.usdcToken(), address(usdc));
        assertTrue(factory.hasRole(factory.DEFAULT_ADMIN_ROLE(), admin));
    }

    function testcreatePayrollContractContract() public {
    vm.startPrank(employer1);
    
    address payrollContract = factory.createPayrollContract();
    
    // Verify contract creation
    assertTrue(factory.isValidPayrollContract(payrollContract));
    (address[] memory contracts, RikaManagement.PayrollDetails[] memory details) = factory.getEmployerPayrollDetails(employer1);
    assertEq(contracts[0], payrollContract);
    
    // Verify initialization
    RikaManagement deployed = RikaManagement(payrollContract);
    assertEq(deployed.getEmployer(), employer1);
    assertEq(address(deployed.usdcToken()), address(usdc));
    vm.stopPrank();
    }


    function testMaxPayrollContractsPerEmployer() public {
        vm.startPrank(employer1);
        
        // Create 3 contracts (maximum allowed)
        factory.createPayrollContract();
        factory.createPayrollContract();
        factory.createPayrollContract();
        
        // Attempt to create 4th contract should revert
        vm.expectRevert(RikaFactory.MaxPayrollContractsAllowed.selector);
        factory.createPayrollContract();
        
        vm.stopPrank();
    }

    function testAddAiAgent() public {
        // Create a payroll contract first
        vm.prank(employer1);
        address payrollContract = factory.createPayrollContract();
        
        vm.startPrank(admin);
        
        vm.expectEmit(true, false, false, true);
        emit AiAgentAdded(aiAgent);
        
        factory.addAiAgent(aiAgent);
        
        // Verify AI agent was added to the payroll contract
        RikaManagement deployed = RikaManagement(payrollContract);
        assertTrue(deployed.hasRole(deployed.AI_AGENT_ROLE(), aiAgent));
        
        vm.stopPrank();
    }

    function testRemoveAiAgent() public {
        // Create a payroll contract and add AI agent first
        vm.prank(employer1);
        address payrollContract = factory.createPayrollContract();
        
        vm.startPrank(admin);
        factory.addAiAgent(aiAgent);
        
        vm.expectEmit(true, false, false, true);
        emit AiAgentRemoved(aiAgent);
        
        factory.removeAiAgent(aiAgent);
        
        // Verify AI agent was removed from the payroll contract
        RikaManagement deployed = RikaManagement(payrollContract);
        assertFalse(deployed.hasRole(deployed.AI_AGENT_ROLE(), aiAgent));
        
        vm.stopPrank();
    }

    function testPauseUnpause() public {
        vm.startPrank(admin);
        
        // Test pause
        factory.pause();
        assertTrue(factory.paused());
        
        // Verify cannot create contracts while paused
        vm.startPrank(employer1);
        vm.expectRevert(Pausable.EnforcedPause.selector);
        factory.createPayrollContract();
        
        // Test unpause
        vm.startPrank(admin);
        factory.unpause();
        assertFalse(factory.paused());
        
        // Verify can create contracts after unpause
        vm.startPrank(employer1);
        address payrollContract = factory.createPayrollContract();
        assertTrue(factory.isValidPayrollContract(payrollContract));
    }

    function testGetEmployerPayrollDetails() public {
        vm.startPrank(employer1);
        
        // Create two payroll contracts
        address payroll1 = factory.createPayrollContract();
        address payroll2 = factory.createPayrollContract();
        
        (address[] memory contracts, RikaManagement.PayrollDetails[] memory details) = 
            factory.getEmployerPayrollDetails(employer1);
        
        assertEq(contracts.length, 2);
        assertEq(contracts[0], payroll1);
        assertEq(contracts[1], payroll2);
        assertEq(details.length, 2);
        
        vm.stopPrank();
    }

    function testGetAllPayrollContractsWithEmployers() public {
    vm.prank(employer1);
    address payroll1 = factory.createPayrollContract();
    
    vm.prank(employer2);
    address payroll2 = factory.createPayrollContract();
    
    (address[] memory employers, address[] memory contracts) = factory.getAllPayrollContractsWithEmployers();
    
    assertEq(employers.length, contracts.length);
    assertEq(employers[0], employer1);
    assertEq(employers[1], employer2);
    assertEq(contracts[0], payroll1);
    assertEq(contracts[1], payroll2);
    }


    function testZeroAddressChecks() public {
        vm.startPrank(admin);
        
        // Test zero address for AI agent
        vm.expectRevert(RikaFactory.ZeroAddress.selector);
        factory.addAiAgent(address(0));
        
        vm.expectRevert(RikaFactory.ZeroAddress.selector);
        factory.removeAiAgent(address(0));
        
        // Test zero address in constructor
        vm.expectRevert(RikaFactory.ZeroAddress.selector);
        new RikaFactory(address(0), address(usdc));
        
        vm.expectRevert(RikaFactory.ZeroAddress.selector);
        new RikaFactory(address(implementation), address(0));
        
        vm.stopPrank();
    }
     function setupTeslaPayroll() internal {
        vm.startPrank(tesla);
        address teslaPayroll1 = factory.createPayrollContract();
        address teslaPayroll2 = factory.createPayrollContract();
        address teslaPayroll3 = factory.createPayrollContract();

        RikaManagement(teslaPayroll1).addEmployee("Engineering Lead", address(0x11), 180000e6);
        RikaManagement(teslaPayroll1).addEmployee("Senior Dev", address(0x12), 150000e6);
        RikaManagement(teslaPayroll1).addEmployee("Product Manager", address(0x13), 160000e6);
        
        RikaManagement(teslaPayroll1).createSchedule(address(0x11), block.timestamp, block.timestamp + 365 days, RikaManagement.Interval.Monthly);
        RikaManagement(teslaPayroll1).createSchedule(address(0x12), block.timestamp, block.timestamp + 365 days, RikaManagement.Interval.Monthly);
        RikaManagement(teslaPayroll1).createSchedule(address(0x13), block.timestamp, block.timestamp + 365 days, RikaManagement.Interval.Monthly);

        usdc.approve(teslaPayroll1, 1000000e6);
        RikaManagement(teslaPayroll1).addFunds(500000e6);
        vm.stopPrank();
    }

    function setupApplePayroll() internal {
        vm.startPrank(apple);
        address applePayroll1 = factory.createPayrollContract();
        address applePayroll2 = factory.createPayrollContract();
        address applePayroll3 = factory.createPayrollContract();

        RikaManagement(applePayroll1).addEmployee("iOS Developer", address(0x21), 200000e6);
        RikaManagement(applePayroll1).addEmployee("UX Designer", address(0x22), 170000e6);
        RikaManagement(applePayroll1).addEmployee("Project Lead", address(0x23), 190000e6);

        RikaManagement(applePayroll1).createSchedule(address(0x21), block.timestamp, block.timestamp + 365 days, RikaManagement.Interval.BiWeekly);
        RikaManagement(applePayroll1).createSchedule(address(0x22), block.timestamp, block.timestamp + 365 days, RikaManagement.Interval.BiWeekly);
        RikaManagement(applePayroll1).createSchedule(address(0x23), block.timestamp, block.timestamp + 365 days, RikaManagement.Interval.BiWeekly);

        usdc.approve(applePayroll1, 1200000e6);
        RikaManagement(applePayroll1).addFunds(600000e6);
        vm.stopPrank();
    }

    function setupMicrosoftPayroll() internal {
        vm.startPrank(microsoft);
        address msPayroll1 = factory.createPayrollContract();
        address msPayroll2 = factory.createPayrollContract();
        address msPayroll3 = factory.createPayrollContract();

        RikaManagement(msPayroll1).addEmployee("Cloud Architect", address(0x31), 195000e6);
        RikaManagement(msPayroll1).addEmployee("DevOps Engineer", address(0x32), 165000e6);
        RikaManagement(msPayroll1).addEmployee("Security Specialist", address(0x33), 175000e6);

        RikaManagement(msPayroll1).createSchedule(address(0x31), block.timestamp, block.timestamp + 365 days, RikaManagement.Interval.Monthly);
        RikaManagement(msPayroll1).createSchedule(address(0x32), block.timestamp, block.timestamp + 365 days, RikaManagement.Interval.Monthly);
        RikaManagement(msPayroll1).createSchedule(address(0x33), block.timestamp, block.timestamp + 365 days, RikaManagement.Interval.Monthly);

        usdc.approve(msPayroll1, 1100000e6);
        RikaManagement(msPayroll1).addFunds(550000e6);
        vm.stopPrank();
    }

    function setupAmazonPayroll() internal {
        vm.startPrank(amazon);
        address amazonPayroll1 = factory.createPayrollContract();
        address amazonPayroll2 = factory.createPayrollContract();
        address amazonPayroll3 = factory.createPayrollContract();

        RikaManagement(amazonPayroll1).addEmployee("AWS Specialist", address(0x41), 185000e6);
        RikaManagement(amazonPayroll1).addEmployee("Data Scientist", address(0x42), 175000e6);
        RikaManagement(amazonPayroll1).addEmployee("ML Engineer", address(0x43), 180000e6);

        RikaManagement(amazonPayroll1).createSchedule(address(0x41), block.timestamp, block.timestamp + 365 days, RikaManagement.Interval.Weekly);
        RikaManagement(amazonPayroll1).createSchedule(address(0x42), block.timestamp, block.timestamp + 365 days, RikaManagement.Interval.Weekly);
        RikaManagement(amazonPayroll1).createSchedule(address(0x43), block.timestamp, block.timestamp + 365 days, RikaManagement.Interval.Weekly);

        usdc.approve(amazonPayroll1, 1300000e6);
        RikaManagement(amazonPayroll1).addFunds(650000e6);
        vm.stopPrank();
    }

    function setupGooglePayroll() internal {
        vm.startPrank(google);
        address googlePayroll1 = factory.createPayrollContract();
        address googlePayroll2 = factory.createPayrollContract();
        address googlePayroll3 = factory.createPayrollContract();

        RikaManagement(googlePayroll1).addEmployee("AI Researcher", address(0x51), 210000e6);
        RikaManagement(googlePayroll1).addEmployee("Software Engineer", address(0x52), 180000e6);
        RikaManagement(googlePayroll1).addEmployee("Technical Lead", address(0x53), 200000e6);

        RikaManagement(googlePayroll1).createSchedule(address(0x51), block.timestamp, block.timestamp + 365 days, RikaManagement.Interval.BiWeekly);
        RikaManagement(googlePayroll1).createSchedule(address(0x52), block.timestamp, block.timestamp + 365 days, RikaManagement.Interval.BiWeekly);
        RikaManagement(googlePayroll1).createSchedule(address(0x53), block.timestamp, block.timestamp + 365 days, RikaManagement.Interval.BiWeekly);

        usdc.approve(googlePayroll1, 1500000e6);
        RikaManagement(googlePayroll1).addFunds(750000e6);
        vm.stopPrank();
    }

    function verifyEmployerDetails(address employer, string memory name) internal view {
        (address[] memory contracts, RikaManagement.PayrollDetails[] memory details) = factory.getEmployerPayrollDetails(employer);
        
        console2.log("---", name, "PAYROLL DETAILS", "---");
        for(uint j = 0; j < contracts.length; j++) {
            console2.log("Contract:", contracts[j]);
            console2.log("Total Employees:", details[j].totalEmployees);
            console2.log("Total Liability:", details[j].totalLiability);
            console2.log("Current Balance:", details[j].currentBalance);
            console2.log("---");
        }
    }

    function testGetEmployerPayrollDetailsMultipleEmployers() public {

        setupTeslaPayroll();
        setupApplePayroll();
        setupMicrosoftPayroll();
        setupAmazonPayroll();
        setupGooglePayroll();

        verifyEmployerDetails(tesla, "TESLA");
        verifyEmployerDetails(apple, "APPLE");
        verifyEmployerDetails(microsoft, "MICROSOFT");
        verifyEmployerDetails(amazon, "AMAZON");
        verifyEmployerDetails(google, "GOOGLE");

        (address[] memory teslaContracts, RikaManagement.PayrollDetails[] memory teslaDetails) = factory.getEmployerPayrollDetails(tesla);
        assertEq(teslaContracts.length, 3);
        assertEq(teslaDetails[0].totalEmployees, 3);
        assertEq(teslaDetails[0].totalLiability, 490000e6);
        assertEq(teslaDetails[0].currentBalance, 500000e6);
    }

    function testGetEmployeeDetails() public {
    console2.log("=== Testing Employee Details ===");
    
    // Setup employer and multiple employees
    address employer = address(0x1);
    address[] memory employees = new address[](6);
    employees[0] = address(0x11);
    employees[1] = address(0x12);
    employees[2] = address(0x13);
    employees[3] = address(0x14);
    employees[4] = address(0x15);
    employees[5] = address(0x16);
    
    string[] memory names = new string[](6);
    names[0] = "Engineering Lead";
    names[1] = "Senior Developer";
    names[2] = "Product Manager";
    names[3] = "UX Designer";
    names[4] = "Data Scientist";
    names[5] = "DevOps Engineer";
    
    uint256[] memory salaries = new uint256[](6);
    salaries[0] = 180000e6;
    salaries[1] = 150000e6;
    salaries[2] = 160000e6;
    salaries[3] = 140000e6;
    salaries[4] = 170000e6;
    salaries[5] = 155000e6;
    
    console2.log("Setting up employer:", employer);
    
    // Create multiple payroll contracts and distribute employees
    vm.startPrank(employer);
    address payrollContract1 = factory.createPayrollContract();
    address payrollContract2 = factory.createPayrollContract();
    
    // Add employees to first payroll contract
    for(uint i = 0; i < 3; i++) {
        RikaManagement(payrollContract1).addEmployee(names[i], employees[i], salaries[i]);
        console2.log("\nAdding to Payroll 1:");
        console2.log("Employee:", employees[i]);
        console2.log("Name:", names[i]);
        console2.log("Salary:", salaries[i]);
    }
    
    // Add employees to second payroll contract
    for(uint i = 3; i < 6; i++) {
        RikaManagement(payrollContract2).addEmployee(names[i], employees[i], salaries[i]);
        console2.log("\nAdding to Payroll 2:");
        console2.log("Employee:", employees[i]);
        console2.log("Name:", names[i]);
        console2.log("Salary:", salaries[i]);
    }
    vm.stopPrank();
    
    // Search and verify each employee
    console2.log("\n=== Verifying All Employees ===");
    for(uint i = 0; i < employees.length; i++) {
        console2.log("\nSearching employee:", names[i]);
        (
            address employeeAddress,
            string memory empName,
            uint256 empSalary,
            uint256 joiningDate,
            bool isActive
        ) = factory.getEmployeeDetails(employer, employees[i]);
        
        console2.log("Retrieved Details:");
        console2.log("Address:", employeeAddress);
        console2.log("Name:", empName);
        console2.log("Salary:", empSalary);
        console2.log("Joining Date:", joiningDate);
        console2.log("Active Status:", isActive);
        
        assertEq(employeeAddress, employees[i], "Employee address mismatch");
        assertEq(empName, names[i], "Employee name mismatch");
        assertEq(empSalary, salaries[i], "Salary mismatch");
        assertTrue(joiningDate > 0, "Join date should be set");
        assertTrue(isActive, "Employee should be active");
    }
    
    // Test non-existent employee
    console2.log("\n=== Testing Non-existent Employee ===");
    (
        address nonExistentAddress,
        string memory nonExistentName,
        uint256 nonExistentSalary,
        uint256 nonExistentJoinDate,
        bool nonExistentActive
    ) = factory.getEmployeeDetails(employer, address(0x999));
    
    console2.log("Non-existent Employee Details:");
    console2.log("Address:", nonExistentAddress);
    console2.log("Name:", nonExistentName);
    console2.log("Salary:", nonExistentSalary);
    console2.log("Joining Date:", nonExistentJoinDate);
    console2.log("Active Status:", nonExistentActive);
    
    assertEq(nonExistentAddress, address(0), "Should return zero address");
    assertEq(nonExistentName, "", "Should return empty name");
    assertEq(nonExistentSalary, 0, "Should return zero salary");
    assertEq(nonExistentJoinDate, 0, "Should return zero join date");
    assertFalse(nonExistentActive, "Should return inactive status");
    
    console2.log("=== Test Complete ===");
    }

    function testGetTotalEmployeesFactory() public {
    // Setup employer and multiple employees
    address employer = address(0x1);
    vm.startPrank(employer);
    
    // Create two payroll contracts
    address payrollContract1 = factory.createPayrollContract();
    address payrollContract2 = factory.createPayrollContract();
    
    // Add employees to first contract
    RikaManagement(payrollContract1).addEmployee("Engineer 1", address(0x11), 100000e6);
    RikaManagement(payrollContract1).addEmployee("Engineer 2", address(0x12), 110000e6);
    
    // Add employees to second contract
    RikaManagement(payrollContract2).addEmployee("Designer 1", address(0x13), 90000e6);
    RikaManagement(payrollContract2).addEmployee("Designer 2", address(0x14), 95000e6);
    RikaManagement(payrollContract2).addEmployee("Designer 3", address(0x15), 97000e6);
    
    vm.stopPrank();
    
    // Verify total employees
    uint256 totalEmployees = factory.getTotalEmployees(employer);
    assertEq(totalEmployees, 5, "Total employees should be 5");
    
    console2.log("Total employees across all contracts:", totalEmployees);
    }


}
