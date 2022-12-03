def get_version_number() -> str:
    from .. import version

    return version.__version__


slug_name_map = {
    "uniswapv2": "UniswapV2",
    "sushiswap": "Sushiswap",
    "quickswap": "Quickswap",
}


def price_str2float(price_str: str) -> float:
    if isinstance(price_str, float):
        return price_str
    return float(price_str.replace(",", "").split("US$")[1])


def get_percentage_increase(num_a, num_b):
    try:
        return (abs(num_a - num_b) / num_b) * 100
    except ZeroDivisionError:
        return float("inf")


def calculate_lp_apy(fees_24h: float, total_liquidity: float) -> float:
    try:
        return (fees_24h * 365 / total_liquidity) * 100
    except ZeroDivisionError:
        return 0
