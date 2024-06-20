import asyncio

import typer
from typing import Annotated, Optional

from communex._common import get_node_url  # type: ignore
from communex.client import CommuneClient  # type: ignore
from communex.compat.key import classic_load_key  # type: ignore
from communex.module.client import ModuleClient
from communex.types import Ss58Address

from .validator._config import ValidatorSettings
from .validator.validator import get_subnet_netuid, TextValidator
from .evaluator.evaluator import another
app = typer.Typer()


@app.command("validator")
def serve(
    commune_key: Annotated[
        str, typer.Argument(help="Name of the key present in `~/.commune/key`")
    ],
    call_timeout: int = 65,
):
    keypair = classic_load_key(commune_key)  # type: ignore
    settings = ValidatorSettings()  # type: ignore
    c_client = CommuneClient(get_node_url())
    subnet_uid = get_subnet_netuid("dippy")
    validator = TextValidator(
        keypair,
        subnet_uid,
        c_client,
        call_timeout=call_timeout,
    )
    validator.validation_loop(settings)

TESTNET_URL="wss://testnet-commune-api-node-0.communeai.net"

@app.command("upload")
def upload(
    commune_key: Annotated[
        str, typer.Argument(help="Name of the key present in `~/.commune/key`")
    ],
):
    keypair = classic_load_key(commune_key)  # type: ignore
    c_client = CommuneClient(TESTNET_URL)
    module_ip = "127.0.0.1"
    port = 9999
    block = c_client.get_block()
    print(block)
    # Fetch all validators
    # upload model info for each validator
    # keypair.public_key
    client = ModuleClient(module_ip, port, keypair)
    f = Ss58Address(keypair.ss58_address)
    c_client.compose_call()

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
