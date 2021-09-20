// SPDX-License-Identifier: UNLICENSED

pragma solidity 0.8.7;

import "./WstETHToETHPriceFeed.sol";


contract MockChainlinkAggregator is IChainlinkAggregator {
    int256 immutable private stETHToETHPriceFeed;

    constructor (int256 _priceFeed) {
        stETHToETHPriceFeed = _priceFeed;
    }

    function latestAnswer() external view override returns (int256) {
        return stETHToETHPriceFeed;
    }
}
