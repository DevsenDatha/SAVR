from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import httpx
import os
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
SPOONACULAR_API_KEY = os.getenv("SPOONACULAR_API_KEY")

# Kroger API credentials
KROGER_CLIENT_ID = os.getenv("KROGER_CLIENT_ID")
KROGER_CLIENT_SECRET = os.getenv("KROGER_CLIENT_SECRET")

print("✅ Supabase URL:", SUPABASE_URL)
print("✅ Supabase Key:", SUPABASE_KEY)
print("✅ Spoonacular Key:", SPOONACULAR_API_KEY)

# App setup
app = FastAPI()

# CORS setup to allow frontend calls
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # React frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ----------------- MODELS -------------------
class Budget(BaseModel):
    user_id: str
    amount: float
    type: str  # monthly or weekly

class Expense(BaseModel):
    user_id: str
    category: str
    description: str
    amount: float
    date: str  # 'YYYY-MM-DD'

# ----------------- ROUTES -------------------

# 🧠 Spoonacular Recipe Search
@app.get("/recipes")
async def get_recipes(query: str):
    url = "https://api.spoonacular.com/recipes/complexSearch"
    params = {
        "query": query,
        "number": 5,
        "addRecipeInformation": True,
        "apiKey": SPOONACULAR_API_KEY
    }
    async with httpx.AsyncClient() as client:
        res = await client.get(url, params=params)
        return res.json()

# 💸 Budget Routes
@app.post("/budget")
async def create_budget(budget: Budget):
    async with httpx.AsyncClient() as client:
        res = await client.post(
            f"{SUPABASE_URL}/rest/v1/budgets",
            headers={
                "apikey": SUPABASE_KEY,
                "Authorization": f"Bearer {SUPABASE_KEY}",
                "Content-Type": "application/json"
            },
            json=budget.dict()
        )
        if res.status_code != 201:
            raise HTTPException(status_code=res.status_code, detail=res.text)
        return {"message": "Budget saved"}

@app.get("/budget/{user_id}")
async def get_budget(user_id: str):
    async with httpx.AsyncClient() as client:
        res = await client.get(
            f"{SUPABASE_URL}/rest/v1/budgets",
            headers={
                "apikey": SUPABASE_KEY,
                "Authorization": f"Bearer {SUPABASE_KEY}"
            },
            params={"user_id": f"eq.{user_id}"}
        )
        return res.json()

# 🧾 Expense Routes
@app.post("/expenses")
async def add_expense(expense: Expense):
    async with httpx.AsyncClient() as client:
        res = await client.post(
            f"{SUPABASE_URL}/rest/v1/expenses",
            headers={
                "apikey": SUPABASE_KEY,
                "Authorization": f"Bearer {SUPABASE_KEY}",
                "Content-Type": "application/json"
            },
            json=expense.dict()
        )
        if res.status_code != 201:
            raise HTTPException(status_code=res.status_code, detail=res.text)
        return {"message": "Expense added"}

@app.get("/expenses/{user_id}")
async def get_expenses(user_id: str):
    async with httpx.AsyncClient() as client:
        res = await client.get(
            f"{SUPABASE_URL}/rest/v1/expenses",
            headers={
                "apikey": SUPABASE_KEY,
                "Authorization": f"Bearer {SUPABASE_KEY}"
            },
            params={"user_id": f"eq.{user_id}"}
        )
        return res.json()

# 🛒 Kroger API Integration for Grocery Products
@app.get("/kroger/products")
async def get_kroger_products(query: str):
    # Get access token from Kroger using client_id and client_secret
    auth_url = "https://api.kroger.com/v1/connect/oauth2/token"
    auth_data = {
        "grant_type": "client_credentials",
        "client_id": KROGER_CLIENT_ID,
        "client_secret": KROGER_CLIENT_SECRET
    }

    async with httpx.AsyncClient() as client:
        auth_res = await client.post(auth_url, data=auth_data)
        if auth_res.status_code != 200:
            raise HTTPException(status_code=auth_res.status_code, detail="Failed to authenticate with Kroger API")
        
        auth_json = auth_res.json()
        access_token = auth_json.get("access_token")

        # Use the access token to fetch product data from Kroger
        products_url = f"https://api.kroger.com/v1/products"
        params = {"query": query}
        headers = {"Authorization": f"Bearer {access_token}"}
        
        res = await client.get(products_url, headers=headers, params=params)
        
        if res.status_code != 200:
            raise HTTPException(status_code=res.status_code, detail="Failed to fetch products from Kroger")
        
        return res.json()

# Optional: base health check
@app.get("/")
def root():
    return {"message": "SAVR API is running ✅"}
