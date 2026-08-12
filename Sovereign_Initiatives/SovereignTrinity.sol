// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

/**
 * @title SovereignTrinity
 * @dev Implements the 33/33/33 Revenue Split and Dignity Payroll.
 */
contract SovereignTrinity {
    address public immutable stateTreasury; // Fiona Ma's Office
    address public immutable globalLegacy;  // Global Debt Fund
    address public immutable kineticGrowth; // Rail Construction
    
    uint256 public constant DIGNITY_WAGE_PER_HOUR = 89.80 ether; // Denominated in Sovereign Credits
    uint256 public constant MAX_SHIFT_HOURS = 4;

    event RoyaltyDistributed(uint256 state, uint256 global, uint256 kinetic);
    event PayrollDisbursed(address indexed specialist, uint256 amount);

    constructor(address _state, address _global, address _kinetic) {
        stateTreasury = _state;
        globalLegacy = _global;
        kineticGrowth = _kinetic;
    }

    // Automated 33/33/33 Sweep
    receive() external payable {
        uint256 tranche = msg.value / 3;
        payable(stateTreasury).transfer(tranche);
        payable(globalLegacy).transfer(tranche);
        payable(kineticGrowth).transfer(address(this).balance);
        
        emit RoyaltyDistributed(tranche, tranche, address(this).balance);
    }

    // Precision Payroll Triggered by IoT Mesh
    function disbursePayroll(address _specialist, uint256 _hours) external {
        require(_hours <= MAX_SHIFT_HOURS, "Shift exceeds 4-hour limit");
        uint256 payment = _hours * DIGNITY_WAGE_PER_HOUR;
        payable(_specialist).transfer(payment);
        
        emit PayrollDisbursed(_specialist, payment);
    }
}
