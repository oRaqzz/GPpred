from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import numpy as np
import pandas as pd
import joblib
from datetime import datetime, timedelta
import os  

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "GPpred.pkl")
STATIC_DIR = os.path.abspath(os.path.join(BASE_DIR, "..", "static"))  
TEMPLATES_DIR = os.path.abspath(os.path.join(BASE_DIR, "..", "templates"))

app = FastAPI()
model = joblib.load(MODEL_PATH)


app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")
templates = Jinja2Templates(directory=TEMPLATES_DIR)

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", { "request" : request })

@app.post("/predict")
async def predict(request: Request):
    data = await request.json()

    Open = float(data["Open"])
    High = float(data["High"])
    Low = float(data["Low"])
    Close = float(data["Close"])
    Volume = float(data["Volume"])
    Full_Date = str(data["Date"])

    Date = datetime.strptime(Full_Date, "%Y-%m-%d")
    Year = Date.year
    Month = Date.month
    Day = Date.day
    DayOfWeek = Date.weekday()
    IsMonthStart = int(Date.day == 1)
    IsMonthEnd = int((Date + timedelta(days=1)).day == 1)

    features = np.array([[Open, High, Low, Close, Volume, Year, Month, Day, DayOfWeek, IsMonthStart, IsMonthEnd]])
    prediction = model.predict(features)

    return JSONResponse(content={"prediction": prediction[0]})