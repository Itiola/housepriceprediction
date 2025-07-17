from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import joblib
import os

app = FastAPI()

# Templates directory is in the parent folder, 'frontend'
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEMPLATE_DIR = os.path.join(BASE_DIR, "frontend")

templates = Jinja2Templates(directory=TEMPLATE_DIR)

# Load model and scaler
model = joblib.load(os.path.join(os.path.dirname(__file__), "model.pkl"))
scaler = joblib.load(os.path.join(os.path.dirname(__file__), "scaler.pkl"))

yes_no_map = {'yes': 1, 'no': 0}
furnish_map = {'unfurnished': 0, 'semi-furnished': 1, 'furnished': 2}
numeric_cols_count = 5  # area, bedrooms, bathrooms, stories, parking

@app.get("/", response_class=HTMLResponse)
async def form_get(request: Request):
    return templates.TemplateResponse("predict.html", {"request": request})

@app.post("/predict", response_class=HTMLResponse)
async def predict(
    request: Request,
    area: float = Form(...),
    bedrooms: int = Form(...),
    bathrooms: int = Form(...),
    stories: int = Form(...),
    mainroad: str = Form(...),
    guestroom: str = Form(...),
    basement: str = Form(...),
    hotwaterheating: str = Form(...),
    airconditioning: str = Form(...),
    parking: int = Form(...),
    prefarea: str = Form(...),
    furnishingstatus: str = Form(...)
):
    raw_features = [
        area, bedrooms, bathrooms, stories, parking,
        yes_no_map[mainroad.lower()],
        yes_no_map[guestroom.lower()],
        yes_no_map[basement.lower()],
        yes_no_map[hotwaterheating.lower()],
        yes_no_map[airconditioning.lower()],
        yes_no_map[prefarea.lower()],
        furnish_map[furnishingstatus.lower()]
    ]

    # Scale numeric features
    scaled_numeric = scaler.transform([raw_features[:numeric_cols_count]])[0]
    final_input = list(scaled_numeric) + raw_features[numeric_cols_count:]

    prediction = model.predict([final_input])[0]
    formatted_price = f"Estimated Price: ₹{round(prediction, 2):,}"

    return templates.TemplateResponse("predict.html", {
        "request": request,
        "result": formatted_price
    })
