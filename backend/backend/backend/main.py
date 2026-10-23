import os
from datetime import datetime
from typing import List, Optional
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from motor.motor_asyncio import AsyncIOMotorClient

app = FastAPI(title="Caseirinho API")

# Permite que o frontend comunique com o backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

MONGO_URI = os.getenv(
    "MONGO_URI",
    "mongodb+srv://nagaragemhamburgueriaartesanal_db_user:xM5r70tnYcUibw0z@cluster0.bheebzr.mongodb.net/?appName=Cluster0"
)
DB_NAME = os.getenv("DB_NAME", "caseirinho")

client = AsyncIOMotorClient(MONGO_URI)
db = client[DB_NAME]

# Modelos de Dados
class OrderItem(BaseModel):
    name: str
    quantity: int
    line: Optional[str] = None

class OrderCreate(BaseModel):
    customer_name: str
    customer_phone: str
    delivery_type: str  # "entrega" ou "retirada"
    cep: Optional[str] = None
    address: Optional[str] = None
    payment_method: str  # "pix", "dinheiro", "cartao"
    notes: Optional[str] = ""
    items: List[OrderItem]

def calculate_pricing(total_items: int):
    """
    Regra gulosa de kits:
    10 unidades = R$ 180,00
    5 unidades = R$ 95,00
    Avulso = R$ 20,00 cada
    """
    k10 = total_items // 10
    rem = total_items % 10
    k5 = rem // 5
    unit = rem % 5
    total = (k10 * 180.0) + (k5 * 95.0) + (unit * 20.0)
    return total, {"kit10": k10, "kit5": k5, "units": unit}

@app.get("/api/settings")
async def get_settings():
    settings = await db.settings.find_one({"_id": "store_settings"})
    if not settings:
        raise HTTPException(status_code=404, detail="Configurações não encontradas")
    settings["_id"] = str(settings["_id"])
    return settings

@app.get("/api/dishes")
async def get_dishes():
    cursor = db.dishes.find({"available": True})
    dishes = await cursor.to_list(length=100)
    for d in dishes:
        d["_id"] = str(d["_id"])
    return dishes

@app.post("/api/orders")
async def create_order(order: OrderCreate):
    total_qty = sum(item.quantity for item in order.items)
    if total_qty == 0:
        raise HTTPException(status_code=400, detail="O pedido deve ter pelo menos um item")
    
    subtotal, breakdown = calculate_pricing(total_qty)
    
    settings = await db.settings.find_one({"_id": "store_settings"})
    delivery_fee = 0.0
    if order.delivery_type == "entrega":
        delivery_fee = float(settings.get("default_fee", 15.0)) if settings else 15.0
        
    total_amount = subtotal + delivery_fee
    
    order_doc = {
        "customer_name": order.customer_name,
        "customer_phone": order.customer_phone,
        "delivery_type": order.delivery_type,
        "cep": order.cep,
        "address": order.address,
        "payment_method": order.payment_method,
        "notes": order.notes,
        "items": [item.dict() for item in order.items],
        "total_quantity": total_qty,
        "subtotal": subtotal,
        "delivery_fee": delivery_fee,
        "total_amount": total_amount,
        "pricing_breakdown": breakdown,
        "status": "novo",
        "created_at": datetime.utcnow()
    }
    
    result = await db.orders.insert_one(order_doc)
    order_doc["_id"] = str(result.inserted_id)
    return order_doc

@app.get("/api/admin/reports")
async def get_reports():
    cursor = db.orders.find().sort("created_at", -1)
    orders = await cursor.to_list(length=500)
    
    total_revenue = sum(o.get("total_amount", 0.0) for o in orders)
    total_orders = len(orders)
    total_dishes = sum(o.get("total_quantity", 0) for o in orders)
    
    for o in orders:
        o["_id"] = str(o["_id"])
        if "created_at" in o and isinstance(o["created_at"], datetime):
            o["created_at"] = o["created_at"].isoformat()
            
    return {
        "summary": {
            "total_revenue": total_revenue,
            "total_orders": total_orders,
            "total_dishes": total_dishes
        },
        "orders": orders
    }
