// SPDX-License-Identifier: UNLICENSED

pragma solidity 0.8.7;

import "./AAVECompatWstETHToETHPriceFeed.sol";


contract MockChainlinkAggregator is IChainlinkAggregator {
    int256 private stETHToETHPriceFeed;

    function setPriceFeed(int256 newValue) external {
        stETHToETHPriceFeed = newValue;
    }

    function latestAnswer() external view override returns (int256) {
        return stETHToETHPriceFeed;
    }
}
