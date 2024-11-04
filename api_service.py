
#define base url and constants
BASE_URL = "https://www.alphavantage.co/query?"
API_KEY = "QEQT8WNAUX7DRILI"
#API_KEY = "JZF7E8T2H2WCEID3"
#for intraday time series, set default interval to 5 mins
INTERVAL = "5min"

#convert time series number to time series string name
def convert_time_series(time_series_function):
    if time_series_function == "1":
        return "TIME_SERIES_INTRADAY"
    elif time_series_function == "2":
        return "TIME_SERIES_DAILY"
    elif time_series_function == "3":
        return "TIME_SERIES_WEEKLY"
    elif time_series_function == "4":
        return "TIME_SERIES_MONTHLY"
    #default
    else:
        return "TIME_SERIES_INTRADAY"

#construct full API url from parameters
def construct_url(base_url, time_series, symbol, interval, api_key):
    if time_series == "TIME_SERIES_INTRADAY":
        #intraday time series requires interval parameter
        full_url = base_url + "function=" + time_series + "&symbol=" + symbol + "&interval=" + interval + "&apikey=" + api_key
    else:
        full_url = base_url + "function=" + time_series + "&symbol=" + symbol + "&apikey=" +api_key
    
    return(full_url)
