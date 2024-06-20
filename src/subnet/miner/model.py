from communex.client import CommuneClient
from communex.compat.key import classic_load_key
from communex.module import Module, endpoint
from communex.key import generate_keypair, check_ss58_address
from fastapi import Header
from keylimiter import TokenBucketLimiter
from substrateinterface.utils.ss58 import ss58_encode

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

class Miner(Module):

    def __init__(self):
        super().__init__()
        self.filepath = "./data/model_submission.json"
        self.client = CommuneClient(TESTNET_URL)
        self.netuid = 0

    """
    A module class for mining and generating responses to prompts.

    Attributes:
        None

    Methods:
        generate: Generates a response to a given prompt using a specified model.
    """
    @endpoint
    def model_submission(
            self,
            competition_id: str = "",
            caller_key: str = Header(None, alias='x-key')):
        if not is_hex_string(caller_key):
            return None
        key = parse_hex(caller_key)

        ss58 = try_ss58_decode(key)
        stake = self.client.get_stake(ss58, self.netuid)
        print(f"stake for {ss58} is stake")

        """
        Generates a response to a given prompt using a specified model.

        Args:
            prompt: The prompt to generate a response for.
            model: The model to use for generating the response (default: "gpt-3.5-turbo").

        Returns:
            None
        """
        import os
        import json
        try:
            with open(self.filepath, 'r') as file:
                return json.load(file)
        except Exception as e:
            print(e)
            return None



if __name__ == "__main__":
    """
    Example
    """
    from communex.module.server import ModuleServer
    import uvicorn

    key = generate_keypair()
    miner = Miner()
    refill_rate = 1 / 400
    # Implementing custom limit
    bucket = TokenBucketLimiter(2, refill_rate)
    server = ModuleServer(miner, key, ip_limiter=bucket, subnets_whitelist=[3])
    app = server.get_fastapi_app()

    # Only allow local connections
    uvicorn.run(app, host="127.0.0.1", port=8000)
