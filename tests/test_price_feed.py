"""
Tests for WstETH2ETHPriceFeed contract.
"""
from collections import namedtuple

import brownie
import pytest

PriceFeedContext = namedtuple(
    'PriceFeedContext', [
        'wstETHToStETH', 'stETHToETH', 'wstETHToETH'
    ]
)


def as_wei(amount: int, decimals: int = 0) -> int:
    """Convert amount to wei."""
    power = 10 ** (18 - decimals)
    return amount * power


test_cases = [
    PriceFeedContext(
        stETHToETH=as_wei(1), wstETHToStETH=as_wei(1),
        wstETHToETH=as_wei(1)
    ),
    PriceFeedContext(
        stETHToETH=as_wei(-1), wstETHToStETH=as_wei(1),
        wstETHToETH=as_wei(-1)
    ),
    PriceFeedContext(
        stETHToETH=as_wei(8, 1), wstETHToStETH=as_wei(75, 2),
        wstETHToETH=as_wei(6, 1)
    ),
    PriceFeedContext(
        stETHToETH=as_wei(8, 1), wstETHToStETH=as_wei(125, 2),
        wstETHToETH=as_wei(1)
    ),
    PriceFeedContext(
        stETHToETH=as_wei(1, 2), wstETHToStETH=as_wei(90),
        wstETHToETH=as_wei(9, 1)
    ),
    PriceFeedContext(
        stETHToETH=as_wei(2), wstETHToStETH=as_wei(5, 3),
        wstETHToETH=as_wei(1, 2)
    )
]


def get_test_name(test_case: PriceFeedContext) -> str:
    """Make a test name based on a test case description."""
    return (
        f'stETH/ETH = {test_case.stETHToETH}; '
        f'stETH/wstETH = {test_case.wstETHToStETH}'
    )


@pytest.fixture(scope='module', params=test_cases, ids=get_test_name)
def expected_value(request, chainlink_agg, wsteth):
    """Prepare a normal price feeding case."""
    test_case: PriceFeedContext = request.param
    chainlink_agg.setPriceFeed(test_case.stETHToETH)
    wsteth.setTokenPerStETH(test_case.wstETHToStETH)

    return test_case.wstETHToETH


def test_price_feed(price_feed, expected_value):
    """Tests for normal price feeding cases."""
    assert price_feed.latestAnswer() == expected_value


def test_handle_overfloating_bug(price_feed, chainlink_agg, wsteth):
    """
    Test for handling of overfloating at multiplication.

    Overfloating should to appear only with a huge stETH/ETH coefficient.
    """
    chainlink_agg.setPriceFeed(10 ** 70)
    wsteth.setTokenPerStETH(10 ** 18)
    with brownie.reverts():
        _ = price_feed.latestAnswer()


def test_handle_conversion_bug(price_feed, chainlink_agg, wsteth):
    """Test for handling of overfloating at from uint to int conversion."""
    chainlink_agg.setPriceFeed(10 ** 18)
    wsteth.setTokenPerStETH(10 ** 77)
    with brownie.reverts():
        price_feed.latestAnswer()
