import requests
import typing as t
from solana.rpc.api import Client
import json
client = Client('https://api.mainnet-beta.solana.com')
base_url = "https://api.saber.so/api/v1/"

Address = str


class SaberException(Exception):
    pass


class SaberPoolTokenInfo(t.TypedDict):
    ticker: str
    name: str

    # address for underlying mint address (eg, USDT)
    underlying_address: str

    # Saber reserve account address
    reserve_address: str

    # amount in Saber reserve
    reserve_amount: float

    # owner address for this token
    owner: str


class SaberPoolInfo(t.TypedDict):
    # id of pool
    ticker: str

    # nice name
    name: str

    # address of pool account, called swapAccount in Saber
    pool_address: str

    lp_token_address: str
    lp_token_supply: float

    token_a: SaberPoolTokenInfo
    token_b: SaberPoolTokenInfo


account_info_cache: t.Dict[Address, t.Any] = {}


def get_account_info(address: str, use_cache=True):
    if use_cache and address in account_info_cache:
        return account_info_cache[address]

    val = client.get_account_info(address, encoding='jsonParsed')['result']['value']['data']['parsed']['info']
    account_info_cache[address] = val
    return val


def get_token_from_swap_state(state, ticker: str, name: str) -> SaberPoolTokenInfo:
    underlying_address = state['mint']
    reserve_address = state['reserve']

    reserve_account_info = get_account_info(reserve_address)
    reserve_amount = float(reserve_account_info['tokenAmount']['uiAmountString'])
    owner = reserve_account_info['owner']

    return SaberPoolTokenInfo(
        ticker=ticker,
        name=name,
        underlying_address=underlying_address,
        reserve_address=reserve_address,
        reserve_amount=reserve_amount,
        owner=owner
    )


def get_pools():
    url = f"{base_url}getPoolsInfo"
    res = requests.get(url)
    res = res.json()
    status = res['status']

    if status != 'ok':
        raise SaberException(f"Return status: {status}")

    data = res['data']

    # TODO: rate limits on Solana API are at 100 per 10s
    pools = data['pools'][:4]

    pool_records: t.Dict[Address, SaberPoolInfo] = {}

    for pool in pools:
        id = pool['id']
        name = pool['name']
        address = pool['swap']['config']['swapAccount']
        state = pool['swap']['state']
        lp_token_address = pool['lpToken']['address']
        lp_token_info = get_account_info(lp_token_address)
        lp_token_supply = int(lp_token_info['supply']) / (10 ** lp_token_info['decimals'])
        token_a_address = state['tokenA']['mint']
        token_b_address = state['tokenB']['mint']
        token_a = next(filter(lambda t: t['address'] == token_a_address, pool['tokens']))
        token_b = next(filter(lambda t: t['address'] == token_b_address, pool['tokens']))
        token_a = get_token_from_swap_state(state['tokenA'], ticker=token_a['symbol'], name=token_a['name'])
        token_b = get_token_from_swap_state(state['tokenB'], ticker=token_b['symbol'], name=token_b['name'])

        s = SaberPoolInfo(
            ticker=id,
            name=name,
            pool_address=address,
            lp_token_address=lp_token_address,
            lp_token_supply=lp_token_supply,
            token_a=token_a,
            token_b=token_b,
        )

        pool_records[address] = s

    return pool_records


if __name__ == '__main__':
    records = get_pools()
    print(json.dumps(records, indent=2))
