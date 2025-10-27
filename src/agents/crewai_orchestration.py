"""
Sistema Multi-Agente CleanPro usando CrewAI
==========================================
Implementa orquestación de múltiples agentes especializados
para flujos de trabajo organizacionales complejos.
"""

import os
from typing import Any, Dict, List, Optional
from crewai import Agent, Task, Crew, Process
from crewai_tools import BaseTool
from langchain_openai import ChatOpenAI

# Importar herramientas personalizadas (adaptadas para CrewAI)
from src.agents.tools.rag_tools import RAGConsultaTool
from src.agents.tools.escritura_tools import EscrituraReporteTool, AnalisisDatosTool
from src.agents.tools.razonamiento_tools import RazonamientoDecisionTool, PlanificacionEstrategicaTool


class CrewCleanPro:
    """
    Sistema de orquestación multi-agente especializado para CleanPro.
    Coordina agentes especializados en investigación, análisis, planificación y documentación.
    """
    
    def __init__(self, session_id: str = "crew_default"):
        self.session_id = session_id
        
        # Configurar variables de entorno para CrewAI (CRÍTICO según RA2)
        self._setup_crewai_environment()
        
        # Configurar LLM
        self.llm = ChatOpenAI(
            model="gpt-4o",
            temperature=0.2
        )
        
        # Configurar herramientas
        self.tools = self._setup_tools()
        
        # Crear agentes especializados
        self.agents = self._create_agents()
        
        # Crew configurado dinámicamente según la tarea
        self.current_crew = None
    
    def _setup_crewai_environment(self):
        """Configura variables de entorno específicas para CrewAI."""
        # CONFIGURACIÓN CRÍTICA según IL2.1 - CrewAI requiere mapeo específico
        os.environ["OPENAI_API_BASE"] = os.environ.get("OPENAI_BASE_URL", "")
        os.environ["OPENAI_API_KEY"] = os.environ.get("GITHUB_TOKEN", "")
    
    def _setup_tools(self) -> List[BaseTool]:
        """Configura herramientas adaptadas para CrewAI."""
        return [
            RAGConsultaTool(),
            EscrituraReporteTool(),
            AnalisisDatosTool(),
            RazonamientoDecisionTool(),
            PlanificacionEstrategicaTool()
        ]
    
    def _create_agents(self) -> Dict[str, Agent]:
        """Crea agentes especializados."""
        
        # Agente Investigador - Especialista en consulta y recopilación de información
        investigador = Agent(
            role="Investigador de Datos CleanPro",
            goal="Investigar y recopilar información relevante de la base de conocimientos organizacional",
            backstory="""Eres un especialista en investigación de datos corporativos de CleanPro.
            Tu expertise incluye análisis de inventarios, turnos, políticas empresariales y 
            procedimientos operativos. Utilizas herramientas RAG para acceder a información
            precisa y contextualizada.""",
            tools=[tool for tool in self.tools if tool.name in ["rag_consulta", "analisis_datos"]],
            verbose=True,
            allow_delegation=False,
            llm=self.llm
        )
        
        # Agente Analista - Especialista en razonamiento y toma de decisiones
        analista = Agent(
            role="Analista Estratégico CleanPro", 
            goal="Realizar análisis profundos, evaluaciones de decisiones y razonamiento estratégico",
            backstory="""Eres un analista estratégico senior de CleanPro con amplia experiencia
            en toma de decisiones organizacionales. Tu fortaleza está en el análisis multi-criterio,
            evaluación de opciones complejas y desarrollo de estrategias fundamentadas en datos.""",
            tools=[tool for tool in self.tools if tool.name in ["razonamiento_decision", "planificacion_estrategica"]],
            verbose=True,
            allow_delegation=False,
            llm=self.llm
        )
        
        # Agente Documentador - Especialista en escritura y reportes
        documentador = Agent(
            role="Especialista en Documentación CleanPro",
            goal="Crear documentación técnica, reportes ejecutivos y comunicaciones organizacionales",
            backstory="""Eres el especialista en comunicación técnica de CleanPro. Tu experticia
            incluye la creación de reportes estructurados, documentación de procesos, y síntesis
            de información compleja en formatos accesibles para diferentes audiencias.""",
            tools=[tool for tool in self.tools if tool.name in ["escritura_reporte"]],
            verbose=True,
            allow_delegation=False,
            llm=self.llm
        )
        
        # Agente Coordinador - Orquesta el trabajo de otros agentes  
        coordinador = Agent(
            role="Coordinador de Proyectos CleanPro",
            goal="Coordinar flujos de trabajo complejos y asegurar integración entre diferentes especialistas",
            backstory="""Eres el coordinador de proyectos senior de CleanPro. Tu rol es orquestar
            el trabajo de diferentes especialistas, asegurar la coherencia en deliverables complejos,
            y mantener la visión estratégica en proyectos multi-facéticos.""",
            tools=self.tools,  # Acceso a todas las herramientas para coordinación
            verbose=True,
            allow_delegation=True,
            llm=self.llm
        )
        
        return {
            "investigador": investigador,
            "analista": analista, 
            "documentador": documentador,
            "coordinador": coordinador
        }
    
    def investigacion_completa(self, tema: str, profundidad: str = "media") -> Dict[str, Any]:
        """
        Ejecuta un flujo de investigación completa sobre un tema.
        """
        
        # Definir tareas del flujo de investigación
        tarea_investigacion = Task(
            description=f"""
            Realiza una investigación exhaustiva sobre: {tema}
            
            OBJETIVOS:
            1. Consultar la base de conocimientos RAG para información relevante
            2. Analizar datos disponibles relacionados con el tema
            3. Identificar patrones, tendencias y hallazgos clave
            
            NIVEL DE PROFUNDIDAD: {profundidad}
            
            ENTREGABLE: Reporte detallado con hallazgos, datos de soporte y fuentes utilizadas.
            """,
            agent=self.agents["investigador"],
            expected_output="Reporte de investigación estructurado con hallazgos clave y datos de soporte"
        )
        
        tarea_analisis = Task(
            description=f"""
            Analiza los hallazgos de la investigación sobre: {tema}
            
            OBJETIVOS:
            1. Evaluar la calidad y relevancia de los datos encontrados
            2. Identificar implicaciones estratégicas y operativas
            3. Generar recomendaciones basadas en el análisis
            
            UTILIZA los resultados de la investigación previa como base para tu análisis.
            
            ENTREGABLE: Análisis estratégico con recomendaciones fundamentadas.
            """,
            agent=self.agents["analista"],
            context=[tarea_investigacion],
            expected_output="Análisis estratégico con evaluación de hallazgos y recomendaciones"
        )
        
        tarea_documentacion = Task(
            description=f"""
            Crea documentación ejecutiva sobre: {tema}
            
            OBJETIVOS:
            1. Sintetizar hallazgos de investigación y análisis
            2. Crear reporte ejecutivo estructurado y profesional
            3. Incluir recomendaciones accionables para la organización
            
            COMBINA los resultados de investigación y análisis en un documento cohesivo.
            
            ENTREGABLE: Reporte ejecutivo final listo para presentación a stakeholders.
            """,
            agent=self.agents["documentador"],
            context=[tarea_investigacion, tarea_analisis],
            expected_output="Reporte ejecutivo profesional con síntesis completa y recomendaciones"
        )
        
        # Crear y ejecutar crew
        crew_investigacion = Crew(
            agents=[self.agents["investigador"], self.agents["analista"], self.agents["documentador"]],
            tasks=[tarea_investigacion, tarea_analisis, tarea_documentacion],
            process=Process.sequential,
            verbose=True
        )
        
        self.current_crew = crew_investigacion
        
        # Ejecutar flujo
        result = crew_investigacion.kickoff()
        
        return {
            "session_id": self.session_id,
            "flujo": "investigacion_completa",
            "tema": tema,
            "resultado": result,
            "agentes_utilizados": ["investigador", "analista", "documentador"],
            "proceso": "secuencial"
        }
    
    def planificacion_estrategica(self, objetivo: str, restricciones: List[str] = None, recursos: List[str] = None) -> Dict[str, Any]:
        """
        Ejecuta un flujo de planificación estratégica coordinada.
        """
        
        if restricciones is None:
            restricciones = []
        if recursos is None:
            recursos = []
        
        # Tarea de análisis de contexto
        tarea_contexto = Task(
            description=f"""
            Analiza el contexto organizacional para el objetivo: {objetivo}
            
            OBJETIVOS:
            1. Investigar información relevante en la base de conocimientos
            2. Evaluar restricciones: {restricciones}
            3. Analizar recursos disponibles: {recursos}
            4. Identificar factores críticos de éxito
            
            ENTREGABLE: Análisis de contexto con factores críticos identificados.
            """,
            agent=self.agents["investigador"],
            expected_output="Análisis contextual con factores críticos y evaluación de situación actual"
        )
        
        # Tarea de desarrollo del plan estratégico
        tarea_planificacion = Task(
            description=f"""
            Desarrolla un plan estratégico detallado para: {objetivo}
            
            OBJETIVOS:
            1. Crear planificación estratégica basada en el análisis de contexto
            2. Descomponer el objetivo en tareas ejecutables
            3. Considerar restricciones y optimizar uso de recursos
            4. Establecer cronograma y hitos críticos
            
            USA el análisis de contexto como base para la planificación.
            
            ENTREGABLE: Plan estratégico detallado con cronograma y asignación de recursos.
            """,
            agent=self.agents["analista"],
            context=[tarea_contexto],
            expected_output="Plan estratégico estructurado con tareas, cronograma y gestión de riesgos"
        )
        
        # Tarea de coordinación e integración
        tarea_coordinacion = Task(
            description=f"""
            Coordina la implementación del plan estratégico para: {objetivo}
            
            OBJETIVOS:
            1. Revisar e integrar análisis de contexto y planificación
            2. Identificar dependencias críticas entre tareas
            3. Desarrollar estrategia de gestión de cambios
            4. Crear dashboard de seguimiento y KPIs
            
            INTEGRA todos los elementos previos en una estrategia de implementación cohesiva.
            
            ENTREGABLE: Estrategia de implementación integral con governance y seguimiento.
            """,
            agent=self.agents["coordinador"],
            context=[tarea_contexto, tarea_planificacion],
            expected_output="Estrategia de implementación completa con governance y sistema de seguimiento"
        )
        
        # Tarea de documentación final
        tarea_documentacion = Task(
            description=f"""
            Documenta el plan estratégico completo para: {objetivo}
            
            OBJETIVOS:
            1. Crear documentación ejecutiva del plan estratégico
            2. Incluir análisis, planificación y estrategia de implementación
            3. Desarrollar materiales de comunicación para stakeholders
            4. Generar templates y herramientas de seguimiento
            
            COMPILA todos los elementos en documentación profesional y ejecutiva.
            
            ENTREGABLE: Pack completo de documentación estratégica lista para implementación.
            """,
            agent=self.agents["documentador"],
            context=[tarea_contexto, tarea_planificacion, tarea_coordinacion],
            expected_output="Documentación estratégica completa con plan de implementación y materiales de comunicación"
        )
        
        # Crear y ejecutar crew
        crew_planificacion = Crew(
            agents=[self.agents["investigador"], self.agents["analista"], self.agents["coordinador"], self.agents["documentador"]],
            tasks=[tarea_contexto, tarea_planificacion, tarea_coordinacion, tarea_documentacion],
            process=Process.sequential,
            verbose=True
        )
        
        self.current_crew = crew_planificacion
        
        # Ejecutar flujo
        result = crew_planificacion.kickoff()
        
        return {
            "session_id": self.session_id,
            "flujo": "planificacion_estrategica",
            "objetivo": objetivo,
            "restricciones": restricciones,
            "recursos": recursos,
            "resultado": result,
            "agentes_utilizados": ["investigador", "analista", "coordinador", "documentador"],
            "proceso": "secuencial"
        }
    
    def flujo_personalizado(self, agentes_roles: List[str], tareas_descripciones: List[str], proceso: str = "sequential") -> Dict[str, Any]:
        """
        Ejecuta un flujo personalizado con agentes y tareas específicas.
        """
        
        # Validar agentes disponibles
        agentes_disponibles = [self.agents[role] for role in agentes_roles if role in self.agents]
        
        if len(agentes_disponibles) != len(agentes_roles):
            return {
                "error": f"Algunos roles no están disponibles. Roles disponibles: {list(self.agents.keys())}"
            }
        
        # Crear tareas dinámicamente
        tareas = []
        for i, descripcion in enumerate(tareas_descripciones):
            agent_idx = i % len(agentes_disponibles)  # Rotar agentes si hay más tareas que agentes
            
            tarea = Task(
                description=descripcion,
                agent=agentes_disponibles[agent_idx],
                expected_output=f"Resultado de tarea {i+1}: {descripcion[:50]}..."
            )
            tareas.append(tarea)
        
        # Configurar proceso
        proceso_mapping = {
            "sequential": Process.sequential,
            "hierarchical": Process.hierarchical
        }
        
        proceso_crew = proceso_mapping.get(proceso, Process.sequential)
        
        # Crear y ejecutar crew
        crew_personalizado = Crew(
            agents=agentes_disponibles,
            tasks=tareas,
            process=proceso_crew,
            verbose=True
        )
        
        self.current_crew = crew_personalizado
        
        # Ejecutar flujo
        result = crew_personalizado.kickoff()
        
        return {
            "session_id": self.session_id,
            "flujo": "personalizado",
            "agentes_utilizados": agentes_roles,
            "numero_tareas": len(tareas_descripciones),
            "proceso": proceso,
            "resultado": result
        }
    
    def get_crew_info(self) -> Dict[str, Any]:
        """Obtiene información sobre el crew actual y agentes disponibles."""
        return {
            "session_id": self.session_id,
            "agentes_disponibles": list(self.agents.keys()),
            "herramientas_disponibles": [tool.name for tool in self.tools],
            "current_crew_active": self.current_crew is not None,
            "flujos_disponibles": ["investigacion_completa", "planificacion_estrategica", "flujo_personalizado"]
        }


def create_cleanpro_crew(session_id: str = "crew_default") -> CrewCleanPro:
    """Factory function para crear un sistema multi-agente CleanPro."""
    return CrewCleanPro(session_id=session_id)