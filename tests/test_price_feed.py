"""
Tests for WstETH2ETHPriceFeed contract.
"""
import pytest
import brownie

from collections import namedtuple

PriceFeedContext = namedtuple(
    'PriceFeedContext', [
        'stETHToWstETH', 'stETHToETH', 'wstETHToETH'
    ]
)


def as_wei(amount: int, decimals: int = 0) -> int:
    """Convert amount to wei."""
    power = 10 ** (18 - decimals)
    return amount * power


test_cases = [
    PriceFeedContext(
        stETHToETH=as_wei(1), stETHToWstETH=as_wei(1),
        wstETHToETH=as_wei(1)
    ),
    PriceFeedContext(
        stETHToETH=as_wei(-1), stETHToWstETH=as_wei(1),
        wstETHToETH=as_wei(-1)
    ),
    PriceFeedContext(
        stETHToETH=as_wei(99, 2), stETHToWstETH=as_wei(33, 2),
        wstETHToETH=as_wei(3)
    ),
    PriceFeedContext(
        stETHToETH=as_wei(75, 2), stETHToWstETH=as_wei(125, 2),
        wstETHToETH=as_wei(6, 1)
    )
]


def get_test_name(test_case: PriceFeedContext) -> str:
    """Make a test name based on a test case description."""
    return (
        f'stETH/ETH = {test_case.stETHToETH}; '
        f'stETH/wstETH = {test_case.stETHToWstETH}'
    )


@pytest.fixture(scope='module', params=test_cases, ids=get_test_name)
def price_feed(
        request, make_fabric_chainlink_agg,
        make_fabric_wsteth, make_fabric_price_feed
):
    """Prepare a normal price feeding case."""
    test_case: PriceFeedContext = request.param
    chainlink_aggregator = make_fabric_chainlink_agg(test_case.stETHToETH)
    wsteth = make_fabric_wsteth(test_case.stETHToWstETH)

    return make_fabric_price_feed(
        chainlink_aggregator, wsteth
    ), test_case.wstETHToETH


def test_price_feed(price_feed):
    """Tests for normal price feeding cases."""
    price_feed_contract, expected = price_feed
    assert price_feed_contract.latestAnswer() == expected


def test_handle_overfloating_bug(
        make_fabric_price_feed, make_fabric_chainlink_agg, make_fabric_wsteth
):
    """
    Test for handling of overfloating at multiplication.

    Overfloating should to appear only with a huge stETH/ETH coefficient.
    """
    price_feed_contract = make_fabric_price_feed(
        make_fabric_chainlink_agg(10 ** 70),  # stETH/ETH
        make_fabric_wsteth(as_wei(1))
    )
    with brownie.reverts():
        price_feed_contract.latestAnswer()


def test_handle_conversion_bug(
        make_fabric_price_feed, make_fabric_chainlink_agg, make_fabric_wsteth
):
    """Test for handling of overfloating at from uint to int conversion."""
    price_feed_contract = make_fabric_price_feed(
        make_fabric_chainlink_agg(10 ** 59),
        make_fabric_wsteth(1)
    )
    with brownie.reverts():
        price_feed_contract.latestAnswer()
