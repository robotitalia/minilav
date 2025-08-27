from fastapi import FastAPI, Request, Response
import httpx

app = FastAPI()

# URL del tuo endpoint target
TARGET_URL = "https://apistg.lavoro.gov.it/InformationDelivery/SmartWorking_Bulk/Rest/1.0/"

@app.api_route("/creaComunicazioni", methods=["GET", "POST", "OPTIONS"])
async def proxy(path: str, request: Request):
    # Costruisci URL completo
    url = f"{TARGET_URL}/{path}"

    # Copia headers (escludendo host)
    headers = {k: v for k, v in request.headers.items() if k.lower() != "host"}
    
    
    # Corpo della richiesta
    body = await request.body()
    console.log("Body: "+body)
    
    # Inoltra la chiamata al target usando httpx
    async with httpx.AsyncClient(verify=False) as client:  # verify=False per self-signed
        resp = await client.request(
            method=request.method,
            url=url,
            headers=headers,
            content=body,
            cookies=request.cookies
        )

    # Crea la risposta da rimandare al client
    response = Response(
        content=resp.content,
        status_code=resp.status_code,
        headers={k: v for k, v in resp.headers.items() if k.lower() not in ["content-encoding", "transfer-encoding", "connection"]}
    )
    return response
