import asyncio
import json

import typer
from typing import Annotated, Optional

from communex._common import get_node_url  # type: ignore
from communex.client import CommuneClient  # type: ignore
from communex.compat.key import classic_load_key  # type: ignore
from communex.module.client import ModuleClient
from communex.types import Ss58Address
from config import settings
from subnet.common.registry_client import RegistryClient
from .validator._config import ValidatorSettings
from subnet.validator.validator import DippyValidator

# from .evaluator.evaluator import another
app = typer.Typer()

from substrateinterface import Keypair, KeypairType
import sr25519

TESTNET_URL = "wss://testnet-commune-api-node-0.communeai.net"
TESTNET_UID = 27
TESTNET_REGISTRY_KEY = "5Exsj2WLrVqAeoRKPKGKmAX3HCsiPwb4LNy6975xCJUKWMp7"
TESTNET_REGISTRY_URL = "35.182.195.207"


@app.command("validator")
def validator(
    commune_key: Annotated[
        str, typer.Argument(help="Name of the key present in `~/.commune/key`")
    ],
    call_timeout: int = 65,
    use_testnet: Annotated[
            bool, typer.Option("--use-testnet", "-t", help="Use testnet instead of mainnet")
        ] = False,
):
    keypair = classic_load_key(commune_key)  # type: ignore
    validator_settings = ValidatorSettings()  # type: ignore
    print(f"use_testnet {use_testnet}")
    c_client = CommuneClient(TESTNET_URL)
    if not use_testnet:
        c_client = CommuneClient(get_node_url())
    # subnet_uid = get_subnet_netuid("dippy")
    subnet_uid = TESTNET_UID
    validator = DippyValidator(
        call_timeout=call_timeout,
        key=keypair,
        netuid=subnet_uid,
        client=c_client,
    )
    validator.validation_loop(validator_settings)


"""
For a miner, register a model
"""


@app.command("register")
def register(
    commune_key: Annotated[
        str, typer.Argument(help="Name of the key present in `~/.commune/key`")
    ],
    registry_address: Annotated[
        str,
        typer.Option(
            "--registry-address", "-r", help="Address of the registry (optional)"
        ),
    ] = "",
):
    keypair = classic_load_key(commune_key)  # type: ignore
    destination = Ss58Address(settings.testnet_registry_key)

    # message = b"million dollar baby"
    request_body = {"repo_namespace": "teknium", "repo_name": "OpenHermes"}
    json_body = json.dumps(request_body)
    message = json_body.encode()

    signed_data = sr25519.sign(  # type: ignore
        (keypair.public_key, keypair.private_key), message
    )
    hexstring = signed_data.hex()
    client = RegistryClient(keypair, True).module_client()

    try:
        # handles the communication with the miner
        miner_answer = asyncio.run(
            client.call(
                "register",
                destination,
                {
                    "commit": message.decode("utf-8"),
                    "ss58": keypair.ss58_address,
                    "signature": hexstring,
                },
            )
        )
        print(miner_answer)
        print("x")
        pass

    except Exception as e:
        print("error calling module")
        print(e)
    print("ayy lmao")


@app.command("entry")
def entry(
    commune_key: Annotated[
        str, typer.Argument(help="Name of the key present in `~/.commune/key`")
    ],
):
    keypair = classic_load_key(commune_key)  # type: ignore
    destination = Ss58Address(TESTNET_REGISTRY_KEY)

    client = RegistryClient(keypair, True).client()
    try:
        # handles the communication with the miner
        miner_answer = asyncio.run(
            client.call(
                "get_entry",
                destination,
                {
                    "key": keypair.ss58_address,
                },
            )
        )
        print(miner_answer)
        print("x")
        pass

    except Exception as e:
        print("error calling module")
        print(e)
    print("ayy lmao")


@app.command("debug")
def debug(
    commune_key: Annotated[
        str, typer.Argument(help="Name of the key present in `~/.commune/key`")
    ],
    # model_name: Optional[
    #     str, typer.Argument(help="Name of the key present in `~/.commune/key`")
    # ],
):
    keypair = classic_load_key(commune_key)  # type: ignore
    c_client = CommuneClient(TESTNET_URL)
    message = "this is mine"
    address_of_registry = ""
    newkey = Keypair(
        ss58_address="5GNLjDNYPAcm4LV9mHRK5K9cYf4FvZdpBEDcojFAY5farF11",
        crypto_type=KeypairType.ED25519,
    )
    keypair.encrypt_message(message, keypair)
    module_ip = "127.0.0.1"
    port = 9999
    block = c_client.get_block()
    print(block)
    # keypair.public_key
    client = ModuleClient(module_ip, port, keypair)

    stake = c_client.get_stake(f, netuid=0)
    print(f"stake for is {stake}")
    # print("created client, making call")
    try:
        # handles the communication with the miner
        # miner_answer = asyncio.run(
        #     client.call(
        #         "model_submission",
        #         f,
        #         {"prompt": "x"},
        #     )
        # )
        # print(miner_answer)
        # another()
        print("x")
        pass

    except Exception as e:
        print(e)
    print("ayy lmao")


if __name__ == "__main__":
    app()
