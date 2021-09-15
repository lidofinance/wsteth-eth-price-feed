// SPDX-License-Identifier: MIT

pragma solidity 0.6.6;

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
    IWstETH internal immutable _wstETH;
    IChainlinkAggregator internal immutable _stETH2ETHPriceFeed;

    uint256 constant internal multiplier = 10 ** 18;

    constructor(
        address _stETH2ETHPriceFeedAddress,
        address _wstETHAddress
    ) public {
        _stETH2ETHPriceFeed = IChainlinkAggregator(_stETH2ETHPriceFeedAddress);
        _wstETH = IWstETH(_wstETHAddress);
    }

    function mul(uint256 a, uint256 b) internal view returns (uint256) {
        /**
         * @notice Multiply with overflow checking
         */
        if (a == 0) {
            return 0;
        }

        uint256 c = a * b;
        assert(c / a == b);
        return c;
    }

    function latestAnswer() external view override returns (int256) {
        /**
         * @notice Get amount of wstETH for a one ETH
         */
        int256 stETH2ETH = _stETH2ETHPriceFeed.latestAnswer();

        if (stETH2ETH > 0) {
            int256 wstETH2ETH = int256(mul(
                uint256(stETH2ETH), multiplier
            ) / _wstETH.stEthPerToken());
            assert(wstETH2ETH > 0);
            return wstETH2ETH;
        } else {
            return stETH2ETH;
        }
    }
}
