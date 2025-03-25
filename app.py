from fastapi import FastAPI, UploadFile, File
import grammalecte
import cyhunspell
from io import BytesIO

app = FastAPI()

# Charger Grammalecte pour le français
grammalecte_instance = grammalecte.GrammarChecker("fr")

# Charger Hunspell pour le français
hunspell_instance = cyhunspell.Hunspell('fr_FR')

@app.get("/")
async def accueil():
    return {"message": "API Grammalecte + Hunspell opérationnelle"}

@app.post("/analyser")
async def analyser_texte(file: UploadFile = File(...)):
    texte = (await file.read()).decode('utf-8')
    resultats_grammaire = grammalecte_instance.check(texte)

    mots = texte.split()
    erreurs_orthographe = [mot for mot in mots if not hunspell_instance.spell(mot)]

    return {
        "erreurs_grammaire": resultats_grammaire,
        "erreurs_orthographe": erreurs_orthographe
    }
