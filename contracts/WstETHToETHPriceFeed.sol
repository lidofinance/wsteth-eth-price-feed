// SPDX-License-Identifier: MIT

pragma solidity 0.8.7;

interface IWstETH {
    /**
     * @notice Get amount of stETH for a one wstETH
     * @return Amount of stETH for 1 wstETH
     */
    function tokensPerStEth() external view returns (uint256);
}

interface IChainlinkAggregator {
    /**
     * @notice Reads the current answer from aggregator delegated to.
     */
    function latestAnswer() external view returns (int256);
}

contract WstETHToETHPriceFeed is IChainlinkAggregator {
    IWstETH public immutable wstETH;
    IChainlinkAggregator public immutable stETHToETHPriceFeed;

    int256 internal constant DECIMALS = 10 ** 18;

    constructor(
        address _stETHToETHPriceFeed,
        address _wstETH
    ) {
        stETHToETHPriceFeed = IChainlinkAggregator(_stETHToETHPriceFeed);
        wstETH = IWstETH(_wstETH);
    }

    /**
     * @notice Get amount of wstETH for a one ETH
     */
    function latestAnswer() external view override returns (int256) {
        int256 wstETHToStETH = int256(wstETH.tokensPerStEth());
        assert(wstETHToStETH > 0);
        int256 stETHToETH = stETHToETHPriceFeed.latestAnswer();

        return wstETHToStETH * stETHToETH / DECIMALS;
    }
}
