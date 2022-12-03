#!/usr/bin/env python3
import click

from .cli.groups import arbitrage, lp_apy, leaderboard
from .cli.types import ClickContext, ClickContextCustomObject
from .cli.utils import get_version_number
from .connectors import PowerloomAPI
from .consts import POWERLOOM_API_KEY


@click.group(context_settings=dict(help_option_names=["-h", "--help"]))
@click.version_option(version=get_version_number())
@click.pass_context
def cli(ctx: ClickContext):
    # this function is always called so we can create our object here
    ctx.obj = ClickContextCustomObject(
        powerloom_uniswapv2=PowerloomAPI(POWERLOOM_API_KEY, "uniswapv2-ethindia"),
        powerloom_sushiswap=PowerloomAPI(POWERLOOM_API_KEY, "sushiswap-ethindia"),
        powerloom_quickswap=PowerloomAPI(POWERLOOM_API_KEY, "quickswap-ethindia"),
    )


# Compile all groups and commands
for c in [leaderboard, arbitrage, lp_apy]:
    cli.add_command(c)

# Entrypoint/executor
if __name__ == "__main__":
    cli()
