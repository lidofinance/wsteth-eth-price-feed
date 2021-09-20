# Price feed for a wstETH/ETH pair

------------------------------------------------------------

[![License](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![testing workflow](https://github.com/lidofinance/wsteth-eth-price-feed/actions/workflows/tests.yaml/badge.svg?branch=main)](https://github.com/lidofinance/wsteth-eth-price-feed/actions/workflows/tests.yaml)

### About

Contains the implementation of price feed for wstETH/ETH pair. 
Implementation is based on value of stETH/ETH from [ChainlinkAggregator](0x86392dC19c0b719886221c78AB11eb8Cf5c52812) and stETH/wstETH rate from [wstETH](0x7f39c581f595b53c5cb19bd0b3f8da6c935e2ca0) contract.
Resulting value for pair is calculated as stETH/ETH value divided by stETH/wstETH rate.

### Core contracts

#### `WstETH2ETHPriceFeed.sol`

The contract is constructed around stETH/ETH pair from the Chainlink. It implements only one function:

```function latestAnswer() external view returns (int256);```

for compability with `IChainlinkAggregator` interface from [AaveOracle contract](0xA50ba011c48153De246E5192C8f9258A2ba79Ca9).

'latestAnswer' is a wrapping for the same function from 'ChainlinkAggregator'. For values from the Chainlink it performs scaling by wstETH/stETH factor.

`constructor` get addresses of a chainlink aggregator for the stETH/ETH pair and the wstETH contract.
