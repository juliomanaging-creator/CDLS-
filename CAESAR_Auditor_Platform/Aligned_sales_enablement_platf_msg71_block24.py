// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import "@openzeppelin/contracts/token/ERC20/ERC20.sol";
import "@openzeppelin/contracts/token/ERC20/extensions/ERC20Burnable.sol";
import "@openzeppelin/contracts/token/ERC20/extensions/ERC20Snapshot.sol";
import "@openzeppelin/contracts/access/Ownable.sol";
import "@openzeppelin/contracts/security/Pausable.sol";

/**
 * @title CDLSToken
 * @dev CDLS governance and equity token with snapshot and burn capabilities
 */
contract CDLSToken is ERC20, ERC20Burnable, ERC20Snapshot, Ownable, Pausable {
    
    // Maximum supply: 1 billion tokens
    uint256 public constant MAX_SUPPLY = 1_000_000_000 * 10**18;
    
    // Addresses for token distribution
    address public treasuryAddress;
    address public stakingContract;
    address public vestingContract;
    
    // Revenue share tracking
    mapping(address => uint256) public lastClaimTimestamp;
    uint256 public totalRevenueDistributed;
    
    // Anti-whale limits (max 5% of supply per wallet initially)
    uint256 public maxWalletAmount = 50_000_000 * 10**18;
    bool public limitsEnabled = true;
    
    // Events
    event RevenueDistributed(uint256 amount, uint256 timestamp);
    event MaxWalletUpdated(uint256 newMax);
    event LimitsRemoved();
    
    constructor(
        address _treasury,
        address _vesting
    ) ERC20("CDLS Network Token", "CDLS") {
        require(_treasury != address(0), "Invalid treasury");
        require(_vesting != address(0), "Invalid vesting");
        
        treasuryAddress = _treasury;
        vestingContract = _vesting;
        
        // Mint initial distribution
        _mint(_vesting, 500_000_000 * 10**18);  // 50% to vesting
        _mint(_treasury, 500_000_000 * 10**18); // 50% to treasury
        
        // Exempt treasury and vesting from limits
        require(totalSupply() == MAX_SUPPLY, "Supply mismatch");
    }
    
    /**
     * @dev Creates a snapshot of token balances for governance/dividends
     * @return Current snapshot ID
     */
    function snapshot() external onlyOwner returns (uint256) {
        return _snapshot();
    }
    
    /**
     * @dev Distribute revenue to token holders (called by treasury)
     * @param amount Amount of USDC to distribute
     */
    function distributeRevenue(uint256 amount) external {
        require(msg.sender == treasuryAddress, "Only treasury");
        totalRevenueDistributed += amount;
        emit RevenueDistributed(amount, block.timestamp);
    }
    
    /**
     * @dev Remove wallet limits after initial growth phase
     */
    function removeLimits() external onlyOwner {
        limitsEnabled = false;
        emit LimitsRemoved();
    }
    
    /**
     * @dev Update max wallet amount (only if limits enabled)
     */
    function updateMaxWallet(uint256 _newMax) external onlyOwner {
        require(limitsEnabled, "Limits removed");
        maxWalletAmount = _newMax;
        emit MaxWalletUpdated(_newMax);
    }
    
    /**
     * @dev Pause all transfers (emergency only)
     */
    function pause() external onlyOwner {
        _pause();
    }
    
    /**
     * @dev Unpause transfers
     */
    function unpause() external onlyOwner {
        _unpause();
    }
    
    /**
     * @dev Override transfer to implement limits and pausable
     */
    function _beforeTokenTransfer(
        address from,
        address to,
        uint256 amount
    ) internal override(ERC20, ERC20Snapshot) whenNotPaused {
        // Anti-whale: Check max wallet on buys (not sells)
        if (limitsEnabled && from != address(0) && to != address(0)) {
            if (to != owner() && to != treasuryAddress && to != stakingContract) {
                require(
                    balanceOf(to) + amount <= maxWalletAmount,
                    "Exceeds max wallet"
                );
            }
        }
        
        super._beforeTokenTransfer(from, to, amount);
    }
}