const hre = require("hardhat");

async function main() {
  const [deployer] = await ethers.getSigners();
  console.log("Deploying contracts with account:", deployer.address);

  // Deploy RUSDC
  const RUSDC = await ethers.getContractFactory("RUSDC");
  const rusdc = await RUSDC.deploy();
  await rusdc.waitForDeployment();
  console.log("RUSDC deployed to:", await rusdc.getAddress());

  // Deploy RUSDCFaucet
  const RUSDCFaucet = await ethers.getContractFactory("RUSDCFaucet");
  const faucet = await RUSDCFaucet.deploy(await rusdc.getAddress());
  await faucet.waitForDeployment();
  console.log("RUSDCFaucet deployed to:", await faucet.getAddress());

  // Fund the faucet with initial RUSDC
  const fundTx = await rusdc.transfer(await faucet.getAddress(), ethers.parseUnits("100000", 6));
  await fundTx.wait();
  console.log("Funded faucet with 100,000 RUSDC");

  // Deploy RikaManagement implementation first
  const RikaManagement = await ethers.getContractFactory("RikaManagement");
  const implementation = await RikaManagement.deploy();
  await implementation.waitForDeployment();
  console.log("RikaManagement implementation deployed to:", await implementation.getAddress());

  // Deploy RikaFactory with implementation and RUSDC addresses
  const RikaFactory = await ethers.getContractFactory("RikaFactory");
  const factory = await RikaFactory.deploy(await implementation.getAddress(), await rusdc.getAddress());
  await factory.waitForDeployment();
  console.log("RikaFactory deployed to:", await factory.getAddress());

  // Wait for block confirmations
  await new Promise(resolve => setTimeout(resolve, 30000));

  // Verify RUSDC
  await hre.run("verify:verify", {
    address: await rusdc.getAddress(),
    constructorArguments: []
  });

  // Verify RUSDCFaucet
  await hre.run("verify:verify", {
    address: await faucet.getAddress(),
    constructorArguments: [await rusdc.getAddress()]
  });

  // Verify RikaManagement
  await hre.run("verify:verify", {
    address: await implementation.getAddress(),
    constructorArguments: []
  });

  // Verify RikaFactory
  await hre.run("verify:verify", {
    address: await factory.getAddress(),
    constructorArguments: [await implementation.getAddress(), await rusdc.getAddress()]
  });
}

main()
  .then(() => process.exit(0))
  .catch((error) => {
    console.error(error);
    process.exit(1);
  });
