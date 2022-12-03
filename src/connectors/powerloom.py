from functools import cached_property, cache
from typing import Optional, Literal

import requests

from .types import Address
from .exceptions import PowerloomAPIException


class PowerloomAPI:

    PowerloomAPIException = PowerloomAPIException
    base_url_format = "https://{protocol}.powerloom.io/api"

    def __init__(
        self,
        api_key: str,
        protocol: Literal[
            "uniswapv2-ethindia", "sushiswap-ethindia", "quickswap-ethindia"
        ] = "uniswapv2-ethindia",
    ) -> None:
        self._protocol = protocol
        self.__api_key = api_key

    def _request(
        self,
        path: str,
        data: Optional[dict] = None,
    ) -> requests.Response:
        if data is None:
            data = {}
        response: requests.Response = None
        try:
            api_url = self.base_url_format.format(protocol=self._protocol)
            urlpath = f"{api_url}/{path}"
            response = requests.get(
                url=urlpath,
                data=data,
                headers={
                    "User-Agent": "example-cli",
                    "Content-Type": "application/json",
                    "X-API-KEY": self.__api_key,
                },
            )
            response.raise_for_status()
        except requests.RequestException as exc:
            raise PowerloomAPIException(exc)

        return response

    @cache
    def get_tokens(self) -> list:
        path = "v2-tokens"
        response = self._request(path)
        return response.json()

    @cache
    def get_pairs(self) -> list:
        path = "v2-pairs"
        response = self._request(path)
        return response.json()

    @cache
    def get_pairs_for_erc20(self, erc20_symbol: str) -> list:
        pairs = []
        for p in self.get_pairs():
            if erc20_symbol in p["name"]:
                pairs.append(p)
        return pairs

    def get_token_info_from_address(self, token_contract_address: Address) -> dict:
        path = f"v2-token/{token_contract_address}"
        response = self._request(path)
        return response.json()["data"] or {}

    def get_token_info_from_symbol(self, erc20_symbol: str) -> dict:
        token = {}
        for t in self.get_tokens():
            if erc20_symbol == t["symbol"]:
                token = t
                break
        return token

    def get_token_price(self, token_contract_address: Address) -> float:
        token_info = self.get_token_info(token_contract_address)
        return token_info["price"]

    @cached_property
    def ETHUSD_PRICE(self) -> float:
        weth_contract_address = "0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2"
        token_info = self.get_token_info(weth_contract_address)
        return token_info["price"]
