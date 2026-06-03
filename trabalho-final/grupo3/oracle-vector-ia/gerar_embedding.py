import oracledb
from sentence_transformers import SentenceTransformer

model = SentenceTransformer("all-MiniLM-L6-v2")

conn = oracledb.connect(
    user="User",
    password="Password",
    dsn="localhost:1526/FREEPDB1"
)

cursor = conn.cursor()

cursor.execute("""
    SELECT id, texto
    FROM kb_docs
    WHERE embedding IS NULL
""")

docs = cursor.fetchall()

for doc_id, texto in docs:
    texto_str = texto.read() if hasattr(texto, "read") else str(texto)

    embedding = model.encode(texto_str)
    embedding_str = "[" + ",".join(map(str, embedding.tolist())) + "]"

    cursor.execute("""
        UPDATE kb_docs
        SET embedding = TO_VECTOR(:embedding, 384, FLOAT32)
        WHERE id = :id
    """, {
        "embedding": embedding_str,
        "id": doc_id
    })

conn.commit()

cursor.close()
conn.close()

print("Embeddings gerados e salvos com sucesso!")