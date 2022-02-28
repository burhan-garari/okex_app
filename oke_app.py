from fastapi import FastAPI, Request, Form
# Handle Excepetiions
from fastapi.exceptions import HTTPException
# Obtain Responses 
from fastapi.responses  import HTMLResponse, RedirectResponse
# To convert the json format to dictionary type 
from fastapi.encoders   import jsonable_encoder
 # TO access the HTML templates
from fastapi.templating import Jinja2Templates
# User_input files contains UserData 
from User_input import UserData, Signal
from oke_bot import Bot
import json

# App Creation 
app = FastAPI()

# Access to templates 
templates = Jinja2Templates(directory = "templates")

# passwords 

trading_view_password = "myStrongPassword"
API_KEY, SECRET_KEY   = "", ""


def write_json(data, filename = ""):
    with open (filename, "w") as f:
        json.dump(data, f, indent = 4)

with open("input_data.json", "r") as u:
        input_data = json.load(u)
        
with open("positions2.json", "r") as f:
    curr_positions = json.load(f)
"""
At start ask you for my exchange
- can set up a Leverage for all the coins at once, or each of them separately
- Investment USDT
- Testnet or Real
-TP/SL at the beginning for all the trades to come, or being able to change it as I go on trading.
- Tradingveiw or Custom

"""
@app.get("/", response_class = HTMLResponse)
def input_home(request:Request):
    curr_context = {'request' : request, "check" : False, "Data" : input_data}
    return templates.TemplateResponse("start_page_1.html", context = curr_context)

@app.post("/input_values", response_class = RedirectResponse)

def input_values(request:Request, EXCHANGE_NAME:str = Form(...), LEVERAGE_VAL:str = Form(...), 
               INVEST_VAL:str = Form(...), COIN_TYPE:str = Form(...), TP:str = Form(...),
               SL:str = Form(...),PLATFORM:str = Form(...)):
    N = len(input_data)
    store_data = UserData(Exchange = EXCHANGE_NAME,
        Leverage    = float(LEVERAGE_VAL),
        Investment  = float(INVEST_VAL),
        Coin_type   = COIN_TYPE,
        Tp          = TP,
        Sl          = SL,
        Platform    = PLATFORM,
        edit_links  = [" /edit/{}/{}".format(N, val) for val in ["Exchange", "Leverage", "Investment", "Coin_type", "Tp", "Sl", "Platform"]],
        delete_link =  "/delete/{}".format(N),
        start_link  =  "/start/{}".format(N),
        stop_link   =  "/stop/{}".format(N))
    
    store_data_dict = jsonable_encoder(store_data)
    
    input_data.append(store_data_dict)
    write_json(input_data, filename = "input_data.json")
    
    curr_context = {"request" : request, "check" : True, "Data" : input_data}
    
    return templates.TemplateResponse("start_page_1.html", context = curr_context)

@app.post("/edit/{number}/{field}", response_class = RedirectResponse)
def update_value(request:Request, number:str, field:str, value:str = Form(...)):
    
    modified_field = ""
    for k in field:
        if(k == ","):
            break
        modified_field+= k
    field  = modified_field
    
    if(type(input_data[int(number)][field])=="float"):
        input_data[int(number)][field] = int(value)
        if field=="Leverage":
            if input_data[int(number)]["Coin_type"] in curr_positions:
                curr_positions[input_data[int(number)]["Coin_type"]] = {
                        "symbol"     : input_data[int(number)]["Coin_type"],
                        "side"       : curr_positions[input_data[int(number)]["Coin_type"]]["side"],
                        "quantity"   : float(value),
                        "price"      : curr_positions[input_data[int(number)]["Coin_type"]]["price"],
                        "total_price": float(value)*curr_positions[input_data[int(number)]["Coin_type"]]["price"],
                        "row_val"    : curr_positions[input_data[int(number)]["Coin_type"]]["row_val"]
                        }
                write_json(curr_positions , filename = "positions2.json")
    else:
        if field=="Coin_type":
            if input_data[int(number)][field] in curr_positions:
                curr_positions[value] = {
                        "symbol"     : value,
                        "side"       : curr_positions[input_data[int(number)]["Coin_type"]]["side"],
                        "quantity"   : float(input_data[int(number)]["Leverage"]),
                        "price"      : curr_positions[input_data[int(number)]["Coin_type"]]["price"],
                        "total_price": float(input_data[int(number)]["Leverage"])*curr_positions[input_data[int(number)]["Coin_type"]]["price"],
                        "row_val"    : curr_positions[input_data[int(number)]["Coin_type"]]["row_val"]}
                del curr_positions[input_data[int(number)]["Coin_type"]]
            input_data[int(number)][field] = value
            write_json(curr_positions , filename = "positions2.json")
        else:
            input_data[int(number)][field] = value
    write_json(input_data, filename = "input_data.json")
    curr_context = {"request" : request, "check" : True, "Data" : input_data}
    return templates.TemplateResponse("start_page_1.html", context = curr_context)

@app.post("/delete/{number}", response_class = RedirectResponse)
def delete_value(request:Request, number:str):
    modified_num = ""
    for k in number:
        if(k==","):
            break
        modified_num += k
    number = int(modified_num)
    # Removing the curr_positions 
    for k in range(len(input_data)):
        if (k==number):
            if input_data[k]["Coin_type"] in curr_positions:
                del curr_positions[input_data[k]["Coin_type"]]
                write_json(curr_positions , filename = "positions2.json")
                    
    del input_data[int(number)]
    for i in range(len(input_data)):
        input_data[i]["edit_links"]  = ["/edit/{}/{}".format(i, val) 
                                        for val in ["Exchange", "Leverage", "Invest", "Coin_type", "Tp", "Sl", "Platform"]]
        input_data[i]["delete_link"] = "/delete/{}".format(i)
        input_data[i]["start_link"]  = "/start/{}".format(i)
        input_data[i]["stop_link"]   = "/stop/{}".format(i)
        if(len(curr_positions)>0):
            for coin in curr_positions:
                if coin == input_data[i]["Coin_type"]:
                    curr_positions[coin]["row_val"] = i

    write_json(curr_positions , filename = "positions2.json")
    write_json(input_data,      filename  = "input_data.json")
    
    curr_context = {"request" : request, "check" : True, "Data" : input_data}
    return templates.TemplateResponse("start_page_1.html", context = curr_context)
    
"""
- It will wait for Tradingveiw Signal
- Once It receive Signal , it will extract coin name , Position Side( for price ,TP ,SL we dont need the tradingview message, we set them up before and at the start of the program)
- Then it will trade on bybit based on Signal
- If tradingveiw is not selected then you have to give:
- Coin,Price,TP,SL,Side
- multiple coins

Signal format 

{
 "auth_code" : "",
 "symbol"    : "",
 "side"      :long,
 "trigger_price":""
 }
"""  
@app.post("/receive_signal")
def recive_signal(signal:Signal):
    signal = jsonable_encoder(signal)
    if signal["auth_code"] == trading_view_password:
        #exchange      = signal["ticker"]
        coin_name      = signal["symbol"]
        position_side  = signal["side"]
        price          = float(signal["trigger_price"])
        #bot_details   = signal["strategy"]["bot_details"]
        leverage       = 0
        row_val        = -1
        found          = False
        for j in range(len(input_data)):
            if (input_data[j]["Coin_type"] == coin_name):
                leverage = float(input_data[j]["Leverage"])
                row_val  = j
                curr_positions[coin_name] = {
                    "symbol"     : coin_name,
                    "side"       : position_side,
                    "quantity"   : leverage,
                    "price"      : price,
                    "total_price": leverage*price,
                    "row_val"    : row_val}
                print("FOund")
                write_json(curr_positions , filename = "positions2.json")
                found = True
        if(found == False): 
            return HTTPException(401, 'Unauthorized')
        #print(curr_positions[coin_name])        
        write_json(input_data     , filename = "input_data.json")        
        print("Start Trading")
        new_Bot = Bot(API_KEY, SECRET_KEY,curr_positions[coin_name])
        new_Bot.place_order()
    else:
        return HTTPException(401, 'Unauthorized')
        
@app.post("/stop_all", response_class = RedirectResponse)
def stop_complete(request:Request):
    curr_positions = {}
    write_json(curr_positions , filename = "positions2.json")      
    curr_context = {"request" : request, 
                    "check"   : True, 
                    "Data"    : input_data}
    return templates.TemplateResponse("start_page_1.html", 
                                      context = curr_context)

@app.post("/start/{number}", response_class = RedirectResponse)
def start_signal(request:Request, number:str):
    modified_num = ""
    for k in number:
        if(k==","):
            break
        modified_num += k
    number = modified_num
    print("Start Trading")
    write_json(input_data, filename = "input_data.json")
    for j in range(len(input_data)):
        if j==int(number):
            if ((input_data[j]["Coin_type"] in curr_positions) and 
                (curr_positions["Coin_type"]["exchange"]==input_data[j]["Excahnge"])):
                new_Bot = Bot(API_KEY, SECRET_KEY,curr_positions["Coin_type"])
                new_Bot.place_order()
                
    curr_context = {"request" : request, 
                    "check"   : True, 
                    "Data"    : input_data}
    
    return templates.TemplateResponse("start_page_1.html", context = curr_context)

@app.post("/stop/{number}", response_class = RedirectResponse)
def stop_signal(number:str, request:Request):
    modified_num = ""
    for k in number:
        if(k==","):
            break
        modified_num += k
    number = modified_num
    print("Stop Trading")
    for k in range(len(input_data)):
        if k==int(number):
            for coin in curr_positions:
                if coin == input_data[k]["Coin_type"]:
                    if  curr_positions[coin]["side"]=="BUY":
                        curr_positions[coin]["side"] = "SELL"
                        new_Bot = Bot(API_KEY, SECRET_KEY,curr_positions[coin])
                        new_Bot.place_order()
                    elif curr_positions[coin]["side"]=="SELL":
                         curr_positions[coin]["side"] = "BUY"
                         new_Bot = Bot(API_KEY, SECRET_KEY,curr_positions[coin])
                         new_Bot.place_order()
                    del curr_positions[coin]
                    break
            break    


    write_json(curr_positions, filename = "positions2.json")
    write_json(input_data    , filename = "input_data.json")
    curr_context = {"request" : request, 
                    "check"   : True, 
                    "Data"    : input_data}
    return templates.TemplateResponse("start_page_1.html", 
                                      context = curr_context)

    


    

    



    
    
    