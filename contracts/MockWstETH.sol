// SPDX-License-Identifier: UNLICENSED

pragma solidity 0.8.7;

import "./WstETHToETHPriceFeed.sol";

contract MockWstETH is IWstETH {
    uint256 private wstETHToStETH;

    function setTokenPerStETH(uint256 newValue) external {
        wstETHToStETH = newValue;
    }

    function tokensPerStEth() external view override returns (uint256) {
        return wstETHToStETH;
    }
}
