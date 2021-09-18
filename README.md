# Scraper

Get data about tokens & pools

## Usage

Requires Python 3.8+

```bash
pip install -r requirements.txt
python saber/saber.py
```

Will print out the pools on Saber, with the associated tokens. Example output, keyed by pool account address:

```json
{
  "YAkoNb6HKmSxQN9L8hiBE5tPJRsniSSMzND1boHmZxe": {
    "ticker": "usdc_usdt",
    "name": "USDT-USDC",
    "pool_address": "YAkoNb6HKmSxQN9L8hiBE5tPJRsniSSMzND1boHmZxe",
    "lp_token_address": "2poo1w1DL6yd2WNTCnNTzDqkC6MBXq7axo77P16yrBuf",
    "lp_token_supply": 694486701.998307,
    "token_a": {
      "ticker": "USDC",
      "name": "USD Coin",
      "underlying_address": "EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v",
      "reserve_address": "CfWX7o2TswwbxusJ4hCaPobu2jLCb1hfXuXJQjVq3jQF",
      "reserve_amount": 338311153.386994,
      "owner": "5C1k9yV7y4CjMnKv8eGYDgWND8P89Pdfj79Trk2qmfGo"
    },
    "token_b": {
      "ticker": "USDT",
      "name": "USDT",
      "underlying_address": "Es9vMFrzaCERmJfrF4H2FYD4KCoNkY11McCe8BenwNYB",
      "reserve_address": "EnTrdMMpdhugeH6Ban6gYZWXughWxKtVGfCwFn78ZmY3",
      "reserve_amount": 371225939.335142,
      "owner": "5C1k9yV7y4CjMnKv8eGYDgWND8P89Pdfj79Trk2qmfGo"
    }
  }
}
```

## Roadmap

Next up: Raydium
