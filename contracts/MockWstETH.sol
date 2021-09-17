// SPDX-License-Identifier: UNLICENSED

pragma solidity 0.8.7;

import "./WstETH2ETHPriceFeed.sol";

contract MockWstETH is IWstETH {
    uint256 immutable private stETH2WstETH;

    constructor (uint256 _convCoefficient) {
        stETH2WstETH = _convCoefficient;
    }

    function stEthPerToken() external view override returns (uint256) {
        return stETH2WstETH;
    }
}
