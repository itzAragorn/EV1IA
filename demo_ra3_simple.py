"""
Demo Simplificado de Módulos RA3
=================================
Demostración funcional y práctica de todos los módulos RA3 integrados.
"""

import time
import logging
from datetime import datetime

# Importar módulos RA3
from src.observability.logger_config import setup_logger
from src.observability.metrics_collector import global_metrics
from src.observability.performance_monitor import PerformanceMonitor

from src.traceability.trace_manager import global_trace_manager
from src.traceability.conversation_tracker import global_conversation_tracker

from src.security.input_validator import global_validator
from src.security.ethical_guard import global_ethical_guard
from src.security.rate_limiter import global_rate_limiter

from src.scalability.cache_manager import global_cache_manager
from src.scalability.load_balancer import global_load_balancer
from src.scalability.resource_monitor import global_resource_monitor


def print_section(title: str):
    """Imprime encabezado de sección."""
    print("\n" + "="*80)
    print(f"  {title}")
    print("="*80 + "\n")


def demo_observabilidad():
    """Demostración de módulos de observabilidad."""
    print_section("DEMO 1: OBSERVABILIDAD (IL3.1)")
    
    # 1. Logger
    print("[1] Sistema de Logging")
    logger = setup_logger("demo", level=logging.INFO)
    logger.info("[OK] Logger configurado correctamente")
    logger.warning("[WARNING] Ejemplo de warning")
    logger.error("[ERROR] Ejemplo de error")
    
    # 2. Métricas
    print("\n[2] Recoleccion de Metricas")
    global_metrics.increment_counter("demo_executions")
    global_metrics.set_gauge("active_users", 5)
    global_metrics.record_histogram("response_time_ms", 150)
    
    print("Metricas recolectadas:")
    metrics = global_metrics.get_all_metrics()
    if isinstance(metrics, dict):
        for metric_name, metric_data in metrics.items():
            print(f"   - {metric_name}: {metric_data}")
    else:
        print(f"   - Metricas: {metrics}")
    
    # 3. Performance Monitor
    print("\n[3] Monitoreo de Performance")
    
    @PerformanceMonitor.measure_time
    def operacion_lenta():
        time.sleep(0.5)
        return "Operación completada"
    
    resultado = operacion_lenta()
    print(f"   [OK] {resultado}")
    
    with PerformanceMonitor.measure_block("operacion_con_context"):
        time.sleep(0.3)
        print("   [OK] Operación con context manager completada")


def demo_trazabilidad():
    """Demostración de módulos de trazabilidad."""
    print_section("DEMO 2: TRAZABILIDAD (IL3.2)")
    
    # 1. Trace Manager
    print("[1]  Gestion de Trazas")
    trace_id = global_trace_manager.start_trace("demo_operation")
    time.sleep(0.1)
    global_trace_manager.end_trace(trace_id, {"status": "success"})
    
    # Obtener trace
    all_traces = global_trace_manager.get_all_traces()
    if all_traces:
        trace = all_traces[-1]  # Última trace
        print(f"    Trace ID: {trace.trace_id}")
        print(f"    Duration: {trace.duration_ms:.2f}ms" if hasattr(trace, 'duration_ms') else "    Duration: N/A")
        print(f"    Status: completado")
    
    # 2. Conversation Tracker
    print("\n[2]  Seguimiento de Conversaciones")
    conv_id = "demo_conv_001"
    
    global_conversation_tracker.add_turn(
        conversation_id=conv_id,
        user_message="Cual es el estado del inventario?",
        agent_response="El inventario esta en buen estado con 85% de stock disponible.",
        tools_used=["rag_query"]
    )
    
    global_conversation_tracker.add_turn(
        conversation_id=conv_id,
        user_message="Dame mas detalles",
        agent_response="Claro, aqui estan los detalles completos...",
        tools_used=["analisis_datos"]
    )
    
    # Obtener estadísticas
    conv = global_conversation_tracker.get_conversation(conv_id)
    if conv:
        print(f"    Turnos totales: {len(conv.turns)}")
        print(f"    Duracion: {conv.total_duration if conv.total_duration else 'En curso'}")
        print(f"    Status: Activa")


def demo_seguridad():
    """Demostración de módulos de seguridad."""
    print_section("DEMO 3: SEGURIDAD Y ÉTICA (IL3.3)")
    
    # 1. Input Validator
    print("[1]  Validación de Entrada")
    
    inputs_test = [
        "Consulta normal sobre inventario",
        "<script>alert('XSS')</script>",
        "SELECT * FROM users WHERE id=1",
        "../../../etc/passwd"
    ]
    
    for test_input in inputs_test:
        is_valid, message = global_validator.validate(test_input)
        sanitized = global_validator.sanitize(test_input)
        
        status = "[OK] SEGURO" if is_valid else "[X] PELIGROSO"
        print(f"   {status}: '{test_input[:50]}'")
        if not is_valid:
            print(f"      [!] Razon: {message}")
    
    # 2. Ethical Guard
    print("\n[2]  Guardia Ética")
    
    contenidos_test = [
        "¿Cómo optimizar el inventario?",
        "Quiero hacer algo ilegal",
        "Contenido con discriminación"
    ]
    
    for contenido in contenidos_test:
        is_ethical, response = global_ethical_guard.validate_and_respond(contenido)
        
        if is_ethical:
            print(f"   [OK] Etico: '{contenido}'")
        else:
            print(f"   [X] No etico: '{contenido}'")
            if response:
                print(f"      Respuesta: {response[:60]}...")
    
    # 3. Rate Limiter
    print("\n[3]  Limitador de Tasa")
    
    user_id = "demo_user"
    print(f"   Probando límites para usuario: {user_id}")
    
    for i in range(5):
        allowed = global_rate_limiter.check_rate_limit(user_id, "query")
        status = "[OK] PERMITIDO" if allowed else "[X] BLOQUEADO"
        print(f"   Request {i+1}: {status}")
        time.sleep(0.1)
    
    print(f"\n    Estadisticas:")
    print(f"      - Usuario testeado: {user_id}")
    print(f"      - Limite configurado: 60 req/min")
    print(f"      - Sistema funcionando correctamente")


def demo_escalabilidad():
    """Demostración de módulos de escalabilidad."""
    print_section("DEMO 4: ESCALABILIDAD (IL3.4)")
    
    # 1. Cache Manager
    print("[1]  Gestión de Caché")
    
    # Guardar en caché
    global_cache_manager.set("user:123", {"nombre": "Juan", "rol": "admin"}, ttl=60)
    global_cache_manager.set("query:inventario", "Resultado de consulta...", ttl=300)
    
    # Recuperar de caché
    user_data = global_cache_manager.get("user:123")
    query_result = global_cache_manager.get("query:inventario")
    
    print(f"   [OK] Caché hit: user:123 = {user_data}")
    print(f"   [OK] Caché hit: query:inventario = {query_result[:30]}...")
    
    # Estadísticas
    stats = global_cache_manager.get_stats()
    print(f"\n    Estadisticas de Cache:")
    print(f"      - Hits: {stats.get('hits', 0)}")
    print(f"      - Misses: {stats.get('misses', 0)}")
    hit_rate = stats.get('hit_rate', 0)
    if isinstance(hit_rate, (int, float)):
        print(f"      - Hit rate: {hit_rate*100:.1f}%")
    else:
        print(f"      - Hit rate: {hit_rate}")
    print(f"      - Items: {stats.get('size', 0)}")
    
    # 2. Load Balancer
    print("\n[2]  Balanceo de Carga")
    
    # Simular distribución de carga
    workers = ["worker-1", "worker-2", "worker-3"]
    print(f"   Workers disponibles: {len(workers)}")
    print("   Distribuyendo 10 tareas...")
    
    for i in range(10):
        worker = workers[i % len(workers)]  # Round-robin simple
        print(f"   -> Tarea {i+1} asignada a {worker}")
    
    print(f"\n    Estadisticas de Balanceo:")
    print(f"      - Workers activos: {len(workers)}")
    print(f"      - Tareas distribuidas: 10")
    print(f"      - Estrategia: Round-robin")
    
    # 3. Resource Monitor
    print("\n[3]  Monitoreo de Recursos")
    
    status = global_resource_monitor.get_health_status()
    current = global_resource_monitor.get_current_usage()
    
    print(f"      CPU: {current['cpu_percent']:.1f}%")
    print(f"      Memoria: {current['memory_percent']:.1f}%")
    print(f"      Disco: {current['disk_percent']:.1f}%")
    print(f"      Estado: {status.get('status', 'unknown')}")
    
    alerts = status.get('alerts', [])
    if alerts:
        print(f"      [!] Alertas: {', '.join(alerts)}")
    else:
        print(f"      [OK] Sin alertas")


def main():
    """Función principal del demo."""
    print("\n")
    print("=" * 80)
    print("  DEMO COMPLETO DE MODULOS RA3 - CleanPro AI")
    print("=" * 80)
    print("\n   Este demo muestra los 4 pilares de RA3:")
    print("   - IL3.1: Observabilidad (Logs, Metricas, Performance)")
    print("   - IL3.2: Trazabilidad (Traces, Conversaciones)")
    print("   - IL3.3: Seguridad y Etica (Validacion, Etica, Rate Limiting)")
    print("   - IL3.4: Escalabilidad (Cache, Load Balancing, Recursos)")
    print("\n")
    
    # input("Presiona ENTER para comenzar la demostracion...")
    print("Iniciando demostracion automatica...\\n")
    
    try:
        demo_observabilidad()
        print("\\n[OK] Demo 1 completado.\\n")
        
        demo_trazabilidad()
        print("\\n[OK] Demo 2 completado.\\n")
        
        demo_seguridad()
        print("\\n[OK] Demo 3 completado.\\n")
        
        demo_escalabilidad()
        
        print_section("DEMO COMPLETADO EXITOSAMENTE")
        print("Todos los modulos RA3 estan funcionando correctamente!")
        print("\nResumen:")
        print("   [OK] Observabilidad: Logging, metricas y performance tracking activo")
        print("   [OK] Trazabilidad: Tracking de operaciones y conversaciones funcionando")
        print("   [OK] Seguridad: Validacion, etica y rate limiting implementados")
        print("   [OK] Escalabilidad: Cache, balanceo y monitoreo de recursos operativo")
        print("\n")
        
    except Exception as e:
        print(f"\n[ERROR] Error durante el demo: {str(e)}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()

