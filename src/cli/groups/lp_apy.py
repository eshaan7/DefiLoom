import click
from itertools import zip_longest
from collections import defaultdict

from ..renderables import display_lp_apy_table
from ..types import ClickContext
from ..utils import slug_name_map, price_str2float, calculate_lp_apy


@click.command("lp_apy")
@click.argument(
    "erc20_symbol",
    required=True,
    type=click.STRING,
)
@click.pass_context
def lp_apy(ctx: ClickContext, erc20_symbol: str):
    """
    Display LP APY leaderboard for a specific ERC-20 token.

    ERC20_SYMBOL is ERC is ERC-20 token contract address or symbol.
    """
    try:
        uniswapv2_pairs = ctx.obj.powerloom_uniswapv2.get_pairs_for_erc20(erc20_symbol)
        sushiswap_pairs = ctx.obj.powerloom_sushiswap.get_pairs_for_erc20(erc20_symbol)
        quickswap_pairs = ctx.obj.powerloom_quickswap.get_pairs_for_erc20(erc20_symbol)
    except ctx.obj.powerloom_uniswapv2.PowerloomAPIException as exc:
        raise click.ClickException(str(exc))

    parse_and_display_lp_apy_table(
        uniswapv2_pairs,
        sushiswap_pairs,
        quickswap_pairs,
        title=f"LP APY Leaderboard for [blue]{erc20_symbol}[/]",
    )


def parse_and_display_lp_apy_table(
    uniswapv2_pairs, sushiswap_pairs, quickswap_pairs, title
) -> None:
    table_data = []
    pairs_map = defaultdict(dict)

    for u_pair, s_pair, q_pair in zip_longest(
        uniswapv2_pairs, sushiswap_pairs, quickswap_pairs
    ):
        if u_pair:
            pairs_map[u_pair["name"]]["uniswapv2"] = u_pair
        if s_pair:
            pairs_map[s_pair["name"]]["sushiswap"] = s_pair
        if q_pair:
            pairs_map[q_pair["name"]]["quickswap"] = q_pair

    for pair_name, token_info_protocol_map in pairs_map.items():
        uniswapv2_pair = token_info_protocol_map.get("uniswapv2")
        sushiswap_pair = token_info_protocol_map.get("sushiswap")
        quickswap_pair = token_info_protocol_map.get("quickswap")

        apy_map = {}
        if uniswapv2_pair:
            apy_map["uniswapv2"] = round(
                calculate_lp_apy(
                    price_str2float(uniswapv2_pair["fees_24h"]),
                    price_str2float(uniswapv2_pair["liquidity"]),
                ),
                2,
            )
        if sushiswap_pair:
            apy_map["sushiswap"] = round(
                calculate_lp_apy(
                    price_str2float(sushiswap_pair["fees_24h"]),
                    price_str2float(sushiswap_pair["liquidity"]),
                ),
                2,
            )
        if quickswap_pair:
            apy_map["quickswap"] = round(
                calculate_lp_apy(
                    price_str2float(quickswap_pair["fees_24h"]),
                    price_str2float(quickswap_pair["liquidity"]),
                ),
                2,
            )

        where_max = max(apy_map, key=apy_map.get)
        strategy = f"[green]LP[/] on {slug_name_map[where_max]}"
        table_data.append(
            {
                "pair_name": pair_name,
                "uniswapv2_lp_apy": apy_map.get("uniswapv2", "-"),
                "sushiswap_lp_apy": apy_map.get("sushiswap", "-"),
                "quickswap_lp_apy": apy_map.get("quickswap", "-"),
                "max_lp_apy": max(apy_map.values()),
                "strategy": strategy,
            }
        )

    table_data = sorted(table_data, key=lambda k: k["max_lp_apy"], reverse=True)
    table_data_top_10 = table_data[:10]

    display_lp_apy_table(table_data_top_10, title=title)
