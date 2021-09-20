"""
Tests configuration.
"""
import pytest

from brownie import (
    MockChainlinkAggregator, MockWstETH, WstETHToETHPriceFeed  # noqa
)


@pytest.fixture(scope='session')
def ape(accounts):
    """Get account."""
    return accounts[0]


@pytest.fixture(scope='session')
def chainlink_agg(ape):
    """Prepare chainlink aggregator for stETH/ETH price feed."""
    return MockChainlinkAggregator.deploy({'from': ape})


@pytest.fixture(scope='session')
def wsteth(ape):
    """Prepare wstETH token."""
    return MockWstETH.deploy({'from': ape})


@pytest.fixture(scope='session')
def price_feed(ape, chainlink_agg, wsteth):
    """Prepare WstETH2ETHPriceFeed."""
    return WstETHToETHPriceFeed.deploy(
        chainlink_agg, wsteth,
        {'from': ape}
    )
