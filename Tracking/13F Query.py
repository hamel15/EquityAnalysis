from sec_api import QueryApi

queryApi = QueryApi(api_key="ca463e956b32cb96b919e9af4444456049e47f3ab961bc9fac41c6fe2ed5c1ad")

query = {
    "query": "formType:\"13F-HR\" AND cik:1801265",
    "from": "0",
    "size": "10",
    "sort": [{"filedAt": {"order": "desc"}}]
}

response = queryApi.get_filings(query)

import json

# response is a dict with multiple keys. The most important one is "filings".
# response["filings"] is a list and includes all filings returned by the Query API.
print(json.dumps(response["filings"][0], indent=2))