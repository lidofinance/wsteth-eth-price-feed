"""
Tests configuration.
"""
import pytest

from brownie import (
    MockChainlinkAggregator, MockWstETH, WstETH2ETHPriceFeed  # noqa
)


@pytest.fixture(scope='session')
def ape(accounts):
    """Get account."""
    return accounts[0]


@pytest.fixture(scope='session')
def make_fabric_chainlink_agg(ape):
    """Prepare fabric for chainlink aggregator with target price."""

    def _make_fabric_chainlink_agg(price_feed: int):
        return MockChainlinkAggregator.deploy(
            price_feed, {'from': ape}
        )

    return _make_fabric_chainlink_agg


@pytest.fixture(scope='session')
def make_fabric_wsteth(ape):
    """Prepare fabric for wstETH with target conversion coefficient."""

    def _make_fabric_wsteth(conv_coef: int):
        return MockWstETH.deploy(
            conv_coef, {'from': ape}
        )

    return _make_fabric_wsteth


@pytest.fixture(scope='session')
def make_fabric_price_feed(ape):
    """Prepare fabrice for WstETH2ETHPriceFeed."""

    def _make_fabric_price_feed(
            chainlink_pair_address, wsteth_address
    ):
        return WstETH2ETHPriceFeed.deploy(
            chainlink_pair_address, wsteth_address,
            {'from': ape}
        )

    return _make_fabric_price_feed
