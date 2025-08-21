#from typing import Optional
#from fastapi import FastAPI

#app = FastAPI()

#@app.get("/")
#async def root():
#    return {"message": "Hello World"}

#@app.get("/items/{item_id}")
#def read_item(item_id: int, q: Optional[str] = None):
#    return {"item_id": item_id, "q": q}


# fast.py
# per far partire il server usare questo su terminale
# uvicorn FastAPI:app --reload --host 0.0.0.0 --port 8080

from fastapi import FastAPI, UploadFile, File
from pydantic import BaseModel, Field
import random
from typing import Optional
from fastapi.openapi.docs import get_swagger_ui_html, get_redoc_html
from fastapi.staticfiles import StaticFiles
import time

# Cartella dove metti la favicon
static_dir = "favicons"
#os.makedirs(static_dir, exist_ok=True)

# Favicon con query string per forzare refresh
favicon_path = f"/favicons/favicon2.ico?v={int(time.time())}"

app = FastAPI(
        title="MiLavo",
        description="Documentazioen MiLavo.",
        version="2.0.0",
        contact={"name": "Ufficio"},
        license_info={"name": "ENTE"},
        #docs_url="/openapi.json",
        #redocs_url="/openapi.json",
        docs_url=None, 
        redoc_url=None
    )

# Monti la cartella statica
app.mount("/favicons", StaticFiles(directory=static_dir), name="favicon2.ico")

@app.get("/docs", include_in_schema=False)
async def custom_docs():
    return get_swagger_ui_html(
        openapi_url="/openapi.json",
        title="MiLavo API Docs",
        swagger_favicon_url=favicon_path
    )

# Endpoint Redoc
@app.get("/redoc", include_in_schema=False)
async def custom_redoc():
    return get_redoc_html(
        openapi_url="/openapi.json",
        title="MiLavo API Docs",
        redoc_favicon_url=favicon_path
    )

# Modello in input
class Item(BaseModel):
    name: str = Field( description="Nominativo", example="Mario Rossi")
    language: str
    id: str = Field(min_length=16, max_length=16, description="ID deve essere di 16",  example="1234567890123456")
    bio: Optional[str] = Field(None, max_length=300)
    version: float

# Modello in output
class ItemResponse(BaseModel):
    nome: str
    versione: float
    response: bool

@app.get("/")
async def check_online_status():
  return {"status":"online"}

@app.get("/saluta")
async def una_API_educata():
  return {"Ciao a tutti!"}

# Crea l'endpoint POST che si aspetta il JSON
@app.post("/json", response_model=list[ItemResponse])
async def Controlla_e_carica_elementi(items: list[Item]):
    out=[]
    for item in items:
        ciccio = {
           "nome": item.name, 
           "versione": item.version, 
           "response":random.choice([True,False])
        }
        if item.bio is not None:
            print (item.name,"--",len(item.bio))
        else:
            print (item.name,"--","0")

        out.append(ciccio)
    #js = json.dumps(out)
    #print(js)
    return out

# non funziona dai test, si invia il file e non viene correttamente riconosciuto
#@app.post("/fileupload")
#async def upload_file(file: UploadFile = File(...)):
#    return {"filename": file.filename, "content_type": file.content_type}
    
