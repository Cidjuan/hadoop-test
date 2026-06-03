import time
import random
import pandas as pd
import matplotlib.pyplot as plt
from pymongo import MongoClient
# ============================================
# CONFIGURACIÓN - CAMBIE ESTA LÍNEA
# ============================================
URL_MONGO = "mongodb+srv://testuser:testpassword@cluster0.gl64i5p.mongodb.net/"
print("="*60)
print("TALLER HADOOP - Prueba de Big Data")
print("Conceptos: Velocidad + Variedad + Visualización")
print("Base de datos: MongoDB (NoSQL)")
print("="*60)
# ============================================
# PRUEBA 1: VELOCIDAD
# ============================================
print("\n[1/3] Probando VELOCIDAD...")
cliente = MongoClient(URL_MONGO)
db_velocidad = cliente["test_velocidad"]
col_velocidad = db_velocidad["eventos"]
inicio = time.time()
TOTAL_REGISTROS = 500
for i in range(TOTAL_REGISTROS):
    col_velocidad.insert_one({
        "id": i,
        "tipo": random.choice(["click", "compra", "vista", "login"]),
        "valor": random.randint(1, 1000),
        "timestamp": time.time()
    })
fin = time.time()
tiempo_total = fin - inicio
velocidad = TOTAL_REGISTROS / tiempo_total
print(f" Registros insertados: {TOTAL_REGISTROS}")
print(f" Tiempo: {tiempo_total:.2f} segundos")
print(f" Velocidad: {velocidad:.2f} ops/segundo")
# ============================================
# PRUEBA 2: VARIEDAD
# ============================================
print("\n[2/3] Probando VARIEDAD...")
db_variedad = cliente["test_variedad"]
col_variedad = db_variedad["datos_variados"]
tipos = ["usuario", "producto", "transaccion", "log"]
for i in range(100):
    tipo = random.choice(tipos)
    if tipo == "usuario":
        doc = {"tipo": "usuario", "nombre": f"user_{i}", "edad": random.randint(18, 70)}
    elif tipo == "producto":
        doc = {"tipo": "producto", "nombre": f"prod_{i}", "precio": random.randint(10, 500)}
    elif tipo == "transaccion":
        doc = {"tipo": "transaccion", "monto": random.randint(1, 1000), "items": random.randint(1, 5)}
    else:
        doc = {"tipo": "log", "mensaje": f"evento_{i}", "nivel": random.choice(["INFO", "ERROR"])}
    col_variedad.insert_one(doc)
total_docs = col_variedad.count_documents({})
print(f" Documentos insertados: {total_docs}")
print(f" Tipos de estructura: {len(tipos)}")
# ============================================
# PRUEBA 3: VISUALIZACIÓN
# ============================================
print("\n[3/3] Generando VISUALIZACIÓN...")
datos = list(col_velocidad.find({}, {"_id": 0, "tipo": 1, "valor": 1}))
df = pd.DataFrame(datos)
# Crear gráfico
fig, axes = plt.subplots(1, 2, figsize=(12, 5))
# Gráfico 1: Barras
df.groupby("tipo")["valor"].mean().plot(kind="bar", ax=axes[0])
axes[0].set_title("Valor promedio por tipo de evento")
axes[0].set_xlabel("Tipo")
axes[0].set_ylabel("Valor promedio")
# Gráfico 2: Pastel
df.groupby("tipo").size().plot(kind="pie", ax=axes[1], autopct='%1.1f%%')
axes[1].set_title("Distribución de eventos")
plt.suptitle("Taller Hadoop - Resultados", fontsize=14)
plt.tight_layout()
plt.savefig("resultado_hadoop.png", dpi=100)
print(" Gráfico guardado: resultado_hadoop.png")
# ============================================
# RESULTADOS FINALES
# ============================================
print("\n" + "="*60)
print("RESULTADOS FINALES")
print("="*60)
print(f"\nVelocidad: {velocidad:.2f} registros/segundo")
print(f"Variedad: {total_docs} documentos con {len(tipos)} estructuras")
print("\nEstadísticas por tipo de evento:")
print(df.groupby("tipo")["valor"].describe())
print("\n" + "="*60)
print("TALLER COMPLETADO EXITOSAMENTE")
print("Conceptos probados: Velocidad + Variedad + Visualización")
print("Tecnologías: Python + MongoDB + Pandas + Matplotlib")
print("="*60)
cliente.close()
print("\nPara ver el gráfico, ejecute el siguiente comando:")
print("python3 -m http.server 8080")
