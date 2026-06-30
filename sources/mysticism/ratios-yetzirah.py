import json
import sys
import numpy as np

valores_gematria = {
    'א': 1, 'ב': 2, 'ג': 3, 'ד': 4, 'ה': 5, 'ו': 6, 'ז': 7, 'ח': 8,
    'ט': 9, 'י': 10, 'כ': 20, 'ל': 30, 'מ': 40, 'נ': 50, 'ס': 60, 'ע': 70,
    'פ': 80, 'צ': 90, 'ק': 100, 'ר': 200, 'ש': 300, 'ת': 400
}

# Función para convertir texto a valores de gematría
def texto_a_gematria(texto):
    gematria = []
    for letra in texto:
        valor = valores_gematria.get(letra, 0)
        gematria.append(valor)
    return gematria

# Función para convertir valores de gematría a texto en hebreo
def gematria_a_texto(gematria):
    texto = ""
    for val in gematria:
        for letra, valor in valores_gematria.items():
            if valor == val:
                texto += letra
                break
    return texto

res=[]
secret = ""
ftorah = open("sefer_yetzirah.json","r").read()
for x in json.loads(ftorah)["text"]:
    for t in x:
        secret += t[0:2]
        print(t)
        togem = list(filter((0).__ne__, texto_a_gematria(t.replace(" ",""))))
        res.append(togem)

#print(res)
for x in res:

    ratios = [x[i] / x[i-1] for i in range(1, len(x))]
    print(ratios)

print(secret)
