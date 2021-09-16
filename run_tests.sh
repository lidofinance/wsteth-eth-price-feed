#!/bin/bash

if [ "$#" -ne 1 ]; then
  echo "Usage: run_test.sh <fork-url>";
  exit 0;
fi

echo "Run brownie tests for mainnet fork at $1"

current_timestamp=$(date +"%s")
mainnet_fork_name="mainnet-tests-fork-$current_timestamp"

brownie networks add                                        \
        development "$mainnet_fork_name"                    \
        host=http://127.0.0.1 port=8545 gas_limit=12000000  \
        accounts=10 evm_version=istanbul mnemonic=brownie   \
        fork="$1" cmd=ganache-cli

# shellcheck disable=SC2181
if [ "$?" != 0 ]; then
  echo "Network creating failed";
  exit 1;
else
  echo "Create $mainnet_fork_name network";
fi

brownie test --network "$mainnet_fork_name"
tests_exit_code="$?"
brownie networks delete "$mainnet_fork_name"

if [ "$tests_exit_code" != 0 ]; then
  echo "Tests running failed";
  exit 1;
else
  echo "Tests finished success";
  exit 0;
fi