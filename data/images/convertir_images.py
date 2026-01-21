from PIL import Image
import os

# convertit tous les JPEG/JPG vers PNG
for nom in os.listdir():
    if nom.lower().endswith((".jpg", ".jpeg")):
        img = Image.open(nom)
        nouveau_nom = nom.rsplit(".", 1)[0] + ".png"
        img.save(nouveau_nom, "PNG")
        print(f"Converti : {nom} → {nouveau_nom}")
