"""
Tests configuration.
"""
import pytest

from brownie import (
    MockChainlinkAggregator, MockWstETH, AAVECompatWstETHToETHPriceFeed  # noqa
)
from brownie import interface  # noqa


@pytest.fixture(scope='session')
def ape(accounts):
    """Get account."""
    return accounts[0]


@pytest.fixture(scope='session')
def mock_chainlink_agg(ape):
    """Prepare mock chainlink aggregator for stETH/ETH price feed."""
    return MockChainlinkAggregator.deploy({'from': ape})


@pytest.fixture(scope='session')
def mock_wsteth(ape):
    """Prepare mock wstETH token."""
    return MockWstETH.deploy({'from': ape})


@pytest.fixture(scope='session')
def price_feed_mock_based(ape, mock_chainlink_agg, mock_wsteth):
    """Prepare AAVECompatWstETH2ETHPriceFeed based on mock contracts."""
    return AAVECompatWstETHToETHPriceFeed.deploy(
        mock_chainlink_agg, mock_wsteth,
        {'from': ape}
    )


@pytest.fixture(scope='session')
def chainlink_agg():
    """Get live chainlink price feed."""
    chainlink_price_feed = '0x86392dC19c0b719886221c78AB11eb8Cf5c52812'
    return interface.ChainlinkPriceFeed(chainlink_price_feed)


@pytest.fixture(scope='session')
def wsteth():
    """Get live wsteth."""
    wsteth = '0x7f39c581f595b53c5cb19bd0b3f8da6c935e2ca0'
    return interface.wstETH(wsteth)


@pytest.fixture(scope='session')
def price_feed_live(ape, chainlink_agg, wsteth):
    """Prepare AAVECompatWstETH2ETHPriceFeed on forked contracts."""
    return AAVECompatWstETHToETHPriceFeed.deploy(
        chainlink_agg, wsteth,
        {'from': ape}
    )
