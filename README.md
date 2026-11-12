# Company financials API: income statements, balance sheets, cash flows, business segments, SEC filings and earnings calls

Get the fundamentals of US listed companies from their SEC filings: income statement, balance sheet and cash flow (summary or every line), revenue by business segment, product and region, SEC filings, earnings call transcripts, investor presentations, the company profile and patents. Every example is one request to the [DataPorium](https://dataporium.tech) REST API, shown in Python and curl.

## Quick start

```bash
pip install git+https://github.com/DataPorium/dataporium-python.git
export DATAPORIUM_API_KEY="YOUR_API_KEY"
```

```python
from dataporium import DataPorium, to_frame

dp = DataPorium()   # reads DATAPORIUM_API_KEY
answer = dp.income_statements_summary(symbol="AAPL")
print(to_frame(answer).head())
```

Or run any example below from this repository:

```bash
git clone https://github.com/DataPorium/company-financials-api.git
cd company-financials-api
pip install -r requirements.txt
python examples.py           # list the examples
python examples.py income-statement     # run one
python examples.py income-statement --csv out.csv
```

## What you can get

| Question | Example | Endpoint |
|---|---|---|
| Income statement, main lines, annual and quarterly | [`income-statement`](#income-statement) | `GET /income-statements-summary` |
| Full income statement, every line, annual | [`income-statement-annual`](#income-statement-annual) | `GET /income-statements` |
| Balance sheet, main lines | [`balance-sheet`](#balance-sheet) | `GET /balance-sheet-statements-summary` |
| Cash flow statement, main lines | [`cash-flow`](#cash-flow) | `GET /cash-flow-statements-summary` |
| Which revenue breakdowns a company reports | [`revenue-views`](#revenue-views) | `GET /business-segments/views` |
| Quarterly revenue by product | [`revenue-by-product`](#revenue-by-product) | `GET /business-segments/quarterly` |
| Quarterly revenue by region | [`revenue-by-region`](#revenue-by-region) | `GET /business-segments/quarterly` |
| Every revenue breakdown of one fiscal year, all levels | [`segment-detail`](#segment-detail) | `GET /business-segments/detail` |
| Annual reports (10-K) of a company | [`sec-filings`](#sec-filings) | `GET /sec-filings` |
| Earnings call transcript of one quarter | [`earnings-call`](#earnings-call) | `GET /earnings-transcripts` |
| Investor and earnings presentations | [`presentations`](#presentations) | `GET /presentations` |
| Company profile | [`company-profile`](#company-profile) | `GET /company-info` |
| Industry classification (NAICS, SIC) | [`industry`](#industry) | `GET /industry` |
| Most cited patents of a company since 2020 | [`patents`](#patents) | `GET /patents` |
| Company logo | [`logo`](#logo) | `GET /logo` |

## Financial statements

<a id="income-statement"></a>
### Income statement, main lines, annual and quarterly

```python
dp.income_statements_summary(symbol="AAPL")
```

```bash
curl -H "apikey: $DATAPORIUM_API_KEY" "https://api.dataporium.io/income-statements-summary?symbol=AAPL"
```

Each period holds its lines as `{metric, value}` under `income_statement`, with `period_type` Annual or Quarterly. Add `fiscal_year_qtr=2025Q2`, or `fiscal_year` with `fiscal_qtr`, for one period.

<a id="income-statement-annual"></a>
### Full income statement, every line, annual

```python
dp.income_statements(symbol="AAPL", period_type="Annual")
```

```bash
curl -H "apikey: $DATAPORIUM_API_KEY" "https://api.dataporium.io/income-statements?symbol=AAPL&period_type=Annual"
```

<a id="balance-sheet"></a>
### Balance sheet, main lines

```python
dp.balance_sheet_statements_summary(symbol="MSFT")
```

```bash
curl -H "apikey: $DATAPORIUM_API_KEY" "https://api.dataporium.io/balance-sheet-statements-summary?symbol=MSFT"
```

`balance_sheet_statements` gives every line.

<a id="cash-flow"></a>
### Cash flow statement, main lines

```python
dp.cash_flow_statements_summary(symbol="MSFT")
```

```bash
curl -H "apikey: $DATAPORIUM_API_KEY" "https://api.dataporium.io/cash-flow-statements-summary?symbol=MSFT"
```

`cash_flow_statements` gives every line.

## Revenue breakdown

<a id="revenue-views"></a>
### Which revenue breakdowns a company reports

```python
dp.business_segments_views(symbol="MSFT")
```

```bash
curl -H "apikey: $DATAPORIUM_API_KEY" "https://api.dataporium.io/business-segments/views?symbol=MSFT"
```

Business segments, products and services, regions, countries and more, with how much quarterly history each has.

<a id="revenue-by-product"></a>
### Quarterly revenue by product

```python
dp.business_segments_quarterly(symbol="AAPL", perspective="product", from_date="2023-01-01")
```

```bash
curl -H "apikey: $DATAPORIUM_API_KEY" "https://api.dataporium.io/business-segments/quarterly?symbol=AAPL&perspective=product&from_date=2023-01-01"
```

`perspective` can be segment, product, region, country, end_market, channel, customer or subsegment.

<a id="revenue-by-region"></a>
### Quarterly revenue by region

```python
dp.business_segments_quarterly(symbol="NVDA", perspective="region", from_date="2023-01-01")
```

```bash
curl -H "apikey: $DATAPORIUM_API_KEY" "https://api.dataporium.io/business-segments/quarterly?symbol=NVDA&perspective=region&from_date=2023-01-01"
```

<a id="segment-detail"></a>
### Every revenue breakdown of one fiscal year, all levels

```python
dp.business_segments_detail(symbol="PFE", fiscal_type="annual")
```

```bash
curl -H "apikey: $DATAPORIUM_API_KEY" "https://api.dataporium.io/business-segments/detail?symbol=PFE&fiscal_type=annual"
```

## Filings, calls and presentations

<a id="sec-filings"></a>
### Annual reports (10-K) of a company

```python
dp.sec_filings(symbol="AAPL", form_type="10-K")
```

```bash
curl -H "apikey: $DATAPORIUM_API_KEY" "https://api.dataporium.io/sec-filings?symbol=AAPL&form_type=10-K"
```

Any form type: 10-Q, 8-K and others.

<a id="earnings-call"></a>
### Earnings call transcript of one quarter

```python
dp.earnings_transcripts(symbol="AAPL", year=2025, quarter="Q2")
```

```bash
curl -H "apikey: $DATAPORIUM_API_KEY" "https://api.dataporium.io/earnings-transcripts?symbol=AAPL&year=2025&quarter=Q2"
```

<a id="presentations"></a>
### Investor and earnings presentations

```python
dp.presentations(symbol="AAPL")
```

```bash
curl -H "apikey: $DATAPORIUM_API_KEY" "https://api.dataporium.io/presentations?symbol=AAPL"
```

## Company profile and more

<a id="company-profile"></a>
### Company profile

```python
dp.company_info(symbol="AAPL")
```

```bash
curl -H "apikey: $DATAPORIUM_API_KEY" "https://api.dataporium.io/company-info?symbol=AAPL"
```

<a id="industry"></a>
### Industry classification (NAICS, SIC)

```python
dp.industry(symbol="AAPL")
```

```bash
curl -H "apikey: $DATAPORIUM_API_KEY" "https://api.dataporium.io/industry?symbol=AAPL"
```

<a id="patents"></a>
### Most cited patents of a company since 2020

```python
dp.patents(symbol="NVDA", year_from=2020, sort="cited_by", order="desc", limit=25)
```

```bash
curl -H "apikey: $DATAPORIUM_API_KEY" "https://api.dataporium.io/patents?symbol=NVDA&year_from=2020&sort=cited_by&order=desc&limit=25"
```

<a id="logo"></a>
### Company logo

```python
dp.logo(symbol="AAPL")
```

```bash
curl -H "apikey: $DATAPORIUM_API_KEY" "https://api.dataporium.io/logo?symbol=AAPL"
```

## Answers

Every answer is JSON. Many are a list of rows; paged answers hold their rows under `rows` with `total`, `limit` and `offset`. `to_frame(answer)` in the Python library finds the rows and returns a pandas DataFrame. Each endpoint and all of its parameters are described in the [API documentation](https://dataporium.tech/api-docs), and `print(dp.describe("<method>"))` shows them in Python.

## Use it in Claude, ChatGPT or Cursor

With the [DataPorium MCP server](https://github.com/DataPorium/dataporium-mcp), Claude, ChatGPT or Cursor can read the statements, segments and transcripts for you: "What did Nvidia report last quarter, and how did data center revenue change?"

## Ready-made scripts

- [company-financials-to-excel](https://github.com/DataPorium/company-financials-to-excel): statements of many companies to one Excel workbook

## Get an API key

Sign up at [dataporium.tech](https://dataporium.tech/pricing) and subscribe to the Premium plan; the key is in your account settings. It works for the REST API (600 requests per minute) and the MCP server. Send it in the `apikey` header, as above; a `?apikey=` query parameter also works, but a key in a URL can end up in logs. Keep the key out of code you commit or share.

## More

- Python library: [dataporium-python](https://github.com/DataPorium/dataporium-python)
- JavaScript and TypeScript library: [dataporium-js](https://github.com/DataPorium/dataporium-js)
- Examples in curl, R, Google Sheets and Excel: [financial-data-api](https://github.com/DataPorium/financial-data-api)
- AI assistants: [dataporium-mcp](https://github.com/DataPorium/dataporium-mcp)
- API documentation: <https://dataporium.tech/api-docs>

## License

The code in this repository is released under the [MIT License](LICENSE). Use of the API and its data is governed by the DataPorium [Terms of Use](https://dataporium.tech/terms-of-use). Data is for information only and is not investment advice.
