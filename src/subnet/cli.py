import asyncio

import typer
from typing import Annotated, Optional

from communex._common import get_node_url  # type: ignore
from communex.client import CommuneClient  # type: ignore
from communex.compat.key import classic_load_key  # type: ignore
from communex.module.client import ModuleClient
from communex.types import Ss58Address

from .validator._config import ValidatorSettings
from .validator.validator import get_subnet_netuid, DippyValidator
# from .evaluator.evaluator import another
app = typer.Typer()

from substrateinterface import Keypair, KeypairType
import sr25519

@app.command("validator")
def validator(
    commune_key: Annotated[
        str, typer.Argument(help="Name of the key present in `~/.commune/key`")
    ],
    call_timeout: int = 65,
):
    keypair = classic_load_key(commune_key)  # type: ignore
    settings = ValidatorSettings()  # type: ignore
    c_client = CommuneClient(get_node_url())
    subnet_uid = get_subnet_netuid("dippy")
    validator = DippyValidator(
        keypair,
        subnet_uid,
        c_client,
        call_timeout=call_timeout,
    )
    validator.validation_loop(settings)

TESTNET_URL="wss://testnet-commune-api-node-0.communeai.net"



@app.command("register")
def register(
    commune_key: Annotated[
        str, typer.Argument(help="Name of the key present in `~/.commune/key`")
    ],
):
    keypair = classic_load_key(commune_key)  # type: ignore
    destination = Ss58Address("5GNLjDNYPAcm4LV9mHRK5K9cYf4FvZdpBEDcojFAY5farF11")

    message = b'million dollar baby'

    signed_data = sr25519.sign(  # type: ignore
        (keypair.public_key, keypair.private_key), message)
    hexstring = signed_data.hex()

    module_ip = "127.0.0.1"
    port = 9769

    client = ModuleClient(module_ip, port, keypair)
    try:
        # handles the communication with the miner
        miner_answer = asyncio.run(
            client.call(
                "register",
                destination,
                {
                    "commit": message.decode('utf-8'),
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
    destination = Ss58Address("5GNLjDNYPAcm4LV9mHRK5K9cYf4FvZdpBEDcojFAY5farF11")

    module_ip = "127.0.0.1"
    port = 9769

    client = ModuleClient(module_ip, port, keypair)
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
    newkey = Keypair(ss58_address="5GNLjDNYPAcm4LV9mHRK5K9cYf4FvZdpBEDcojFAY5farF11", crypto_type=KeypairType.ED25519)
    keypair.encrypt_message(message, keypair)
    module_ip = "127.0.0.1"
    port = 9999
    block = c_client.get_block()
    print(block)
    # keypair.public_key
    client = ModuleClient(module_ip, port, keypair)

    stake = c_client.get_stake(f, netuid=0)
    print(f"stake for {f} is {stake}")
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
