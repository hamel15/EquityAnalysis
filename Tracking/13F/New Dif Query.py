from sec_api import QueryApi
import pandas as pd
from datetime import datetime

# Define your API key
api_key = "ca463e956b32cb96b919e9af4444456049e47f3ab961bc9fac41c6fe2ed5c1ad"

# Define CIKs
ciks = ["1601086", "1535392", "1559706", "1697591", "1699673", "1745214", "1741129", "1697848","1412741"]

# Create a QueryApi instance
queryApi = QueryApi(api_key=api_key)

# List to store holdings data for first and second filings
holdings_first_filing = []
holdings_second_filing = []

# Loop through each CIK
for cik in ciks:
    # Define the query parameters for the current CIK to get the two most recent filings
    query = {
        "query": f"formType:\"13F-HR\" AND cik:{cik}",
        "from": "0",
        "size": "2",
        "sort": [{"filedAt": {"order": "desc"}}]
    }

    # Get filings using the Query API
    response = queryApi.get_filings(query)

    # Check if filings are available
    if 'filings' in response:
        for i, filing in enumerate(response["filings"]):
            try:
                # Extract relevant data from the response
                company_name = filing["companyName"]
                period_of_report = filing["periodOfReport"]
                effectiveness_date = filing["effectivenessDate"]
                holdings_data = filing["holdings"]

                # Convert the holdings data into rows and columns
                for item in holdings_data:
                    ticker = item.get("ticker", "")
                    name_of_issuer = item.get("nameOfIssuer", "")
                    value = item.get("value", "")
                    title_of_class = item.get("titleOfClass", "")
                    put_call = item.get("putCall", "")
                    holdings_list = holdings_first_filing if i == 0 else holdings_second_filing
                    holdings_list.append({
                        "CIK": cik, "Company Name": company_name, "Period of Report": period_of_report,
                        "Effectiveness Date": effectiveness_date, "Ticker": ticker, "Name of Issuer": name_of_issuer,
                        "Value": value, "Title of Class": title_of_class, "Put/Call": put_call
                    })
            except KeyError:
                print(f"Error in data extraction for CIK: {cik}")
    else:
        print(f"No filings found for CIK: {cik}")

# Create DataFrames for holdings data from first and second filings
df_first_filing = pd.DataFrame(holdings_first_filing)
df_second_filing = pd.DataFrame(holdings_second_filing)

# Define the file path with a timestamp
timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
file_path = f"C:\\Users\\tdham\\PycharmProjects\\EquityAnalysis\\Tracking\\Results\\13F_Holdings_{timestamp}.xlsx"

# Save the DataFrames to an Excel file with two separate tabs
with pd.ExcelWriter(file_path) as writer:
    df_first_filing.to_excel(writer, index=False, sheet_name="Most Recent Filings")
    df_second_filing.to_excel(writer, index=False, sheet_name="Second Most Recent Filings")

print(f"File saved to: {file_path}")
