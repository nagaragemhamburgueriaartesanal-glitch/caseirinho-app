# backend/seed.py
import asyncio
from motor.motor_asyncio import AsyncIOMotorClient

MONGO_URI = "mongodb+srv://nagaragemhamburgueriaartesanal_db_user:xM5r70tnYcUibw0z@cluster0.bheebzr.mongodb.net/?appName=Cluster0"
DB_NAME = "caseirinho"

SETTINGS = {
    "_id": "store_settings",
    "store_name": "Caseirinho Refeições Congeladas",
    "whatsapp": "5562982638169",
    "instagram": "@caseirinhorefeicoescongeladas",
    "pickup_address": "Goiânia - GO (Retirada combinada via WhatsApp)",
    "default_fee": 15.0,
    "pricing": {
        "unit": 20.0,
        "kit5": 95.0,
        "kit10": 180.0
    }
}

DISHES = [
    # Linha Tradicional (330g)
    {"code": 2, "name": "Fricassê de Frango com arroz branco", "weight": "330g", "line": "tradicional", "available": True},
    {"code": 3, "name": "Sobrecoxa assada com arroz branco e legumes", "weight": "330g", "line": "tradicional", "available": True},
    {"code": 6, "name": "Picadinho de Carne, Arroz branco e Legumes", "weight": "330g", "line": "tradicional", "available": True},
    {"code": 7, "name": "Galinhada e Feijão carioca", "weight": "330g", "line": "tradicional", "available": True},
    {"code": 8, "name": "Bobô de Frango com arroz branco e batata sotê", "weight": "330g", "line": "tradicional", "available": True},
    {"code": 10, "name": "Carne Oriental, Arroz e legumes", "weight": "330g", "line": "tradicional", "available": True},
    {"code": 12, "name": "Talharim à bolonhesa ervilha e queijo", "weight": "330g", "line": "tradicional", "available": True},
    {"code": 13, "name": "Parmegiana de frango com arroz e batata assada", "weight": "330g", "line": "tradicional", "available": True},
    {"code": 15, "name": "Lombo ao molho de mostarda, arroz colorido e batata assada", "weight": "330g", "line": "tradicional", "available": True},
    {"code": 16, "name": "Panqueca (massa tradicional) com carne moída", "weight": "330g", "line": "tradicional", "available": True},
    {"code": 17, "name": "Carne de Panela com Legumes e arroz branco", "weight": "330g", "line": "tradicional", "available": True},
    
    # Linha Fit (320g)
    {"code": 31, "name": "Frango Xadrez com Purê de Abóbora e Legumes", "weight": "320g", "line": "fit", "available": True},
    {"code": 32, "name": "Sobrecoxa assada com Purê de Batata e legumes", "weight": "320g", "line": "fit", "available": True},
    {"code": 34, "name": "Carne Moída com Purê de Batata Doce e Legumes", "weight": "320g", "line": "fit", "available": True},
    {"code": 35, "name": "Galinhada Fit com Legumes", "weight": "320g", "line": "fit", "available": True},
    {"code": 36, "name": "Panqueca Fit com carne moída", "weight": "320g", "line": "fit", "available": True},
    {"code": 37, "name": "Carne Oriental com Purê de Abóbora e Legumes", "weight": "320g", "line": "fit", "available": True},
    {"code": 38, "name": "Parmegiana de frango com Purê de Batata e legumes", "weight": "320g", "line": "fit", "available": True},
    {"code": 42, "name": "Frango em cubos ao molho de mostarda com Legumes assados", "weight": "320g", "line": "fit", "available": True},
    {"code": 43, "name": "Carne moída, purê de batata e brócolis", "weight": "320g", "line": "fit", "available": True},
    {"code": 11, "name": "Lombo desfiado com purê de mandioca e legumes", "weight": "320g", "line": "fit", "available": True},
    {"code": 47, "name": "Almôndega de porco com purê de batata e legumes", "weight": "320g", "line": "fit", "available": True},
    
    # Sopas e Caldos (450g)
    {"code": 61, "name": "Sopa de Legumes com carne picadinha", "weight": "450g", "line": "sopa", "available": True},
    {"code": 62, "name": "Caldo de Cabotiá com carne desfiada", "weight": "450g", "line": "sopa", "available": True},
    {"code": 63, "name": "Caldo de Milho com frango desfiado", "weight": "450g", "line": "sopa", "available": True},
]

async def seed():
    client = AsyncIOMotorClient(MONGO_URI)
    db = client[DB_NAME]
    
    await db.settings.replace_one({"_id": SETTINGS["_id"]}, SETTINGS, upsert=True)
    await db.dishes.delete_many({})
    await db.dishes.insert_many(DISHES)
    print("Banco de dados populado com sucesso com os 24 pratos e ajustes do Caseirinho!")

if __name__ == "__main__":
    asyncio.run(seed())
