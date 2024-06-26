import datetime

from communex.client import CommuneClient
from communex.compat.key import classic_load_key
from communex.module import Module, endpoint
from communex.key import generate_keypair, check_ss58_address
from communex.module._rate_limiters.limiters import StakeLimiterParams, IpLimiterParams
from fastapi import Header, Request
from keylimiter import TokenBucketLimiter
from substrateinterface import Keypair, KeypairType
from substrateinterface.utils.ss58 import ss58_encode
from cachetools import LRUCache
from util.event_logger import EventLogger
import re

HEX_PATTERN = re.compile(r"^[0-9a-fA-F]+$")
def is_hex_string(string: str):
    return bool(HEX_PATTERN.match(string))

def parse_hex(hex_str: str) -> bytes:
    if hex_str[0:2] == "0x":
        return bytes.fromhex(hex_str[2:])
    else:
        return bytes.fromhex(hex_str)

def try_ss58_decode(key: bytes | str):
    ss58_format = 42
    try:
        ss58 = ss58_encode(key, ss58_format)
        ss58 = check_ss58_address(ss58, ss58_format)
    except Exception:
        return None
    return ss58

TESTNET_URL="wss://testnet-commune-api-node-0.communeai.net"

class MinerRegistry(Module):

    def __init__(self):
        super().__init__()
        self.filepath = "./data/model_submission.json"
        self.client = CommuneClient(TESTNET_URL)
        self.netuid = 27
        # Double the amount of registrable keys
        self.registry = LRUCache(maxsize=1640)
        self.logger = EventLogger()


    """
    A module class for mining and generating responses to prompts.

    Attributes:
        None

    Methods:
        generate: Generates a response to a given prompt using a specified model.
    """
    @endpoint
    def get_entry(
            self,
            key: str,
            ):
        result = self.registry.get(key, None)
        self.logger.info("entry", result=result)
        return result



    @endpoint
    def register(self,
                 signature: str,
                 commit: str,
                 ss58: str, ):
        try:
            verified = self._register_model(signature, commit, ss58)
            result = {"commit": commit, "verified": verified, "entry": ss58}
            self.logger.info("registered", result=result)
            return result
        except Exception as e:
            return {"verified": False}


    def _register_model(
            self,
            signature: str,
            commit: str,
            ss58: str,
            ):

        newkey = Keypair(
            ss58_address=ss58,
            crypto_type=KeypairType.SR25519,
        )
        raw_sig_data = bytes.fromhex(signature)
        verified = newkey.verify(commit, raw_sig_data)
        now = datetime.datetime.utcnow().isoformat()
        if verified:
            self.registry[ss58] = {
                "time": now,
                "data": commit,
            }
        return verified


def cli(
        keyname: str,
):

    keypair = classic_load_key(keyname)
    # if test_mode:
    #     subnets_whitelist = None
    # token_refill_rate = token_refill_rate_base_multiplier or 1
    # limiter_params = IpLimiterParams() if use_ip_limiter else StakeLimiterParams(token_ratio=token_refill_rate)
    limiter_params = IpLimiterParams(bucket_size=100)

    m = MinerRegistry()
    server = ModuleServer(
        m, keypair,
        subnets_whitelist=[27],
        limiter=limiter_params,
        use_testnet=True
    )
    app = server.get_fastapi_app()
    host = "0.0.0.0"
    port = 9769
    uvicorn.run(app, host=host, port=port)  # type: ignore



if __name__ == "__main__":
    """
    Example
    """
    from communex.module.server import ModuleServer
    import uvicorn
    cli("key0")
    #
    # key = generate_keypair()
    # miner = MinerRegistry()
    # refill_rate = 1 / 400
    # # Implementing custom limit
    # bucket = TokenBucketLimiter(2, refill_rate)
    # server = ModuleServer(miner, key, ip_limiter=bucket, subnets_whitelist=[3])
    # app = server.get_fastapi_app()
    #
    # # Only allow local connections
    # uvicorn.run(app, host="127.0.0.1", port=8000)
