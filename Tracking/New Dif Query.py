from sec_api import QueryApi
import pandas as pd
from datetime import datetime

# Define your API key
api_key = "ca463e956b32cb96b919e9af4444456049e47f3ab961bc9fac41c6fe2ed5c1ad"

# Define CIKs
ciks = ["1801265", "949509", "1569241", "1894571", "1785988", "1601086", "1899655", "1676292", "1535392", "1827442",
        "1559706", "1512162", "1510974", "1535264", "1107310", "1789779", "1536630", "1540531", "1543170", "1697591",
        "1699673", "1512171", "1599383", "1471085", "1061768", "1745214", "1741129", "1340807", "1697848", "1700362",
        "1233099", "1412741"]

# Create a QueryApi instance
queryApi = QueryApi(api_key=api_key)

# List to store holdings data for first and second filings
combined_holdings_list_first = []
combined_holdings_list_second = []

# Loop through each CIK
for cik in ciks:
    # Define the query parameters for the current CIK to get the two most recent filings
    query = {
        "query": f"formType:\"13F-HR\" AND cik:{cik}",
        "from": "0",
        "size": "2",  # Update to get the two most recent filings
        "sort": [{"filedAt": {"order": "desc"}}]
    }

    # Get filings using the Query API
    response = queryApi.get_filings(query)

    # Check if filings are available
    if response.get("filings"):
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
                    if i == 0:
                        combined_holdings_list_first.append({"CIK": cik, "Company Name": company_name, "Period of Report": period_of_report, "Effectiveness Date": effectiveness_date, "Ticker": ticker, "NameOfIssuer": name_of_issuer, "Value": value, "TitleOfClass": title_of_class, "Put/Call": put_call})
                    elif i == 1:
                        combined_holdings_list_second.append({"CIK": cik, "Company Name": company_name, "Period of Report": period_of_report, "Effectiveness Date": effectiveness_date, "Ticker": ticker, "NameOfIssuer": name_of_issuer, "Value": value, "TitleOfClass": title_of_class, "Put/Call": put_call})
            except KeyError:
                print(f"No filings found for CIK: {cik}")
    else:
        print(f"No filings found for CIK: {cik}")

# Create DataFrames for combined holdings data for first and second filings
combined_holdings_df_first = pd.DataFrame(combined_holdings_list_first)
combined_holdings_df_second = pd.DataFrame(combined_holdings_list_second)

# Define the file path with a timestamp
timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
file_name = f"13F_Results_{timestamp}.xlsx"
file_path = f"C:\\Users\\tdham\\PycharmProjects\\EquityAnalysis\\Tracking\\Results\\{file_name}"

# Save the DataFrames to an Excel file with two separate tabs
with pd.ExcelWriter(file_path) as writer:
    combined_holdings_df_first.to_excel(writer, index=False, sheet_name="Most Recent Filings")
    combined_holdings_df_second.to_excel(writer, index=False, sheet_name="Second Most Recent Filings")

print(f"File saved to: {file_path}")
