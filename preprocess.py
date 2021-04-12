#!/usr/bin/env python3

import csv
import click
import datetime

def get_field_column(header_row, field_name):
    return header_row.index(field_name)

def update_field_in_row(row, update_position, update_value):
    row[update_position] = update_value
    return row

def get_updated_ticker_symbol(original_ts, exchange):
    if exchange == "NSE":
        return "{}.NS".format(original_ts)

    if exchange == "BSE":
        return "{}.BO".format(original_ts)

    return original_ts

def process_csv(csv_in, csv_out, use_exchange):
    header_row = next(csv_in)

    ticker_symbol_column = get_field_column(header_row, "symbol")
    exchange_column = get_field_column(header_row, "exchange")
    quantity_column = get_field_column(header_row, "quantity")
    price_column = get_field_column(header_row, "price")
    trade_date_column = get_field_column(header_row, "trade_date")
    trade_type_column = get_field_column(header_row, "trade_type")

    updated_rows = []

    for row in csv_in:
        exchange = use_exchange if use_exchange != "None" else row[exchange_column]
        ticker_symbol = row[ticker_symbol_column]
        updated_row = update_field_in_row(
            row,
            ticker_symbol_column,
            get_updated_ticker_symbol(ticker_symbol, exchange)
        )

        # the value column is expected to be the total exchange value
        quantity = row[quantity_column]
        price = row[price_column]
        updated_row = update_field_in_row(
            updated_row,
            price_column,
            float(price)*float(quantity)
        )

        updated_rows.append(updated_row)

    # PP doesn't support short selling while importing, so we need to keep buy above sell
    updated_sorted_rows = sorted(
        updated_rows,
        key=lambda x: (
            datetime.datetime.strptime(x[trade_date_column], "%Y-%m-%d"),
            x[ticker_symbol_column],
            x[trade_type_column]
        )
    )

    updated_sorted_rows = [header_row] + updated_sorted_rows
    csv_out.writerows(updated_sorted_rows)

@click.command()
@click.option("--input_csv", prompt="Input file (tradebook csv)")
@click.option("--output_csv", prompt="Output file (for outputting compatible tradebook csv)")
@click.option("--use_exchange", prompt="Fixed exchange to use for all trades", type=click.Choice(["NSE", "BSE", "None"]), default="None")
def init(input_csv, output_csv, use_exchange):
    in_file = open(input_csv, "r")
    out_file = open(output_csv, mode="w")
    csv_in = csv.reader(in_file, delimiter=",")
    csv_out = csv.writer(out_file, delimiter=",")

    process_csv(csv_in, csv_out, use_exchange)

if __name__ == '__main__':
    init()