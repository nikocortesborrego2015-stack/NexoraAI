from flask import Flask, render_template, request
from ollama import chat
from ddgs import DDGS
import time

app = Flask(__name__)


def cargar_conocimientos():
    try:
        with open("conocimientos.txt", "r", encoding="utf-8") as archivo:
            return archivo.read()
    except Exception:
        return ""


def buscar_internet(pregunta):
    resultados = ""

    try:
        with DDGS() as ddgs:
            consulta = pregunta + " Colombia significado oficial"

            for resultado in ddgs.text(consulta, max_results=5):
                titulo = resultado.get("title", "")
                cuerpo = resultado.get("body", "")
                enlace = resultado.get("href", "")

                resultados += f"Título: {titulo}\n"
                resultados += f"Contenido: {cuerpo}\n"
                resultados += f"Fuente: {enlace}\n\n"

    except Exception as e:
        print("Error buscando en Internet:", e)

    return resultados


@app.route("/")
def inicio():
    return render_template("index.html")


@app.route("/preguntar", methods=["POST"])
def preguntar():

    inicio = time.time()

    pregunta = request.form["pregunta"]

    conocimientos = cargar_conocimientos()
    informacion_web = buscar_internet(pregunta)

    print("Búsqueda:", round(time.time() - inicio, 2), "segundos")

    respuesta = chat(
        model="qwen3:8b",
        think=False,
        options={
            "temperature": 0.2,
            "num_predict": 180
        },
        messages=[
            {
                "role": "system",
                "content": f"""
Eres Nexora AI, un asistente de inteligencia artificial.

Siempre respondes en español.

Reglas:

- Analiza primero la información encontrada en Internet.
- Si Internet contiene la respuesta, úsala.
- No inventes información.
- Si existen varios significados, explica primero el más usado según el contexto.
- Si la búsqueda es sobre Colombia, prioriza fuentes colombianas.
- Si no encuentras suficiente información, dilo claramente.
- Responde de forma clara, precisa y breve.

Información encontrada en Internet:

{informacion_web}

Información adicional:

{conocimientos}
"""
            },
            {
                "role": "user",
                "content": pregunta
            }
        ]
    )

    texto = respuesta["message"]["content"]

    print("Tiempo total:", round(time.time() - inicio, 2), "segundos")

    if "</think>" in texto:
        texto = texto.split("</think>")[-1]

    return texto.strip()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)