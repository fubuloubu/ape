import json

import pytest

from ape import Contract
from ape.contracts import ContractInstance
from ape.exceptions import ChainError

"""NOTE: This is testing Contract with a capital C."""


def test_Contract_from_abi(contract_instance):
    contract = Contract(contract_instance.address, abi=contract_instance.contract_type.abi)
    assert isinstance(contract, ContractInstance)
    assert contract.address == contract_instance.address
    assert contract.myNumber() == 0
    assert contract.balance == 0


def test_Contract_from_abi_list(contract_instance):
    contract = Contract(
        contract_instance.address,
        abi=[abi.model_dump() for abi in contract_instance.contract_type.abi],
    )

    assert isinstance(contract, ContractInstance)
    assert contract.address == contract_instance.address
    assert contract.myNumber() == 0


def test_Contract_from_json_str(contract_instance):
    contract = Contract(
        contract_instance.address,
        abi=json.dumps([abi.model_dump() for abi in contract_instance.contract_type.abi]),
    )

    assert isinstance(contract, ContractInstance)
    assert contract.address == contract_instance.address
    assert contract.myNumber() == 0


def test_Contract_from_json_str_retrieval_check_fails(mocker, chain, vyper_contract_instance):
    """
    Tests a bug when providing an abi= but fetch-attempt raises that we don't
    raise since the abi was already given.
    """
    # Make `.get()` fail.
    orig = chain.contracts.get
    mock_get = mocker.MagicMock()
    mock_get.side_effect = Exception

    abi_str = json.dumps([abi.model_dump() for abi in vyper_contract_instance.contract_type.abi])

    chain.contracts.get = mock_get
    try:
        contract = Contract(vyper_contract_instance.address, abi=abi_str)
    finally:
        chain.contracts.get = orig

    # Mostly, we are asserting it did not fail.
    assert isinstance(contract, ContractInstance)


def test_Contract_from_file(contract_instance, project):
    """
    need feedback about the json file specifications
    """
    json_abi_file = project.sources.lookup("contract_abi.json")
    address = contract_instance.address
    contract = Contract(address, abi=json_abi_file)

    assert isinstance(contract, ContractInstance)
    assert contract.address == address
    assert contract.myNumber() == 0


def test_Contract_at_unknown_address(networks_connected_to_tester, address):
    _ = networks_connected_to_tester  # Need fixture or else get ProviderNotConnectedError
    with pytest.raises(ChainError, match=f"Failed to get contract type for address '{address}'."):
        Contract(address)


def test_Contract_specify_contract_type(
    vyper_contract_instance, solidity_contract_instance, owner, networks_connected_to_tester
):
    """
    When specifying a contract type, it merges it with the existing cached contract-type.
    """
    # Solidity's contract type is very close to Vyper's.
    # This test purposely uses the other just to show we are able to specify it externally.
    solidity_contract_type = solidity_contract_instance.contract_type
    contract = Contract(vyper_contract_instance.address, contract_type=solidity_contract_type)
    assert contract.address == vyper_contract_instance.address

    abis = [abi.name for abi in contract.contract_type.abi if hasattr(abi, "name")]
    assert "setNumber" in abis  # Shared ABI.
    assert "ACustomError" in abis  # SolidityContract-defined ABI.
