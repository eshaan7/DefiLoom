from rich.console import Console
from rich.table import Table
from rich.panel import Panel


def display_arbitrage_table(table_data: list, title: str) -> None:

    table_data = table_data[:10]

    table = Table(title=title)
    table.add_column("Currency")
    table.add_column("Symbol")
    table.add_column("UniswapV2 Price (USD)")
    table.add_column("Sushiswap Price (USD)")
    table.add_column("Quickswap Price (USD)")
    table.add_column("Max Price Difference (%) ⬇️")
    table.add_column("🤑 Strategy 🤑")

    for row_data in table_data:
        table.add_row(*[str(v) for v in row_data.values()])

    panels = [Panel(table)]
    console = Console()
    for p in panels:
        console.print(p, justify="center")


def display_lp_apy_table(table_data: list, title: str) -> None:

    table = Table(title=title)
    table.add_column("Pair Name")
    table.add_column("UniswapV2 LP APY (%)")
    table.add_column("Sushiswap LP APY (%)")
    table.add_column("Quickswap LP APY (%)")
    table.add_column("Max LP APY (%) ⬇️")
    table.add_column("🤑 Strategy 🤑")

    for row_data in table_data:
        table.add_row(*[str(v) for v in row_data.values()])

    panels = [Panel(table)]
    console = Console()
    for p in panels:
        console.print(p, justify="center")
