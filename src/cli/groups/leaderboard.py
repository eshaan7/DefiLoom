import click

from ..types import ClickContext

from .arbitrage import parse_and_display_arbitrage_table
from .lp_apy import parse_and_display_lp_apy_table


@click.command("leaderboard")
@click.pass_context
def leaderboard(ctx: ClickContext):
    """
    Display Arbitrage and LP APY leaderboards
    """

    # Arbitrage

    try:
        uniswapv2_tokens = ctx.obj.powerloom_uniswapv2.get_tokens()
        sushiswap_tokens = ctx.obj.powerloom_sushiswap.get_tokens()
        quickswap_tokens = ctx.obj.powerloom_quickswap.get_tokens()
    except ctx.obj.powerloom_uniswapv2.PowerloomAPIException as exc:
        raise click.ClickException(str(exc))

    parse_and_display_arbitrage_table(
        uniswapv2_tokens,
        sushiswap_tokens,
        quickswap_tokens,
        title="Arbitrage Leaderboard [Top 10]",
    )

    # LP APY

    try:
        uniswapv2_pairs = ctx.obj.powerloom_uniswapv2.get_pairs()
        sushiswap_pairs = ctx.obj.powerloom_sushiswap.get_pairs()
        quickswap_pairs = ctx.obj.powerloom_quickswap.get_pairs()
    except ctx.obj.powerloom_uniswapv2.PowerloomAPIException as exc:
        raise click.ClickException(str(exc))

    parse_and_display_lp_apy_table(
        uniswapv2_pairs,
        sushiswap_pairs,
        quickswap_pairs,
        title="LP APY Leaderboard [Top 10]",
    )