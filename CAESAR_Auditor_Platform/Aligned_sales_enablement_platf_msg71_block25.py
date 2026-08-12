// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import "@openzeppelin/contracts/token/ERC20/ERC20.sol";
import "@openzeppelin/contracts/token/ERC20/extensions/ERC20Burnable.sol";
import "@openzeppelin/contracts/access/AccessControl.sol";

/**
 * @title HAULToken
 * @dev Utility token for platform rewards and payments
 * Inflationary with burn mechanisms for sustainability
 */
contract HAULToken is ERC20, ERC20Burnable, AccessControl {
    
    bytes32 public constant MINTER_ROLE = keccak256("MINTER_ROLE");
    bytes32 public constant BURNER_ROLE = keccak256("BURNER_ROLE");
    
    // Inflation control
    uint256 public inflationRate = 15; // 15% annual, decreases over time
    uint256 public lastInflationUpdate;
    uint256 public constant SECONDS_PER_YEAR = 365 days;
    
    // Rewards tracking
    mapping(address => uint256) public totalEarned;
    mapping(address => uint256) public totalSpent;
    
    // Activity multipliers
    mapping(address => uint256) public activityMultiplier; // 1x to 3x based on engagement
    
    // Events
    event TokensMinted(address indexed to, uint256 amount, string reason);
    event TokensBurned(address indexed from, uint256 amount, string reason);
    event InflationRateUpdated(uint256 newRate);
    event MultiplierUpdated(address indexed user, uint256 multiplier);
    
    constructor() ERC20("HAUL Utility Token", "HAUL") {
        _grantRole(DEFAULT_ADMIN_ROLE, msg.sender);
        _grantRole(MINTER_ROLE, msg.sender);
        _grantRole(BURNER_ROLE, msg.sender);
        
        // Initial supply: 100M tokens
        _mint(msg.sender, 100_000_000 * 10**18);
        lastInflationUpdate = block.timestamp;
    }
    
    /**
     * @dev Mint new tokens as rewards (controlled inflation)
     * @param to Recipient address
     * @param amount Amount to mint
     * @param reason Description of reward
     */
    function mintReward(
        address to,
        uint256 amount,
        string memory reason
    ) external onlyRole(MINTER_ROLE) {
        require(to != address(0), "Invalid address");
        
        // Apply activity multiplier (1x to 3x)
        uint256 multiplier = activityMultiplier[to];
        if (multiplier == 0) multiplier = 100; // Default 1x (100%)
        
        uint256 finalAmount = (amount * multiplier) / 100;
        
        _mint(to, finalAmount);
        totalEarned[to] += finalAmount;
        
        emit TokensMinted(to, finalAmount, reason);
    }
    
    /**
     * @dev Burn tokens when spent on platform
     * @param from User spending tokens
     * @param amount Amount to burn
     * @param reason What the tokens were spent on
     */
    function burnForUtility(
        address from,
        uint256 amount,
        string memory reason
    ) external onlyRole(BURNER_ROLE) {
        require(balanceOf(from) >= amount, "Insufficient balance");
        
        _burn(from, amount);
        totalSpent[from] += amount;
        
        emit TokensBurned(from, amount, reason);
    }
    
    /**
     * @dev Update user's activity multiplier based on engagement
     * @param user Address of user
     * @param multiplier New multiplier (100 = 1x, 200 = 2x, 300 = 3x)
     */
    function updateMultiplier(
        address user,
        uint256 multiplier
    ) external onlyRole(DEFAULT_ADMIN_ROLE) {
        require(multiplier >= 100 && multiplier <= 300, "Invalid multiplier");
        activityMultiplier[user] = multiplier;
        emit MultiplierUpdated(user, multiplier);
    }
    
    /**
     * @dev Decrease inflation rate annually (15% -> 14% -> ... -> 5% floor)
     */
    function decreaseInflation() external {
        require(
            block.timestamp >= lastInflationUpdate + SECONDS_PER_YEAR,
            "Too early"
        );
        
        if (inflationRate > 5) {
            inflationRate -= 1;
            lastInflationUpdate = block.timestamp;
            emit InflationRateUpdated(inflationRate);
        }
    }
    
    /**
     * @dev Get user's net token position (earned - spent)
     */
    function netPosition(address user) external view returns (int256) {
        return int256(totalEarned[user]) - int256(totalSpent[user]);
    }
}