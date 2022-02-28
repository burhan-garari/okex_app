import requests

url = 'http://127.0.0.1:8000'


def create_strategy_webhook(strategyId:str,strategyName:str,apiKey:str,apiSecret:str) -> str:
	"""
	Creates strategy webhook from the data\n
	Here strategyId and Username are same\n
	"""
	d = {"UserName":strategyName,"API_KEY":apiKey,"SECRET_KEY":apiSecret}
	requests.post(url+'/create_user/',json=d)
	d = {"API_KEY":apiKey,"Strategy_id":strategyId,"Strategy_Name":strategyName}
	requests.post(url+'/create_strategy',json=d)
	return url + f'/strategy/{strategyId}'

# webhook = create_strategy_webhook('s1','My dummy strategy','myApiKey','myApiSecret')
#signal = {"auth_code":"myStrongPassword","strategy":"s1","symbol":"BTCUSDT","side":"BUY","quantity":0.001,"trigger_price":38501.36}
#r = requests.post(webhook,json=signal)
#print(r)
#print(r.json())
"""
#CREATE USER ACCOUNT
#NOTE DO NOT USE API KEY IN URL PATH, ITS NOT SECURE 
d = {"USER_NAME":"Dummyuser110","API_KEY":"api110","SECRET_KEY":"secret100"}
r = requests.post(url+'/create_user/',json=d)
print(r)
print(r.json())

# ATTACH USER ACCOUNT TO STRATEGY
d = {"API_KEY":"api110","strategy_ID":"s110","Strategy_Name":"RED"}
r = requests.post(url+'/create_strategy',json=d)
print(r)
print(r.json())

# CREATION OF BOT 
d = {"strategy_ID":"WS1", "API_KEY": "api110" , "SECRET_KEY":"secret100"}
r = requests.post(url+"/submitdetails", json = d)

# WEBHOOK SIGNAL WILL LOOK LIKE THIS
# SERVER WILL RECEIVE THIS SIGNAL 
# webhook url = http://127.0.0.1:8000/receive_signal
"""
signal = {"auth_code"    :"myStrongPassword",
          "symbol"       :"BTC/USDT:USDT",
          "side"         :"BUY ",
          "trigger_price":3000}
r = requests.post(url+"/receive_signal",json=signal)
print(r)
#print(r.json())