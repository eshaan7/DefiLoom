from decimal import Decimal


def get_token_value_as_float(
    token_amount: str, token_decimals: int = 18
) -> str:  # 18 is the most common
    return float(Decimal(token_amount) / (Decimal(10) ** token_decimals))
