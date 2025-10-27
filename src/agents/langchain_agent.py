"""
Agente Principal CleanPro usando LangChain
=========================================
Implementa un agente individual potente con herramientas integradas,
memoria conversacional y capacidades de razonamiento avanzado.
"""

import os
from typing import Any, Dict, List, Optional
from langchain.agents import AgentExecutor, create_openai_functions_agent
from langchain.agents.openai_functions_agent.agent_token_buffer_memory import AgentTokenBufferMemory
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.tools import BaseTool

# Importar herramientas personalizadas
from src.agents.tools.rag_tools import get_rag_consulta_tool
from src.agents.tools.escritura_tools import get_escritura_tools
from src.agents.tools.razonamiento_tools import get_razonamiento_tools
from src.agents.memory.advanced_memory import memory_manager


class AgenteCleanPro:
    """
    Agente principal de CleanPro con capacidades de:
    - Consulta RAG sobre conocimientos organizacionales
    - Escritura y análisis de reportes
    - Razonamiento y toma de decisiones
    - Memoria conversacional avanzada
    """
    
    def __init__(self, session_id: str = "default"):
        self.session_id = session_id
        self.memory_session = memory_manager.get_session(session_id)
        
        # Configurar LLM
        self.llm = ChatOpenAI(
            model="gpt-4o",
            temperature=0.2,
            openai_api_base=os.getenv("OPENAI_BASE_URL"),
            openai_api_key=os.getenv("OPENAI_API_KEY")
        )
        
        # Configurar herramientas
        self.tools = self._setup_tools()
        
        # Configurar memoria para el agente
        self.agent_memory = AgentTokenBufferMemory(
            llm=self.llm,
            max_token_limit=4000,
            memory_key="chat_history",
            return_messages=True
        )
        
        # Configurar prompt del sistema
        self.system_prompt = self._create_system_prompt()
        
        # Crear agente
        self.agent = create_openai_functions_agent(
            llm=self.llm,
            tools=self.tools,
            prompt=self.system_prompt
        )
        
        # Crear executor
        self.agent_executor = AgentExecutor(
            agent=self.agent,
            tools=self.tools,
            memory=self.agent_memory,
            verbose=True,
            max_iterations=10,
            max_execution_time=120,
            return_intermediate_steps=True
        )
    
    def _setup_tools(self) -> List[BaseTool]:
        """Configura todas las herramientas del agente."""
        tools = []
        
        # Herramienta de consulta RAG
        tools.append(get_rag_consulta_tool())
        
        # Herramientas de escritura y análisis
        tools.extend(get_escritura_tools())
        
        # Herramientas de razonamiento
        tools.extend(get_razonamiento_tools())
        
        return tools
    
    def _create_system_prompt(self) -> ChatPromptTemplate:
        """Crea el prompt del sistema para el agente."""
        
        system_message = f"""
Eres el Asistente Inteligente de CleanPro, una empresa de servicios industriales de limpieza.

IDENTIDAD Y MISIÓN:
- Nombre: Agente CleanPro
- Sesión: {self.session_id}
- Especialización: Automatización de flujos de trabajo organizacionales
- Objetivo: Asistir en la gestión, análisis y planificación estratégica

CAPACIDADES PRINCIPALES:
1. 🔍 CONSULTA: Acceso a base de conocimientos sobre inventario, turnos, políticas
2. ✍️ ESCRITURA: Generación de reportes, análisis y documentación técnica  
3. 🧠 RAZONAMIENTO: Toma de decisiones, planificación estratégica, adaptación contextual

HERRAMIENTAS DISPONIBLES:
- rag_consulta: Para consultar información de la base de datos corporativa
- escritura_reporte: Para generar reportes estructurados y documentos
- analisis_datos: Para analizar datasets de inventario y turnos
- razonamiento_decision: Para análisis de decisiones con múltiples criterios
- planificacion_estrategica: Para crear planes y descomponer objetivos complejos
- adaptacion_contextual: Para ajustar comportamiento según condiciones cambiantes

INSTRUCCIONES DE COMPORTAMIENTO:
1. Siempre considera el contexto organizacional de CleanPro
2. Usa múltiples herramientas cuando sea necesario para respuestas completas
3. Mantén coherencia conversacional usando la memoria de sesión
4. Proporciona análisis fundamentados y recomendaciones prácticas
5. Adapta tu respuesta según la complejidad de la tarea
6. Documenta tus procesos de razonamiento paso a paso

FLUJO DE TRABAJO TÍPICO:
1. Analizar la consulta del usuario
2. Determinar qué herramientas son necesarias
3. Ejecutar consultas/análisis en orden lógico
4. Sintetizar información de múltiples fuentes
5. Proporcionar respuesta integral con recomendaciones
6. Actualizar memoria de sesión con la interacción

Responde siempre en español, de manera profesional pero accesible.
"""
        
        prompt = ChatPromptTemplate.from_messages([
            ("system", system_message),
            MessagesPlaceholder(variable_name="chat_history"),
            ("human", "{input}"),
            MessagesPlaceholder(variable_name="agent_scratchpad")
        ])
        
        return prompt
    
    def process_query(self, query: str) -> Dict[str, Any]:
        """Procesa una consulta del usuario."""
        try:
            # Obtener contexto de memoria previo
            memory_context = self.memory_session.get_memory_context()
            
            # Ejecutar agente
            result = self.agent_executor.invoke({
                "input": query,
                "chat_history": memory_context.get("chat_history", [])
            })
            
            # Extraer respuesta y pasos intermedios
            response = result["output"]
            intermediate_steps = result.get("intermediate_steps", [])
            
            # Actualizar memoria de sesión
            self.memory_session.add_interaction(query, response)
            
            return {
                "response": response,
                "intermediate_steps": intermediate_steps,
                "session_id": self.session_id,
                "tools_used": [step[0].tool for step in intermediate_steps if len(step) > 0],
                "memory_summary": self.memory_session.get_memory_summary()
            }
            
        except Exception as e:
            error_msg = f"Error procesando consulta: {str(e)}"
            # Aún así actualizar memoria con el error
            self.memory_session.add_interaction(query, error_msg)
            
            return {
                "response": error_msg,
                "intermediate_steps": [],
                "session_id": self.session_id,
                "error": str(e)
            }
    
    def get_session_info(self) -> Dict[str, Any]:
        """Obtiene información de la sesión actual."""
        return {
            "session_id": self.session_id,
            "memory_summary": self.memory_session.get_memory_summary(),
            "available_tools": [tool.name for tool in self.tools],
            "llm_model": self.llm.model_name,
            "conversation_export": self.memory_session.export_conversation()
        }
    
    def reset_session(self):
        """Reinicia la sesión de memoria."""
        self.memory_session.clear_memory()
        self.agent_memory.clear()


def create_cleanpro_agent(session_id: str = "default") -> AgenteCleanPro:
    """Factory function para crear un agente CleanPro."""
    return AgenteCleanPro(session_id=session_id)