// SPDX-License-Identifier: UNLICENSED

pragma solidity 0.8.7;

import "./AAVECompatWstETHToETHPriceFeed.sol";

contract MockWstETH is IWstETH {
    uint256 private wstETHToStETH;

    function setStETHPerToken(uint256 newValue) external {
        wstETHToStETH = newValue;
    }

    function stEthPerToken() external view override returns (uint256) {
        return wstETHToStETH;
    }
}
