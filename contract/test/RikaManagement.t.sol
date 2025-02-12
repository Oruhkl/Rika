// SPDX-License-Identifier: MIT
pragma solidity ^0.8.28;

import {Test, console2} from "forge-std/Test.sol";
import {RikaFactory} from "../contracts/RikaFactory.sol";
import {RikaManagement} from "../contracts/RikaManagement.sol";
import {RUSDC} from "../contracts/RUSDC.sol";

contract RikaManagementTest is Test {
    RikaManagement public payroll;
    RUSDC public usdc;
    
    address public admin = address(1);
    address public employer = address(2);
    address public employee1 = address(3);
    address public employee2 = address(4);
    address public aiAgent = address(5);
    
    uint256 public constant INITIAL_BALANCE = 1000000e6; // 1M USDC
    uint256 public constant EMPLOYEE_SALARY = 5000e6;    // 5000 USDC
    
    event EmployeeAdded(address indexed employer, address indexed employeeAddress, string name);
    event ScheduleCreated(
        address indexed employer,
        address indexed employeeAddress,
        uint256 scheduleId,
        uint256 startDate,
        uint256 endDate,
        RikaManagement.Interval interval
    );
    
    function setUp() public {
        vm.startPrank(admin);
        
        // Deploy USDC and Payroll contracts
        usdc = new RUSDC();
        payroll = new RikaManagement();
        
        // Initialize payroll
        payroll.initialize(address(usdc), employer);
        
        // Mint USDC to employer
        usdc.mint(employer, INITIAL_BALANCE);
        
        vm.stopPrank();
    }
    
    function testEmployeeManagement() public {
        vm.startPrank(employer);
        
        // Add employee
        string memory name = "John Doe";
        payroll.addEmployee(name, employee1, EMPLOYEE_SALARY);
        
        // Verify employee details
        (
            address empAddress,
            string memory empName,
            uint256 empSalary,
            uint256 joiningDate,
            bool isActive
        ) = payroll.getEmployeeDetails(employer, employee1);
        
        assertEq(empAddress, employee1);
        assertEq(empName, name);
        assertEq(empSalary, EMPLOYEE_SALARY);
        assertTrue(isActive);
        
        vm.stopPrank();
    }
    
    function testScheduleCreation() public {
        vm.startPrank(employer);
        
        // Add employee first
        payroll.addEmployee("John Doe", employee1, EMPLOYEE_SALARY);
        
        // Create schedule
        uint256 startDate = block.timestamp;
        uint256 endDate = startDate + 30 days;
        
        payroll.createSchedule(
            employee1,
            startDate,
            endDate,
            RikaManagement.Interval.Monthly
        );
        
        vm.stopPrank();
    }
    
    function testPayrollProcessing() public {
        vm.startPrank(employer);
        
        // Setup: Add employee and schedule
        payroll.addEmployee("John Doe", employee1, EMPLOYEE_SALARY);
        
        uint256 startDate = block.timestamp;
        uint256 endDate = startDate + 30 days;
        
        payroll.createSchedule(
            employee1,
            startDate,
            endDate,
            RikaManagement.Interval.Monthly
        );
        
        // Add funds
        usdc.approve(address(payroll), EMPLOYEE_SALARY);
        payroll.addFunds(EMPLOYEE_SALARY);
        
        // Process payroll
        vm.warp(startDate + 31 days); // Move time forward
        payroll.processAllPayrolls();
        
        // Verify payment
        assertEq(usdc.balanceOf(employee1), EMPLOYEE_SALARY);
        
        vm.stopPrank();
    }
    
    function testFundManagement() public {
        vm.startPrank(employer);
        
        // Add funds
        uint256 fundAmount = 10000e6;
        usdc.approve(address(payroll), fundAmount);
        payroll.addFunds(fundAmount);
        
        // Verify balance
        assertEq(payroll.getEmployerBalance(employer), fundAmount);
        
        // Withdraw funds
        payroll.withdrawFunds(fundAmount);
        assertEq(payroll.getEmployerBalance(employer), 0);
        
        vm.stopPrank();
    }
    
    function testAiAgentFunctionality() public {
        vm.startPrank(admin);
        
        // Add AI agent
        payroll.addAiAgent(aiAgent);
        assertTrue(payroll.hasRole(payroll.AI_AGENT_ROLE(), aiAgent));
        
        // Remove AI agent
        payroll.removeAiAgent(aiAgent);
        assertFalse(payroll.hasRole(payroll.AI_AGENT_ROLE(), aiAgent));
        
        vm.stopPrank();
    }
    
    function testEdgeCases() public {
        vm.startPrank(employer);
        
        // Test adding employee with zero address
        vm.expectRevert(RikaManagement.InvalidAddress.selector);
        payroll.addEmployee("Invalid", address(0), EMPLOYEE_SALARY);
        
        // Test adding employee with zero salary
        vm.expectRevert(RikaManagement.ZeroAmount.selector);
        payroll.addEmployee("Invalid", employee1, 0);
        
        // Test duplicate employee
        payroll.addEmployee("John", employee1, EMPLOYEE_SALARY);
        vm.expectRevert(RikaManagement.EmployeeAlreadyExists.selector);
        payroll.addEmployee("John", employee1, EMPLOYEE_SALARY);
        
        // Test insufficient funds for payroll
        uint256 startDate = block.timestamp;
        uint256 endDate = startDate + 30 days;
        
        payroll.createSchedule(
            employee1,
            startDate,
            endDate,
            RikaManagement.Interval.Monthly
        );
        
        vm.warp(startDate + 31 days);
        vm.expectRevert(RikaManagement.InsufficientBalance.selector);
        payroll.processAllPayrolls();
        
        vm.stopPrank();
    }
    
    function testAccessControl() public {
        // Test unauthorized access
        vm.startPrank(employee1);
        vm.expectRevert();
        payroll.addEmployee("Unauthorized", employee2, EMPLOYEE_SALARY);
        vm.stopPrank();
        
        // Test AI agent permissions
        vm.startPrank(aiAgent);
        vm.expectRevert();
        payroll.addEmployee("Unauthorized", employee2, EMPLOYEE_SALARY);
        vm.stopPrank();
    }


    function testUpdateEmployeeSalary() public {
    vm.startPrank(employer);
    
    // Add employee first
    payroll.addEmployee("John Doe", employee1, EMPLOYEE_SALARY);
    
    // Update salary
    uint256 newSalary = EMPLOYEE_SALARY * 2;
    payroll.updateEmployeeSalary(employee1, newSalary);
    
    // Verify updated salary
    (, , uint256 salary, , ) = payroll.getEmployeeDetails(employer, employee1);
    assertEq(salary, newSalary);
    
    vm.stopPrank();
    }

    function testNextPayrollDate() public {
        vm.startPrank(employer);
        
        // Add employee and schedule
        payroll.addEmployee("John Doe", employee1, EMPLOYEE_SALARY);
        
        uint256 startDate = block.timestamp;
        uint256 endDate = startDate + 90 days;
        
        payroll.createSchedule(
            employee1,
            startDate,
            endDate,
            RikaManagement.Interval.Monthly
        );
        
        // Get next payroll date
        uint256 nextDate = payroll.getNextPayrollDate(employer, employee1);
        assertEq(nextDate, startDate + 30 days);
        
        vm.stopPrank();
    }

    function testHasSufficientBalanceForPayroll() public {
        vm.startPrank(employer);
        
        // Add employee
        payroll.addEmployee("John Doe", employee1, EMPLOYEE_SALARY);
        
        // Initially should be false
        assertFalse(payroll.hasSufficientBalanceForPayroll(employer));
        
        // Add funds
        usdc.approve(address(payroll), EMPLOYEE_SALARY);
        payroll.addFunds(EMPLOYEE_SALARY);
        
        // Now should be true
        assertTrue(payroll.hasSufficientBalanceForPayroll(employer));
        
        vm.stopPrank();
    }

    function testGetAllEmployeesWithDetails() public {
    vm.startPrank(employer);
    
    // Add multiple employees
    payroll.addEmployee("John Doe", employee1, EMPLOYEE_SALARY);
    payroll.addEmployee("Jane Doe", employee2, EMPLOYEE_SALARY * 2);
    
    RikaManagement.Employee[] memory employees = payroll.getAllEmployeesWithDetails(employer);
    
    // Log each employee's details individually
    for(uint i = 0; i < employees.length; i++) {
        console2.log("Employee", i);
        console2.log("Address:", employees[i].employeeAddress);
        console2.log("Name:", employees[i].name);
        console2.log("Salary:", employees[i].salary);
        console2.log("Joining Date:", employees[i].joiningDate);
        console2.log("Active:", employees[i].isActive);
    }
    
    assertEq(employees.length, 2);
    assertEq(employees[0].employeeAddress, employee1);
    assertEq(employees[1].employeeAddress, employee2);
    
    vm.stopPrank();
    }


    function testScheduleOverlap() public {
        vm.startPrank(employer);
        
        payroll.addEmployee("John Doe", employee1, EMPLOYEE_SALARY);
        
        uint256 startDate = block.timestamp;
        uint256 endDate = startDate + 30 days;
        
        payroll.createSchedule(
            employee1,
            startDate,
            endDate,
            RikaManagement.Interval.Monthly
        );
        
        // Try to create overlapping schedule
        vm.expectRevert(RikaManagement.OverlappingSchedule.selector);
        payroll.createSchedule(
            employee1,
            startDate + 15 days,
            endDate + 15 days,
            RikaManagement.Interval.Monthly
        );
        
        vm.stopPrank();
    }

    function testInvalidScheduleDates() public {
    vm.startPrank(employer);
    payroll.addEmployee("John Doe", employee1, EMPLOYEE_SALARY);
    
    // Test end date before start date
    vm.expectRevert(RikaManagement.InvalidSchedule.selector);
    payroll.createSchedule(
        employee1,
        block.timestamp + 1 days,
        block.timestamp,
        RikaManagement.Interval.Monthly
    );
    
    // Test same start and end date
    vm.expectRevert(RikaManagement.InvalidSchedule.selector);
    payroll.createSchedule(
        employee1,
        block.timestamp,
        block.timestamp,
        RikaManagement.Interval.Monthly
    );
    
    vm.stopPrank();
    }

    function testWithdrawalLockPeriod() public {
    vm.startPrank(employer);
    
    // Setup employee and schedule
    payroll.addEmployee("John Doe", employee1, EMPLOYEE_SALARY);
    uint256 startDate = block.timestamp;
    payroll.createSchedule(
        employee1,
        startDate,
        startDate + 90 days,
        RikaManagement.Interval.Monthly
    );
    
    // Add funds
    usdc.approve(address(payroll), EMPLOYEE_SALARY * 2);
    payroll.addFunds(EMPLOYEE_SALARY * 2);
    
    // Move time to just before next payroll
    vm.warp(startDate + 28 days);
    
    // Get the actual next payment date
    uint256 nextPaymentDate = payroll.getNextPayrollDate(employer, employee1);
    
    // Should revert due to lock period
    vm.expectRevert(abi.encodeWithSelector(
        RikaManagement.WithdrawalLocked.selector,
        nextPaymentDate
    ));
    payroll.withdrawFunds(EMPLOYEE_SALARY);
    
    vm.stopPrank();
    }


    function testInvalidEmployeeOperations() public {
        vm.startPrank(employer);
        
        // Test operations on non-existent employee
        vm.expectRevert(RikaManagement.EmployeeNotFound.selector);
        payroll.updateEmployeeSalary(employee1, EMPLOYEE_SALARY);
        
        vm.expectRevert(RikaManagement.EmployeeNotFound.selector);
        payroll.deactivateEmployee(employee1);
        
        vm.expectRevert(RikaManagement.EmployeeNotFound.selector);
        payroll.createSchedule(
            employee1,
            block.timestamp,
            block.timestamp + 30 days,
            RikaManagement.Interval.Monthly
        );
        
        vm.stopPrank();
    }

    function testProcessPayrollEdgeCases() public {
        vm.startPrank(employer);
        
        // Test processing with no employees
        vm.expectRevert(RikaManagement.EmployeeNotFound.selector);
        payroll.processAllPayrolls();
        
        // Add employee but no schedule
        payroll.addEmployee("John Doe", employee1, EMPLOYEE_SALARY);
        
        // Add insufficient funds
        usdc.approve(address(payroll), EMPLOYEE_SALARY / 2);
        payroll.addFunds(EMPLOYEE_SALARY / 2);
        
        // Create schedule
        payroll.createSchedule(
            employee1,
            block.timestamp,
            block.timestamp + 30 days,
            RikaManagement.Interval.Monthly
        );
        
        // Move time forward
        vm.warp(block.timestamp + 31 days);
        
        // Should revert due to insufficient balance
        vm.expectRevert(RikaManagement.InsufficientBalance.selector);
        payroll.processAllPayrolls();
        
        vm.stopPrank();
    }

    function testDoubleInitialization() public {
        vm.startPrank(admin);
        
        // Try to initialize again
        vm.expectRevert(RikaManagement.AlreadyInitialized.selector);
        payroll.initialize(address(usdc), employer);
        
        vm.stopPrank();
    }

   function testMultipleEmployeePayrollAutomation() public {
    vm.startPrank(admin);
    payroll.grantRole(payroll.AI_AGENT_ROLE(), aiAgent);
    vm.stopPrank();

    vm.startPrank(employer);
    
    payroll.addEmployee("John Weekly", employee1, EMPLOYEE_SALARY);
    payroll.addEmployee("Jane Monthly", employee2, EMPLOYEE_SALARY * 2);
    
    uint256 startDate = block.timestamp;
    uint256 endDate = startDate + 90 days;
    
    payroll.createSchedule(
        employee1,
        startDate,
        endDate,
        RikaManagement.Interval.Weekly
    );
    
    payroll.createSchedule(
        employee2,
        startDate,
        endDate,
        RikaManagement.Interval.Monthly
    );

    uint256 totalFunds = (EMPLOYEE_SALARY * 12) + (EMPLOYEE_SALARY * 2 * 3);
    usdc.approve(address(payroll), totalFunds);
    payroll.addFunds(totalFunds);
    
    vm.warp(startDate + 7 days);
    payroll.processAllPayrolls();
    assertEq(usdc.balanceOf(employee1), EMPLOYEE_SALARY);
    assertEq(usdc.balanceOf(employee2), 0);

    vm.warp(startDate + 14 days);
    payroll.processAllPayrolls();
    assertEq(usdc.balanceOf(employee1), EMPLOYEE_SALARY * 2);
    assertEq(usdc.balanceOf(employee2), 0);

    vm.warp(startDate + 30 days);
    payroll.processAllPayrolls();
    assertEq(usdc.balanceOf(employee1), EMPLOYEE_SALARY * 3);
    assertEq(usdc.balanceOf(employee2), EMPLOYEE_SALARY * 2);

    vm.stopPrank();
    }

    function testGetEmployeeDetailsByNameAndAddress() public {
    // Setup
    string memory employeeName = "John Doe";
    address employeeAddress = address(0x1);
    uint256 salary = 1000e6; // 1000 USDC

    // Add employee first
    vm.prank(employer);
    payroll.addEmployee(employeeName, employeeAddress, salary);

    // Get employee details
    vm.prank(employer);
    (
        address retAddress,
        string memory retName,
        uint256 retSalary,
        uint256 retJoiningDate,
        bool retIsActive
    ) = payroll.getEmployeeDetailsByNameAndAddress(employer, employeeAddress, employeeName);

    // Assert all returned values match
    assertEq(retAddress, employeeAddress);
    assertEq(retName, employeeName);
    assertEq(retSalary, salary);
    assertTrue(retJoiningDate > 0);
    assertTrue(retIsActive);
    }

    function testLogEmployeeDetailsByNameAndAddress() public {
    // Setup initial values
    string memory employeeName = "John Doe";
    address employeeAddress = address(0x1);
    uint256 salary = 1000e6; // 1000 USDC

    // Add employee
    vm.prank(employer);
    payroll.addEmployee(employeeName, employeeAddress, salary);

    // Get and log employee details
    vm.prank(employer);
    (
        address retAddress,
        string memory retName,
        uint256 retSalary,
        uint256 retJoiningDate,
        bool retIsActive
    ) = payroll.getEmployeeDetailsByNameAndAddress(employer, employeeAddress, employeeName);

    // Log all details
    console2.log("Employee Details Retrieved:");
    console2.log("Address:", retAddress);
    console2.log("Name:", retName);
    console2.log("Salary:", retSalary);
    console2.log("Joining Date:", retJoiningDate);
    console2.log("Active Status:", retIsActive);

    // Verify logged data matches expected values
    assertEq(retAddress, employeeAddress, "Employee address mismatch");
    assertEq(retName, employeeName, "Employee name mismatch");
    assertEq(retSalary, salary, "Salary mismatch");
    assertTrue(retJoiningDate > 0, "Invalid joining date");
    assertTrue(retIsActive, "Employee should be active");
    }


    function testGetTotalEmployeesManagement() public {
    vm.startPrank(employer);
    
    // Add multiple employees
    payroll.addEmployee("Developer 1", address(0x11), 100000e6);
    payroll.addEmployee("Developer 2", address(0x12), 110000e6);
    payroll.addEmployee("Developer 3", address(0x13), 120000e6);
    
    // Get total employees
    uint256 totalEmployees = payroll.getTotalEmployees(employer);
    assertEq(totalEmployees, 3, "Should have 3 employees");
    
    // Add more employees
    payroll.addEmployee("Developer 4", address(0x14), 130000e6);
    payroll.addEmployee("Developer 5", address(0x15), 140000e6);
    
    // Verify updated total
    totalEmployees = payroll.getTotalEmployees(employer);
    assertEq(totalEmployees, 5, "Should have 5 employees");
    
    console2.log("Total employees in contract:", totalEmployees);
    
    vm.stopPrank();
    }


    function testEmployeeActivationStatus() public {
    vm.startPrank(employer);
    
    // Add employee
    payroll.addEmployee("John Doe", employee1, EMPLOYEE_SALARY);
    
    // Verify initial active status
    (, , , , bool isActive) = payroll.getEmployeeDetails(employer, employee1);
    assertTrue(isActive, "Employee should be active initially");
    
    // Deactivate employee
    payroll.deactivateEmployee(employee1);
    
    // Verify deactivated status
    (, , , , isActive) = payroll.getEmployeeDetails(employer, employee1);
    assertFalse(isActive, "Employee should be deactivated");
    
    // Reactivate employee
    payroll.reactivateEmployee(employee1);
    
    // Verify reactivated status
    (, , , , isActive) = payroll.getEmployeeDetails(employer, employee1);
    assertTrue(isActive, "Employee should be reactivated");
    
    vm.stopPrank();
    }


    function testBatchOperations() public {
    vm.startPrank(employer);
    
    // Test batch adding employees
    string[] memory names = new string[](3);
    names[0] = "Employee 1";
    names[1] = "Employee 2";
    names[2] = "Employee 3";
    
    address[] memory addresses = new address[](3);
    addresses[0] = address(0x100);
    addresses[1] = address(0x101);
    addresses[2] = address(0x102);
    
    uint256[] memory salaries = new uint256[](3);
    salaries[0] = 1000e6;
    salaries[1] = 2000e6;
    salaries[2] = 3000e6;
    
    // Test addEmployeesBatch
    payroll.addEmployeesBatch(names, addresses, salaries);
    
    // Verify employees were added correctly
    for(uint i = 0; i < 3; i++) {
        (address empAddress, string memory empName, uint256 empSalary, , bool isActive) = 
            payroll.getEmployeeDetails(employer, addresses[i]);
        
        assertEq(empAddress, addresses[i]);
        assertEq(empName, names[i]);
        assertEq(empSalary, salaries[i]);
        assertTrue(isActive);
    }
    
    // Test updateSalariesBatch
    uint256[] memory newSalaries = new uint256[](3);
    newSalaries[0] = 1500e6;
    newSalaries[1] = 2500e6;
    newSalaries[2] = 3500e6;
    
    payroll.updateSalariesBatch(addresses, newSalaries);
    
    // Verify salaries were updated
    for(uint i = 0; i < 3; i++) {
        (, , uint256 empSalary, ,) = payroll.getEmployeeDetails(employer, addresses[i]);
        assertEq(empSalary, newSalaries[i]);
    }
    
    vm.stopPrank();
    }




}
