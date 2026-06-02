import random
import signal
import threading
import time
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime

import oracledb


# ============================================================
# CONFIGURAÇÃO PRINCIPAL
# ============================================================

# Opções aceitas:
# "suave"
# "media"
# "média"
# "intensa"
CARGA = "media"

# Ambiente Docker atual:
# Windows/DBeaver: localhost:1522/FREEPDB1
DSN = "localhost:1522/FREEPDB1"

USUARIOS = [
    {"user": "SIM_USER_01", "password": "SimUser123"},
    {"user": "SIM_USER_02", "password": "SimUser123"},
    {"user": "SIM_USER_03", "password": "SimUser123"},
]


# ============================================================
# PERFIS DE CARGA
# ============================================================

PERFIS = {
    "suave": {
        "workers": 3,
        "sleep_min": 1.5,
        "sleep_max": 3.0,
        "cpu_level": 8000,
        "lock_probability": 0.02,
        "lock_hold_min": 0.5,
        "lock_hold_max": 1.5,
    },
    "media": {
        "workers": 8,
        "sleep_min": 0.4,
        "sleep_max": 1.2,
        "cpu_level": 30000,
        "lock_probability": 0.06,
        "lock_hold_min": 1.0,
        "lock_hold_max": 2.5,
    },
    "intensa": {
        "workers": 18,
        "sleep_min": 0.05,
        "sleep_max": 0.35,
        "cpu_level": 90000,
        "lock_probability": 0.14,
        "lock_hold_min": 2.0,
        "lock_hold_max": 5.0,
    },
}


# ============================================================
# QUERIES UTILIZADAS NA SIMULAÇÃO
# ============================================================

QUERY_COUNT_INDEXADA = """
SELECT COUNT(*) AS total
FROM sim_owner.carga_lab
WHERE categoria = :categoria
  AND cidade = :cidade
"""

QUERY_AGREGADA = """
SELECT cidade,
       categoria,
       COUNT(*) AS total_vendas,
       ROUND(SUM(valor_total), 2) AS valor_total
FROM sim_owner.carga_lab
WHERE data_venda >= SYSDATE - :dias
GROUP BY cidade, categoria
ORDER BY cidade, categoria
"""

QUERY_FULL_SCAN = """
SELECT COUNT(*) AS total,
       ROUND(AVG(valor_total), 2) AS ticket_medio
FROM sim_owner.carga_lab
WHERE MOD(id, :modulo) = 0
"""

QUERY_CPU = """
SELECT SUM(SQRT(LEVEL)) AS carga_cpu
FROM dual
CONNECT BY LEVEL <= :nivel
"""

QUERY_LOCK = """
UPDATE sim_owner.lock_lab
SET descricao = :descricao,
    updated_at = SYSTIMESTAMP
WHERE id = 1
"""


CATEGORIAS = [
    "INFORMATICA",
    "MOVEIS",
    "AUDIO",
    "VIDEO",
    "PERIFERICOS",
]

CIDADES = [
    "BELO HORIZONTE",
    "SAO PAULO",
    "RIO DE JANEIRO",
    "CURITIBA",
    "SALVADOR",
    "RECIFE",
]


# ============================================================
# CONTROLE DE EXECUÇÃO
# ============================================================

stop_event = threading.Event()


def normalizar_carga(valor: str) -> str:
    valor = valor.strip().lower()
    valor = valor.replace("é", "e").replace("ê", "e")
    return valor


def configurar_sinal_de_parada():
    def parar(signum, frame):
        print("\nParando simulação...")
        stop_event.set()

    signal.signal(signal.SIGINT, parar)
    signal.signal(signal.SIGTERM, parar)


def criar_conexao(usuario: dict):
    conn = oracledb.connect(
        user=usuario["user"],
        password=usuario["password"],
        dsn=DSN,
    )

    # Evita que uma sessão fique presa por tempo excessivo em caso de lock.
    # Valor em milissegundos.
    conn.call_timeout = 30000

    return conn


def definir_modulo_sessao(cursor, worker_id: int, perfil_nome: str):
    """
    Ajuda a identificar as sessões no v$session.
    Se o usuário não tiver permissão para executar DBMS_APPLICATION_INFO,
    a simulação continua normalmente.
    """
    try:
        cursor.callproc(
            "DBMS_APPLICATION_INFO.SET_MODULE",
            [f"SIMULADOR_ORACLE_{perfil_nome.upper()}", f"WORKER_{worker_id}"],
        )
    except Exception:
        pass


def executar_query_leitura(cursor, perfil: dict):
    tipo = random.choices(
        population=[
            "count_indexada",
            "agregada",
            "full_scan",
            "cpu",
        ],
        weights=[
            35,
            25,
            25,
            15,
        ],
        k=1,
    )[0]

    if tipo == "count_indexada":
        cursor.execute(
            QUERY_COUNT_INDEXADA,
            categoria=random.choice(CATEGORIAS),
            cidade=random.choice(CIDADES),
        )
        cursor.fetchall()
        return "COUNT_INDEXADA"

    if tipo == "agregada":
        cursor.execute(
            QUERY_AGREGADA,
            dias=random.choice([30, 60, 90, 180, 365]),
        )
        cursor.fetchall()
        return "AGREGADA"

    if tipo == "full_scan":
        cursor.execute(
            QUERY_FULL_SCAN,
            modulo=random.choice([2, 3, 5, 7, 11]),
        )
        cursor.fetchall()
        return "FULL_SCAN"

    if tipo == "cpu":
        cursor.execute(
            QUERY_CPU,
            nivel=perfil["cpu_level"],
        )
        cursor.fetchall()
        return "CPU"

    return "DESCONHECIDA"


def executar_lock(conn, cursor, worker_id: int, usuario: str, perfil: dict):
    descricao = (
        f"{usuario} | worker={worker_id} | "
        f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
    )

    cursor.execute(
        QUERY_LOCK,
        descricao=descricao,
    )

    tempo_segundos = random.uniform(
        perfil["lock_hold_min"],
        perfil["lock_hold_max"],
    )

    print(
        f"[{usuario}] worker={worker_id} segurando lock por "
        f"{tempo_segundos:.2f}s"
    )

    time.sleep(tempo_segundos)

    conn.commit()

    return "LOCK"


def worker(worker_id: int, perfil_nome: str, perfil: dict):
    usuario = USUARIOS[worker_id % len(USUARIOS)]

    nome_usuario = usuario["user"]

    try:
        conn = criar_conexao(usuario)

        with conn.cursor() as cursor:
            definir_modulo_sessao(cursor, worker_id, perfil_nome)

            while not stop_event.is_set():
                inicio = time.time()

                try:
                    if random.random() < perfil["lock_probability"]:
                        tipo_operacao = executar_lock(
                            conn=conn,
                            cursor=cursor,
                            worker_id=worker_id,
                            usuario=nome_usuario,
                            perfil=perfil,
                        )
                    else:
                        tipo_operacao = executar_query_leitura(cursor, perfil)

                    duracao = time.time() - inicio

                    print(
                        f"[{nome_usuario}] worker={worker_id} "
                        f"operacao={tipo_operacao} "
                        f"duracao={duracao:.3f}s"
                    )

                except oracledb.Error as erro:
                    try:
                        conn.rollback()
                    except Exception:
                        pass

                    print(
                        f"[{nome_usuario}] worker={worker_id} "
                        f"erro Oracle: {erro}"
                    )

                except Exception as erro:
                    try:
                        conn.rollback()
                    except Exception:
                        pass

                    print(
                        f"[{nome_usuario}] worker={worker_id} "
                        f"erro inesperado: {erro}"
                    )

                pausa = random.uniform(
                    perfil["sleep_min"],
                    perfil["sleep_max"],
                )

                time.sleep(pausa)

    except Exception as erro:
        print(f"[{nome_usuario}] worker={worker_id} falhou ao conectar: {erro}")

    finally:
        try:
            conn.close()
        except Exception:
            pass


def main():
    configurar_sinal_de_parada()

    perfil_nome = normalizar_carga(CARGA)

    if perfil_nome not in PERFIS:
        raise ValueError(
            f"CARGA inválida: {CARGA}. "
            f"Use: suave, media ou intensa."
        )

    perfil = PERFIS[perfil_nome]

    print("=" * 70)
    print("Simulador de usuários Oracle")
    print("=" * 70)
    print(f"DSN: {DSN}")
    print(f"Carga selecionada: {perfil_nome}")
    print(f"Workers/sessões simultâneas: {perfil['workers']}")
    print("Usuários:")
    for usuario in USUARIOS:
        print(f" - {usuario['user']}")
    print("=" * 70)
    print("Pressione CTRL + C para parar.")
    print("=" * 70)

    with ThreadPoolExecutor(max_workers=perfil["workers"]) as executor:
        futures = [
            executor.submit(worker, i + 1, perfil_nome, perfil)
            for i in range(perfil["workers"])
        ]

        try:
            while not stop_event.is_set():
                time.sleep(1)
        finally:
            stop_event.set()

            for future in futures:
                try:
                    future.result(timeout=5)
                except Exception:
                    pass

    print("Simulação encerrada.")


if __name__ == "__main__":
    main()