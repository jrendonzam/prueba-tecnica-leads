"""
Mock CRM API Server
Ejecutar con:
    uvicorn src.api:app --reload --port 8000
"""
from fastapi import FastAPI, HTTPException, Header, status
from pydantic import BaseModel
from typing import Optional, List
import random

app = FastAPI(title="CRM Mock API", version="1.0.0", description="API simulada para prueba técnica de integración de Leads")

request_counter = 0

DESARROLLOS_DB = [
    {"id": 1, "nombre": "Residencial Cumbres", "ciudad": "Cancún", "estado": "Quintana Roo"},
    {"id": 2, "nombre": "Puerta de Hierro", "ciudad": "Guadalajara", "estado": "Jalisco"},
    {"id": 3, "nombre": "Valle Real", "ciudad": "Monterrey", "estado": "Nuevo León"},
    {"id": 4, "nombre": "Bosque Real", "ciudad": "Naucalpan", "estado": "Estado de México"},
    {"id": 5, "nombre": "Paseo de la Castellana", "ciudad": "Mérida", "estado": "Yucatán"},
    {"id": 6, "nombre": "Alamedas del Sur", "ciudad": "Puebla", "estado": "Puebla"}
]

class LeadPayload(BaseModel):
    id: int
    nombre: str
    email: str
    telefono: str
    origen: str
    fecha_registro: str
    estatus: str
    presupuesto: Optional[float] = None
    desarrollo_id: int
    comentarios: Optional[str] = None

@app.get("/api/desarrollos")
def get_desarrollos():
    """Retorna el catálogo oficial de desarrollos activos."""
    return {"status": "success", "data": DESARROLLOS_DB}

@app.post("/api/leads")
def sync_lead(lead: LeadPayload, authorization: Optional[str] = Header(None)):
    """
    Recibe un prospecto para sincronizarlo con el CRM.
    Simula validaciones de autenticación, rate limit, datos erróneos y fallas de red.
    """
    global request_counter
    request_counter += 1

    # 1. Simulación de 401 Unauthorized
    if authorization != "Bearer atlas-token-2026":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="No autorizado: Requiere header 'Authorization: Bearer atlas-token-2026'"
        )

    # 2. Simulación de 429 Too Many Requests (cada 15 peticiones)
    if request_counter % 15 == 0:
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="Rate limit excedido: Máximo 15 peticiones por minuto. Espera antes de reintentar."
        )

    # 3. Simulación de 400 Bad Request
    if "@" not in lead.email or not lead.nombre.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Lead {lead.id} rechazado: email ('{lead.email}') o nombre inválido."
        )

    # 4. Simulación de 500 Internal Server Error (intermitente)
    if random.random() < 0.05:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error temporal en el servicio de CRM. Reintente la transacción."
        )

    return {
        "status": "created",
        "lead_id": lead.id,
        "message": f"Lead {lead.nombre} sincronizado exitosamente."
    }
