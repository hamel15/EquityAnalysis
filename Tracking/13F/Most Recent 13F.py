from sec_api import QueryApi
import pandas as pd
from datetime import datetime

# Define your API key
api_key = "ca463e956b32cb96b919e9af4444456049e47f3ab961bc9fac41c6fe2ed5c1ad"

# Define CIKs
ciks = ["1801265", "949509", "1894571", "1785988", "1512162", "1540531", "1471085", "1061768"]

# Create a QueryApi instance
queryApi = QueryApi(api_key=api_key)

# List to store holdings data
combined_holdings_list = []

# Loop through each CIK
for cik in ciks:
    # Define the query parameters for the current CIK
    query = {
        "query": f"formType:\"13F-HR\" AND cik:{cik}",
        "from": "0",
        "size": "2",
        "sort": [{"filedAt": {"order": "desc"}}]
    }

    # Get filings using the Query API
    response = queryApi.get_filings(query)

    # Check if filings are available
    if response.get("filings"):
        try:
            # Extract data from the most recent filing
            company_name = response["filings"][0]["companyName"]
            period_of_report = response["filings"][0]["periodOfReport"]
            effectiveness_date = response["filings"][0]["effectivenessDate"]
            holdings_data = response["filings"][0]["holdings"]

            # Extract data from the second most recent filing
            if len(response["filings"]) > 1:
                holdings_data_prev = response["filings"][1]["holdings"]
                prev_holdings = {item["ticker"]: item["value"] for item in holdings_data_prev}
            else:
                prev_holdings = {}

            # Calculate the difference in 'Value' column for each ticker
            for item in holdings_data:
                ticker = item.get("ticker", "")
                name_of_issuer = item.get("nameOfIssuer", "")
                value = item.get("value", "")
                title_of_class = item.get("titleOfClass", "")
                put_call = item.get("putCall", "")

                # Calculate the difference in 'Value' column
                prev_value = prev_holdings.get(ticker, 0)
                value_diff = value - prev_value

                combined_holdings_list.append({"CIK": cik, "Company Name": company_name, "Period of Report": period_of_report,
                                               "Effectiveness Date": effectiveness_date, "Ticker": ticker, "NameOfIssuer": name_of_issuer,
                                               "Value": value, "TitleOfClass": title_of_class, "Put/Call": put_call, "Value Difference": value_diff})
        except KeyError:
            print(f"No filings found for CIK: {cik}")
    else:
        print(f"No filings found for CIK: {cik}")

# Create a DataFrame for combined holdings data
combined_holdings_df = pd.DataFrame(combined_holdings_list)

# Define the file path with a timestamp
timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
file_name = f"13F_Results_{timestamp}.xlsx"
file_path = f"C:\\Users\\tdham\\PycharmProjects\\EquityAnalysis\\Tracking\\Results\\{file_name}"

# Save the DataFrame to an Excel file
with pd.ExcelWriter(file_path) as writer:
    combined_holdings_df.to_excel(writer, index=False, sheet_name="Combined Holdings")

print(f"File saved to: {file_path}")
