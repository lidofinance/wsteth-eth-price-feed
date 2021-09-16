# Price feed for a wstETH/ETH pair

------------------------------------------------------------

[![License](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![testing workflow](https://github.com/lidofinance/wsteth-eth-price-feed/actions/workflows/tests.yaml/badge.svg?branch=main)](https://github.com/lidofinance/wsteth-eth-price-feed/actions/workflows/tests.yaml)

### About

Contains the implementation of price feed for wstETH/ETH pair. 
Implementation is based on value of stETH/ETH from [ChainlinkAggregator](0x86392dC19c0b719886221c78AB11eb8Cf5c52812) and stETH/wstETH rate from [wstETH](0x7f39c581f595b53c5cb19bd0b3f8da6c935e2ca0) contract.
Resulting value for pair is calculated as stETH/ETH value divided by stETH/wstETH rate.
