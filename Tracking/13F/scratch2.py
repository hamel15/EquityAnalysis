from sec_api import FullTextSearchApi
import pandas as pd

# Setup
api_key = "YOUR_API_KEY"
fullTextSearchApi = FullTextSearchApi(api_key=api_key)
query = {
  "query": "formType:\"13F-HR\"",
  "sort": [{"filedAt": {"order": "desc"}}],
  "from": "0",
  "size": "1"
}

# Fetch data
response = fullTextSearchApi.get_filings(query)
print("Response:", response)  # Debug print to see the structure

# Check and process the response
if 'filings' in response and len(response['filings']) > 0:
    filing = response['filings'][0]
    data = {
        'CIK': [filing['cik']],
        'Accession Number': [filing['accessionNo']],
        'Company Name': [filing['companyNameLong']],
        'Filed At': [filing['filedAt']],
        'Form Type': [filing['formType']],
        'Filing URL': [filing['filingUrl']]
    }

    # Convert to DataFrame and save to Excel
    df = pd.DataFrame(data)
    df.to_excel('latest_13f_filing.xlsx', index=False)
    print("The most recent 13F filing data has been saved to 'latest_13f_filing.xlsx'.")
else:
    print("No filings found or incorrect response format.")
