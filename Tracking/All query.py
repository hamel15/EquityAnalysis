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

# List to store holdings data
combined_holdings_list = []

# Loop through each CIK
for cik in ciks:
    # Define the query parameters for the current CIK
    query = {
        "query": f"formType:\"13F-HR\" AND cik:{cik}",
        "from": "0",
        "size": "1",
        "sort": [{"filedAt": {"order": "desc"}}]
    }

    # Get filings using the Query API
    response = queryApi.get_filings(query)

    # Check if filings are available
    if response.get("filings"):
        try:
            # Extract relevant data from the response
            company_name = response["filings"][0]["companyName"]
            holdings_data = response["filings"][0]["holdings"]

            # Convert the holdings data into rows and columns
            for item in holdings_data:
                ticker = item.get("ticker", "")
                name_of_issuer = item.get("nameOfIssuer", "")
                value = item.get("value", "")
                title_of_class = item.get("titleOfClass", "")
                put_call = item.get("putCall", "")
                combined_holdings_list.append({"CIK": cik, "Company Name": company_name, "Ticker": ticker, "NameOfIssuer": name_of_issuer, "Value": value, "TitleOfClass": title_of_class, "Put/Call": put_call})
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
