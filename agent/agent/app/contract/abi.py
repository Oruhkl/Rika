RIKA_FACTORY_ABI =  [
    {
      "inputs": [
        {
          "internalType": "address",
          "name": "_implementation",
          "type": "address"
        },
        {
          "internalType": "address",
          "name": "_usdcToken",
          "type": "address"
        }
      ],
      "stateMutability": "nonpayable",
      "type": "constructor"
    },
    {
      "inputs": [],
      "name": "AccessControlBadConfirmation",
      "type": "error"
    },
    {
      "inputs": [
        {
          "internalType": "address",
          "name": "account",
          "type": "address"
        },
        {
          "internalType": "bytes32",
          "name": "neededRole",
          "type": "bytes32"
        }
      ],
      "name": "AccessControlUnauthorizedAccount",
      "type": "error"
    },
    {
      "inputs": [],
      "name": "EnforcedPause",
      "type": "error"
    },
    {
      "inputs": [],
      "name": "ExpectedPause",
      "type": "error"
    },
    {
      "inputs": [],
      "name": "FailedDeployment",
      "type": "error"
    },
    {
      "inputs": [
        {
          "internalType": "uint256",
          "name": "balance",
          "type": "uint256"
        },
        {
          "internalType": "uint256",
          "name": "needed",
          "type": "uint256"
        }
      ],
      "name": "InsufficientBalance",
      "type": "error"
    },
    {
      "inputs": [],
      "name": "MaxPayrollContractsAllowed",
      "type": "error"
    },
    {
      "inputs": [],
      "name": "PayrollContractNotFound",
      "type": "error"
    },
    {
      "inputs": [],
      "name": "UnauthorizedAccess",
      "type": "error"
    },
    {
      "inputs": [],
      "name": "ZeroAddress",
      "type": "error"
    },
    {
      "anonymous": False,
      "inputs": [
        {
          "indexed": True,
          "internalType": "address",
          "name": "agent",
          "type": "address"
        }
      ],
      "name": "AiAgentAdded",
      "type": "event"
    },
    {
      "anonymous": False,
      "inputs": [
        {
          "indexed": True,
          "internalType": "address",
          "name": "agent",
          "type": "address"
        }
      ],
      "name": "AiAgentRemoved",
      "type": "event"
    },
    {
      "anonymous": False,
      "inputs": [
        {
          "indexed": False,
          "internalType": "address",
          "name": "account",
          "type": "address"
        }
      ],
      "name": "Paused",
      "type": "event"
    },
    {
      "anonymous": False,
      "inputs": [
        {
          "indexed": True,
          "internalType": "address",
          "name": "employer",
          "type": "address"
        },
        {
          "indexed": True,
          "internalType": "address",
          "name": "payrollContract",
          "type": "address"
        }
      ],
      "name": "PayrollContractCreated",
      "type": "event"
    },
    {
      "anonymous": False,
      "inputs": [
        {
          "indexed": True,
          "internalType": "address",
          "name": "employer",
          "type": "address"
        },
        {
          "indexed": True,
          "internalType": "address",
          "name": "payrollContract",
          "type": "address"
        }
      ],
      "name": "PayrollContractUpdated",
      "type": "event"
    },
    {
      "anonymous": False,
      "inputs": [
        {
          "indexed": True,
          "internalType": "bytes32",
          "name": "role",
          "type": "bytes32"
        },
        {
          "indexed": True,
          "internalType": "bytes32",
          "name": "previousAdminRole",
          "type": "bytes32"
        },
        {
          "indexed": True,
          "internalType": "bytes32",
          "name": "newAdminRole",
          "type": "bytes32"
        }
      ],
      "name": "RoleAdminChanged",
      "type": "event"
    },
    {
      "anonymous": False,
      "inputs": [
        {
          "indexed": True,
          "internalType": "bytes32",
          "name": "role",
          "type": "bytes32"
        },
        {
          "indexed": True,
          "internalType": "address",
          "name": "account",
          "type": "address"
        },
        {
          "indexed": True,
          "internalType": "address",
          "name": "sender",
          "type": "address"
        }
      ],
      "name": "RoleGranted",
      "type": "event"
    },
    {
      "anonymous": False,
      "inputs": [
        {
          "indexed": True,
          "internalType": "bytes32",
          "name": "role",
          "type": "bytes32"
        },
        {
          "indexed": True,
          "internalType": "address",
          "name": "account",
          "type": "address"
        },
        {
          "indexed": True,
          "internalType": "address",
          "name": "sender",
          "type": "address"
        }
      ],
      "name": "RoleRevoked",
      "type": "event"
    },
    {
      "anonymous": False,
      "inputs": [
        {
          "indexed": False,
          "internalType": "address",
          "name": "account",
          "type": "address"
        }
      ],
      "name": "Unpaused",
      "type": "event"
    },
    {
      "inputs": [],
      "name": "DEFAULT_ADMIN_ROLE",
      "outputs": [
        {
          "internalType": "bytes32",
          "name": "",
          "type": "bytes32"
        }
      ],
      "stateMutability": "view",
      "type": "function"
    },
    {
      "inputs": [
        {
          "internalType": "address",
          "name": "agent",
          "type": "address"
        }
      ],
      "name": "addAiAgent",
      "outputs": [],
      "stateMutability": "nonpayable",
      "type": "function"
    },
    {
      "inputs": [
        {
          "internalType": "uint256",
          "name": "",
          "type": "uint256"
        }
      ],
      "name": "allPayrollContracts",
      "outputs": [
        {
          "internalType": "address",
          "name": "",
          "type": "address"
        }
      ],
      "stateMutability": "view",
      "type": "function"
    },
    {
      "inputs": [],
      "name": "createPayrollContract",
      "outputs": [
        {
          "internalType": "address",
          "name": "payrollContract",
          "type": "address"
        }
      ],
      "stateMutability": "nonpayable",
      "type": "function"
    },
    {
      "inputs": [],
      "name": "getAllPayrollContracts",
      "outputs": [
        {
          "internalType": "address[]",
          "name": "",
          "type": "address[]"
        }
      ],
      "stateMutability": "view",
      "type": "function"
    },
    {
      "inputs": [],
      "name": "getAllPayrollContractsWithEmployers",
      "outputs": [
        {
          "internalType": "address[]",
          "name": "employers",
          "type": "address[]"
        },
        {
          "internalType": "address[]",
          "name": "contracts",
          "type": "address[]"
        }
      ],
      "stateMutability": "view",
      "type": "function"
    },
    {
      "inputs": [
        {
          "internalType": "address",
          "name": "_employer",
          "type": "address"
        },
        {
          "internalType": "address",
          "name": "_employeeAddress",
          "type": "address"
        }
      ],
      "name": "getEmployeeDetails",
      "outputs": [
        {
          "internalType": "address",
          "name": "employeeAddress",
          "type": "address"
        },
        {
          "internalType": "string",
          "name": "name",
          "type": "string"
        },
        {
          "internalType": "uint256",
          "name": "salary",
          "type": "uint256"
        },
        {
          "internalType": "uint256",
          "name": "joiningDate",
          "type": "uint256"
        },
        {
          "internalType": "bool",
          "name": "isActive",
          "type": "bool"
        }
      ],
      "stateMutability": "view",
      "type": "function"
    },
    {
      "inputs": [
        {
          "internalType": "address",
          "name": "employer",
          "type": "address"
        }
      ],
      "name": "getEmployerPayrollDetails",
      "outputs": [
        {
          "internalType": "address[]",
          "name": "contracts",
          "type": "address[]"
        },
        {
          "components": [
            {
              "internalType": "uint256",
              "name": "totalEmployees",
              "type": "uint256"
            },
            {
              "internalType": "uint256",
              "name": "totalLiability",
              "type": "uint256"
            },
            {
              "internalType": "uint256",
              "name": "currentBalance",
              "type": "uint256"
            }
          ],
          "internalType": "struct RikaManagement.PayrollDetails[]",
          "name": "details",
          "type": "tuple[]"
        }
      ],
      "stateMutability": "view",
      "type": "function"
    },
    {
      "inputs": [
        {
          "internalType": "address",
          "name": "employer",
          "type": "address"
        }
      ],
      "name": "getEmployerPayrolls",
      "outputs": [
        {
          "internalType": "address[]",
          "name": "",
          "type": "address[]"
        }
      ],
      "stateMutability": "view",
      "type": "function"
    },
    {
      "inputs": [
        {
          "internalType": "bytes32",
          "name": "role",
          "type": "bytes32"
        }
      ],
      "name": "getRoleAdmin",
      "outputs": [
        {
          "internalType": "bytes32",
          "name": "",
          "type": "bytes32"
        }
      ],
      "stateMutability": "view",
      "type": "function"
    },
    {
      "inputs": [
        {
          "internalType": "address",
          "name": "_employer",
          "type": "address"
        }
      ],
      "name": "getTotalEmployees",
      "outputs": [
        {
          "internalType": "uint256",
          "name": "total",
          "type": "uint256"
        }
      ],
      "stateMutability": "view",
      "type": "function"
    },
    {
      "inputs": [
        {
          "internalType": "bytes32",
          "name": "role",
          "type": "bytes32"
        },
        {
          "internalType": "address",
          "name": "account",
          "type": "address"
        }
      ],
      "name": "grantRole",
      "outputs": [],
      "stateMutability": "nonpayable",
      "type": "function"
    },
    {
      "inputs": [
        {
          "internalType": "bytes32",
          "name": "role",
          "type": "bytes32"
        },
        {
          "internalType": "address",
          "name": "account",
          "type": "address"
        }
      ],
      "name": "hasRole",
      "outputs": [
        {
          "internalType": "bool",
          "name": "",
          "type": "bool"
        }
      ],
      "stateMutability": "view",
      "type": "function"
    },
    {
      "inputs": [],
      "name": "implementationContract",
      "outputs": [
        {
          "internalType": "address",
          "name": "",
          "type": "address"
        }
      ],
      "stateMutability": "view",
      "type": "function"
    },
    {
      "inputs": [
        {
          "internalType": "address",
          "name": "contractAddress",
          "type": "address"
        }
      ],
      "name": "isValidPayrollContract",
      "outputs": [
        {
          "internalType": "bool",
          "name": "",
          "type": "bool"
        }
      ],
      "stateMutability": "view",
      "type": "function"
    },
    {
      "inputs": [],
      "name": "pause",
      "outputs": [],
      "stateMutability": "nonpayable",
      "type": "function"
    },
    {
      "inputs": [],
      "name": "paused",
      "outputs": [
        {
          "internalType": "bool",
          "name": "",
          "type": "bool"
        }
      ],
      "stateMutability": "view",
      "type": "function"
    },
    {
      "inputs": [
        {
          "internalType": "address",
          "name": "agent",
          "type": "address"
        }
      ],
      "name": "removeAiAgent",
      "outputs": [],
      "stateMutability": "nonpayable",
      "type": "function"
    },
    {
      "inputs": [
        {
          "internalType": "bytes32",
          "name": "role",
          "type": "bytes32"
        },
        {
          "internalType": "address",
          "name": "callerConfirmation",
          "type": "address"
        }
      ],
      "name": "renounceRole",
      "outputs": [],
      "stateMutability": "nonpayable",
      "type": "function"
    },
    {
      "inputs": [
        {
          "internalType": "bytes32",
          "name": "role",
          "type": "bytes32"
        },
        {
          "internalType": "address",
          "name": "account",
          "type": "address"
        }
      ],
      "name": "revokeRole",
      "outputs": [],
      "stateMutability": "nonpayable",
      "type": "function"
    },
    {
      "inputs": [
        {
          "internalType": "bytes4",
          "name": "interfaceId",
          "type": "bytes4"
        }
      ],
      "name": "supportsInterface",
      "outputs": [
        {
          "internalType": "bool",
          "name": "",
          "type": "bool"
        }
      ],
      "stateMutability": "view",
      "type": "function"
    },
    {
      "inputs": [],
      "name": "unpause",
      "outputs": [],
      "stateMutability": "nonpayable",
      "type": "function"
    },
    {
      "inputs": [],
      "name": "usdcToken",
      "outputs": [
        {
          "internalType": "address",
          "name": "",
          "type": "address"
        }
      ],
      "stateMutability": "view",
      "type": "function"
    }
  ]

RIKA_MANAGEMENT_ABI = [
    {
      "inputs": [],
      "name": "AccessControlBadConfirmation",
      "type": "error"
    },
    {
      "inputs": [
        {
          "internalType": "address",
          "name": "account",
          "type": "address"
        },
        {
          "internalType": "bytes32",
          "name": "neededRole",
          "type": "bytes32"
        }
      ],
      "name": "AccessControlUnauthorizedAccount",
      "type": "error"
    },
    {
      "inputs": [],
      "name": "AlreadyInitialized",
      "type": "error"
    },
    {
      "inputs": [],
      "name": "ArrayLengthMismatch",
      "type": "error"
    },
    {
      "inputs": [],
      "name": "EmployeeAlreadyExists",
      "type": "error"
    },
    {
      "inputs": [],
      "name": "EmployeeNotFound",
      "type": "error"
    },
    {
      "inputs": [],
      "name": "EnforcedPause",
      "type": "error"
    },
    {
      "inputs": [],
      "name": "ExpectedPause",
      "type": "error"
    },
    {
      "inputs": [],
      "name": "InsufficientAllowance",
      "type": "error"
    },
    {
      "inputs": [],
      "name": "InsufficientBalance",
      "type": "error"
    },
    {
      "inputs": [],
      "name": "InvalidAddress",
      "type": "error"
    },
    {
      "inputs": [],
      "name": "InvalidInitAddress",
      "type": "error"
    },
    {
      "inputs": [],
      "name": "InvalidSchedule",
      "type": "error"
    },
    {
      "inputs": [],
      "name": "OverlappingSchedule",
      "type": "error"
    },
    {
      "inputs": [],
      "name": "PayrollAlreadyProcessed",
      "type": "error"
    },
    {
      "inputs": [
        {
          "internalType": "address",
          "name": "token",
          "type": "address"
        }
      ],
      "name": "SafeERC20FailedOperation",
      "type": "error"
    },
    {
      "inputs": [],
      "name": "ScheduleNotCompleted",
      "type": "error"
    },
    {
      "inputs": [],
      "name": "TransferFailed",
      "type": "error"
    },
    {
      "inputs": [],
      "name": "UnauthorizedAccess",
      "type": "error"
    },
    {
      "inputs": [
        {
          "internalType": "uint256",
          "name": "nextPayrollDate",
          "type": "uint256"
        }
      ],
      "name": "WithdrawalLocked",
      "type": "error"
    },
    {
      "inputs": [],
      "name": "ZeroAmount",
      "type": "error"
    },
    {
      "anonymous": False,
      "inputs": [
        {
          "indexed": True,
          "internalType": "address",
          "name": "employer",
          "type": "address"
        },
        {
          "indexed": True,
          "internalType": "address",
          "name": "employeeAddress",
          "type": "address"
        },
        {
          "indexed": False,
          "internalType": "string",
          "name": "name",
          "type": "string"
        }
      ],
      "name": "EmployeeAdded",
      "type": "event"
    },
    {
      "anonymous": False,
      "inputs": [
        {
          "indexed": True,
          "internalType": "address",
          "name": "employer",
          "type": "address"
        },
        {
          "indexed": True,
          "internalType": "address",
          "name": "employeeAddress",
          "type": "address"
        }
      ],
      "name": "EmployeeDeactivated",
      "type": "event"
    },
    {
      "anonymous": False,
      "inputs": [
        {
          "indexed": True,
          "internalType": "address",
          "name": "employer",
          "type": "address"
        },
        {
          "indexed": True,
          "internalType": "address",
          "name": "employeeAddress",
          "type": "address"
        }
      ],
      "name": "EmployeeReactivated",
      "type": "event"
    },
    {
      "anonymous": False,
      "inputs": [
        {
          "indexed": True,
          "internalType": "address",
          "name": "employer",
          "type": "address"
        },
        {
          "indexed": True,
          "internalType": "address",
          "name": "employeeAddress",
          "type": "address"
        }
      ],
      "name": "EmployeeUpdated",
      "type": "event"
    },
    {
      "anonymous": False,
      "inputs": [
        {
          "indexed": True,
          "internalType": "address",
          "name": "employer",
          "type": "address"
        },
        {
          "indexed": False,
          "internalType": "string[]",
          "name": "names",
          "type": "string[]"
        },
        {
          "indexed": False,
          "internalType": "address[]",
          "name": "employeeAddresses",
          "type": "address[]"
        },
        {
          "indexed": False,
          "internalType": "uint256[]",
          "name": "salaries",
          "type": "uint256[]"
        }
      ],
      "name": "EmployeesAddedBatch",
      "type": "event"
    },
    {
      "anonymous": False,
      "inputs": [
        {
          "indexed": True,
          "internalType": "address",
          "name": "employer",
          "type": "address"
        },
        {
          "indexed": False,
          "internalType": "uint256",
          "name": "amount",
          "type": "uint256"
        }
      ],
      "name": "FundsAdded",
      "type": "event"
    },
    {
      "anonymous": False,
      "inputs": [
        {
          "indexed": True,
          "internalType": "address",
          "name": "employer",
          "type": "address"
        },
        {
          "indexed": False,
          "internalType": "uint256",
          "name": "amount",
          "type": "uint256"
        }
      ],
      "name": "FundsWithdrawn",
      "type": "event"
    },
    {
      "anonymous": False,
      "inputs": [
        {
          "indexed": False,
          "internalType": "address",
          "name": "account",
          "type": "address"
        }
      ],
      "name": "Paused",
      "type": "event"
    },
    {
      "anonymous": False,
      "inputs": [
        {
          "indexed": True,
          "internalType": "address",
          "name": "employer",
          "type": "address"
        },
        {
          "indexed": False,
          "internalType": "uint256",
          "name": "totalPayout",
          "type": "uint256"
        },
        {
          "indexed": False,
          "internalType": "uint256",
          "name": "timestamp",
          "type": "uint256"
        }
      ],
      "name": "PayrollProcessed",
      "type": "event"
    },
    {
      "anonymous": False,
      "inputs": [
        {
          "indexed": True,
          "internalType": "bytes32",
          "name": "role",
          "type": "bytes32"
        },
        {
          "indexed": True,
          "internalType": "bytes32",
          "name": "previousAdminRole",
          "type": "bytes32"
        },
        {
          "indexed": True,
          "internalType": "bytes32",
          "name": "newAdminRole",
          "type": "bytes32"
        }
      ],
      "name": "RoleAdminChanged",
      "type": "event"
    },
    {
      "anonymous": False,
      "inputs": [
        {
          "indexed": True,
          "internalType": "bytes32",
          "name": "role",
          "type": "bytes32"
        },
        {
          "indexed": True,
          "internalType": "address",
          "name": "account",
          "type": "address"
        },
        {
          "indexed": True,
          "internalType": "address",
          "name": "sender",
          "type": "address"
        }
      ],
      "name": "RoleGranted",
      "type": "event"
    },
    {
      "anonymous": False,
      "inputs": [
        {
          "indexed": True,
          "internalType": "bytes32",
          "name": "role",
          "type": "bytes32"
        },
        {
          "indexed": True,
          "internalType": "address",
          "name": "account",
          "type": "address"
        },
        {
          "indexed": True,
          "internalType": "address",
          "name": "sender",
          "type": "address"
        }
      ],
      "name": "RoleRevoked",
      "type": "event"
    },
    {
      "anonymous": False,
      "inputs": [
        {
          "indexed": True,
          "internalType": "address",
          "name": "employer",
          "type": "address"
        },
        {
          "indexed": False,
          "internalType": "address[]",
          "name": "employeeAddresses",
          "type": "address[]"
        },
        {
          "indexed": False,
          "internalType": "uint256[]",
          "name": "newSalaries",
          "type": "uint256[]"
        }
      ],
      "name": "SalariesUpdatedBatch",
      "type": "event"
    },
    {
      "anonymous": False,
      "inputs": [
        {
          "indexed": True,
          "internalType": "address",
          "name": "employer",
          "type": "address"
        },
        {
          "indexed": True,
          "internalType": "address",
          "name": "employeeAddress",
          "type": "address"
        },
        {
          "indexed": False,
          "internalType": "uint256",
          "name": "amount",
          "type": "uint256"
        }
      ],
      "name": "SalaryPaid",
      "type": "event"
    },
    {
      "anonymous": False,
      "inputs": [
        {
          "indexed": True,
          "internalType": "address",
          "name": "employer",
          "type": "address"
        },
        {
          "indexed": True,
          "internalType": "address",
          "name": "employeeAddress",
          "type": "address"
        },
        {
          "indexed": False,
          "internalType": "uint256",
          "name": "scheduleId",
          "type": "uint256"
        },
        {
          "indexed": False,
          "internalType": "uint256",
          "name": "startDate",
          "type": "uint256"
        },
        {
          "indexed": False,
          "internalType": "uint256",
          "name": "endDate",
          "type": "uint256"
        },
        {
          "indexed": False,
          "internalType": "enum RikaManagement.Interval",
          "name": "interval",
          "type": "uint8"
        }
      ],
      "name": "ScheduleCreated",
      "type": "event"
    },
    {
      "anonymous": False,
      "inputs": [
        {
          "indexed": True,
          "internalType": "address",
          "name": "employer",
          "type": "address"
        },
        {
          "indexed": True,
          "internalType": "address",
          "name": "employeeAddress",
          "type": "address"
        },
        {
          "indexed": False,
          "internalType": "uint256",
          "name": "scheduleId",
          "type": "uint256"
        },
        {
          "indexed": False,
          "internalType": "enum RikaManagement.Interval",
          "name": "interval",
          "type": "uint8"
        }
      ],
      "name": "ScheduleDeactivated",
      "type": "event"
    },
    {
      "anonymous": False,
      "inputs": [
        {
          "indexed": True,
          "internalType": "address",
          "name": "employer",
          "type": "address"
        },
        {
          "indexed": True,
          "internalType": "address",
          "name": "employeeAddress",
          "type": "address"
        },
        {
          "indexed": False,
          "internalType": "uint256",
          "name": "scheduleId",
          "type": "uint256"
        },
        {
          "indexed": False,
          "internalType": "enum RikaManagement.Interval",
          "name": "interval",
          "type": "uint8"
        }
      ],
      "name": "ScheduleReactivated",
      "type": "event"
    },
    {
      "anonymous": False,
      "inputs": [
        {
          "indexed": True,
          "internalType": "address",
          "name": "employer",
          "type": "address"
        },
        {
          "indexed": True,
          "internalType": "address",
          "name": "employeeAddress",
          "type": "address"
        },
        {
          "indexed": False,
          "internalType": "uint256",
          "name": "scheduleId",
          "type": "uint256"
        },
        {
          "indexed": False,
          "internalType": "enum RikaManagement.Interval",
          "name": "interval",
          "type": "uint8"
        }
      ],
      "name": "ScheduleUpdated",
      "type": "event"
    },
    {
      "anonymous": False,
      "inputs": [
        {
          "indexed": False,
          "internalType": "address",
          "name": "account",
          "type": "address"
        }
      ],
      "name": "Unpaused",
      "type": "event"
    },
    {
      "inputs": [],
      "name": "AI_AGENT_ROLE",
      "outputs": [
        {
          "internalType": "bytes32",
          "name": "",
          "type": "bytes32"
        }
      ],
      "stateMutability": "view",
      "type": "function"
    },
    {
      "inputs": [],
      "name": "DEFAULT_ADMIN_ROLE",
      "outputs": [
        {
          "internalType": "bytes32",
          "name": "",
          "type": "bytes32"
        }
      ],
      "stateMutability": "view",
      "type": "function"
    },
    {
      "inputs": [],
      "name": "EMPLOYER_ROLE",
      "outputs": [
        {
          "internalType": "bytes32",
          "name": "",
          "type": "bytes32"
        }
      ],
      "stateMutability": "view",
      "type": "function"
    },
    {
      "inputs": [
        {
          "internalType": "address",
          "name": "agent",
          "type": "address"
        }
      ],
      "name": "addAiAgent",
      "outputs": [],
      "stateMutability": "nonpayable",
      "type": "function"
    },
    {
      "inputs": [
        {
          "internalType": "string",
          "name": "_name",
          "type": "string"
        },
        {
          "internalType": "address",
          "name": "_employeeAddress",
          "type": "address"
        },
        {
          "internalType": "uint256",
          "name": "_salary",
          "type": "uint256"
        }
      ],
      "name": "addEmployee",
      "outputs": [],
      "stateMutability": "nonpayable",
      "type": "function"
    },
    {
      "inputs": [
        {
          "internalType": "string[]",
          "name": "_names",
          "type": "string[]"
        },
        {
          "internalType": "address[]",
          "name": "_employeeAddresses",
          "type": "address[]"
        },
        {
          "internalType": "uint256[]",
          "name": "_salaries",
          "type": "uint256[]"
        }
      ],
      "name": "addEmployeesBatch",
      "outputs": [],
      "stateMutability": "nonpayable",
      "type": "function"
    },
    {
      "inputs": [
        {
          "internalType": "uint256",
          "name": "_amount",
          "type": "uint256"
        }
      ],
      "name": "addFunds",
      "outputs": [],
      "stateMutability": "nonpayable",
      "type": "function"
    },
    {
      "inputs": [
        {
          "internalType": "address",
          "name": "_employeeAddress",
          "type": "address"
        },
        {
          "internalType": "uint256",
          "name": "_startDate",
          "type": "uint256"
        },
        {
          "internalType": "uint256",
          "name": "_endDate",
          "type": "uint256"
        },
        {
          "internalType": "enum RikaManagement.Interval",
          "name": "_interval",
          "type": "uint8"
        }
      ],
      "name": "createSchedule",
      "outputs": [],
      "stateMutability": "nonpayable",
      "type": "function"
    },
    {
      "inputs": [
        {
          "internalType": "address",
          "name": "_employeeAddress",
          "type": "address"
        }
      ],
      "name": "deactivateEmployee",
      "outputs": [],
      "stateMutability": "nonpayable",
      "type": "function"
    },
    {
      "inputs": [
        {
          "internalType": "address",
          "name": "_employeeAddress",
          "type": "address"
        },
        {
          "internalType": "uint256",
          "name": "_scheduleId",
          "type": "uint256"
        }
      ],
      "name": "deactivateSchedule",
      "outputs": [],
      "stateMutability": "nonpayable",
      "type": "function"
    },
    {
      "inputs": [
        {
          "internalType": "address",
          "name": "_employer",
          "type": "address"
        }
      ],
      "name": "getAllEmployeesWithDetails",
      "outputs": [
        {
          "components": [
            {
              "internalType": "address",
              "name": "employeeAddress",
              "type": "address"
            },
            {
              "internalType": "string",
              "name": "name",
              "type": "string"
            },
            {
              "internalType": "uint256",
              "name": "salary",
              "type": "uint256"
            },
            {
              "internalType": "uint256",
              "name": "joiningDate",
              "type": "uint256"
            },
            {
              "internalType": "bool",
              "name": "isActive",
              "type": "bool"
            }
          ],
          "internalType": "struct RikaManagement.Employee[]",
          "name": "",
          "type": "tuple[]"
        }
      ],
      "stateMutability": "view",
      "type": "function"
    },
    {
      "inputs": [
        {
          "internalType": "address",
          "name": "employer",
          "type": "address"
        },
        {
          "internalType": "address",
          "name": "employee",
          "type": "address"
        }
      ],
      "name": "getEmployee",
      "outputs": [
        {
          "components": [
            {
              "internalType": "address",
              "name": "employeeAddress",
              "type": "address"
            },
            {
              "internalType": "string",
              "name": "name",
              "type": "string"
            },
            {
              "internalType": "uint256",
              "name": "salary",
              "type": "uint256"
            },
            {
              "internalType": "uint256",
              "name": "joiningDate",
              "type": "uint256"
            },
            {
              "internalType": "bool",
              "name": "isActive",
              "type": "bool"
            }
          ],
          "internalType": "struct RikaManagement.Employee",
          "name": "",
          "type": "tuple"
        }
      ],
      "stateMutability": "view",
      "type": "function"
    },
    {
      "inputs": [
        {
          "internalType": "address",
          "name": "_employer",
          "type": "address"
        },
        {
          "internalType": "address",
          "name": "_employeeAddress",
          "type": "address"
        }
      ],
      "name": "getEmployeeDetails",
      "outputs": [
        {
          "internalType": "address",
          "name": "employeeAddress",
          "type": "address"
        },
        {
          "internalType": "string",
          "name": "name",
          "type": "string"
        },
        {
          "internalType": "uint256",
          "name": "salary",
          "type": "uint256"
        },
        {
          "internalType": "uint256",
          "name": "joiningDate",
          "type": "uint256"
        },
        {
          "internalType": "bool",
          "name": "isActive",
          "type": "bool"
        }
      ],
      "stateMutability": "view",
      "type": "function"
    },
    {
      "inputs": [
        {
          "internalType": "address",
          "name": "_employer",
          "type": "address"
        },
        {
          "internalType": "address",
          "name": "_employeeAddress",
          "type": "address"
        },
        {
          "internalType": "string",
          "name": "_name",
          "type": "string"
        }
      ],
      "name": "getEmployeeDetailsByNameAndAddress",
      "outputs": [
        {
          "internalType": "address",
          "name": "employeeAddress",
          "type": "address"
        },
        {
          "internalType": "string",
          "name": "name",
          "type": "string"
        },
        {
          "internalType": "uint256",
          "name": "salary",
          "type": "uint256"
        },
        {
          "internalType": "uint256",
          "name": "joiningDate",
          "type": "uint256"
        },
        {
          "internalType": "bool",
          "name": "isActive",
          "type": "bool"
        }
      ],
      "stateMutability": "view",
      "type": "function"
    },
    {
      "inputs": [
        {
          "internalType": "address",
          "name": "employer",
          "type": "address"
        }
      ],
      "name": "getEmployeeList",
      "outputs": [
        {
          "internalType": "address[]",
          "name": "",
          "type": "address[]"
        }
      ],
      "stateMutability": "view",
      "type": "function"
    },
    {
      "inputs": [],
      "name": "getEmployer",
      "outputs": [
        {
          "internalType": "address",
          "name": "",
          "type": "address"
        }
      ],
      "stateMutability": "view",
      "type": "function"
    },
    {
      "inputs": [
        {
          "internalType": "address",
          "name": "_employer",
          "type": "address"
        }
      ],
      "name": "getEmployerBalance",
      "outputs": [
        {
          "internalType": "uint256",
          "name": "",
          "type": "uint256"
        }
      ],
      "stateMutability": "view",
      "type": "function"
    },
    {
      "inputs": [
        {
          "internalType": "address",
          "name": "_employer",
          "type": "address"
        },
        {
          "internalType": "address",
          "name": "_employeeAddress",
          "type": "address"
        }
      ],
      "name": "getNextPayrollDate",
      "outputs": [
        {
          "internalType": "uint256",
          "name": "nextPaymentDate",
          "type": "uint256"
        }
      ],
      "stateMutability": "view",
      "type": "function"
    },
    {
      "inputs": [
        {
          "internalType": "bytes32",
          "name": "role",
          "type": "bytes32"
        }
      ],
      "name": "getRoleAdmin",
      "outputs": [
        {
          "internalType": "bytes32",
          "name": "",
          "type": "bytes32"
        }
      ],
      "stateMutability": "view",
      "type": "function"
    },
    {
      "inputs": [
        {
          "internalType": "address",
          "name": "employer",
          "type": "address"
        },
        {
          "internalType": "address",
          "name": "employee",
          "type": "address"
        }
      ],
      "name": "getSchedules",
      "outputs": [
        {
          "components": [
            {
              "internalType": "uint256",
              "name": "scheduleId",
              "type": "uint256"
            },
            {
              "internalType": "uint256",
              "name": "startDate",
              "type": "uint256"
            },
            {
              "internalType": "uint256",
              "name": "endDate",
              "type": "uint256"
            },
            {
              "internalType": "enum RikaManagement.Interval",
              "name": "interval",
              "type": "uint8"
            },
            {
              "internalType": "uint256",
              "name": "lastProcessedDate",
              "type": "uint256"
            },
            {
              "internalType": "bool",
              "name": "isProcessed",
              "type": "bool"
            },
            {
              "internalType": "bool",
              "name": "isActive",
              "type": "bool"
            }
          ],
          "internalType": "struct RikaManagement.Schedule[]",
          "name": "",
          "type": "tuple[]"
        }
      ],
      "stateMutability": "view",
      "type": "function"
    },
    {
      "inputs": [
        {
          "internalType": "address",
          "name": "_employer",
          "type": "address"
        }
      ],
      "name": "getTotalEmployees",
      "outputs": [
        {
          "internalType": "uint256",
          "name": "",
          "type": "uint256"
        }
      ],
      "stateMutability": "view",
      "type": "function"
    },
    {
      "inputs": [
        {
          "internalType": "address",
          "name": "_employer",
          "type": "address"
        }
      ],
      "name": "getTotalPayrollLiability",
      "outputs": [
        {
          "internalType": "uint256",
          "name": "totalLiability",
          "type": "uint256"
        }
      ],
      "stateMutability": "view",
      "type": "function"
    },
    {
      "inputs": [
        {
          "internalType": "bytes32",
          "name": "role",
          "type": "bytes32"
        },
        {
          "internalType": "address",
          "name": "account",
          "type": "address"
        }
      ],
      "name": "grantRole",
      "outputs": [],
      "stateMutability": "nonpayable",
      "type": "function"
    },
    {
      "inputs": [
        {
          "internalType": "bytes32",
          "name": "role",
          "type": "bytes32"
        },
        {
          "internalType": "address",
          "name": "account",
          "type": "address"
        }
      ],
      "name": "hasRole",
      "outputs": [
        {
          "internalType": "bool",
          "name": "",
          "type": "bool"
        }
      ],
      "stateMutability": "view",
      "type": "function"
    },
    {
      "inputs": [
        {
          "internalType": "address",
          "name": "_employer",
          "type": "address"
        }
      ],
      "name": "hasSufficientBalanceForPayroll",
      "outputs": [
        {
          "internalType": "bool",
          "name": "",
          "type": "bool"
        }
      ],
      "stateMutability": "view",
      "type": "function"
    },
    {
      "inputs": [
        {
          "internalType": "address",
          "name": "_usdcToken",
          "type": "address"
        },
        {
          "internalType": "address",
          "name": "_employer",
          "type": "address"
        }
      ],
      "name": "initialize",
      "outputs": [],
      "stateMutability": "nonpayable",
      "type": "function"
    },
    {
      "inputs": [],
      "name": "paused",
      "outputs": [
        {
          "internalType": "bool",
          "name": "",
          "type": "bool"
        }
      ],
      "stateMutability": "view",
      "type": "function"
    },
    {
      "inputs": [],
      "name": "processAllPayrolls",
      "outputs": [],
      "stateMutability": "nonpayable",
      "type": "function"
    },
    {
      "inputs": [
        {
          "internalType": "address",
          "name": "_employeeAddress",
          "type": "address"
        }
      ],
      "name": "reactivateEmployee",
      "outputs": [],
      "stateMutability": "nonpayable",
      "type": "function"
    },
    {
      "inputs": [
        {
          "internalType": "address",
          "name": "_employeeAddress",
          "type": "address"
        },
        {
          "internalType": "uint256",
          "name": "_scheduleId",
          "type": "uint256"
        }
      ],
      "name": "reactivateSchedule",
      "outputs": [],
      "stateMutability": "nonpayable",
      "type": "function"
    },
    {
      "inputs": [
        {
          "internalType": "address",
          "name": "agent",
          "type": "address"
        }
      ],
      "name": "removeAiAgent",
      "outputs": [],
      "stateMutability": "nonpayable",
      "type": "function"
    },
    {
      "inputs": [
        {
          "internalType": "bytes32",
          "name": "role",
          "type": "bytes32"
        },
        {
          "internalType": "address",
          "name": "callerConfirmation",
          "type": "address"
        }
      ],
      "name": "renounceRole",
      "outputs": [],
      "stateMutability": "nonpayable",
      "type": "function"
    },
    {
      "inputs": [
        {
          "internalType": "bytes32",
          "name": "role",
          "type": "bytes32"
        },
        {
          "internalType": "address",
          "name": "account",
          "type": "address"
        }
      ],
      "name": "revokeRole",
      "outputs": [],
      "stateMutability": "nonpayable",
      "type": "function"
    },
    {
      "inputs": [
        {
          "internalType": "bytes4",
          "name": "interfaceId",
          "type": "bytes4"
        }
      ],
      "name": "supportsInterface",
      "outputs": [
        {
          "internalType": "bool",
          "name": "",
          "type": "bool"
        }
      ],
      "stateMutability": "view",
      "type": "function"
    },
    {
      "inputs": [
        {
          "internalType": "address",
          "name": "_employeeAddress",
          "type": "address"
        },
        {
          "internalType": "uint256",
          "name": "_newSalary",
          "type": "uint256"
        }
      ],
      "name": "updateEmployeeSalary",
      "outputs": [],
      "stateMutability": "nonpayable",
      "type": "function"
    },
    {
      "inputs": [
        {
          "internalType": "address[]",
          "name": "_employeeAddresses",
          "type": "address[]"
        },
        {
          "internalType": "uint256[]",
          "name": "_newSalaries",
          "type": "uint256[]"
        }
      ],
      "name": "updateSalariesBatch",
      "outputs": [],
      "stateMutability": "nonpayable",
      "type": "function"
    },
    {
      "inputs": [
        {
          "internalType": "address",
          "name": "_employeeAddress",
          "type": "address"
        },
        {
          "internalType": "uint256",
          "name": "_scheduleId",
          "type": "uint256"
        },
        {
          "internalType": "enum RikaManagement.Interval",
          "name": "_interval",
          "type": "uint8"
        }
      ],
      "name": "updateSchedule",
      "outputs": [],
      "stateMutability": "nonpayable",
      "type": "function"
    },
    {
      "inputs": [],
      "name": "usdcToken",
      "outputs": [
        {
          "internalType": "contract IERC20",
          "name": "",
          "type": "address"
        }
      ],
      "stateMutability": "view",
      "type": "function"
    },
    {
      "inputs": [
        {
          "internalType": "uint256",
          "name": "_amount",
          "type": "uint256"
        }
      ],
      "name": "withdrawFunds",
      "outputs": [],
      "stateMutability": "nonpayable",
      "type": "function"
    }
  ]