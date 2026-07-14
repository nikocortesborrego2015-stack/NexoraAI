from ollama import chat

print("=" * 40)
print("Orivox IA")
print("Tu asistente para tareas y preguntas")
print("=" * 40)

while True:
    pregunta = input("\nTú: ")

    if pregunta.lower() == "salir":
        print("👋 ¡Hasta luego!")
        break

    respuesta = chat(
        model="qwen3:8b",
        think=False,
        messages=[
            {
                "role": "system",
                "content": """
Eres Nexora AI, un asistente de inteligencia artificial.

Siempre respondes en español.

Tu trabajo es:
- Ayudar con tareas escolares.
- Explicar paso a paso.
- Resolver matemáticas.
- Ayudar con programación.
- Ayudar con ciencias, historia, inglés y cualquier materia.
- Si no sabes algo, dilo con sinceridad.
- Sé amable y claro.
"""
            },
            {
                "role": "user",
                "content": pregunta
            }
        ]
    )

    print("\n Orivox IA:", respuesta["message"]["content"])