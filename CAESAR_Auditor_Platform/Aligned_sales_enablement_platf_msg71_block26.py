// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import "@openzeppelin/contracts/token/ERC1155/ERC1155.sol";
import "@openzeppelin/contracts/access/AccessControl.sol";
import "@openzeppelin/contracts/security/ReentrancyGuard.sol";

/**
 * @title CarbonCreditNFT
 * @dev ERC-1155 semi-fungible tokens representing LCFS carbon credits
 * Each token represents 1 verified carbon credit
 */
contract CarbonCreditNFT is ERC1155, AccessControl, ReentrancyGuard {
    
    bytes32 public constant MINTER_ROLE = keccak256("MINTER_ROLE");
    bytes32 public constant VERIFIER_ROLE = keccak256("VERIFIER_ROLE");
    
    // Token ID => Credit metadata
    struct CarbonCredit {
        string vintage;          // e.g., "2026-Q1"
        address generator;       // Dealer who generated credit
        string vehicleVIN;       // Vehicle identification
        uint256 milesDriven;     // Miles driven to generate credit
        uint256 co2Avoided;      // Tons of CO2 avoided
        uint256 creditAmount;    // Number of credits (usually 1.0)
        bool verified;           // CARB verification status
        string carbReportId;     // CARB report reference
        uint256 generatedAt;     // Timestamp
        uint256 verifiedAt;      // Verification timestamp
    }
    
    mapping(uint256 => CarbonCredit) public credits;
    uint256 public nextTokenId = 1;
    
    // Tracking
    mapping(address => uint256) public totalGenerated;
    mapping(address => uint256) public totalVerified;
    uint256 public totalCreditsIssued;
    uint256 public totalCreditsVerified;
    
    // Events
    event CreditMinted(uint256 indexed tokenId, address indexed generator, uint256 amount);
    event CreditVerified(uint256 indexed tokenId, string carbReportId);
    event CreditRedeemed(uint256 indexed tokenId, address indexed redeemer, uint256 amount);
    
    constructor() ERC1155("https://api.cdls.network/carbon/{id}.json") {
        _grantRole(DEFAULT_ADMIN_ROLE, msg.sender);
        _grantRole(MINTER_ROLE, msg.sender);
        _grantRole(VERIFIER_ROLE, msg.sender);
    }
    
    /**
     * @dev Mint new carbon credit NFT (pre-verification)
     * @param generator Address of dealer generating credit
     * @param vintage Quarter generated (e.g., "2026-Q1")
     * @param vehicleVIN Vehicle identification number
     * @param milesDriven Miles driven to generate credit
     * @param co2Avoided Tons of CO2 avoided
     * @param amount Number of credits (decimals supported)
     * @return tokenId ID of minted NFT
     */
    function mintCredit(
        address generator,
        string memory vintage,
        string memory vehicleVIN,
        uint256 milesDriven,
        uint256 co2Avoided,
        uint256 amount
    ) external onlyRole(MINTER_ROLE) returns (uint256) {
        require(generator != address(0), "Invalid generator");
        require(amount > 0, "Amount must be > 0");
        
        uint256 tokenId = nextTokenId++;
        
        credits[tokenId] = CarbonCredit({
            vintage: vintage,
            generator: generator,
            vehicleVIN: vehicleVIN,
            milesDriven: milesDriven,
            co2Avoided: co2Avoided,
            creditAmount: amount,
            verified: false,
            carbReportId: "",
            generatedAt: block.timestamp,
            verifiedAt: 0
        });
        
        _mint(generator, tokenId, amount, "");
        
        totalGenerated[generator] += amount;
        totalCreditsIssued += amount;
        
        emit CreditMinted(tokenId, generator, amount);
        
        return tokenId;
    }
    
    /**
     * @dev Verify carbon credit after CARB approval
     * @param tokenId ID of credit to verify
     * @param carbReportId CARB report reference
     */
    function verifyCredit(
        uint256 tokenId,
        string memory carbReportId
    ) external onlyRole(VERIFIER_ROLE) {
        require(credits[tokenId].generatedAt > 0, "Credit does not exist");
        require(!credits[tokenId].verified, "Already verified");
        
        credits[tokenId].verified = true;
        credits[tokenId].carbReportId = carbReportId;
        credits[tokenId].verifiedAt = block.timestamp;
        
        address generator = credits[tokenId].generator;
        uint256 amount = credits[tokenId].creditAmount;
        
        totalVerified[generator] += amount;
        totalCreditsVerified += amount;
        
        emit CreditVerified(tokenId, carbReportId);
    }
    
    /**
     * @dev Redeem credit (burn NFT, transfer to CARB)
     * @param tokenId ID of credit to redeem
     * @param amount Amount to redeem
     */
    function redeemCredit(
        uint256 tokenId,
        uint256 amount
    ) external nonReentrant {
        require(credits[tokenId].verified, "Credit not verified");
        require(balanceOf(msg.sender, tokenId) >= amount, "Insufficient balance");
        
        _burn(msg.sender, tokenId, amount);
        
        emit CreditRedeemed(tokenId, msg.sender, amount);
    }
    
    /**
     * @dev Get credit details
     * @param tokenId ID of credit
     * @return Credit struct
     */
    function getCreditDetails(uint256 tokenId) external view returns (CarbonCredit memory) {
        require(credits[tokenId].generatedAt > 0, "Credit does not exist");
        return credits[tokenId];
    }
    
    /**
     * @dev Check if credit is verified
     * @param tokenId ID of credit
     * @return bool Verification status
     */
    function isVerified(uint256 tokenId) external view returns (bool) {
        return credits[tokenId].verified;
    }
    
    /**
     * @dev Update metadata URI
     * @param newuri New base URI
     */
    function setURI(string memory newuri) external onlyRole(DEFAULT_ADMIN_ROLE) {
        _setURI(newuri);
    }
    
    /**
     * @dev Required override for AccessControl
     */
    function supportsInterface(bytes4 interfaceId)
        public
        view
        override(ERC1155, AccessControl)
        returns (bool)
    {
        return super.supportsInterface(interfaceId);
    }
}