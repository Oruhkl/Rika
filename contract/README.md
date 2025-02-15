# Rika Payroll System

A decentralized payroll management system built with Solidity that enables companies to manage employee payroll using USDC tokens.

## Contracts Deployed

- **RUSDC**: [0xdB58fAF32AD9A22c8705F789b7b36B6fBfb5f5Ad](https://testnet.sonicscan.org/address/0xdB58fAF32AD9A22c8705F789b7b36B6fBfb5f5Ad#code)

- **RUSDCFaucet**: [0x33fcd38fD7339414D46AC2bd9f16620d836005A6](https://testnet.sonicscan.org/address/0x33fcd38fD7339414D46AC2bd9f16620d836005A6#code)

- **RikaManagement Implementation**: [0xC1F72FFCF59E0DeFD645DDAe8762318486a0c2d1](https://testnet.sonicscan.org/address/0xC1F72FFCF59E0DeFD645DDAe8762318486a0c2d1#code)

- **RikaFactory**: [0x11adB1411296FBC480Cd17E86e76EC00Ac006B7A](https://testnet.sonicscan.org/address/0x11adB1411296FBC480Cd17E86e76EC00Ac006B7A#code)

## Contract Details

### RikaFactory
- Creates and manages RikaManagement contracts for employers
- Limits employers to maximum 3 payroll contracts
- Maintains registry of deployed contracts
- Controls AI agent role assignments
- Provides administrative functions for pausing/unpausing contracts
- Includes comprehensive view functions for employer and employee data

Key features:
- Role-based access control (DEFAULT_ADMIN_ROLE)
- Contract deployment limits
- AI agent integration
- Contract registry and validation
- Minimal proxy pattern implementation
- USDC token integration

### RikaManagement
- Handles complete employee lifecycle management
- Processes payroll through schedules and intervals
- Manages employer funds and salary payments
- Implements role-based access (DEFAULT_ADMIN_ROLE, EMPLOYER_ROLE, AI_AGENT_ROLE)

Key features:
- Employee management (add, update, deactivate)
- Schedule creation and processing
- Weekly, bi-weekly, and monthly payment intervals
- Fund management (deposits/withdrawals)
- Withdrawal lock periods (3 days before next payroll)
- Comprehensive reporting functions
- Pausable operations
- AI agent integration for automated processing
- Safe USDC token handling

## Technical Features

- Built with OpenZeppelin's AccessControl and Pausable
- Uses SafeERC20 for token transfers
- Custom error handling
- Comprehensive event logging
- View functions for transparency
- Multi-role authorization system
- Modular contract architecture

## Security Features

- Role-based access control
- Pausable functionality
- Fund withdrawal restrictions
- Balance and allowance checks
- Input validation
- Employer approval system
- Contract validation checks
- Safe token handling

## Integration Points

- USDC token integration
- AI agent capabilities
- Factory-managed deployment
- Cross-contract communication
- Event-driven updates

## Prerequisites

- Node.js v14.x or v16.x
- Hardhat
- Sonic Testnet account with funds

## Setup

1. Clone the repository:
    
    git clone https://github.com/your-repo/rika-payroll-system.git
    cd rika-payroll-system
    

2. Install dependencies:
    
    npm install
    

3. Create a [`.env`](.env ) file and add your Sonic Testnet private key and API key:
    
    PRIVATE_KEY=your_private_key
    SONIC_API_KEY=your_api_key
    SONIC_RPC_URL=https://rpc.soniclabs.com
    
## Testing
To run the tests, use:

npx hardhat test


## Deployment

To deploy the contracts to the Sonic Testnet, run:

npx hardhat run scripts/deploy.js --network sonicTestnet


## License
This project is licensed under the MIT License.
