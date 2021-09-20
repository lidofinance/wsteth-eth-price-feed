// SPDX-License-Identifier: UNLICENSED

pragma solidity 0.8.7;

import "./WstETHToETHPriceFeed.sol";

contract MockWstETH is IWstETH {
    uint256 immutable private stETHToWstETH;

    constructor (uint256 _convCoefficient) {
        stETHToWstETH = _convCoefficient;
    }

    function stEthPerToken() external view override returns (uint256) {
        return stETHToWstETH;
    }
}
