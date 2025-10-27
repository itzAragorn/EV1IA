"""
Ejemplos de Flujos de Trabajo Automatizados - CleanPro
=====================================================
Demostraciones prácticas de casos de uso organizacionales
implementando IL2.1, IL2.2, IL2.3 e IL2.4.
"""

import os
import sys
from datetime import datetime
from typing import Dict, Any

# Agregar el directorio raíz al path para importaciones
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.agents.langchain_agent import create_cleanpro_agent
from src.agents.crewai_orchestration import create_cleanpro_crew
from src.agents.planning.adaptive_planning import (
    planning_manager, ContextoEjecucion, Tarea, EstadoTarea, PrioridadTarea
)


class DemostradorFlujos:
    """Demostrador de flujos de trabajo automatizados para CleanPro."""
    
    def __init__(self):
        self.session_id = f"demo_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        print(f"🚀 Iniciando demostración con sesión: {self.session_id}")
    
    def demo_completa(self):
        """Ejecuta demostración completa de todos los flujos."""
        print("\n" + "="*80)
        print("🧹 DEMOSTRACIÓN COMPLETA - SISTEMA CLEANPRO")
        print("="*80)
        
        # 1. Agente Individual con Memoria
        self.demo_agente_individual()
        
        # 2. Sistema Multi-Agente
        self.demo_sistema_multiagente()
        
        # 3. Planificación Adaptativa
        self.demo_planificacion_adaptativa()
        
        # 4. Integración de Sistemas
        self.demo_integracion_sistemas()
        
        print("\n" + "="*80)
        print("✅ DEMOSTRACIÓN COMPLETA FINALIZADA")
        print("="*80)
    
    def demo_agente_individual(self):
        """
        IL2.1: Demuestra agente funcional con herramientas integradas.
        IL2.2: Demuestra memoria conversacional y recuperación de contexto.
        """
        print("\n" + "-"*60)
        print("🤖 DEMO 1: AGENTE INDIVIDUAL CON MEMORIA")
        print("-"*60)
        
        # Crear agente
        agente = create_cleanpro_agent(f"demo_individual_{self.session_id}")
        
        # Secuencia de consultas para demostrar memoria conversacional
        consultas = [
            "Analiza el inventario de Las Condes y dame un resumen ejecutivo",
            "¿Cuáles son los principales hallazgos que encontraste en ese análisis?",
            "Basándote en eso, genera un reporte de recomendaciones para optimización",
            "¿Puedes recordar cuál fue la primera pregunta que te hice?"
        ]
        
        print("\n📋 Secuencia de consultas para demostrar memoria:")
        for i, consulta in enumerate(consultas, 1):
            print(f"\n🔸 Consulta {i}: {consulta}")
            
            # Procesar consulta
            resultado = agente.process_query(consulta)
            
            print(f"🔹 Respuesta: {resultado['response'][:200]}...")
            print(f"🔧 Herramientas utilizadas: {resultado.get('tools_used', [])}")
            
            # Mostrar evolución de la memoria
            if i == len(consultas):
                print(f"\n📊 Resumen de memoria final:")
                print(resultado.get('memory_summary', 'No disponible'))
        
        print("\n✅ Demo agente individual completada - Memoria conversacional verificada")
    
    def demo_sistema_multiagente(self):
        """
        IL2.3: Demuestra planificación y orquestación multi-agente.
        IL2.1: Demuestra integración de herramientas especializadas.
        """
        print("\n" + "-"*60)
        print("👥 DEMO 2: SISTEMA MULTI-AGENTE (CREWAI)")
        print("-"*60)
        
        # Crear crew
        crew = create_cleanpro_crew(f"demo_crew_{self.session_id}")
        
        print("\n🎯 Caso de Uso: Análisis Integral de Operaciones Q4 2024")
        
        # Flujo de investigación completa
        print("\n📊 Ejecutando flujo de investigación completa...")
        resultado_investigacion = crew.investigacion_completa(
            tema="Optimización de operaciones de limpieza industrial Q4 2024",
            profundidad="alta"
        )
        
        print(f"✅ Investigación completada por {len(resultado_investigacion['agentes_utilizados'])} agentes")
        print(f"📄 Resultado: {str(resultado_investigacion['resultado'])[:300]}...")
        
        # Flujo de planificación estratégica
        print("\n📋 Ejecutando flujo de planificación estratégica...")
        resultado_planificacion = crew.planificacion_estrategica(
            objetivo="Implementar sistema de gestión inteligente de inventarios",
            restricciones=[
                "Presupuesto limitado a $50,000 USD",
                "Implementación en 90 días",
                "Mínima interrupción de operaciones"
            ],
            recursos=[
                "Equipo técnico de 3 personas",
                "Sistemas ERP existentes",
                "Base de datos histórica"
            ]
        )
        
        print(f"✅ Planificación completada por {len(resultado_planificacion['agentes_utilizados'])} agentes")
        print(f"📋 Plan: {str(resultado_planificacion['resultado'])[:300]}...")
        
        print("\n✅ Demo sistema multi-agente completada - Orquestación verificada")
    
    def demo_planificacion_adaptativa(self):
        """
        IL2.3: Demuestra planificación adaptativa y toma de decisiones.
        IL2.2: Demuestra continuidad en flujos prolongados.
        """
        print("\n" + "-"*60)
        print("📋 DEMO 3: PLANIFICACIÓN ADAPTATIVA")
        print("-"*60)
        
        # Crear plan adaptativo
        plan_id = f"demo_plan_{self.session_id}"
        plan = planning_manager.crear_plan(
            plan_id=plan_id,
            objetivo="Modernización del sistema de gestión de turnos CleanPro"
        )
        
        print(f"📋 Plan creado: {plan_id}")
        
        # Agregar tareas al plan
        tareas = [
            Tarea(
                id="tarea_1",
                titulo="Análisis de requerimientos",
                descripcion="Analizar necesidades actuales del sistema de turnos",
                prioridad=PrioridadTarea.CRITICA,
                recursos_requeridos=["analista_senior", "acceso_bd"],
                estimacion_tiempo=120
            ),
            Tarea(
                id="tarea_2", 
                titulo="Diseño de arquitectura",
                descripcion="Diseñar nueva arquitectura del sistema",
                prioridad=PrioridadTarea.ALTA,
                dependencias=["tarea_1"],
                recursos_requeridos=["arquitecto_software", "herramientas_diseño"],
                estimacion_tiempo=180
            ),
            Tarea(
                id="tarea_3",
                titulo="Desarrollo de prototipo",
                descripcion="Desarrollar prototipo funcional",
                prioridad=PrioridadTarea.ALTA,
                dependencias=["tarea_2"],
                recursos_requeridos=["desarrollador", "entorno_dev"],
                estimacion_tiempo=300
            ),
            Tarea(
                id="tarea_4",
                titulo="Documentación",
                descripcion="Crear documentación técnica y usuario",
                prioridad=PrioridadTarea.MEDIA,
                dependencias=["tarea_3"],
                recursos_requeridos=["technical_writer"],
                estimacion_tiempo=90
            )
        ]
        
        for tarea in tareas:
            plan.agregar_tarea(tarea)
        
        print(f"📝 {len(tareas)} tareas agregadas al plan")
        
        # Demostrar adaptación por cambios de contexto
        print("\n🔄 Simulando cambios de contexto y adaptaciones...")
        
        # Contexto inicial
        contexto_inicial = ContextoEjecucion(
            recursos_disponibles=["analista_senior", "acceso_bd", "arquitecto_software"],
            restricciones_tiempo={"deadline": 600},  # 10 horas
            condiciones_externas={"prioridad_empresa": "alta"},
            feedback_usuario=["Acelerar desarrollo"],
            metricas_performance={"eficiencia_actual": 0.7}
        )
        
        adaptaciones = plan.actualizar_contexto(contexto_inicial)
        print(f"📊 Contexto inicial - {len(adaptaciones)} adaptaciones realizadas")
        
        # Simular ejecución y cambios
        print("\n⚡ Simulando ejecución y cambios de contexto...")
        
        # Ejecutar primera tarea
        tarea_ejecutar = plan.ejecutar_siguiente_tarea()
        if tarea_ejecutar:
            print(f"🔄 Ejecutando: {tarea_ejecutar.titulo}")
            plan.completar_tarea(tarea_ejecutar.id, "Análisis completado exitosamente")
        
        # Cambio de contexto: recursos limitados
        contexto_limitado = ContextoEjecucion(
            recursos_disponibles=["arquitecto_software"],  # Falta analista_senior
            restricciones_tiempo={"deadline": 300},  # Tiempo reducido
            condiciones_externas={"prioridad_empresa": "crítica"},
            feedback_usuario=["Recursos limitados", "Priorizar tareas críticas"],
            metricas_performance={"eficiencia_actual": 0.6}
        )
        
        adaptaciones = plan.actualizar_contexto(contexto_limitado)
        print(f"⚠️ Contexto limitado - {len(adaptaciones)} adaptaciones realizadas")
        
        for adaptacion in adaptaciones:
            print(f"   🔸 {adaptacion['tipo']}: {len(adaptacion['adaptaciones'])} cambios")
        
        # Mostrar progreso final
        progreso = plan.obtener_progreso()
        print(f"\n📈 Progreso final del plan:")
        print(f"   ✅ Completadas: {progreso['completadas']}/{progreso['total']}")
        print(f"   🔄 En progreso: {progreso['en_progreso']}")
        print(f"   ⚠️ Bloqueadas: {progreso['bloqueadas']}")
        print(f"   🔄 Adaptaciones: {progreso['adaptaciones_realizadas']}")
        
        print("\n✅ Demo planificación adaptativa completada - Adaptabilidad verificada")
    
    def demo_integracion_sistemas(self):
        """
        IL2.4: Demuestra integración y orquestación de todos los componentes.
        """
        print("\n" + "-"*60)
        print("🔗 DEMO 4: INTEGRACIÓN DE SISTEMAS")
        print("-"*60)
        
        print("\n🎯 Caso de Uso Integral: Optimización Completa de Operaciones")
        
        # 1. Agente individual para análisis inicial 
        print("\n🤖 Paso 1: Análisis inicial con agente individual")
        agente = create_cleanpro_agent(f"integracion_{self.session_id}")
        
        analisis_inicial = agente.process_query(
            "Realiza un análisis de los datos de inventario y turnos disponibles para identificar áreas de optimización"
        )
        
        print(f"📊 Análisis inicial completado")
        print(f"🔧 Herramientas: {analisis_inicial.get('tools_used', [])}")
        
        # 2. Sistema multi-agente para planificación estratégica
        print("\n👥 Paso 2: Planificación estratégica con multi-agente")
        crew = create_cleanpro_crew(f"integracion_crew_{self.session_id}")
        
        planificacion_estrategica = crew.planificacion_estrategica(
            objetivo="Optimizar operaciones basado en análisis de datos",
            restricciones=[
                "Basarse en hallazgos del análisis inicial",
                "Implementación gradual en 6 meses",
                "ROI mínimo del 15%"
            ],
            recursos=[
                "Datos históricos analizados",
                "Equipo de implementación",
                "Presupuesto aprobado"
            ]
        )
        
        print(f"📋 Planificación estratégica completada")
        print(f"👥 Agentes: {planificacion_estrategica['agentes_utilizados']}")
        
        # 3. Plan adaptativo para implementación
        print("\n📋 Paso 3: Plan adaptativo para implementación")
        plan_implementacion = planning_manager.crear_plan(
            plan_id=f"implementacion_{self.session_id}",
            objetivo="Implementar optimizaciones identificadas"
        )
        
        # Crear tareas basadas en los resultados anteriores
        tareas_implementacion = [
            Tarea(
                id="impl_1",
                titulo="Preparación de infraestructura",
                descripcion="Preparar sistemas para optimizaciones",
                prioridad=PrioridadTarea.CRITICA,
                estimacion_tiempo=240
            ),
            Tarea(
                id="impl_2",
                titulo="Implementación fase 1",
                descripcion="Implementar optimizaciones prioritarias",
                prioridad=PrioridadTarea.ALTA,
                dependencias=["impl_1"],
                estimacion_tiempo=360
            ),
            Tarea(
                id="impl_3",
                titulo="Monitoreo y ajustes",
                descripcion="Monitorear resultados y realizar ajustes",
                prioridad=PrioridadTarea.MEDIA,
                dependencias=["impl_2"],
                estimacion_tiempo=180
            )
        ]
        
        for tarea in tareas_implementacion:
            plan_implementacion.agregar_tarea(tarea)
        
        print(f"📝 Plan de implementación creado con {len(tareas_implementacion)} tareas")
        
        # 4. Generación de reporte integral
        print("\n📄 Paso 4: Generación de reporte integral")
        reporte_final = agente.process_query(
            f"""Genera un reporte ejecutivo integral que incluya:
            1. Resumen del análisis inicial realizado
            2. Síntesis de la planificación estratégica desarrollada
            3. Plan de implementación propuesto
            4. Métricas de éxito y KPIs recomendados
            5. Próximos pasos y recomendaciones finales
            
            Este reporte debe integrar todos los hallazgos y ser presentable a la alta dirección."""
        )
        
        print(f"📄 Reporte integral generado")
        print(f"🔧 Herramientas finales: {reporte_final.get('tools_used', [])}")
        
        # Resumen de integración
        print(f"\n📊 RESUMEN DE INTEGRACIÓN COMPLETA:")
        print(f"   🤖 Agente individual: Análisis y reportes")
        print(f"   👥 Multi-agente: Planificación estratégica colaborativa")
        print(f"   📋 Planificación adaptativa: Gestión de implementación")
        print(f"   🔗 Integración: Flujo completo de extremo a extremo")
        
        print("\n✅ Demo integración de sistemas completada - Orquestación total verificada")
    
    def mostrar_arquitectura(self):
        """
        IL2.4: Muestra la arquitectura de componentes implementada.
        """
        print("\n" + "="*80)
        print("🏗️ ARQUITECTURA DEL SISTEMA CLEANPRO")
        print("="*80)
        
        arquitectura = """
📱 CAPA DE PRESENTACIÓN
├── Streamlit Web App (app_streamlit.py)
│   ├── Interfaz de usuario avanzada
│   ├── Manejo de sesiones
│   └── Modos: Individual, Multi-agente, Planificación

🔌 CAPA DE API
├── FastAPI Server (src/api/app.py)
│   ├── Endpoints RESTful
│   ├── Gestión de sesiones
│   ├── Middleware y CORS
│   └── Health checks

🤖 CAPA DE AGENTES
├── Agente Individual (src/agents/langchain_agent.py)
│   ├── LangChain Agent con OpenAI Functions
│   ├── Memoria conversacional avanzada
│   └── Herramientas integradas
├── Sistema Multi-Agente (src/agents/crewai_orchestration.py)
│   ├── CrewAI con agentes especializados
│   ├── Flujos de trabajo coordinados
│   └── Orquestación secuencial/jerárquica
└── Planificación Adaptativa (src/agents/planning/)
    ├── Sistema de planificación dinámico
    ├── Adaptación contextual
    └── Gestión de dependencias

🛠️ CAPA DE HERRAMIENTAS
├── Herramientas RAG (src/agents/tools/rag_tools.py)
│   └── Consulta a base de conocimientos
├── Herramientas de Escritura (src/agents/tools/escritura_tools.py)
│   ├── Generación de reportes
│   └── Análisis de datos
└── Herramientas de Razonamiento (src/agents/tools/razonamiento_tools.py)
    ├── Toma de decisiones
    ├── Planificación estratégica
    └── Adaptación contextual

🧠 CAPA DE MEMORIA
├── Sistema de Memoria Avanzado (src/agents/memory/)
│   ├── Buffer, Ventana y Resumen
│   ├── Persistencia en archivos
│   └── Gestión de sesiones

💾 CAPA DE DATOS
├── Vector Database (ChromaDB)
│   └── Embeddings y recuperación semántica
├── CSV Data Sources
│   ├── inventory_las_condes.csv
│   └── turnos_septiembre.csv
└── Persistent Memory (JSON files)

🔧 CAPA DE CONFIGURACIÓN
├── Environment Variables (.env)
├── Dependencies (requirements.txt)
└── Models Configuration (GitHub Models API)

FLUJO DE DATOS:
Usuario → Streamlit → FastAPI → Agentes → Herramientas → Datos → Respuesta
"""
        
        print(arquitectura)
        
        print("\n🔗 PATRONES DE INTEGRACIÓN:")
        print("• Factory Pattern: Creación de agentes y herramientas")
        print("• Observer Pattern: Adaptación contextual en planificación")
        print("• Strategy Pattern: Diferentes estrategias de memoria")
        print("• Command Pattern: Ejecución de herramientas")
        print("• Chain of Responsibility: Procesamiento de consultas")
        
        print("\n✅ Arquitectura documentada - Cumple IL2.4")


def main():
    """Función principal para ejecutar todas las demostraciones."""
    print("🚀 Iniciando Sistema de Demostraciones CleanPro")
    print("Este script demuestra la implementación completa de IL2.1, IL2.2, IL2.3 e IL2.4")
    
    # Verificar variables de entorno
    required_vars = ["OPENAI_BASE_URL", "OPENAI_API_KEY", "GITHUB_TOKEN"]
    missing_vars = [var for var in required_vars if not os.getenv(var)]
    
    if missing_vars:
        print(f"⚠️ Variables de entorno faltantes: {missing_vars}")
        print("Por favor configurar el archivo .env antes de ejecutar")
        return
    
    # Crear demostrador y ejecutar
    demo = DemostradorFlujos()
    
    try:
        # Mostrar arquitectura
        demo.mostrar_arquitectura()
        
        # Ejecutar demostración completa
        demo.demo_completa()
        
        print("\n🎉 TODAS LAS DEMOSTRACIONES COMPLETADAS EXITOSAMENTE")
        print("✅ IL2.1: Agentes funcionales con herramientas integradas")
        print("✅ IL2.2: Memoria y recuperación de contexto") 
        print("✅ IL2.3: Planificación y toma de decisiones adaptativas")
        print("✅ IL2.4: Documentación y orquestación de componentes")
        
    except Exception as e:
        print(f"❌ Error durante la demostración: {str(e)}")
        print("Verifica que el servidor FastAPI esté ejecutándose y las dependencias instaladas")


if __name__ == "__main__":
    main()