import click
from itertools import zip_longest, permutations
from collections import defaultdict

from ..renderables import display_arbitrage_table
from ..types import ClickContext
from ..utils import slug_name_map, price_str2float, get_percentage_increase


@click.command("arbitrage")
@click.argument(
    "erc20_symbol_or_address",
    required=True,
    type=click.STRING,
)
@click.pass_context
def arbitrage(ctx: ClickContext, erc20_symbol_or_address: str):
    """
    Display Arbitrage opportunity for a specific ERC-20 token.

    ERC20_SYMBOL_OR_ADDRESS is ERC-20 token contract address or symbol.
    """

    method_name = (
        "get_token_info_from_address"
        if erc20_symbol_or_address.startswith("0x")
        else "get_token_info_from_symbol"
    )

    try:
        uniswapv2_token = getattr(ctx.obj.powerloom_uniswapv2, method_name)(
            erc20_symbol_or_address
        )
        sushiswap_token = getattr(ctx.obj.powerloom_sushiswap, method_name)(
            erc20_symbol_or_address
        )
        quickswap_token = getattr(ctx.obj.powerloom_quickswap, method_name)(
            erc20_symbol_or_address
        )
    except ctx.obj.powerloom_uniswapv2.PowerloomAPIException as exc:
        raise click.ClickException(str(exc))

    prices = {}
    if uniswapv2_token:
        prices["uniswapv2"] = price_str2float(uniswapv2_token["price"])
    if sushiswap_token:
        prices["sushiswap"] = price_str2float(sushiswap_token["price"])
    if quickswap_token:
        prices["quickswap"] = price_str2float(quickswap_token["price"])

    if not prices:
        click.echo("Token not found.")
        return
    if len(prices.keys()) <= 1:
        # can't arbitrage if not found on multiple
        click.echo("Token only found on 1 DEX. Can't arbitrage.")
        return

    where_max = max(prices, key=prices.get)
    where_min = min(prices, key=prices.get)
    strategy = f"[green]Buy[/] on {slug_name_map[where_min]}, [red]Sell[/] on {slug_name_map[where_max]}"
    max_price_diff = max(
        round(get_percentage_increase(protocol1_price, protocol2_price), 2)
        for protocol1_price, protocol2_price in permutations(prices.values(), 2)
    )

    table_data = [
        {
            "currency": uniswapv2_token["name"],
            "symbol": uniswapv2_token["symbol"],
            "uniswapv2_price": uniswapv2_token.get("price", "-"),
            "sushiswap_price": sushiswap_token.get("price", "-"),
            "quickswap_price": quickswap_token.get("price", "-"),
            "max_price_diff": max_price_diff,
            "strategy": strategy,
        }
    ]

    display_arbitrage_table(
        table_data,
        title=f"Arbitrage opportunity for [blue]{erc20_symbol_or_address}[/]",
    )


def parse_and_display_arbitrage_table(
    uniswapv2_tokens, sushiswap_tokens, quickswap_tokens, title
) -> None:
    table_data = []
    tokens_map = defaultdict(dict)

    for u_token, s_token, q_token in zip_longest(
        uniswapv2_tokens, sushiswap_tokens, quickswap_tokens
    ):
        if u_token:
            tokens_map[u_token["symbol"]]["uniswapv2"] = u_token
        if s_token:
            tokens_map[s_token["symbol"]]["sushiswap"] = s_token
        if q_token:
            tokens_map[q_token["symbol"]]["quickswap"] = q_token

    for symbol, token_info_protocol_map in tokens_map.items():
        if len(token_info_protocol_map.keys()) <= 1:
            # can't arbitrage if not found on multiple
            continue

        first_available_protocol = list(token_info_protocol_map.keys())[0]
        uniswapv2_token = token_info_protocol_map.get("uniswapv2")
        sushiswap_token = token_info_protocol_map.get("sushiswap")
        quickswap_token = token_info_protocol_map.get("quickswap")

        prices = {}
        if uniswapv2_token:
            prices["uniswapv2"] = price_str2float(uniswapv2_token["price"])
        if sushiswap_token:
            prices["sushiswap"] = price_str2float(sushiswap_token["price"])
        if quickswap_token:
            prices["quickswap"] = price_str2float(quickswap_token["price"])

        if 0 in prices.values():
            # assuming that 0 price means no liquidity
            continue

        where_max = max(prices, key=prices.get)
        where_min = min(prices, key=prices.get)
        strategy = f"[green]Buy[/] on {slug_name_map[where_min]}, [red]Sell[/] on {slug_name_map[where_max]}"
        max_price_diff = max(
            round(get_percentage_increase(protocol1_price, protocol2_price), 2)
            for protocol1_price, protocol2_price in permutations(prices.values(), 2)
        )
        table_data.append(
            {
                "currency": token_info_protocol_map[first_available_protocol]["name"][
                    :15
                ],
                "symbol": symbol,
                "uniswapv2_price": prices.get("uniswapv2", "-"),
                "sushiswap_price": prices.get("sushiswap", "-"),
                "quickswap_price": prices.get("quickswap", "-"),
                "max_price_diff": max_price_diff,
                "strategy": strategy,
            }
        )

    table_data = sorted(table_data, key=lambda k: k["max_price_diff"], reverse=True)

    display_arbitrage_table(table_data, title=title)
