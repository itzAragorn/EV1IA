# app_streamlit.py - Sistema Avanzado de Agentes CleanPro
import streamlit as st
import requests
import json
from datetime import datetime
from typing import Dict, Any

st.set_page_config(
    page_title="CleanPro Intelligent Agents", 
    page_icon="🤖",
    layout="wide"
)

# Estilos CSS personalizados para tema oscuro
st.markdown("""
<style>
    /* Mejorar contraste y legibilidad general */
    .stSelectbox > div > div {
        background-color: #2d3748;
        color: white;
    }
    
    .stTextInput > div > div > input {
        background-color: #2d3748;
        color: white;
        border: 1px solid #4a5568;
    }
    
    .stTextArea > div > div > textarea {
        background-color: #2d3748;
        color: white;
        border: 1px solid #4a5568;
    }
    
    /* Mejorar botones */
    .stButton > button {
        background-color: #4299e1;
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.5rem 1rem;
        font-weight: 600;
        transition: background-color 0.2s;
    }
    
    .stButton > button:hover {
        background-color: #3182ce;
    }
    
    /* Mejorar sidebar si se usa */
    .sidebar .sidebar-content {
        background-color: #1a202c;
    }
    
    /* Estilo para los expandir/collapse */
    .streamlit-expanderHeader {
        background-color: #2d3748;
        color: white;
    }
</style>
""", unsafe_allow_html=True)

# Configuración de la API
API_BASE_URL = "http://127.0.0.1:8000"

# ============================================================================
# FUNCIONES DE UTILIDAD
# ============================================================================

def make_api_request(endpoint: str, method: str = "GET", data: Dict = None) -> Dict[str, Any]:
    """Realiza peticiones a la API de manera segura."""
    try:
        url = f"{API_BASE_URL}{endpoint}"
        
        if method == "GET":
            response = requests.get(url, timeout=30)
        elif method == "POST":
            response = requests.post(url, json=data, timeout=60)
        elif method == "PUT":
            response = requests.put(url, json=data, timeout=30)
        elif method == "DELETE":
            response = requests.delete(url, timeout=30)
        else:
            return {"error": f"Método {method} no soportado"}
        
        if response.status_code == 200:
            return response.json()
        else:
            return {"error": f"Error {response.status_code}: {response.text}"}
            
    except Exception as e:
        return {"error": f"Error de conexión: {str(e)}"}


def display_message(role: str, content: str, timestamp: str = None):
    """Muestra un mensaje en el chat con formato."""
    if timestamp is None:
        timestamp = datetime.now().strftime("%H:%M:%S")
    
    if role == "user":
        st.markdown(f"""
        <div style="background-color: #2d3748; color: white; padding: 15px; border-radius: 12px; margin: 8px 0; border-left: 4px solid #4299e1;">
            <strong>🧑 Usuario ({timestamp}):</strong><br>
            <div style="margin-top: 8px; line-height: 1.5;">
                {content}
            </div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div style="background-color: #1a202c; color: white; padding: 15px; border-radius: 12px; margin: 8px 0; border-left: 4px solid #38b2ac;">
            <strong>🤖 Agente CleanPro ({timestamp}):</strong><br>
            <div style="margin-top: 8px; line-height: 1.5;">
                {content}
            </div>
        </div>
        """, unsafe_allow_html=True)


# ============================================================================
# INICIALIZACIÓN DE ESTADO
# ============================================================================

if "messages" not in st.session_state:
    st.session_state["messages"] = []

if "session_id" not in st.session_state:
    st.session_state["session_id"] = f"web_session_{datetime.now().strftime('%Y%m%d_%H%M%S')}"

if "agent_mode" not in st.session_state:
    st.session_state["agent_mode"] = "individual"

if "system_health" not in st.session_state:
    st.session_state["system_health"] = None


# ============================================================================
# INTERFAZ PRINCIPAL
# ============================================================================

# Título principal con estilo personalizado
st.markdown("""
<div style="background: linear-gradient(90deg, #1a202c 0%, #2d3748 100%); 
            padding: 2rem; 
            border-radius: 15px; 
            margin-bottom: 2rem;
            border: 1px solid #4a5568;">
    <h1 style="color: white; text-align: center; margin: 0; font-size: 2.5rem;">
        🤖 Sistema Inteligente de Agentes CleanPro
    </h1>
    <p style="color: #a0aec0; text-align: center; margin: 0.5rem 0 0 0; font-size: 1.2rem;">
        ✨ Automatización organizacional con IA avanzada ✨
    </p>
    <p style="color: #68d391; text-align: center; margin: 0.5rem 0 0 0; font-size: 1rem;">
        IL2.1 • IL2.2 • IL2.3 • IL2.4 | LangChain • CrewAI • Memoria Adaptativa
    </p>
</div>
""", unsafe_allow_html=True)

# Sidebar con configuraciones
with st.sidebar:
    st.header("⚙️ Configuración")
    
    # Selector de modo de agente
    agent_mode = st.selectbox(
        "Modo de Agente:",
        ["individual", "multi_agente", "planificacion"],
        index=["individual", "multi_agente", "planificacion"].index(st.session_state["agent_mode"]),
        help="Individual: Un agente con memoria\nMulti-agente: Crew de especialistas\nPlanificación: Sistema adaptativo"
    )
    st.session_state["agent_mode"] = agent_mode
    
    # ID de sesión
    st.text_input(
        "ID de Sesión:",
        value=st.session_state["session_id"],
        key="session_id_input",
        help="Identificador único para mantener memoria conversacional"
    )
    
    # Botón de estado del sistema
    if st.button("🔍 Verificar Estado del Sistema"):
        health = make_api_request("/health")
        st.session_state["system_health"] = health
    
    # Mostrar estado del sistema
    if st.session_state["system_health"]:
        health = st.session_state["system_health"]
        if "error" not in health:
            st.success("✅ Sistema Operativo")
            st.json(health["systems"])
        else:
            st.error(f"❌ Error: {health['error']}")
    
    # Botón de limpiar sesión
    if st.button("🗑️ Limpiar Conversación"):
        st.session_state["messages"] = []
        st.rerun()
    
    # Información de capacidades
    st.markdown("### 🔧 Capacidades Disponibles")
    st.markdown("""
    - **🔍 Consulta RAG:** Base de conocimientos
    - **✍️ Escritura:** Reportes y documentos  
    - **🧠 Razonamiento:** Toma de decisiones
    - **📊 Análisis:** Datos e insights
    - **📋 Planificación:** Estrategias adaptativas
    - **👥 Multi-agente:** Orquestación de equipos
    """)


# ============================================================================
# ÁREA DE CONVERSACIÓN
# ============================================================================

# Header de conversación con estilo
st.markdown("""
<div style="background-color: #2d3748; 
            padding: 1rem; 
            border-radius: 10px; 
            margin-bottom: 1rem;
            border-left: 4px solid #4299e1;">
    <h2 style="color: white; margin: 0; font-size: 1.5rem;">
        💬 Conversación Inteligente
    </h2>
    <p style="color: #a0aec0; margin: 0.3rem 0 0 0; font-size: 0.9rem;">
        Interactúa con el agente usando lenguaje natural
    </p>
</div>
""", unsafe_allow_html=True)

# Mostrar historial de mensajes
for msg in st.session_state["messages"]:
    display_message(msg["role"], msg["content"], msg.get("timestamp"))

# ============================================================================
# INTERFAZ SEGÚN MODO SELECCIONADO
# ============================================================================

if agent_mode == "individual":
    st.subheader("🤖 Agente Individual con Memoria")
    
    # Input para consulta
    question = st.text_input(
        "💭 Pregunta para el agente:",
        placeholder="Ej: Analiza el inventario y genera un reporte ejecutivo...",
        key="individual_query"
    )
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        if st.button("🚀 Enviar a Agente Individual", key="send_individual"):
            if question:
                # Agregar mensaje del usuario
                timestamp = datetime.now().strftime("%H:%M:%S")
                st.session_state["messages"].append({
                    "role": "user", 
                    "content": question,
                    "timestamp": timestamp
                })
                
                # Mostrar spinner
                with st.spinner("🤖 El agente está procesando tu solicitud..."):
                    # Llamar a la API del agente individual
                    response = make_api_request("/agent/query", "POST", {
                        "query": question,
                        "session_id": st.session_state["session_id"]
                    })
                
                # Procesar respuesta
                if "error" not in response:
                    answer = response["response"]
                    tools_used = response.get("tools_used", [])
                    
                    # Agregar información de herramientas usadas
                    if tools_used:
                        answer += f"\n\n🔧 **Herramientas utilizadas:** {', '.join(tools_used)}"
                else:
                    answer = f"❌ Error: {response['error']}"
                
                # Agregar respuesta del agente
                st.session_state["messages"].append({
                    "role": "assistant",
                    "content": answer,
                    "timestamp": datetime.now().strftime("%H:%M:%S")
                })
                
                st.rerun()
    
    with col2:
        if st.button("📊 Info Sesión"):
            info = make_api_request(f"/agent/sessions/{st.session_state['session_id']}/info")
            if "error" not in info:
                st.json(info)
            else:
                st.error(info["error"])


elif agent_mode == "multi_agente":
    st.subheader("👥 Sistema Multi-Agente (CrewAI)")
    
    # Selector de tipo de flujo
    flow_type = st.selectbox(
        "Tipo de Flujo:",
        ["investigacion_completa", "planificacion_estrategica"],
        help="Investigación: Análisis profundo de un tema\nPlanificación: Desarrollo de estrategias"
    )
    
    # Input principal
    objective = st.text_area(
        "🎯 Objetivo del Flujo:",
        placeholder="Ej: Realizar análisis completo del inventario Q4 2024 y proponer optimizaciones...",
        height=100
    )
    
    # Campos adicionales para planificación estratégica
    if flow_type == "planificacion_estrategica":
        col1, col2 = st.columns(2)
        
        with col1:
            restrictions = st.text_area(
                "⚠️ Restricciones:",
                placeholder="Ej: Presupuesto limitado, plazo de 30 días...",
                height=60
            )
        
        with col2:
            resources = st.text_area(
                "🔧 Recursos Disponibles:",
                placeholder="Ej: Equipo de 5 personas, sistemas actuales...",
                height=60
            )
    
    if st.button("🚀 Ejecutar Flujo Multi-Agente", key="execute_crew"):
        if objective:
            # Preparar datos
            crew_data = {
                "objective": objective,
                "flow_type": flow_type,
                "session_id": f"crew_{st.session_state['session_id']}"
            }
            
            if flow_type == "planificacion_estrategica":
                crew_data["restrictions"] = [r.strip() for r in restrictions.split("\n") if r.strip()] if 'restrictions' in locals() else []
                crew_data["resources"] = [r.strip() for r in resources.split("\n") if r.strip()] if 'resources' in locals() else []
            
            # Agregar mensaje del usuario
            timestamp = datetime.now().strftime("%H:%M:%S")
            st.session_state["messages"].append({
                "role": "user",
                "content": f"**Flujo Multi-Agente:** {flow_type}\n**Objetivo:** {objective}",
                "timestamp": timestamp
            })
            
            # Mostrar progreso
            with st.spinner("👥 El equipo de agentes está trabajando... Esto puede tomar varios minutos."):
                response = make_api_request("/crew/execute", "POST", crew_data)
            
            # Procesar respuesta
            if "error" not in response:
                result = response["result"]
                agents_used = result.get("agentes_utilizados", [])
                
                answer = f"**Resultado del {flow_type}:**\n\n{result.get('resultado', 'Completado exitosamente')}"
                if agents_used:
                    answer += f"\n\n👥 **Agentes participantes:** {', '.join(agents_used)}"
            else:
                answer = f"❌ Error en flujo multi-agente: {response['error']}"
            
            # Agregar respuesta
            st.session_state["messages"].append({
                "role": "assistant",
                "content": answer,
                "timestamp": datetime.now().strftime("%H:%M:%S")
            })
            
            st.rerun()


elif agent_mode == "planificacion":
    st.subheader("📋 Planificación Adaptativa")
    
    # Input para crear plan
    col1, col2 = st.columns(2)
    
    with col1:
        plan_id = st.text_input(
            "🆔 ID del Plan:",
            placeholder="Ej: plan_inventario_2024",
            key="plan_id_input"
        )
    
    with col2:
        objective = st.text_input(
            "🎯 Objetivo del Plan:",
            placeholder="Ej: Optimizar gestión de inventario...",
            key="plan_objective_input"
        )
    
    # Contexto del plan
    st.markdown("**Contexto del Plan:**")
    
    col1, col2 = st.columns(2)
    
    with col1:
        recursos_text = st.text_area(
            "🔧 Recursos:",
            placeholder="Un recurso por línea...",
            height=80,
            key="plan_recursos"
        )
        
        feedback_text = st.text_area(
            "💬 Feedback:",
            placeholder="Comentarios y ajustes...", 
            height=80,
            key="plan_feedback"
        )
    
    with col2:
        tiempo_limite = st.number_input(
            "⏰ Tiempo límite (minutos):",
            min_value=0,
            value=0,
            key="plan_tiempo"
        )
        
        condiciones_text = st.text_area(
            "🌍 Condiciones Externas:",
            placeholder="Factores externos relevantes...",
            height=80,
            key="plan_condiciones"
        )
    
    # Botones de acción
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("📋 Crear Plan", key="create_plan"):
            if plan_id and objective:
                # Preparar contexto
                context = {}
                
                if recursos_text:
                    context["recursos"] = [r.strip() for r in recursos_text.split("\n") if r.strip()]
                
                if tiempo_limite > 0:
                    context["tiempo"] = {"deadline": tiempo_limite}
                
                if condiciones_text:
                    context["condiciones"] = {"descripcion": condiciones_text}
                
                if feedback_text:
                    context["feedback"] = [feedback_text]
                
                # Crear plan
                plan_data = {
                    "plan_id": plan_id,
                    "objective": objective,
                    "context": context,
                    "session_id": st.session_state["session_id"]
                }
                
                response = make_api_request("/planning/create", "POST", plan_data)
                
                if "error" not in response:
                    st.success(f"✅ Plan '{plan_id}' creado exitosamente")
                    st.json(response["plan_data"])
                else:
                    st.error(f"❌ Error: {response['error']}")
    
    with col2:
        if st.button("📋 Listar Planes", key="list_plans"):
            response = make_api_request("/planning/plans")
            
            if "error" not in response:
                plans = response["plans"]
                if plans:
                    st.success(f"📋 {len(plans)} planes activos encontrados")
                    for plan in plans:
                        st.json(plan)
                else:
                    st.info("No hay planes activos")
            else:
                st.error(f"❌ Error: {response['error']}")
    
    with col3:
        if st.button("🔄 Actualizar Contexto", key="update_context"):
            if plan_id:
                # Preparar contexto actualizado
                context = {}
                
                if recursos_text:
                    context["recursos"] = [r.strip() for r in recursos_text.split("\n") if r.strip()]
                
                if tiempo_limite > 0:
                    context["tiempo"] = {"deadline": tiempo_limite}
                
                if condiciones_text:
                    context["condiciones"] = {"descripcion": condiciones_text}
                
                if feedback_text:
                    context["feedback"] = [feedback_text]
                
                response = make_api_request(f"/planning/plans/{plan_id}/context", "PUT", context)
                
                if "error" not in response:
                    adaptaciones = response["adaptaciones"]
                    st.success(f"✅ Contexto actualizado - {len(adaptaciones)} adaptaciones realizadas")
                    
                    if adaptaciones:
                        for adaptacion in adaptaciones:
                            st.info(f"🔄 {adaptacion['tipo']}: {len(adaptacion['adaptaciones'])} cambios")
                else:
                    st.error(f"❌ Error: {response['error']}")


# ============================================================================
# FOOTER CON INFORMACIÓN DEL SISTEMA
# ============================================================================

st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666;">
    <strong>CleanPro Intelligent Agents v2.0</strong><br>
    Sistema de Automatización Organizacional con IA Avanzada<br>
    <em>Implementa IL2.1, IL2.2, IL2.3 e IL2.4 según RA2</em>
</div>
""", unsafe_allow_html=True)
