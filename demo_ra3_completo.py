"""
Demo Completo de RA3 - CleanPro AI System
Demuestra todas las funcionalidades de Observabilidad, Trazabilidad, Seguridad y Escalabilidad
"""

import time
from src.observability.logger_config import setup_logger, get_logger
from src.observability.metrics_collector import global_metrics
from src.observability.performance_monitor import PerformanceMonitor
from src.traceability.trace_manager import global_trace_manager
from src.traceability.conversation_tracker import global_conversation_tracker
from src.security.input_validator import global_validator, SecurityLevel
from src.security.ethical_guard import global_ethical_guard
from src.security.rate_limiter import global_rate_limiter
from src.scalability.cache_manager import global_cache_manager
from src.scalability.resource_monitor import global_resource_monitor
from src.scalability.load_balancer import global_load_balancer, LoadBalancingStrategy

# Configurar logger para el demo
logger = setup_logger('demo_ra3', log_file='logs/demo_ra3.log')

def demo_observabilidad():
    """IL3.1: Demo de Herramientas de Observabilidad"""
    print("\n" + "="*80)
    print("🔍 IL3.1: DEMO DE OBSERVABILIDAD Y MÉTRICAS")
    print("="*80)
    
    logger.info("Iniciando demo de observabilidad...")
    
    # 1. Métricas básicas
    print("\n📊 1. Recolección de Métricas")
    global_metrics.increment_counter('demo.requests')
    global_metrics.set_gauge('demo.active_users', 42)
    global_metrics.record_histogram('demo.response_time', 0.125)
    global_metrics.record_histogram('demo.response_time', 0.089)
    global_metrics.record_histogram('demo.response_time', 0.234)
    
    print(f"  ✓ Contador 'demo.requests': {global_metrics.get_counter('demo.requests')}")
    print(f"  ✓ Gauge 'demo.active_users': {global_metrics.get_gauge('demo.active_users')}")
    
    stats = global_metrics.get_histogram_stats('demo.response_time')
    print(f"  ✓ Histograma 'demo.response_time':")
    print(f"    - Promedio: {stats['avg']:.3f}s")
    print(f"    - Mínimo: {stats['min']:.3f}s")
    print(f"    - Máximo: {stats['max']:.3f}s")
    
    # 2. Monitor de rendimiento con decorador
    print("\n⏱️  2. Monitor de Rendimiento")
    
    @PerformanceMonitor.measure_time
    def tarea_ejemplo():
        """Tarea de ejemplo que será medida"""
        time.sleep(0.1)
        return "Tarea completada"
    
    resultado = tarea_ejemplo()
    print(f"  ✓ {resultado}")
    
    # 3. Monitor de rendimiento con context manager
    print("\n🎯 3. Medición de Bloques de Código")
    with PerformanceMonitor.measure_block("procesamiento_datos"):
        time.sleep(0.05)
        print("  ✓ Procesando datos...")
        time.sleep(0.05)
    
    # 4. Métricas del sistema
    print("\n💻 4. Métricas del Sistema")
    global_resource_monitor.take_snapshot()
    current = global_resource_monitor.get_current_usage()
    print(f"  ✓ CPU: {current['cpu_percent']:.1f}%")
    print(f"  ✓ Memoria: {current['memory_percent']:.1f}%")
    print(f"  ✓ Disco: {current['disk_percent']:.1f}%")
    
    # Resumen
    print("\n📈 Resumen de Métricas:")
    summary = global_metrics.get_summary()
    print(f"  Total de métricas registradas: {summary['total_metrics']}")
    print(f"  Contadores activos: {len(summary['counters'])}")
    print(f"  Gauges activos: {len(summary['gauges'])}")

def demo_trazabilidad():
    """IL3.2: Demo de Análisis de Trazabilidad"""
    print("\n" + "="*80)
    print("🔍 IL3.2: DEMO DE TRAZABILIDAD Y LOGS")
    print("="*80)
    
    logger.info("Iniciando demo de trazabilidad...")
    
    # 1. Trazas de operaciones
    print("\n📋 1. Sistema de Trazas")
    trace_id = global_trace_manager.start_trace(
        "demo_operation",
        user_id="demo_user",
        operation_type="analysis"
    )
    print(f"  ✓ Traza iniciada: {trace_id[:8]}...")
    
    # Crear spans dentro de la traza
    span1_id = global_trace_manager.start_span(trace_id, "data_loading")
    time.sleep(0.05)
    global_trace_manager.add_span_log(span1_id, "Datos cargados correctamente", records=100)
    global_trace_manager.end_span(span1_id)
    print("  ✓ Span 'data_loading' completado")
    
    span2_id = global_trace_manager.start_span(trace_id, "data_processing")
    time.sleep(0.08)
    global_trace_manager.add_span_log(span2_id, "Procesamiento completado", records_processed=100)
    global_trace_manager.end_span(span2_id)
    print("  ✓ Span 'data_processing' completado")
    
    global_trace_manager.end_trace(trace_id, status="success")
    print(f"  ✓ Traza finalizada exitosamente")
    
    # 2. Rastreo de conversaciones
    print("\n💬 2. Rastreo de Conversaciones")
    conv_id = "conv_demo_001"
    global_conversation_tracker.start_conversation(conv_id, user="demo_user")
    
    global_conversation_tracker.add_turn(
        conv_id,
        user_message="¿Cuál es el inventario en Las Condes?",
        agent_response="Hay 150 unidades de productos de limpieza disponibles.",
        tools_used=["rag_consulta", "inventario"],
        duration=0.234
    )
    print("  ✓ Turno 1 registrado")
    
    global_conversation_tracker.add_turn(
        conv_id,
        user_message="¿Y en Providencia?",
        agent_response="En Providencia hay 89 unidades disponibles.",
        tools_used=["rag_consulta", "inventario"],
        duration=0.189
    )
    print("  ✓ Turno 2 registrado")
    
    global_conversation_tracker.end_conversation(conv_id)
    
    # Resumen
    print("\n📊 Resumen de Trazabilidad:")
    trace_summary = global_trace_manager.get_traces_summary()
    print(f"  Trazas totales: {trace_summary['total_traces']}")
    print(f"  Trazas exitosas: {trace_summary['successful']}")
    print(f"  Duración promedio: {trace_summary['avg_duration']:.3f}s")
    
    conv_summary = global_conversation_tracker.get_summary()
    print(f"  Conversaciones: {conv_summary['total_conversations']}")
    print(f"  Turnos totales: {conv_summary['total_turns']}")

def demo_seguridad():
    """IL3.3: Demo de Seguridad y Ética"""
    print("\n" + "="*80)
    print("🛡️  IL3.3: DEMO DE SEGURIDAD Y ÉTICA")
    print("="*80)
    
    logger.info("Iniciando demo de seguridad...")
    
    # 1. Validación de entradas
    print("\n🔒 1. Validación de Entradas")
    
    entradas_prueba = [
        ("Hola, ¿cómo estás?", True),
        ("<script>alert('xss')</script>", False),
        ("2 + 2", True),
        ("SELECT * FROM users WHERE id=1; DROP TABLE users;", False)
    ]
    
    for entrada, esperado in entradas_prueba:
        is_valid, message = global_validator.validate(entrada)
        status = "✓" if is_valid == esperado else "✗"
        print(f"  {status} '{entrada[:40]}...' -> {'Válido' if is_valid else 'Bloqueado'}")
    
    # 2. Evaluación segura
    print("\n🧮 2. Evaluación Segura de Expresiones")
    expresiones = [
        ("2 + 2 * 3", True),
        ("(10 + 5) / 3", True),
        ("import os", False),
        ("exec('print(1)')", False)
    ]
    
    for expr, esperado in expresiones:
        is_safe, result = global_validator.safe_eval(expr)
        status = "✓" if is_safe == esperado else "✗"
        if is_safe:
            print(f"  {status} '{expr}' = {result}")
        else:
            print(f"  {status} '{expr}' -> Bloqueado")
    
    # 3. Guardián ético
    print("\n🤝 3. Guardián Ético")
    
    preguntas = [
        "¿Cómo puedo optimizar mi inventario?",
        "¿Cómo puedo hackear un sistema?",
        "Dame información sobre turnos de empleados",
        "Quiero robar información privada"
    ]
    
    for pregunta in preguntas:
        is_ethical, response = global_ethical_guard.validate_and_respond(pregunta)
        if is_ethical:
            print(f"  ✓ Pregunta apropiada: '{pregunta}'")
        else:
            print(f"  🚫 Pregunta bloqueada: '{pregunta[:40]}...'")
            print(f"     Respuesta: {response}")
    
    # 4. Rate limiting
    print("\n⏱️  4. Limitación de Tasa")
    user_id = "demo_user"
    
    for i in range(5):
        allowed, message = global_rate_limiter.check_rate_limit(user_id, "query")
        if allowed:
            global_rate_limiter.record_request(user_id, "query")
            print(f"  ✓ Request {i+1}/5 permitido")
        else:
            print(f"  🚫 Request {i+1}/5 bloqueado: {message}")
    
    stats = global_rate_limiter.get_user_stats(user_id)
    print(f"\n  Estadísticas del usuario:")
    print(f"    Requests en ventana (query): {stats['query']['requests_in_window']}/{stats['query']['max_requests']}")
    print(f"    Requests restantes: {stats['query']['remaining']}")

def demo_escalabilidad():
    """IL3.4: Demo de Escalabilidad y Sostenibilidad"""
    print("\n" + "="*80)
    print("📈 IL3.4: DEMO DE ESCALABILIDAD Y SOSTENIBILIDAD")
    print("="*80)
    
    logger.info("Iniciando demo de escalabilidad...")
    
    # 1. Sistema de caché
    print("\n💾 1. Sistema de Caché")
    
    # Simular consultas con caché
    print("  Primera consulta (cache miss):")
    result = global_cache_manager.get("query:inventario_las_condes")
    if result is None:
        print("    🔴 Cache miss - consultando base de datos...")
        time.sleep(0.1)  # Simular consulta lenta
        result = {"producto": "Limpiadores", "cantidad": 150}
        global_cache_manager.set("query:inventario_las_condes", result, ttl=60)
        print(f"    ✓ Resultado guardado en caché")
    
    print("  Segunda consulta (cache hit):")
    result = global_cache_manager.get("query:inventario_las_condes")
    if result is not None:
        print(f"    🟢 Cache hit - {result}")
    
    stats = global_cache_manager.get_stats()
    print(f"\n  Estadísticas de caché:")
    print(f"    Hit rate: {stats['hit_rate']}")
    print(f"    Total requests: {stats['total_requests']}")
    
    # 2. Balanceo de carga
    print("\n⚖️  2. Balanceo de Carga")
    
    def worker_handler(task):
        """Handler de ejemplo para un worker"""
        time.sleep(0.02)
        return f"Procesado: {task}"
    
    # Agregar workers
    for i in range(3):
        global_load_balancer.add_worker(f"worker_{i+1}", worker_handler)
    
    # Procesar tareas
    print("  Procesando tareas distribuidas...")
    tareas = ["tarea_1", "tarea_2", "tarea_3", "tarea_4", "tarea_5"]
    for tarea in tareas:
        result = global_load_balancer.process(tarea)
        print(f"    ✓ {result}")
    
    lb_stats = global_load_balancer.get_stats()
    print(f"\n  Estadísticas del balanceador:")
    print(f"    Workers activos: {lb_stats['workers']}")
    print(f"    Total procesado: {lb_stats['total_processed']}")
    print(f"    Estrategia: {lb_stats['strategy']}")
    
    # 3. Monitor de recursos
    print("\n🖥️  3. Monitor de Recursos")
    
    global_resource_monitor.take_snapshot()
    health = global_resource_monitor.get_health_status()
    
    print(f"  Estado del sistema: {health['status'].upper()}")
    print(f"  CPU: {health['current_usage']['cpu_percent']:.1f}%")
    print(f"  Memoria: {health['current_usage']['memory_percent']:.1f}%")
    
    if health['issues']:
        print("  ⚠️  Problemas detectados:")
        for issue in health['issues']:
            print(f"    - {issue}")
    
    recommendations = global_resource_monitor.get_recommendations()
    if recommendations:
        print("  💡 Recomendaciones:")
        for rec in recommendations[:3]:  # Primeras 3
            print(f"    - {rec}")

def main():
    """Ejecuta el demo completo de RA3"""
    print("\n" + "="*80)
    print("🚀 DEMO COMPLETO DE RA3 - CLEANPRO AI SYSTEM")
    print("="*80)
    print("\nIntegración de Observabilidad, Trazabilidad, Seguridad y Escalabilidad")
    print("Evaluación 3 - Sistemas de Agentes de IA")
    
    try:
        # Ejecutar cada demo
        demo_observabilidad()
        time.sleep(0.5)
        
        demo_trazabilidad()
        time.sleep(0.5)
        
        demo_seguridad()
        time.sleep(0.5)
        
        demo_escalabilidad()
        
        # Resumen final
        print("\n" + "="*80)
        print("✅ DEMO COMPLETADO EXITOSAMENTE")
        print("="*80)
        
        print("\n📊 Resumen General:")
        print(f"  - Métricas registradas: {global_metrics.get_summary()['total_metrics']}")
        print(f"  - Trazas completadas: {global_trace_manager.get_traces_summary()['total_traces']}")
        print(f"  - Conversaciones rastreadas: {global_conversation_tracker.get_summary()['total_conversations']}")
        print(f"  - Violaciones éticas detectadas: {global_ethical_guard.get_violations_summary()['total_violations']}")
        print(f"  - Cache hit rate: {global_cache_manager.get_stats()['hit_rate']}")
        print(f"  - Workers activos: {global_load_balancer.get_stats()['workers']}")
        
        print("\n💾 Datos guardados en:")
        print("  - logs/cleanpro.log")
        print("  - logs/demo_ra3.log")
        
        logger.info("Demo RA3 completado exitosamente")
        
    except Exception as e:
        logger.error(f"Error en demo: {str(e)}", exc_info=True)
        print(f"\n❌ Error en el demo: {str(e)}")
        raise

if __name__ == "__main__":
    main()
