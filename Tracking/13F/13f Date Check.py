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

# List to store combined data
combined_list = []

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
            # Extract data from the most recent filing
            company_name = response["filings"][0]["companyName"]
            period_of_report = response["filings"][0]["periodOfReport"]
            effectiveness_date = response["filings"][0]["effectivenessDate"]

            combined_list.append(
                {"CIK": cik, "Company Name": company_name, "Period of Report": period_of_report,
                 "Effectiveness Date": effectiveness_date})

        except KeyError:
            print(f"No filings found for CIK: {cik}")
    else:
        print(f"No filings found for CIK: {cik}")

# Create a DataFrame for combined data
combined_df = pd.DataFrame(combined_list)

# Define the file path with a timestamp
timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
file_name = f"13F_Filing_Dates_{timestamp}.xlsx"
file_path = f"C:\\Users\\tdham\\PycharmProjects\\EquityAnalysis\\Tracking\\Results\\{file_name}"

# Save the DataFrame to an Excel file
combined_df.to_excel(file_path, index=False, sheet_name="Summary")

