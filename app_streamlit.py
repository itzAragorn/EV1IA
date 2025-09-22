# app_streamlit.py
import streamlit as st
import requests

st.set_page_config(page_title="CleanPro RAG", page_icon="🧹")

st.title("🧹 Asistente CleanPro")
st.write("Haz preguntas sobre inventario y turnos usando el RAG conectado a FastAPI.")

# Inicializar historial en la sesión
if "messages" not in st.session_state:
    st.session_state["messages"] = []

# Mostrar historial como burbujas estilo chat
for msg in st.session_state["messages"]:
    if msg["role"] == "user":
        st.markdown(f"🧑 **Tú:** {msg['content']}")
    else:
        st.markdown(f"🤖 **Asistente:** {msg['content']}")

# Caja de texto para nueva pregunta
question = st.text_input("❓ Escribe tu pregunta:")

if st.button("Enviar") and question:
    # Guardar mensaje del usuario
    st.session_state["messages"].append({"role": "user", "content": question})

    try:
        response = requests.post(
            "http://127.0.0.1:8000/query",
            json={"q": question},
            timeout=30
        )

        if response.status_code == 200:
            data = response.json()
            answer = data["answer"]
        else:
            answer = f"⚠️ Error {response.status_code}: {response.text}"

    except Exception as e:
        answer = f"❌ No se pudo conectar con la API: {e}"

    # Guardar respuesta del asistente
    st.session_state["messages"].append({"role": "assistant", "content": answer})

    # Refrescar la página para mostrar la nueva interacción
    st.rerun()
