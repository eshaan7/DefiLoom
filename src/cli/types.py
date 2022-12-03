from typing import NamedTuple

import click

from src.connectors import PowerloomAPI


class ClickContextCustomObject(NamedTuple):
    powerloom_uniswapv2: PowerloomAPI
    powerloom_sushiswap: PowerloomAPI
    powerloom_quickswap: PowerloomAPI


class ClickContext(click.Context):
    obj: ClickContextCustomObject
