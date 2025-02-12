// SPDX-License-Identifier: MIT
pragma solidity ^0.8.28;

// Importing necessary OpenZeppelin contracts
import {AccessControl} from "@openzeppelin/contracts/access/AccessControl.sol";
import {Pausable} from "@openzeppelin/contracts/utils/Pausable.sol";
import {IERC20} from "@openzeppelin/contracts/token/ERC20/IERC20.sol";
import {SafeERC20} from "@openzeppelin/contracts/token/ERC20/utils/SafeERC20.sol";

/**
 * @title RikaPayrollManager
 * @notice This contract allows employers to add employees, set up schedules, fund payrolls, process payments,
 * and withdraw excess funds. It uses role-based access control (AccessControl) and can be paused (Pausable).
 *
 * @dev This version uses the employee's wallet address as the key instead of an employee ID.
 */
contract RikaManagement is AccessControl, Pausable {
    using SafeERC20 for IERC20;

    // ============================
    // Custom Errors for Gas Savings
    // ============================
    error ArrayLengthMismatch();
    error InvalidAddress();
    error EmployeeAlreadyExists();
    error EmployeeNotFound();
    error UnauthorizedAccess();
    error InvalidSchedule();
    error ScheduleNotCompleted();
    error InsufficientBalance();
    error TransferFailed();
    error PayrollAlreadyProcessed();
    error ZeroAmount();
    error InsufficientAllowance();
    error WithdrawalLocked(uint256 nextPayrollDate);
    error AlreadyInitialized();
    error InvalidInitAddress();
    error OverlappingSchedule();

    bool private initialized;
    address private  employerAddress;


    // =====================
    // Roles for Access Control
    // =====================
    bytes32 public constant EMPLOYER_ROLE = keccak256("EMPLOYER_ROLE");
    bytes32 public constant AI_AGENT_ROLE = keccak256("AI_AGENT_ROLE");

    // =====================
    // Immutable Token Contract
    // =====================
    IERC20 public usdcToken;

    // =====================
    // Enums and Structs for Data Management
    // =====================

    /// @notice Represents the interval for schedules.
    enum Interval {
        Weekly,
        BiWeekly,
        Monthly
    }

    /// @notice Represents an employee's basic details.
    struct Employee {
        address employeeAddress; // Employee's wallet address.
        string name; // Employee's name.
        uint256 salary; // Employee's salary.
        uint256 joiningDate; // Date when the employee joined.
        bool isActive;  // Indicates if the employee is currently active.
    }

    /// @notice Represents a schedule for an employee.
    struct Schedule {
        uint256 scheduleId;
        uint256 startDate;
        uint256 endDate;
        Interval interval;         // Interval for the schedule.
        uint256 lastProcessedDate; // Timestamp when payroll was last processed.
        bool isProcessed;          // (Optional) Flag if the schedule has been processed.
        bool isActive;             // Indicates whether this schedule is currently active.
    }

    /// @notice Represents the details of a payroll.
    struct PayrollDetails {
        uint256 totalEmployees;
        uint256 totalLiability; 
        uint256 currentBalance;
    }


    // ================================================
    // Mappings for Employee and Schedule Data Storage
    // ================================================

    // Mapping employer => (employeeAddress => Employee)
    mapping(address => mapping(address => Employee)) private employeesByEmployer;
    // Mapping employer => list of employee addresses (for iteration)
    mapping(address => address[]) private employerEmployees;
    /**
     * @notice Mapping to store schedules for an employee.
     * @dev Key: employer address => employeeAddress => array of Schedule.
     */
    mapping(address => mapping(address => Schedule[])) private employeeSchedules;
    // Mapping employer => available funds (in USDC) for payroll
    mapping(address => uint256) private employerBalances;

    // =====================
    // Events for Logging
    // =====================
    event EmployeeAdded(address indexed employer, address indexed employeeAddress, string name);
    event EmployeeUpdated(address indexed employer, address indexed employeeAddress);
    event EmployeeDeactivated(address indexed employer, address indexed employeeAddress);
    event ScheduleCreated(
        address indexed employer,
        address indexed employeeAddress,
        uint256 scheduleId,
        uint256 startDate,
        uint256 endDate,
        Interval interval
    );
    event EmployeeReactivated(address indexed employer, address indexed employeeAddress);
    event ScheduleUpdated(address indexed employer, address indexed employeeAddress, uint256 scheduleId, Interval interval);
    event SalaryPaid(address indexed employer, address indexed employeeAddress, uint256 amount);
    event FundsAdded(address indexed employer, uint256 amount);
    event FundsWithdrawn(address indexed employer, uint256 amount);
    event PayrollProcessed(address indexed employer, uint256 totalPayout, uint256 timestamp);

    // =====================
    // Modifiers for Access Control and Validation
    // =====================
    function initialize(address _usdcToken, address _employer) external {
    if (initialized) revert AlreadyInitialized();
    if (_usdcToken == address(0) || _employer == address(0)) revert InvalidInitAddress();
    
    initialized = true;
    usdcToken = IERC20(_usdcToken);
    employerAddress = _employer;
    
    // Set up roles hierarchy
    _setRoleAdmin(AI_AGENT_ROLE, DEFAULT_ADMIN_ROLE);
    
    // Grant employer role
    _grantRole(EMPLOYER_ROLE, _employer);
    // Keep factory as admin
    _grantRole(DEFAULT_ADMIN_ROLE, msg.sender);
    }


    /**
     * @dev Checks that the caller is the employer of the employee with _employeeAddress.
     */
    modifier onlyEmployerOf(address _employeeAddress) {
        if (employeesByEmployer[msg.sender][_employeeAddress].joiningDate == 0)
            revert EmployeeNotFound();
        _;
    }

    /**
     * @dev Checks that the caller has either EMPLOYER_ROLE or AI_AGENT_ROLE.
     */
    modifier onlyEmployerOrAgent() {
        if (!hasRole(EMPLOYER_ROLE, msg.sender) && !hasRole(AI_AGENT_ROLE, msg.sender))
            revert UnauthorizedAccess();
        _;
    }

    // =====================
    // Employee Management Functions
    // =====================

    /**
     * @notice Adds a new employee for the caller (employer).
     * @param _name The employee’s name.
     * @param _employeeAddress The employee’s wallet address.
     * @param _salary The salary assigned to the employee (in smallest USDC unit).
     */
    function addEmployee(string memory _name, address _employeeAddress, uint256 _salary)
        public
        whenNotPaused
        onlyRole(EMPLOYER_ROLE)
    {
        if (_employeeAddress == address(0)) revert InvalidAddress();
        if (_salary == 0) revert ZeroAmount();

        // Ensure the employee does not already exist for this employer.
        if (employeesByEmployer[msg.sender][_employeeAddress].joiningDate != 0) {
            revert EmployeeAlreadyExists();
        }

        // Add the employee to the employer's list.
        employeesByEmployer[msg.sender][_employeeAddress] = Employee({
            employeeAddress: _employeeAddress, // Add employee address to the struct.
            name: _name,
            salary: _salary,
            joiningDate: block.timestamp,
            isActive: true
        });

        // Record the new employee address for iteration.
        employerEmployees[msg.sender].push(_employeeAddress);

        emit EmployeeAdded(msg.sender, _employeeAddress, _name);
    }

    /**
     * @notice Creates a new schedule for an existing employee.
     * @param _employeeAddress The employee’s wallet address.
     * @param _startDate The start timestamp for the schedule.
     * @param _endDate The end timestamp for the schedule.
     * @param _interval The interval for the schedule.
     */
    function createSchedule(
        address _employeeAddress,
        uint256 _startDate,
        uint256 _endDate,
        Interval _interval
    )
        external
        whenNotPaused
        onlyRole(EMPLOYER_ROLE)
        onlyEmployerOf(_employeeAddress)
    {
        Employee storage employee = employeesByEmployer[msg.sender][_employeeAddress];
        if (!employee.isActive) revert EmployeeNotFound();
        if (_startDate >= _endDate) revert InvalidSchedule();

        // Check for any overlapping schedules.
        Schedule[] storage schedules = employeeSchedules[msg.sender][_employeeAddress];
        for (uint256 i = 0; i < schedules.length; i++) {
            if (_startDate < schedules[i].endDate && _endDate > schedules[i].startDate) {
                revert OverlappingSchedule();
            }
        }

        // The scheduleId is the current length of the schedules array.
        uint256 scheduleId = schedules.length;
        schedules.push(
            Schedule({
                scheduleId: scheduleId,
                startDate: _startDate,
                endDate: _endDate,
                interval: _interval,
                lastProcessedDate: block.timestamp,
                isProcessed: false,
                isActive: true
            })
        );

        emit ScheduleCreated(msg.sender, _employeeAddress, scheduleId, _startDate, _endDate, _interval);
    }

    /**
    * @notice Deactivates a schedule for an employee.
    * @param _employeeAddress The employee's address.
    * @param _scheduleId The schedule ID to deactivate.
    */
    function deactivateSchedule(address _employeeAddress, uint256 _scheduleId)
        external
        onlyRole(EMPLOYER_ROLE)
        onlyEmployerOf(_employeeAddress)
    {
        Schedule[] storage schedules = employeeSchedules[msg.sender][_employeeAddress];
        if (_scheduleId >= schedules.length) revert InvalidSchedule();

        schedules[_scheduleId].isActive = false;
        emit ScheduleUpdated(msg.sender, _employeeAddress, _scheduleId, schedules[_scheduleId].interval);
    }

    /**
     * @notice Updates the interval for an existing schedule.
     * @param _employeeAddress The employee’s wallet address.
     * @param _scheduleId The schedule ID to update.
     * @param _interval The new interval for the schedule.
     */
    function updateSchedule(
        address _employeeAddress,
        uint256 _scheduleId,
        Interval _interval
    )
        external
        whenNotPaused
        onlyRole(EMPLOYER_ROLE)
        onlyEmployerOf(_employeeAddress)
    {
        Schedule[] storage schedules = employeeSchedules[msg.sender][_employeeAddress];
        if (_scheduleId >= schedules.length) revert InvalidSchedule();

        schedules[_scheduleId].interval = _interval;
        emit ScheduleUpdated(msg.sender, _employeeAddress, _scheduleId, _interval);
    }

    /**
     * @notice Updates an employee's salary.
     * @param _employeeAddress The employee’s wallet address.
     * @param _newSalary The new salary amount.
     */
    function updateEmployeeSalary(address _employeeAddress, uint256 _newSalary)
        public
        whenNotPaused
        onlyRole(EMPLOYER_ROLE)
        onlyEmployerOf(_employeeAddress)
    {
        if (_newSalary == 0) revert ZeroAmount();
        employeesByEmployer[msg.sender][_employeeAddress].salary = _newSalary;
        emit EmployeeUpdated(msg.sender, _employeeAddress);
    }


    /**
    * @notice Reactivates a deactivated employee.
    * @param _employeeAddress The employee's address.
    */
    function reactivateEmployee(address _employeeAddress)
        external
        onlyRole(EMPLOYER_ROLE)
        onlyEmployerOf(_employeeAddress)
    {
        employeesByEmployer[msg.sender][_employeeAddress].isActive = true;
        emit EmployeeUpdated(msg.sender, _employeeAddress);
    }
    /**
     * @notice Deactivates an employee, so they no longer receive payroll.
     * @param _employeeAddress The employee’s wallet address.
     */
    function deactivateEmployee(address _employeeAddress)
        external
        whenNotPaused
        onlyRole(EMPLOYER_ROLE)
        onlyEmployerOf(_employeeAddress)
    {
        employeesByEmployer[msg.sender][_employeeAddress].isActive = false;
        emit EmployeeDeactivated(msg.sender, _employeeAddress);
    }

    /**
     * @notice Updates salaries for multiple employees in a single transaction.
     * @param _employeeAddresses Array of employee addresses.
     * @param _newSalaries Array of new salaries.
     */
    function updateSalariesBatch(
        address[] memory _employeeAddresses,
        uint256[] memory _newSalaries
    ) external onlyRole(EMPLOYER_ROLE) {
        if (_employeeAddresses.length != _newSalaries.length) {
            revert ArrayLengthMismatch();
        }

        for (uint256 i = 0; i < _employeeAddresses.length; i++) {
            updateEmployeeSalary(_employeeAddresses[i], _newSalaries[i]);
        }
    }

    /**
     * @notice Adds multiple employees in a single transaction.
     * @param _names Array of employee names.
     * @param _employeeAddresses Array of employee addresses.
     * @param _salaries Array of employee salaries.
     */
    function addEmployeesBatch(
        string[] memory _names,
        address[] memory _employeeAddresses,
        uint256[] memory _salaries
    ) external onlyRole(EMPLOYER_ROLE) {
        if (_names.length != _employeeAddresses.length || _employeeAddresses.length != _salaries.length) {
            revert ArrayLengthMismatch();
        }

        for (uint256 i = 0; i < _employeeAddresses.length; i++) {
            addEmployee(_names[i], _employeeAddresses[i], _salaries[i]);
        }
    }


    // =====================
    // Fund and Payroll Functions
    // =====================

    /**
     * @notice Adds funds to the caller’s (employer’s) balance.
     * @param _amount The amount of USDC (in smallest unit) to add.
     */
    function addFunds(uint256 _amount) external whenNotPaused onlyRole(EMPLOYER_ROLE) {
        if (_amount == 0) revert ZeroAmount();

        // Check that the employer has approved enough USDC for the transfer.
        uint256 allowance = usdcToken.allowance(msg.sender, address(this));
        if (allowance < _amount) revert InsufficientAllowance();

        usdcToken.safeTransferFrom(msg.sender, address(this), _amount);
        employerBalances[msg.sender] += _amount;

        emit FundsAdded(msg.sender, _amount);
    }

    /**
     * @notice Processes payroll for all employees of the caller.
     *         It calculates the total payout needed and then processes payment for each eligible schedule.
     */
    function processAllPayrolls() external whenNotPaused onlyEmployerOrAgent {
    address[] memory employeeAddresses = employerEmployees[msg.sender];
    if (employeeAddresses.length == 0) revert EmployeeNotFound();

    uint256 totalPayout = 0;
    uint256 employerBalance = employerBalances[msg.sender]; // Cache employer balance

    // First pass: calculate the total payout required.
    for (uint256 i = 0; i < employeeAddresses.length; i++) {
        Employee storage employee = employeesByEmployer[msg.sender][employeeAddresses[i]];
        Schedule[] storage schedules = employeeSchedules[msg.sender][employeeAddresses[i]];

        for (uint256 j = 0; j < schedules.length; j++) {
            Schedule storage schedule = schedules[j];
            if (!schedule.isActive || !employee.isActive) continue;

            uint256 nextPaymentDate = schedule.lastProcessedDate + getIntervalDuration(schedule.interval);
            if (block.timestamp < nextPaymentDate) continue;

            totalPayout += employee.salary;
        }
    }

    if (employerBalance < totalPayout) revert InsufficientBalance();

    // Second pass: process payroll for each employee.
    for (uint256 i = 0; i < employeeAddresses.length; i++) {
        Employee storage employee = employeesByEmployer[msg.sender][employeeAddresses[i]];
        Schedule[] storage schedules = employeeSchedules[msg.sender][employeeAddresses[i]];

        for (uint256 j = 0; j < schedules.length; j++) {
            Schedule storage schedule = schedules[j];
            if (!schedule.isActive || !employee.isActive) continue;

            uint256 nextPaymentDate = schedule.lastProcessedDate + getIntervalDuration(schedule.interval);
            if (block.timestamp < nextPaymentDate) continue;

            schedule.lastProcessedDate = block.timestamp;
            employerBalance -= employee.salary; // Update cached balance
            usdcToken.safeTransfer(employeeAddresses[i], employee.salary);
            emit SalaryPaid(msg.sender, employeeAddresses[i], employee.salary);
        }
    }

    employerBalances[msg.sender] = employerBalance; // Update storage once
    emit PayrollProcessed(msg.sender, totalPayout, block.timestamp);
    }

    /**
     * @notice Withdraws funds from the caller’s (employer’s) balance.
     *         The withdrawal is prevented if a payroll is scheduled soon (within 3 days).
     * @param _amount The amount to withdraw.
     */
    function withdrawFunds(uint256 _amount) external whenNotPaused onlyRole(EMPLOYER_ROLE) {
        if (_amount == 0) revert ZeroAmount();
        if (employerBalances[msg.sender] < _amount) revert InsufficientBalance();

        // Determine the next payroll payment date across all employees.
        uint256 nextPayrollDate = 0;
        address[] storage empAddresses = employerEmployees[msg.sender];
        for (uint256 i = 0; i < empAddresses.length; i++) {
            Schedule[] storage schedules = employeeSchedules[msg.sender][empAddresses[i]];
            for (uint256 j = 0; j < schedules.length; j++) {
                Schedule storage schedule = schedules[j];
                if (schedule.isActive) {
                    uint256 nextPaymentDate = schedule.lastProcessedDate + getIntervalDuration(schedule.interval);
                    if (nextPaymentDate > nextPayrollDate) {
                        nextPayrollDate = nextPaymentDate;
                    }
                }
            }
        }

        // Prevent withdrawal if within 3 days of the next scheduled payroll.
        if (nextPayrollDate > 0 && block.timestamp >= nextPayrollDate - 3 days) {
            revert WithdrawalLocked(nextPayrollDate);
        }

        employerBalances[msg.sender] -= _amount;
        usdcToken.safeTransfer(msg.sender, _amount);

        emit FundsWithdrawn(msg.sender, _amount);
    }

    /**
    * @notice Add an AI agent role to an address
    * @param agent Address to grant AI agent role to
    */
    function addAiAgent(address agent) external onlyRole(DEFAULT_ADMIN_ROLE) {
        if(agent == address(0)) revert InvalidAddress();
        _grantRole(AI_AGENT_ROLE, agent);
    }

    /**
    * @notice Remove an AI agent role from an address
    * @param agent Address to revoke AI agent role from
    */
    function removeAiAgent(address agent) external onlyRole(DEFAULT_ADMIN_ROLE) {
        if(agent == address(0)) revert InvalidAddress();
        _revokeRole(AI_AGENT_ROLE, agent);
    }

    // =====================
    // Helper Functions
    // =====================

    /**
     * @notice Returns the duration in seconds for a given interval.
     * @param _interval The interval to get the duration for.
     * @return duration The duration in seconds.
     */
    function getIntervalDuration(Interval _interval) internal pure returns (uint256 duration) {
        if (_interval == Interval.Weekly) {
            return 1 weeks;
        } else if (_interval == Interval.BiWeekly) {
            return 2 weeks;
        } else if (_interval == Interval.Monthly) {
            return 30 days;
        } else {
            revert InvalidSchedule();
        }
    }

    // =====================
    // View Functions for Querying Data
    // =====================

    /**
     * @notice Returns the employer's available funds.
     * @param _employer The employer's address.
     */
    function getEmployerBalance(address _employer) external view returns (uint256) {
        return employerBalances[_employer];
    }

    // Get employee details from employeesByEmployer mapping
    function getEmployee(address employer, address employee) external view returns (Employee memory) {
        return employeesByEmployer[employer][employee];
    }

    // Get list of employee addresses from employerEmployees mapping 
    function getEmployeeList(address employer) external view returns (address[] memory) {
        return employerEmployees[employer];
    }

    // Get schedules from employeeSchedules mapping
    function getSchedules(address employer, address employee) external view returns (Schedule[] memory) {
        return employeeSchedules[employer][employee];
    }


    /**
     * @notice Returns the total monthly payroll liability for an employer.
     * @param _employer The employer's address.
     */
    function getTotalPayrollLiability(address _employer) external view returns (uint256 totalLiability) {
        address[] memory empAddresses = employerEmployees[_employer];

        for (uint256 i = 0; i < empAddresses.length; i++) {
            Employee memory employee = employeesByEmployer[_employer][empAddresses[i]];
            if (employee.isActive) {
                totalLiability += employee.salary;
            }
        }

        return totalLiability;
    }

    /**
     * @notice Returns the next payroll date for a specific employee.
     * @return nextPaymentDate The next timestamp when payroll is scheduled.
     */
    function getNextPayrollDate(address _employer, address _employeeAddress)
        external
        view
        returns (uint256 nextPaymentDate)
    {
        Schedule[] storage schedules = employeeSchedules[_employer][_employeeAddress];
        for (uint256 i = 0; i < schedules.length; i++) {
            Schedule storage schedule = schedules[i];
            if (schedule.isActive) {
                uint256 nextDate = schedule.lastProcessedDate + getIntervalDuration(schedule.interval);
                if (nextDate > nextPaymentDate) {
                    nextPaymentDate = nextDate;
                }
            }
        }
        return nextPaymentDate;
    }

    /**
     * @notice Checks whether the employer has sufficient funds to cover payroll liabilities.
     * @return True if the employer's balance is at least the total payroll liability.
     */
    function hasSufficientBalanceForPayroll(address _employer) external view returns (bool) {
        uint256 totalLiability = this.getTotalPayrollLiability(_employer);
        return employerBalances[_employer] >= totalLiability;
    }

    /**
     * @notice Returns all employees (with details) for a given employer.
     * @return Employee[] An array of Employee structs containing employee details.
     */
    function getAllEmployeesWithDetails(address _employer) external view returns (Employee[] memory) {
        address[] memory empAddresses = employerEmployees[_employer];
        Employee[] memory employeeList = new Employee[](empAddresses.length);

        for (uint256 i = 0; i < empAddresses.length; i++) {
            employeeList[i] = employeesByEmployer[_employer][empAddresses[i]];
        }

        return employeeList;
    }

    /**
     * @notice Returns the details of a specific employee.
     */
    function getEmployeeDetails(address _employer, address _employeeAddress)
        external
        view
        returns (
            address employeeAddress,
            string memory name,
            uint256 salary,
            uint256 joiningDate,
            bool isActive
        )
    {
        Employee memory emp = employeesByEmployer[_employer][_employeeAddress];
        return (emp.employeeAddress, emp.name, emp.salary, emp.joiningDate, emp.isActive);
    }

    /**
    * @notice Returns the details of a specific employee by name and address
    * @param _employer The employer's address
    * @param _employeeAddress The employee's address
    * @param _name The employee's name
    */
    function getEmployeeDetailsByNameAndAddress(
        address _employer,
        address _employeeAddress,
        string memory _name
    )
        external
        view
        returns (
            address employeeAddress,
            string memory name,
            uint256 salary,
            uint256 joiningDate,
            bool isActive
        )
    {
        Employee memory emp = employeesByEmployer[_employer][_employeeAddress];
        if (keccak256(bytes(emp.name)) != keccak256(bytes(_name))) revert EmployeeNotFound();
        return (emp.employeeAddress, emp.name, emp.salary, emp.joiningDate, emp.isActive);
    }

    function getEmployer() public view returns (address) {
    return employerAddress;
    }

    /**
    * @notice Returns the total number of employees for an employer
    * @param _employer The employer's address
    * @return total The total number of employees
    */
    function getTotalEmployees(address _employer) external view returns (uint256) {
        return employerEmployees[_employer].length;
    }


}