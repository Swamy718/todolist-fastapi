from fastapi import FastAPI,HTTPException
from .auth import router
from fastapi.middleware.cors import CORSMiddleware

app=FastAPI()

app.include_router(router)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)












































# state_capitals = {
#     "Andhra Pradesh": "Amaravati",
#     "Arunachal Pradesh": "Itanagar",
#     "Assam": "Dispur",
#     "Bihar": "Patna",
#     "Chhattisgarh": "Raipur",
#     "Goa": "Panaji",
#     "Gujarat": "Gandhinagar",
#     "Haryana": "Chandigarh",
#     "Himachal Pradesh": "Shimla",
#     "Jharkhand": "Ranchi",
#     "Karnataka": "Bengaluru",
#     "Kerala": "Thiruvananthapuram",
#     "Madhya Pradesh": "Bhopal",
#     "Maharashtra": "Mumbai",
#     "Manipur": "Imphal",
#     "Meghalaya": "Shillong",
#     "Mizoram": "Aizawl",
#     "Nagaland": "Kohima",
#     "Odisha": "Bhubaneswar",
#     "Punjab": "Chandigarh",
#     "Rajasthan": "Jaipur",
#     "Sikkim": "Gangtok",
#     "Tamil Nadu": "Chennai",
#     "Telangana": "Hyderabad",
#     "Tripura": "Agartala",
#     "Uttar Pradesh": "Lucknow",
#     "Uttarakhand": "Dehradun",
#     "West Bengal": "Kolkata"
# }

# @app.get("/get_capital_city")
# def get_capital(state_name:str):
#     for key,value in state_capitals.items():
#         if (key.lower()==state_name.lower()):
#             return {"capital_city":value}
#     raise HTTPException(status_code=400,detail="Enter Correct State")

# @app.get("/is_city_capital")
# def is_city_capital(city_name:str):
#     k=False
#     for value in state_capitals.values():
#         if (value.lower()==city_name.lower()):
#             k=True
#     return {"response": "yes" if k else "no"}

# @app.get("/get_current_weather")
# def get_current_weather(state_name:str):
#     capital=""
#     for key,value in state_capitals.items():
#         if (key.lower()==state_name.lower()):
#             capital=value
    
#     # if capital=="":
#     #     raise HTTPException(status_code=400,detail="Enter Correct State")
    
#     conn = http.client.HTTPSConnection("weather-api167.p.rapidapi.com")
#     headers = {
#         'x-rapidapi-key': "f70bc8f669mshee0c16aa169b239p1f500bjsnd7da4f0abca8",
#         'x-rapidapi-host': "weather-api167.p.rapidapi.com",
#         'Accept': "application/json"
#     }

#     conn.request("GET", "/api/weather/current?place=Amaravati&units=standard&lang=en&mode=json", headers=headers)

#     res = conn.getresponse()
#     data = res.read()

#     decoded_data = data.decode("utf-8")

#     json_data = json.loads(decoded_data)
#     summary = json_data.get("summery")

#     return summary 
