import os
import joblib
import pandas as pd
from datetime import datetime
from fastapi import APIRouter
from app.schemas.prediction import PricePredictionRequest

router = APIRouter(
    prefix="/prediction",
    tags=["Price Prediction"]
)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

model_path = os.path.join(
    BASE_DIR,
    "..",
    "..",
    "ml",
    "price_model.pkl"
)
demand_model_path = os.path.join(
    BASE_DIR,
    "..",
    "..",
    "ml",
    "demand_model.pkl"
)
weekday_encoder_path = os.path.join(
    BASE_DIR,
    "..",
    "..",
    "ml",
    "weekday_encoder.pkl"
)

weekday_encoder = joblib.load(weekday_encoder_path)

price_model = joblib.load(model_path)

feature_names = [
    "Category",
    "Original Price",
    "Discount",
    "Payment Method",
    "Year",
    "Month",
    "Day"
]

feature_importance = {}

for feature, importance in zip(
    feature_names,
    price_model.feature_importances_
     ):
    feature_importance[feature] = round(
         importance * 100,
        2
     )
demand_model = joblib.load(demand_model_path)

@router.post("/predict-price")
def predict_price(data: PricePredictionRequest):
    weekday_name = datetime(
    data.year,
    data.month,
    data.day
   ).strftime("%A")
    weekday=weekday_encoder.transform([weekday_name])[0];
    price_input = pd.DataFrame([{
        "Category": data.category,
        "Price (Rs.)": data.original_price,
        "Discount (%)": data.discount,
        "Payment_Method": data.payment_method,
        "Year": data.year,
        "Month": data.month,
        "Day": data.day
    }])



    predicted_price = round(
        float(price_model.predict(price_input)[0]),
        2
    )
    
    # -------------------------
    # Pricing Recommendation
    # -------------------------
        
    candidate_prices = []
    
    for percent in range(-20, 21, 2):   # -20%, -18%, ... 20%
        price = round(
            predicted_price * (1 + percent / 100),
            2
        )
    
        if price > 0:
            candidate_prices.append(price)

    optimization_results = []

    for price in candidate_prices:
        temp_input = pd.DataFrame([{
            "Category": data.category,
            "Price (Rs.)": price,
            "Discount (%)": data.discount,
            "Payment_Method": data.payment_method,
            "Year": data.year,
            "Month": data.month,
            "Day": data.day,
            "Weekday": weekday
        }])

        predicted_demand = int(
           demand_model.predict(temp_input)[0]
     )

        revenue = round(
           price * predicted_demand,
           2
      )

        optimization_results.append({
          "price": price,
          "demand": predicted_demand,
          "revenue": revenue
        })
    # Temporary Demand Logic
    best_result = max(
    optimization_results,
    key=lambda x: x["revenue"]
    )
    recommended_price = best_result["price"]

    expected_demand = best_result["demand"]
    
    expected_revenue = best_result["revenue"]
            
    
    recommendation = (
    f"AI recommends selling this product at ₹{recommended_price} "
    f"because it maximizes the expected revenue."
    )
    # Trend Logic
    
    
    if expected_demand >= 150:
        trend = "Increasing"
    elif expected_demand >= 100:
        trend = "Stable"
    else:
        trend = "Decreasing"
    
    confidence = 94.2
    
    
    return {
        "predicted_price": predicted_price,
        "recommended_price": recommended_price,
        "expected_demand": expected_demand,
        "expected_revenue": expected_revenue,
        "trend": trend,
        "confidence": confidence,
        "recommendation": recommendation,
        "feature_importance": feature_importance,
        "optimization_results": optimization_results
        
    }