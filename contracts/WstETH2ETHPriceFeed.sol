// SPDX-License-Identifier: MIT

pragma solidity 0.8.7;

interface IWstETH {
    /**
     * @notice Get amount of stETH for a one wstETH
     * @return Amount of stETH for 1 wstETH
     */
    function stEthPerToken() external view returns (uint256);
}

interface IChainlinkAggregator {
    /**
     * @notice Reads the current answer from aggregator delegated to.
     */
    function latestAnswer() external view returns (int256);
}

contract WstETH2ETHPriceFeed is IChainlinkAggregator {
    IWstETH internal immutable wstETH;
    IChainlinkAggregator internal immutable stETH2ETHPriceFeed;

    int256 internal constant MULTIPLIER = 10 ** 18;

    constructor(
        address _stETH2ETHPriceFeed,
        address _wstETH
    ) {
        stETH2ETHPriceFeed = IChainlinkAggregator(_stETH2ETHPriceFeed);
        wstETH = IWstETH(_wstETH);
    }

    /**
     * @notice Get amount of wstETH for a one ETH
     */
    function latestAnswer() external view override returns (int256) {
        int256 stETH2ETH = stETH2ETHPriceFeed.latestAnswer() * MULTIPLIER;
        int256 stETH2wstETH = int256(wstETH.stEthPerToken());
        assert(stETH2wstETH > 0);

        return stETH2ETH / stETH2wstETH;
    }
}
