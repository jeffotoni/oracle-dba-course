import oracledb
from sentence_transformers import SentenceTransformer

model = SentenceTransformer("all-MiniLM-L6-v2")

conn = oracledb.connect(
    user="User",
    password="Password",
    dsn="localhost:1526/FREEPDB1"
)

cursor = conn.cursor()

while True:
    pergunta = input("\nOi, como posso ajudar? (Digite 'sair' para encerrar): ")

    if pergunta.lower() == "sair":
        print("Até mais! Bons estudos.")
        break

    embedding = model.encode(pergunta)
    embedding_str = "[" + ",".join(map(str, embedding.tolist())) + "]"

    cursor.execute("""
        SELECT titulo,
               texto,
               VECTOR_DISTANCE(
                 embedding,
                 TO_VECTOR(:embedding, 384, FLOAT32),
                 COSINE
               ) AS distancia
        FROM kb_docs
        WHERE embedding IS NOT NULL
        ORDER BY distancia
        FETCH FIRST 3 ROWS ONLY
    """, {
        "embedding": embedding_str
    })

    resultados = cursor.fetchall()

    print("\nResposta do Assistente:")
    print("-------------------")

    if not resultados:
        print("Ainda não encontrei materiais cadastrados para responder essa pergunta.")
        continue

    titulo, texto, distancia = resultados[0]

    if distancia > 0.55:
        print("""
Desculpe, não consegui localizar uma resposta para essa pergunta no momento.
Posso ajudar você a encontrar informações sobre outros temas?
""")
    else:
        print(f"Encontrei um conteúdo relacionado: {titulo}")
        print()
        print(texto)
        print()
        print(f"Nível de similaridade: {round(1 - distancia, 2)}")

cursor.close()
conn.close()