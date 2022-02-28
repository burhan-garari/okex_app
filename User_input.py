from pydantic import BaseModel

class UserData(BaseModel):
    Exchange   : str
    Leverage   : float
    Investment : float
    Coin_type  : str
    Tp         : float
    Sl         : float
    Platform   : str
    edit_links : list
    delete_link: str
    start_link : str
    stop_link  : str

class Signal(BaseModel):
    auth_code    :str
    symbol       :str
    side         :str
    trigger_price:float


