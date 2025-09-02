from fastapi import FastAPI, Request
from fastapi.responses import Response
from fastapi.middleware.cors import CORSMiddleware

import httpx
import json
import logging

# Configurazione base del logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("proxy_app")

app = FastAPI()

# URL del tuo endpoint target
TARGET_URL = "https://apistg.lavoro.gov.it/InformationDelivery/SmartWorking_Bulk/Rest/1.0"

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # meglio specificare i domini consentiti
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.api_route("/creaComunicazioni", methods=["GET", "POST"])
async def proxy(request: Request):

    logger.info("=== Nuova richiesta ricevuta ===")
    logger.info("Metodo: %s", request.method)
    logger.info("Query params: %s", dict(request.query_params))
    logger.info("Headers: %s", json.dumps(dict(request.headers), indent=2))

    # Costruisci URL completo
    url = f"{TARGET_URL}/creaComunicazioni"

    # Copia headers (escludendo host)
    #headers = {k: v for k, v in request.headers.items() if k.lower() != "host"}

    # Mantieni solo i necessariC
    headers = { 
        k: v for k, v in request.headers.items()
        if k.lower() in ["authorization", "content-type"]
    }

    # Corpo della richiesta
    body = await request.body()
    try:
        body_json = json.loads(body)
        logger.info("Body JSON: %s", json.dumps(body_json, indent=2))
    except:
        logger.info("Body raw: %s", body.decode(errors="ignore"))

    logger.info("=== Inoltro richiesta ===")
    logger.info("Metodo: %s", request.method)
    logger.info("Query params: %s", dict(request.query_params))
    logger.info("Headers: %s", json.dumps(dict(headers), indent=2))
    logger.info("Body: %s", body.decode("utf-8", errors="ignore"))
    logger.info("Chiamo target URL: %s", url)
    
    # Inoltra la chiamata al target usando httpx
    async with httpx.AsyncClient(verify=False, timeout=20.0) as client:  # verify=False per self-signed
        resp = await client.request(
            method=request.method,
            url=url,
            headers=headers,
            content=body,
            cookies=request.cookies
        )

    # Log completo della risposta
    logger.info("--- Risposta dal target ---")
    logger.info("Status code: %d", resp.status_code)
    logger.info("Headers: %s", json.dumps(dict(resp.headers), indent=2))
    try:
        resp_json = resp.json()
        logger.info("Body JSON: %s", json.dumps(resp_json, indent=2))
    except:
        logger.info("Body raw: %s", resp.text)

    # Crea la risposta da rimandare al client
    response = Response(
        content=resp.content,
        status_code=resp.status_code,
        headers={k: v for k, v in resp.headers.items() if k.lower() not in ["content-encoding", "transfer-encoding", "connection"]}
    )
    return response
