"""
Deploy WstETH2ETHPriceFeed.
"""
import os
import sys

from brownie import WstETH2ETHPriceFeed  # noqa
from brownie import (
    network, accounts, Wei
)

# Contracts addresses.
CHAINLINK_STETH_ETH = os.getenv(
    'CHAINLINK_STETH_ETH', '0x86392dC19c0b719886221c78AB11eb8Cf5c52812'
)
WSTETH = os.getenv(
    'WSTETH', '0x7f39c581f595b53c5cb19bd0b3f8da6c935e2ca0'
)
# Gas price.
GAS_PRICE = os.getenv(
    'GAS_PRICE', '50 gwei'
)


def get_is_live() -> bool:
    """Check that live is active network."""
    return network.show_active() != 'development'


def get_deployer_account(is_live: bool):
    """Get account for deploying."""
    if is_live and 'DEPLOYER' not in os.environ:
        raise EnvironmentError(
            'Please set DEPLOYER env variable to the deployer account name'
        )

    return accounts.load(os.environ['DEPLOYER']) if is_live else accounts[0]


def prompt_bool():
    """Get conformation from user."""
    sys.stdout.write('Proceed? [y/n]: ')
    while True:
        choice = input().lower()
        if choice == 'yes' or choice == 'y':
            return True
        elif choice == 'no' or choice == 'n':
            return False
        else:
            sys.stdout.write(
                'Please respond with \'yes\' or \'no\''
            )


def deploy_price_feed(
        chainlink_aggregator: str,
        wsteth: str,
        tx_params, publish_source: bool = True
):
    """Deploy WstETH2ETHPriceFeed."""
    return WstETH2ETHPriceFeed.deploy(
        chainlink_aggregator,  # _stETH2ETHPriceFeedAddress
        wsteth,  # _wstETHAddress
        tx_params, publish_source
    )


def main():
    is_live = get_is_live()
    deployer = get_deployer_account(is_live)

    print(
        f'Deployer: {deployer}\n'
        f'Chainlink stETH/ETH pair address: {CHAINLINK_STETH_ETH}\n'
        f'wstETH address: {WSTETH}\n'
        f'Gas price: {GAS_PRICE}'
    )

    if not prompt_bool():
        print('Aborting.')
        return

    deploy_price_feed(
        CHAINLINK_STETH_ETH, WSTETH, {
            'from': deployer,
            'gas_price': Wei(GAS_PRICE),
            'required_confs': 1
        }, publish_source=is_live
    )
