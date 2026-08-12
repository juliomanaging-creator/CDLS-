// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import "@openzeppelin/contracts/token/ERC20/IERC20.sol";
import "@openzeppelin/contracts/token/ERC20/utils/SafeERC20.sol";
import "@openzeppelin/contracts/security/ReentrancyGuard.sol";
import "@openzeppelin/contracts/access/Ownable.sol";

/**
 * @title CDLSStaking
 * @dev Stake $CDLS to earn $HAUL rewards and revenue share
 */
contract CDLSStaking is ReentrancyGuard, Ownable {
    using SafeERC20 for IERC20;
    
    IERC20 public cdlsToken;
    IERC20 public haulToken;
    IERC20 public usdcToken; // For revenue distribution
    
    // Staking info
    struct Stake {
        uint256 amount;          // Amount of $CDLS staked
        uint256 startTime;       // When stake started
        uint256 lastClaimTime;   // Last time rewards claimed
        uint256 haulEarned;      // Total $HAUL earned
        uint256 usdcEarned;      // Total USDC earned
    }
    
    mapping(address => Stake) public stakes;
    
    // Pool stats
    uint256 public totalStaked;
    uint256 public baseAPY = 8; // 8% base APY in $HAUL
    uint256 public bonusAPY = 3; // +3% for long-term stakers (12+ months)
    
    // Revenue distribution
    uint256 public totalRevenueDistributed;
    uint256 public revenuePerTokenStaked;
    
    // Minimum stake amounts for tiers
    uint256 public constant STARTER_TIER = 10_000 * 10**18;     // 10,000 $CDLS
    uint256 public constant PRO_TIER = 100_000 * 10**18;        // 100,000 $CDLS
    uint256 public constant ENTERPRISE_TIER = 1_000_000 * 10**18; // 1,000,000 $CDLS
    
    // Events
    event Staked(address indexed user, uint256 amount);
    event Unstaked(address indexed user, uint256 amount);
    event RewardsClaimed(address indexed user, uint256 haulAmount, uint256 usdcAmount);
    event RevenueDistributed(uint256 amount);
    
    constructor(
        address _cdls,
        address _haul,
        address _usdc
    ) {
        cdlsToken = IERC20(_cdls);
        haulToken = IERC20(_haul);
        usdcToken = IERC20(_usdc);
    }
    
    /**
     * @dev Stake $CDLS tokens
     * @param amount Amount to stake
     */
    function stake(uint256 amount) external nonReentrant {
        require(amount > 0, "Cannot stake 0");
        
        // Claim pending rewards before staking more
        if (stakes[msg.sender].amount > 0) {
            _claimRewards();
        }
        
        cdlsToken.safeTransferFrom(msg.sender, address(this), amount);
        
        stakes[msg.sender].amount += amount;
        stakes[msg.sender].startTime = block.timestamp;
        stakes[msg.sender].lastClaimTime = block.timestamp;
        
        totalStaked += amount;
        
        emit Staked(msg.sender, amount);
    }
    
    /**
     * @dev Unstake $CDLS tokens
     * @param amount Amount to unstake
     */
    function unstake(uint256 amount) external nonReentrant {
        require(stakes[msg.sender].amount >= amount, "Insufficient stake");
        
        // Claim rewards before unstaking
        _claimRewards();
        
        stakes[msg.sender].amount -= amount;
        totalStaked -= amount;
        
        cdlsToken.safeTransfer(msg.sender, amount);
        
        emit Unstaked(msg.sender, amount);
    }
    
    /**
     * @dev Claim pending rewards ($HAUL + USDC)
     */
    function claimRewards() external nonReentrant {
        _claimRewards();
    }
    
    /**
     * @dev Internal function to calculate and distribute rewards
     */
    function _claimRewards() internal {
        Stake storage userStake = stakes[msg.sender];
        require(userStake.amount > 0, "No stake");
        
        uint256 timeStaked = block.timestamp - userStake.lastClaimTime;
        uint256 haulRewards = _calculateHaulRewards(msg.sender, timeStaked);
        uint256 usdcRewards = _calculateUSDCRewards(msg.sender);
        
        if (haulRewards > 0) {
            haulToken.safeTransfer(msg.sender, haulRewards);
            userStake.haulEarned += haulRewards;
        }
        
        if (usdcRewards > 0) {
            usdcToken.safeTransfer(msg.sender, usdcRewards);
            userStake.usdcEarned += usdcRewards;
        }
        
        userStake.lastClaimTime = block.timestamp;
        
        emit RewardsClaimed(msg.sender, haulRewards, usdcRewards);
    }
    
    /**
     * @dev Calculate $HAUL rewards based on APY
     * @param user Address of staker
     * @param timeStaked Seconds since last claim
     * @return Amount of $HAUL rewards
     */
    function _calculateHaulRewards(
        address user,
        uint256 timeStaked
    ) internal view returns (uint256) {
        Stake memory userStake = stakes[user];
        
        // Base APY
        uint256 apy = baseAPY;
        
        // Bonus for long-term staking (12+ months)
        if (block.timestamp - userStake.startTime >= 365 days) {
            apy += bonusAPY;
        }
        
        // Calculate rewards: (amount * APY * time) / (100 * 365 days)
        uint256 rewards = (userStake.amount * apy * timeStaked) / (100 * 365 days);
        
        return rewards;
    }
    
    /**
     * @dev Calculate USDC revenue share
     * @param user Address of staker
     * @return Amount of USDC rewards
     */
    function _calculateUSDCRewards(address user) internal view returns (uint256) {
        Stake memory userStake = stakes[user];
        
        // Pro-rata share of revenue based on stake
        if (totalStaked == 0) return 0;
        
        uint256 userShare = (userStake.amount * revenuePerTokenStaked) / 10**18;
        
        return userShare;
    }
    
    /**
     * @dev Distribute revenue to all stakers (called by treasury)
     * @param amount Amount of USDC to distribute
     */
    function distributeRevenue(uint256 amount) external onlyOwner {
        require(amount > 0, "Cannot distribute 0");
        require(totalStaked > 0, "No stakers");
        
        usdcToken.safeTransferFrom(msg.sender, address(this), amount);
        
        // Update revenue per token
        revenuePerTokenStaked += (amount * 10**18) / totalStaked;
        totalRevenueDistributed += amount;
        
        emit RevenueDistributed(amount);
    }
    
    /**
     * @dev Get user's platform access tier based on stake
     * @param user Address to check
     * @return Tier level (0 = Free, 1 = Starter, 2 = Pro, 3 = Enterprise)
     */
    function getUserTier(address user) external view returns (uint8) {
        uint256 staked = stakes[user].amount;
        
        if (staked >= ENTERPRISE_TIER) return 3;
        if (staked >= PRO_TIER) return 2;
        if (staked >= STARTER_TIER) return 1;
        return 0;
    }
    
    /**
     * @dev Get pending rewards for user
     * @param user Address to check
     * @return haulRewards Pending $HAUL
     * @return usdcRewards Pending USDC
     */
    function pendingRewards(address user) external view returns (uint256 haulRewards, uint256 usdcRewards) {
        if (stakes[user].amount == 0) return (0, 0);
        
        uint256 timeStaked = block.timestamp - stakes[user].lastClaimTime;
        haulRewards = _calculateHaulRewards(user, timeStaked);
        usdcRewards = _calculateUSDCRewards(user);
    }
}