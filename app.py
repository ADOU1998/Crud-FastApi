from ast import Raise
from datetime import date, datetime
from http.client import HTTPException
import imp
from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional
from uuid import uuid4

app = FastAPI() # Création de l'objet

etudiants = []

# Etudiant Model
class Etudiant(BaseModel):
    id: Optional[str]
    sexe: str
    nom: str
    prenoms: str
    date_naiss: date
    lieu_naiss: str
    created_ad: datetime = datetime.now()
    updated_at: datetime = datetime.now()
    

# Endpoint Initail
@app.get("/")
async def read_root():
    return {"Méssage": "Bienvenu sur mon api crud"}

# Endpoint : Créer
@app.post("/etudiants/", status_code=201)
async def create_etudiant(etudiant: Etudiant):
    etudiant.id = str(uuid4())
    etudiants.append(etudiant.dict())
    return "Enregistrement éffectué avec succés !"

# Endpoint : Afficher la liste complête
@app.get("/etudiants")
async def get_etudiants():
    return etudiants

# Endpoint : Afficher l'info d'un étudiant via l' id
@app.get("/etudiants/{etudiant_id}")
async def get_etudiants(etudiant_id: str):
    for etudiant in etudiants:
        if etudiant["id"] == etudiant_id:
            return etudiant 
    raise HTTPException(status_code=404, detail="L'etudiant n'a pas été trouvé !")

# Endpoint : Modifier
@app.put("/etudiants/{etudiant_id}")
async def update_etudiant(etudiant_id: str, updateEtudiant: Etudiant):
    for index, etudiant in enumerate(etudiants):
        if etudiant["id"] == etudiant_id:
            etudiants[index]["sexe"] = updateEtudiant.sexe
            etudiants[index]["nom"] = updateEtudiant.nom
            etudiants[index]["prenoms"] = updateEtudiant.prenoms
            etudiants[index]["date_naiss"] = updateEtudiant.date_naiss
            etudiants[index]["lieu_naiss"] = updateEtudiant.lieu_naiss
            return {"Méssage": "Cet éttudiant a été modifié avec succès !"}
        
# Endpoint : Suppression
@app.delete("/etudiants/{etudiant_id}")
async def delete_etudiants(etudiant_id: str):
    for index, etudiant in enumerate(etudiants):
        if etudiant["id"] == etudiant_id:
            etudiants.pop(index)
            return {"Méssage": "Cet étudiant a été supprimé !"}
    raise HTTPException(status_code=404, detail="Aucun étudiant trouvé !")

