"""
Pruebas de Validación del Sistema CleanPro
=========================================
Script para validar el funcionamiento de todos los componentes
antes de la entrega del proyecto.
"""

import os
import sys
import requests
import json
from datetime import datetime

# Agregar el directorio raíz al path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_environment():
    """Valida la configuración del entorno."""
    print("🔧 Validando configuración del entorno...")
    
    required_vars = ["OPENAI_BASE_URL", "OPENAI_API_KEY", "GITHUB_TOKEN"]
    missing_vars = []
    
    for var in required_vars:
        if not os.getenv(var):
            missing_vars.append(var)
    
    if missing_vars:
        print(f"❌ Variables faltantes: {missing_vars}")
        return False
    else:
        print("✅ Variables de entorno configuradas correctamente")
        return True

def test_api_health():
    """Verifica que la API esté funcionando."""
    print("\n🔍 Verificando estado de la API...")
    
    try:
        response = requests.get("http://localhost:8000/health", timeout=10)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ API funcionando - Status: {data['status']}")
            print(f"   Sistemas activos: {data['systems']}")
            return True
        else:
            print(f"❌ API error - Status: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ No se pudo conectar a la API: {e}")
        print("   Asegúrate de que el servidor esté ejecutándose con:")
        print("   uvicorn src.api.app:app --reload")
        return False

def test_individual_agent():
    """Prueba el agente individual (IL2.1, IL2.2)."""
    print("\n🤖 Probando agente individual...")
    
    session_id = f"test_{datetime.now().strftime('%H%M%S')}"
    
    # Primera consulta
    query1 = {
        "query": "¿Cuál es el estado actual del inventario de Las Condes?",
        "session_id": session_id
    }
    
    try:
        response1 = requests.post(
            "http://localhost:8000/agent/query",
            json=query1,
            timeout=30
        )
        
        if response1.status_code == 200:
            data1 = response1.json()
            print("✅ Primera consulta exitosa")
            print(f"   Herramientas usadas: {data1.get('tools_used', [])}")
            
            # Segunda consulta para probar memoria
            query2 = {
                "query": "Basándote en ese análisis, ¿qué recomendaciones harías?",
                "session_id": session_id
            }
            
            response2 = requests.post(
                "http://localhost:8000/agent/query", 
                json=query2,
                timeout=30
            )
            
            if response2.status_code == 200:
                data2 = response2.json()
                print("✅ Segunda consulta exitosa - Memoria funcionando")
                print(f"   Respuesta hace referencia al contexto previo")
                return True
            else:
                print(f"❌ Error en segunda consulta: {response2.status_code}")
                return False
        else:
            print(f"❌ Error en primera consulta: {response1.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Error probando agente individual: {e}")
        return False

def test_multi_agent_crew():
    """Prueba el sistema multi-agente (IL2.3)."""
    print("\n👥 Probando sistema multi-agente...")
    
    crew_data = {
        "objective": "Realizar análisis rápido de las operaciones de CleanPro",
        "flow_type": "investigacion_completa",
        "session_id": f"crew_test_{datetime.now().strftime('%H%M%S')}"
    }
    
    try:
        response = requests.post(
            "http://localhost:8000/crew/execute",
            json=crew_data,
            timeout=60
        )
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Sistema multi-agente funcionando")
            print(f"   Agentes utilizados: {data['result'].get('agentes_utilizados', [])}")
            return True
        else:
            print(f"❌ Error en sistema multi-agente: {response.status_code}")
            print(f"   Respuesta: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Error probando multi-agente: {e}")
        return False

def test_adaptive_planning():
    """Prueba la planificación adaptativa (IL2.3)."""
    print("\n📋 Probando planificación adaptativa...")
    
    plan_id = f"test_plan_{datetime.now().strftime('%H%M%S')}"
    
    # Crear plan
    plan_data = {
        "plan_id": plan_id,
        "objective": "Plan de prueba para validación del sistema",
        "context": {
            "recursos": ["recurso_test_1", "recurso_test_2"],
            "tiempo": {"deadline": 300}
        }
    }
    
    try:
        response = requests.post(
            "http://localhost:8000/planning/create",
            json=plan_data,
            timeout=20
        )
        
        if response.status_code == 200:
            print("✅ Plan creado exitosamente")
            
            # Actualizar contexto para probar adaptación
            context_update = {
                "recursos": ["recurso_test_1"],  # Recurso reducido
                "tiempo": {"deadline": 150},     # Tiempo reducido
                "feedback": ["Acelerar proceso"]
            }
            
            response2 = requests.put(
                f"http://localhost:8000/planning/plans/{plan_id}/context",
                json=context_update,
                timeout=20
            )
            
            if response2.status_code == 200:
                data = response2.json()
                adaptaciones = data.get('adaptaciones', [])
                print(f"✅ Adaptación exitosa - {len(adaptaciones)} adaptaciones realizadas")
                return True
            else:
                print(f"❌ Error en adaptación: {response2.status_code}")
                return False
        else:
            print(f"❌ Error creando plan: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Error probando planificación: {e}")
        return False

def test_file_structure():
    """Verifica que todos los archivos clave estén presentes."""
    print("\n📁 Verificando estructura de archivos...")
    
    required_files = [
        "README.md",
        "requeriments.txt", 
        "app_streamlit.py",
        "demo_flujos_automatizados.py",
        "src/api/app.py",
        "src/agents/langchain_agent.py",
        "src/agents/crewai_orchestration.py",
        "src/agents/memory/advanced_memory.py",
        "src/agents/planning/adaptive_planning.py",
        "src/agents/tools/rag_tools.py",
        "src/agents/tools/escritura_tools.py",
        "src/agents/tools/razonamiento_tools.py"
    ]
    
    missing_files = []
    for file_path in required_files:
        if not os.path.exists(file_path):
            missing_files.append(file_path)
    
    if missing_files:
        print(f"❌ Archivos faltantes: {missing_files}")
        return False
    else:
        print("✅ Todos los archivos clave están presentes")
        return True

def test_data_files():
    """Verifica que los archivos de datos estén disponibles."""
    print("\n💾 Verificando archivos de datos...")
    
    data_files = [
        "data/inventory_las_condes.csv",
        "data/turnos_septiembre.csv"
    ]
    
    missing_data = []
    for file_path in data_files:
        if not os.path.exists(file_path):
            missing_data.append(file_path)
    
    if missing_data:
        print(f"⚠️ Archivos de datos faltantes: {missing_data}")
        print("   Esto puede afectar algunas funcionalidades")
        return False
    else:
        print("✅ Archivos de datos disponibles")
        return True

def main():
    """Ejecuta todas las pruebas de validación."""
    print("🚀 INICIANDO VALIDACIÓN DEL SISTEMA CLEANPRO")
    print("=" * 60)
    
    tests = [
        ("Configuración de entorno", test_environment),
        ("Estructura de archivos", test_file_structure),
        ("Archivos de datos", test_data_files),
        ("Estado de la API", test_api_health),
        ("Agente individual", test_individual_agent),
        ("Sistema multi-agente", test_multi_agent_crew),
        ("Planificación adaptativa", test_adaptive_planning)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ Error ejecutando {test_name}: {e}")
            results.append((test_name, False))
    
    # Resumen de resultados
    print("\n" + "=" * 60)
    print("📊 RESUMEN DE VALIDACIÓN")
    print("=" * 60)
    
    passed = 0
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASÓ" if result else "❌ FALLÓ" 
        print(f"{status:<10} {test_name}")
        if result:
            passed += 1
    
    print(f"\n🎯 RESULTADO FINAL: {passed}/{total} pruebas exitosas")
    
    if passed == total:
        print("🎉 ¡SISTEMA COMPLETAMENTE FUNCIONAL!")
        print("   Listo para entrega y evaluación")
    elif passed >= total * 0.8:
        print("⚠️ Sistema mayormente funcional")
        print("   Revisar pruebas fallidas antes de entrega")
    else:
        print("❌ Sistema requiere correcciones")
        print("   Resolver problemas antes de entrega")
    
    # Instrucciones finales
    print("\n" + "=" * 60)
    print("📋 PRÓXIMOS PASOS:")
    print("1. Si todas las pruebas pasaron: ¡Listo para entregar!")
    print("2. Si hay fallas: Revisar errores y volver a ejecutar")
    print("3. Para demostración completa: python demo_flujos_automatizados.py")
    print("4. Para interfaz web: streamlit run app_streamlit.py")
    print("=" * 60)

if __name__ == "__main__":
    main()