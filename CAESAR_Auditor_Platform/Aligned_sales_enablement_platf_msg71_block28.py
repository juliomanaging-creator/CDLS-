// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import "@openzeppelin/contracts/token/ERC1155/IERC1155.sol";
import "@openzeppelin/contracts/token/ERC20/IERC20.sol";
import "@openzeppelin/contracts/security/ReentrancyGuard.sol";
import "@openzeppelin/contracts/access/Ownable.sol";

/**
 * @title CarbonMarketplace
 * @dev Decentralized marketplace for trading carbon credit NFTs
 */
contract CarbonMarketplace is ReentrancyGuard, Ownable {
    
    IERC1155 public carbonNFT;
    IERC20 public cdlsToken;
    IERC20 public haulToken;
    IERC20 public usdcToken;
    
    // Listing structure
    struct Listing {
        address seller;
        uint256 tokenId;
        uint256 amount;
        uint256 pricePerCredit;   // In USDC (6 decimals)
        bool active;
        uint256 listedAt;
    }
    
    // Order book
    mapping(uint256 => Listing) public listings;
    uint256 public nextListingId = 1;
    
    // Fees
    uint256 public marketplaceFee = 200; // 2% (200 basis points)
    address public feeRecipient;
    
    // Stats
    uint256 public totalVolume;      // Total USDC volume
    uint256 public totalTrades;
    uint256 public totalFeesCollected;
    
    // Events
    event Listed(uint256 indexed listingId, address indexed seller, uint256 tokenId, uint256 amount, uint256 price);
    event Sold(uint256 indexed listingId, address indexed buyer, uint256 amount, uint256 totalPrice);
    event Cancelled(uint256 indexed listingId);
    event FeeUpdated(uint256 newFee);
    
    constructor(
        address _carbonNFT,
        address _cdls,
        address _haul,
        address _usdc,
        address _feeRecipient
    ) {
        carbonNFT = IERC1155(_carbonNFT);
        cdlsToken = IERC20(_cdls);
        haulToken = IERC20(_haul);
        usdcToken = IERC20(_usdc);
        feeRecipient = _feeRecipient;
    }
    
    /**
     * @dev List carbon credits for sale
     * @param tokenId ID of carbon credit NFT
     * @param amount Number of credits to sell
     * @param pricePerCredit Price per credit in USDC (6 decimals)
     * @return listingId ID of created listing
     */
    function listCredit(
        uint256 tokenId,
        uint256 amount,
        uint256 pricePerCredit
    ) external nonReentrant returns (uint256) {
        require(amount > 0, "Amount must be > 0");
        require(pricePerCredit > 0, "Price must be > 0");
        require(
            carbonNFT.balanceOf(msg.sender, tokenId) >= amount,
            "Insufficient balance"
        );
        
        // Transfer NFT to marketplace (escrow)
        carbonNFT.safeTransferFrom(
            msg.sender,
            address(this),
            tokenId,
            amount,
            ""
        );
        
        uint256 listingId = nextListingId++;
        
        listings[listingId] = Listing({
            seller: msg.sender,
            tokenId: tokenId,
            amount: amount,
            pricePerCredit: pricePerCredit,
            active: true,
            listedAt: block.timestamp
        });
        
        emit Listed(listingId, msg.sender, tokenId, amount, pricePerCredit);
        
        return listingId;
    }
    
    /**
     * @dev Buy carbon credits from listing
     * @param listingId ID of listing to buy from
     * @param amount Number of credits to buy
     */
    function buyCredit(
        uint256 listingId,
        uint256 amount
    ) external nonReentrant {
        Listing storage listing = listings[listingId];
        require(listing.active, "Listing not active");
        require(amount > 0 && amount <= listing.amount, "Invalid amount");
        
        uint256 totalPrice = (amount * listing.pricePerCredit) / 10**18;
        uint256 fee = (totalPrice * marketplaceFee) / 10000;
        uint256 sellerProceeds = totalPrice - fee;
        
        // Transfer payment
        usdcToken.transferFrom(msg.sender, listing.seller, sellerProceeds);
        usdcToken.transferFrom(msg.sender, feeRecipient, fee);
        
        // Transfer NFT
        carbonNFT.safeTransferFrom(
            address(this),
            msg.sender,
            listing.tokenId,
            amount,
            ""
        );
        
        // Update listing
        listing.amount -= amount;
        if (listing.amount == 0) {
            listing.active = false;
        }
        
        // Update stats
        totalVolume += totalPrice;
        totalTrades += 1;
        totalFeesCollected += fee;
        
        emit Sold(listingId, msg.sender, amount, totalPrice);
    }
    
    /**
     * @dev Cancel listing and return NFTs to seller
     * @param listingId ID of listing to cancel
     */
    function cancelListing(uint256 listingId) external nonReentrant {
        Listing storage listing = listings[listingId];
        require(listing.seller == msg.sender, "Not seller");
        require(listing.active, "Already inactive");
        
        listing.active = false;
        
        // Return NFT to seller
        carbonNFT.safeTransferFrom(
            address(this),
            msg.sender,
            listing.tokenId,
            listing.amount,
            ""
        );
        
        emit Cancelled(listingId);
    }
    
    /**
     * @dev Update marketplace fee (governance controlled)
     * @param newFee New fee in basis points (200 = 2%)
     */
    function updateFee(uint256 newFee) external onlyOwner {
        require(newFee <= 500, "Fee too high"); // Max 5%
        marketplaceFee = newFee;
        emit FeeUpdated(newFee);
    }
    
    /**
     * @dev Get all active listings for a token ID
     * @param tokenId Carbon credit token ID
     * @return Array of listing IDs
     */
    function getActiveListings(uint256 tokenId) external view returns (uint256[] memory) {
        // Note: In production, use subgraph for efficient queries
        // This is a simplified version
        uint256[] memory activeListings = new uint256[](nextListingId);
        uint256 count = 0;
        
        for (uint256 i = 1; i < nextListingId; i++) {
            if (listings[i].active && listings[i].tokenId == tokenId) {
                activeListings[count] = i;
                count++;
            }
        }
        
        // Resize array
        uint256[] memory result = new uint256[](count);
        for (uint256 i = 0; i < count; i++) {
            result[i] = activeListings[i];
        }
        
        return result;
    }
    
    /**
     * @dev Required for receiving ERC1155 tokens
     */
    function onERC1155Received(
        address,
        address,
        uint256,
        uint256,
        bytes memory
    ) public pure returns (bytes4) {
        return this.onERC1155Received.selector;
    }
}