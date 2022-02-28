import ccxt 
import json
def write_json(data, filename = ""):
    with open (filename, "w") as f:
        json.dump(data, f, indent = 4)
        
with open("positions2.json", "r") as f:
    curr_positions = json.load(f)
"""
exchanges = ccxt.exchanges 

for exchange in exchanges:
    print(exchange)

    


markets  = exchange.load_markets()

for market in markets:
    print(market)

exchange1 = ccxt.okex()
exchange2 = ccxt.bybit()
markets  = exchange1.load_markets()

for market in markets:
    print(market)
"""

class Bot():
    
    def __init__(self, API_KEY, SECRET_KEY, curr_signal):
        self.signal   = curr_signal
        #self.exchange = ccxt.okex({ 'apiKey' : API_KEY,'secret' : SECRET_KEY})
        self.exchange = ccxt.okex()
    
    def place_order(self):
        ticker = self.exchange.fetch_ticker(self.signal["symbol"])
        # BUY ORDER 
        if (self.signal["side"] == "BUY"):
            current_price = float(ticker['last'])
            if(current_price<=self.signal["price"]):
                curr_positions[self.signal["symbol"]]["side"] = "SELL"
                #self.exchange.create_market_buy_order(self.signal["side"], float(self.signal["quantity"]))
                print("Buying "    + str(self.signal["quantity"]) + " of " + self.signal["symbol"] 
                      + " costing " + str(self.signal["total_price"]))  
        elif(self.signal["side"]=="SELL"):
            # SELL ORDER
            current_price = float(ticker['last'])
            if(current_price>=self.signal["price"]):
                #self.exchange.create_market_buy_order(self.signal["side"], float(self.signal["quantity"]))
                print("Selling "    + str(self.signal["quantity"]) + " of " + self.signal["symbol"] 
                      + " costing " + str(self.signal["total_price"]))
        else:
            # OTHER MARKET ORDERS
            #self.exchange.create_market_buy_order(self.signal["side"], float(self.signal["quantity"]))
            print(str(self.signal["side"])    + str(self.signal["quantity"]) + " of " + self.signal["symbol"] 
                      + " costing " + str(self.signal["total_price"]))  
            
        write_json(curr_positions , filename = "positions.json")

if __name__ == "__main__":
    print("okex_bot Module")