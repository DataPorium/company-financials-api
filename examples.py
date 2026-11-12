"""Company financials API: income statements, balance sheets, cash flows, business segments, SEC filings and earnings calls

Runnable examples: each one is a single request to the DataPorium API.

    python examples.py                      # list the examples
    python examples.py income-statement
    python examples.py income-statement --csv out.csv
    python examples.py income-statement --json       # the raw answer

Needs a DataPorium API key in the DATAPORIUM_API_KEY environment variable.
"""
from __future__ import annotations

import argparse
import json
import sys

from dataporium import DataPorium, to_frame

# name: (question, method, parameters, key of the rows inside the answer)
EXAMPLES = {
    'income-statement': ('Income statement, main lines, every quarter', 'income_statements_summary', {'symbol': 'AAPL'}, None),
    'income-statement-annual': ('Full income statement, every line, annual', 'income_statements', {'symbol': 'AAPL', 'period_type': 'Annual'}, None),
    'balance-sheet': ('Balance sheet, main lines', 'balance_sheet_statements_summary', {'symbol': 'MSFT'}, None),
    'cash-flow': ('Cash flow statement, main lines', 'cash_flow_statements_summary', {'symbol': 'MSFT'}, None),
    'revenue-views': ('Which revenue breakdowns a company reports', 'business_segments_views', {'symbol': 'MSFT'}, None),
    'revenue-by-product': ('Quarterly revenue by product', 'business_segments_quarterly', {'symbol': 'AAPL', 'perspective': 'product', 'from_date': '2023-01-01'}, None),
    'revenue-by-region': ('Quarterly revenue by region', 'business_segments_quarterly', {'symbol': 'NVDA', 'perspective': 'region', 'from_date': '2023-01-01'}, None),
    'segment-detail': ('Every revenue breakdown of one fiscal year, all levels', 'business_segments_detail', {'symbol': 'PFE', 'fiscal_type': 'annual'}, None),
    'sec-filings': ('Annual reports (10-K) of a company', 'sec_filings', {'symbol': 'AAPL', 'form_type': '10-K'}, None),
    'earnings-call': ('Earnings call transcript of one quarter', 'earnings_transcripts', {'symbol': 'AAPL', 'year': 2025, 'quarter': 'Q2'}, None),
    'presentations': ('Investor and earnings presentations', 'presentations', {'symbol': 'AAPL'}, None),
    'company-profile': ('Company profile', 'company_info', {'symbol': 'AAPL'}, None),
    'industry': ('Industry classification (NAICS, SIC)', 'industry', {'symbol': 'AAPL'}, None),
    'mergers': ('Acquisitions made or received by a company', 'ma_transactions_summary', {'symbol': 'MSFT', 'transaction_classification': 'Acquisition'}, None),
    'patents': ('Most cited patents of a company since 2020', 'patents', {'symbol': 'NVDA', 'year_from': 2020, 'sort': 'cited_by', 'order': 'desc', 'limit': 25}, None),
    'logo': ('Company logo', 'logo', {'symbol': 'AAPL'}, None),
}


def rows(answer, key=None):
    """The answer as a DataFrame, or None when it has no table in it."""
    try:
        frame = to_frame(answer, key=key)
    except (KeyError, TypeError):
        return None
    return frame if len(frame.columns) > 1 or len(frame) > 1 else None


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("example", nargs="?", help="Name of the example; leave out to list them")
    parser.add_argument("--csv", help="Save the rows to this CSV file")
    parser.add_argument("--json", action="store_true", help="Print the raw JSON answer")
    parser.add_argument("--rows", type=int, default=20, help="Rows to print (default 20)")
    args = parser.parse_args(argv)

    if not args.example:
        width = max(len(name) for name in EXAMPLES)
        for name, (question, *_rest) in EXAMPLES.items():
            print(f"{name:<{width}}  {question}")
        return 0
    if args.example not in EXAMPLES:
        parser.error(f"unknown example {args.example!r}; run without arguments to list them")

    question, method, params, key = EXAMPLES[args.example]
    print(f"{question}\n  dp.{method}({', '.join(f'{k}={v!r}' for k, v in params.items())})\n")
    answer = DataPorium().call(method, **params)

    frame = None if args.json else rows(answer, key)
    if frame is None:
        print(json.dumps(answer, indent=2, default=str)[:20000])
    else:
        print(frame.head(args.rows).to_string(max_colwidth=40))
        print(f"\n{len(frame)} rows")
    if args.csv:
        if frame is None:
            frame = rows(answer, key)
        if frame is None:
            print("This answer has no table to save.", file=sys.stderr)
            return 1
        frame.to_csv(args.csv, index=False)
        print(f"Saved {args.csv}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
