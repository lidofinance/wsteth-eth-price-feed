// SPDX-License-Identifier: UNLICENSED

pragma solidity 0.8.7;

import "./WstETH2ETHPriceFeed.sol";


contract MockChainlinkAggregator is IChainlinkAggregator {
    int256 immutable private stETH2ETHPriceFeed;

    constructor (int256 _priceFeed) {
        stETH2ETHPriceFeed = _priceFeed;
    }

    function latestAnswer() external view override returns (int256) {
        return stETH2ETHPriceFeed;
    }
}
