# 🧹 CleanPro RAG Assistant

Asistente inteligente para la empresa **CleanPro**, que responde preguntas sobre **inventario** y **turnos** usando **RAG (Retrieval-Augmented Generation)**.  

Construido con:  
- **LangChain** (pipeline de RAG)  
- **ChromaDB** (vectorstore)  
- **OpenAI embeddings & LLM**  
- **FastAPI** (backend)  
- **Streamlit** (frontend)  

---

## 🚀 Características
- 📦 Consultas sobre inventario de **Las Condes** (desde `inventory_las_condes.csv`).  
- 🧑‍🤝‍🧑 Consultas sobre turnos de **septiembre** (desde `turnos_septiembre.csv`).  
- 🌐 API en **FastAPI**.  
- 💬 Interfaz web en **Streamlit** con historial estilo chat.  
- 🧪 Script de pruebas en **PowerShell**.  

---

## 📂 Estructura del proyecto

```
EV1/
├── data/                     
│   ├── inventory_las_condes.csv
│   └── turnos_septiembre.csv
├── src/
│   ├── ingestion/
│   │   └── ingest_all.py     # Ingesta de datos y creación del vectorstore
│   ├── chains/
│   │   └── rag_chain.py      # Configuración del RAG
│   └── api/
│       └── app.py            # API con FastAPI
├── app_streamlit.py          # Interfaz frontend con Streamlit
├── test.ps1                  # Script de pruebas en PowerShell
└── README.md
```

---

## ⚙️ Instalación

### 1. Clonar el proyecto y crear entorno virtual
```powershell
git clone <repo>
cd EV1
python -m venv .venv
.\.venv\Scriptsctivate
```

### 2. Instalar dependencias
```powershell
pip install -r requirements.txt
```

Dependencias principales:
```
langchain
langchain-community
langchain-openai
chromadb
fastapi
uvicorn
python-dotenv
streamlit
requests
```

### 3. Configurar variables de entorno
Crea un archivo `.env` en la raíz (`EV1/.env`) con:

```ini
OPENAI_API_KEY=tu_api_key
OPENAI_BASE_URL=https://models.inference.ai.azure.com
OPENAI_EMBEDDINGS_URL=https://models.github.ai/inference
```

---

## 📥 Ingesta de datos
Ejecuta el proceso que carga los CSV en ChromaDB:

```powershell
python src/ingestion/ingest_all.py
```

Deberías ver algo como:
```
🔄 Ingestando documentos...
Total docs: 2
Total chunks: 16
✅ Vectorstore creado en ./.chroma_db
```

---

## 🌐 Usar la API con FastAPI

1. Levanta el backend con Uvicorn:
```powershell
uvicorn src.api.app:app --reload --port 8000
```

Verás:
```
Uvicorn running on http://127.0.0.1:8000
Application startup complete.
```

2. En otra consola, haz consultas desde PowerShell:  
   Ejemplo:
```powershell
$body = @{ q = "¿Cuánto cloro queda en la bodega de Las Condes?" } | ConvertTo-Json -Compress
Invoke-RestMethod -Uri "http://127.0.0.1:8000/query" -Method Post -ContentType "application/json; charset=utf-8" -Body ([System.Text.Encoding]::UTF8.GetBytes($body))
```

Respuesta:
```json
{
  "answer": "Actualmente hay 12 litros de cloro en la bodega de Las Condes (último registro 20/08/2025)."
}
```

---

## 🧪 Script de pruebas (PowerShell)

En la raíz tienes un `test.ps1` para probar varias consultas de una sola vez.  

Ejecuta:
```powershell
.	est.ps1
```

Ejemplo de salida:
```
🚀 Probando API RAG...
Pregunta: ¿Cuánto cloro queda en la bodega de Las Condes?
Respuesta: En la sucursal Las Condes hay 12 litros de cloro registrados en el último movimiento.
---------------------------------------------
Pregunta: ¿Quién tiene turno mañana en oficinas administrativas el 2025-09-25?
Respuesta: El 25 de septiembre de 2025 tiene turno Juan Pérez (07:00 a 15:00).
---------------------------------------------
```

---

## 💬 Interfaz Web con Streamlit

1. Deja corriendo la API FastAPI en una consola:
```powershell
uvicorn src.api.app:app --reload --port 8000
```

2. En otra consola, corre Streamlit:
```powershell
streamlit run app_streamlit.py
```

3. Se abrirá en tu navegador en:
```
http://localhost:8501
```

### Funcionalidades
- Caja de texto para preguntar.  
- Botón **Enviar**.  
- Historial de chat estilo WhatsApp (preguntas y respuestas acumuladas).  

---

## 📝 Ejemplos de preguntas

### Inventario
- ¿Cuánto cloro queda en la bodega de Las Condes?  
- ¿Qué stock de guantes hay en la bodega de Las Condes?  

### Turnos
- ¿Quién tiene turno mañana en oficinas administrativas el 2025-09-25?  
- ¿Qué turnos tiene Juan Pérez en septiembre?  

### Preguntas fuera de evidencia (para probar negaciones)
- ¿Qué productos hay en Providencia?  
- ¿Quién tiene turno en octubre?  

El asistente responderá algo como:  
> *“La evidencia no incluye información sobre la sucursal Providencia.”*  

---

## 🔮 Futuras mejoras
- Añadir más fuentes (otras sucursales, otros meses).  
- Mostrar evidencia en Streamlit (ej: CSV de donde salió la respuesta).  
- Desplegar en la nube (Render, Railway o Azure).  

---

## 👨‍💻 Autor
Proyecto desarrollado por **Nico Osses** para la asignatura de **IA - Evaluación 1**.  
