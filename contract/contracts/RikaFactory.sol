// SPDX-License-Identifier: MIT
pragma solidity ^0.8.28;

import {AccessControl} from "@openzeppelin/contracts/access/AccessControl.sol";
import {Pausable} from "@openzeppelin/contracts/utils/Pausable.sol";
import {Clones} from "@openzeppelin/contracts/proxy/Clones.sol";
import {RikaManagement} from "./RikaManagement.sol";

/**
 * @title RikaPayrollFactory
 * @notice Factory contract for deploying and managing PayrollManagement instances
 * @dev Uses minimal proxy pattern for gas-efficient deployment of RikaPayrollManagement contracts
 */
contract RikaFactory is AccessControl, Pausable {
    // ============================
    // Custom Errors
    // ============================
    error UnauthorizedAccess();
    error PayrollContractNotFound();
    error ZeroAddress();
    error MaxPayrollContractsAllowed();

    // ============================
    // Events
    // ============================
    event PayrollContractCreated(address indexed employer, address indexed payrollContract);
    event PayrollContractUpdated(address indexed employer, address indexed payrollContract);
    event AiAgentAdded(address indexed agent);
    event AiAgentRemoved(address indexed agent);
    // ============================
    // State Variables
    // ============================
    address public immutable implementationContract;
    address public immutable usdcToken;


    struct PayrollDetails {
        uint256 totalEmployees;
        uint256 totalLiability; 
        uint256 currentBalance;
    }


    // Mapping of employer address to their PayrollManagement contracts (up to 3 per employer)
    mapping(address => address[]) private employerToPayroll;
    // Array to keep track of all deployed payroll contracts
    address[] public allPayrollContracts;
    // Mapping to track if an address is a deployed payroll contract
    mapping(address => bool) private isPayrollContract;

    // ============================
    // Constructor
    // ============================
    constructor(address _implementation, address _usdcToken) {
        if (_implementation == address(0) || _usdcToken == address(0)) revert ZeroAddress();
        
        implementationContract = _implementation;
        usdcToken = _usdcToken;
        _grantRole(DEFAULT_ADMIN_ROLE, msg.sender);
    }

    // ============================
    // Main Functions
    // ============================

    /**
     * @notice Creates a new PayrollManagement contract for an employer
     * @dev Uses minimal proxy pattern to create a new contract
     * @return payrollContract Address of the newly created contract
     */
    function createPayrollContract() external whenNotPaused returns (address payrollContract) {
        // Check if employer already has 3 payroll contracts
        if (employerToPayroll[msg.sender].length >= 3) revert MaxPayrollContractsAllowed();

        // Deploy new proxy contract
        payrollContract = Clones.clone(implementationContract);
        
        // Update state: add the new contract for the employer and to the global list
        employerToPayroll[msg.sender].push(payrollContract);
        allPayrollContracts.push(payrollContract);
        isPayrollContract[payrollContract] = true;

        // Initialize the new PayrollManagement contract with USDC token and employer's address
        RikaManagement(payrollContract).initialize(usdcToken, msg.sender);

        emit PayrollContractCreated(msg.sender, payrollContract);
    }


    // Add to admin functions section
    /**
    * @notice Add an AI agent role to an address
    * @param agent Address to grant AI agent role to
    */
    function addAiAgent(address agent) external onlyRole(DEFAULT_ADMIN_ROLE) {
        if(agent == address(0)) revert ZeroAddress();
        
        // Grant AI agent role to all existing payroll contracts
        for(uint256 i = 0; i < allPayrollContracts.length; i++) {
            RikaManagement(allPayrollContracts[i]).addAiAgent(agent);
        }
        
        emit AiAgentAdded(agent);
    }

    /**
    * @notice Remove an AI agent role from all existing payroll contracts
    * @param agent Address to revoke AI agent role from
    */
    function removeAiAgent(address agent) external onlyRole(DEFAULT_ADMIN_ROLE) {
        if(agent == address(0)) revert ZeroAddress();
        
        // Remove AI agent role from all existing payroll contracts
        for(uint256 i = 0; i < allPayrollContracts.length; i++) {
            RikaManagement(allPayrollContracts[i]).removeAiAgent(agent);
        }
        
        emit AiAgentRemoved(agent);
    }


    // ============================
    // View Functions
    // ============================


    // Get all payroll contracts for a specific employer
    function getEmployerPayrolls(address employer) external view returns (address[] memory) {
        return employerToPayroll[employer];
    }

    // Get all deployed payroll contracts
    function getAllPayrollContracts() external view returns (address[] memory) {
        return allPayrollContracts;
    }

    // Check if address is a payroll contract
    function isValidPayrollContract(address contractAddress) external view returns (bool) {
    return isPayrollContract[contractAddress];
    }

    /**
    * @notice Get employer's payroll contracts with key details
    */
    function getEmployerPayrollDetails(address employer) 
    external 
    view 
    returns (
        address[] memory contracts,
        RikaManagement.PayrollDetails[] memory details
    ) 
    {
        contracts = employerToPayroll[employer];
        details = new RikaManagement.PayrollDetails[](contracts.length);
        
        for (uint256 i = 0; i < contracts.length; i++) {
            RikaManagement payroll = RikaManagement(contracts[i]);
            details[i] = RikaManagement.PayrollDetails({
                totalEmployees: payroll.getAllEmployeesWithDetails(employer).length,
                totalLiability: payroll.getTotalPayrollLiability(employer),
                currentBalance: payroll.getEmployerBalance(employer)
            });
        }
    }

    /**
    * @notice Returns the details of a specific employee from a payroll contract
    * @param _employer The employer's address
    * @param _employeeAddress The employee's address
    * @return employeeAddress The employee's address
    * @return name The employee's name
    * @return salary The employee's salary
    * @return joiningDate The employee's joining date
    * @return isActive Whether the employee is active
    */
    function getEmployeeDetails(
        address _employer,
        address _employeeAddress
    ) external view returns (
        address employeeAddress,
        string memory name,
        uint256 salary,
        uint256 joiningDate,
        bool isActive
    ) {
        address[] memory contracts = employerToPayroll[_employer];
        for (uint256 i = 0; i < contracts.length; i++) {
            RikaManagement payroll = RikaManagement(contracts[i]);
            (employeeAddress, name, salary, joiningDate, isActive) = 
                payroll.getEmployeeDetails(_employer, _employeeAddress);
            if (employeeAddress != address(0)) {
                return (employeeAddress, name, salary, joiningDate, isActive);
            }
        }
        return (address(0), "", 0, 0, false);
    }


    /**
    * @notice Get all payroll contracts with their respective employers
    * @return employers Array of employer addresses
    * @return contracts Array of corresponding payroll contract addresses
    */
    function getAllPayrollContractsWithEmployers() external view returns (
        address[] memory employers,
        address[] memory contracts
    ) {
        contracts = allPayrollContracts;
        employers = new address[](contracts.length);
        
        for (uint256 i = 0; i < contracts.length; i++) {
            employers[i] = RikaManagement(contracts[i]).getEmployer();
        }
    }

    /**
    * @notice Returns the total number of employees across all payroll contracts for an employer
    * @param _employer The employer's address
    * @return total The total number of employees
    */
    function getTotalEmployees(address _employer) external view returns (uint256 total) {
        address[] memory contracts = employerToPayroll[_employer];
        for (uint256 i = 0; i < contracts.length; i++) {
            RikaManagement payroll = RikaManagement(contracts[i]);
            total += payroll.getAllEmployeesWithDetails(_employer).length;
        }
        return total;
    }


    // ============================
    // Admin Functions
    // ============================

    /**
     * @notice Pause the factory contract
     * @dev Only callable by an admin
     */
    function pause() external onlyRole(DEFAULT_ADMIN_ROLE) {
        _pause();
    }

    /**
     * @notice Unpause the factory contract
     * @dev Only callable by an admin
     */
    function unpause() external onlyRole(DEFAULT_ADMIN_ROLE) {
        _unpause();
    }
}
