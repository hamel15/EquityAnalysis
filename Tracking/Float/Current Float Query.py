import pandas as pd
from sec_api import FloatApi

# Initialize the FloatApi with your actual API key
api_key = 'ca463e956b32cb96b919e9af4444456049e47f3ab961bc9fac41c6fe2ed5c1ad'
floatApi = FloatApi(api_key)

# List of tickers for which to fetch float data
tickers = [
    "TLYS", "SRV.UN-TC", "CTRN", "TTSH", "BJRI", "VNCE", "DXLG", "HIBB", "FLWS", "VRA", "FIHO\12-MEX", "FNKO",
    "HLF", "JILL", "LOCO", "RRGB", "0973-HKG", "ANGO", "SN", "TPR", "ZUMZ", "SWBI", "PRPL", "IWM", "CURV", "FOSL",
    "STKS", "PRGO", "HGV", "TTI", "M", "BORR", "TV", "ABY-ASX", "CUERVO-MEX", "OXY", "AR", "AMZN", "BABA", "CCL",
    "ASO", "BBWI", "SFIX", "VSCO", "6920-TSE", "LPP-WAR", "G24-XET", "RH", "ARHS", "DBI", "PLAY", "GIII", "UPWK",
    "CROX", "CVNA", "6804-TSE", "CTC.A-TC", "BME-LON", "PLCE", "TWST", "SG", "ARKK", "AUR", "BRCC", "CAVA", "ETD",
    "FWRG", "HRMY", "HVT", "KTB", "NU", "PTLO", "SVV", "ATZ-TC", "BBW", "CAL", "CENTA", "CHUY", "COLM", "CSGP",
    "DECK", "DKS", "DLTR", "DOCU", "DRI", "FL", "FND", "KSS", "NKE", "NVDA", "OXM", "QQQ", "SCS", "SCVL", "SHAK",
    "SIG", "SMAR", "SMPL", "SNAP", "SPY", "TWLO", "XRT", "ZUO", "AGUILAS\CPO-MEX", "ARWR", "BC-MIL", "BE", "BF/A",
    "BLMN", "BYON", "CAKE", "CBRL", "CDLX", "CTC.A-TC", "CTRI", "EAT", "EYE", "FUN", "GPS", "KAI", "LEG", "LFST",
    "NFLX", "ODD", "ODFL", "SAIA", "SHOP", "TSLA", "UBER", "ULS", "ULTA", "VFC", "W", "WNC", "WSM", "XHB", "XPOF", "YETI"
]

# DataFrame to hold the data
data = []

# Fetch float data for each ticker
for ticker in tickers:
    try:
        response = floatApi.get_float(ticker=ticker)
        # Initialize sum for the ticker
        total_float = 0
        if response['data']:
            # Loop through all share classes
            for share_class in response['data'][0]['float']['outstandingShares']:
                total_float += share_class['value']
            data.append({
                'Ticker': ticker,
                'Reported At': response['data'][0]['reportedAt'],
                'Total Float Shares': total_float
            })
        else:
            data.append({'Ticker': ticker, 'Reported At': None, 'Total Float Shares': 'No Data'})
    except Exception as e:
        print(f"Error fetching data for {ticker}: {str(e)}")
        data.append({'Ticker': ticker, 'Reported At': None, 'Total Float Shares': 'Failed to Retrieve'})

# Convert to DataFrame
df = pd.DataFrame(data)

# Save to CSV
df.to_csv('total_float_data.csv', index=False)
print("Data saved to total_float_data.csv.")
