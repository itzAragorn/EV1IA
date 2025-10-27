# 🎓 Guía Rápida para Evaluación - CleanPro AI

> **Para el Profesor**: Esta guía proporciona los pasos esenciales para evaluar el proyecto de manera eficiente.

---

## 🚀 Inicio Rápido (5 minutos)

### 1. Configuración Inicial
```powershell
# Clonar/abrir el proyecto
cd "c:\Users\Nico Osses\Documents\Materia\IA\EV1"

# Configurar token de GitHub (usar tu propio token)
$env:GITHUB_TOKEN="tu_github_token_aqui"
$env:OPENAI_API_KEY="tu_github_token_aqui"

# Instalar dependencias
pip install -r requirements.txt
```

### 2. Validación Automatizada
```powershell
# Ejecutar validación completa del sistema
python validar_sistema.py
```
**✅ Resultado esperado**: Todas las validaciones deben pasar (API, memoria, herramientas, frameworks)

### 3. Iniciar Demostración
```powershell
# Opción A: Script automatizado (recomendado)
.\iniciar_api.bat

# Opción B: Manual
# Terminal 1: API
cd src/api && python app.py

# Terminal 2: Interfaz Web  
streamlit run app_streamlit.py
```

### 4. Probar Sistema
**URL**: http://localhost:8501
- Probar consulta válida: "¿Cuánto stock hay en Las Condes?"
- Probar consulta inválida: "¿Cuánto stock hay en Madrid?" (debe manejar limitación)
- Probar diferentes modos: Individual, Multi-Agente, Planificación

---

## 📋 Checklist de Evaluación IL2.1-IL2.4

### ✅ IL2.1: Agentes Funcionales
- [ ] **Archivo**: `src/agents/langchain_agent.py` - Agente con 6 herramientas
- [ ] **Demo**: Consultas de inventario y turnos funcionando
- [ ] **Framework**: LangChain con OpenAI Functions Agent
- [ ] **Herramientas**: RAG, análisis, reportes, razonamiento, planificación

### ✅ IL2.2: Memoria y Contexto  
- [ ] **Archivo**: `src/agents/memory/advanced_memory.py`
- [ ] **Estrategias**: Buffer (≤10), Window (deslizante), Summary (resumen)
- [ ] **Persistencia**: JSON con metadatos de sesión
- [ ] **Demo**: Mantiene contexto en conversaciones largas

### ✅ IL2.3: Planificación Adaptativa
- [ ] **Archivos**: `src/agents/crewai_orchestration.py`, `src/agents/planning/`
- [ ] **Multi-Agente**: CrewAI con roles especializados (Investigador, Analista, etc.)
- [ ] **Adaptación**: Por recursos, tiempo, feedback del usuario
- [ ] **Demo**: `demo_flujos_automatizados.py`

### ✅ IL2.4: Documentación/Orquestación
- [ ] **README.md**: Arquitectura completa con diagramas Mermaid
- [ ] **INFORME_TECNICO.md**: Análisis técnico detallado  
- [ ] **Integración**: API + Streamlit + Componentes coordinados
- [ ] **Ejemplos**: Casos de uso organizacionales demostrados

---

## 🔍 Puntos Clave de Evaluación

### Funcionalidad Técnica
- **API Inteligente**: Detecta sinónimos (stock=inventario), reconoce ubicaciones
- **Memoria Adaptativa**: Cambia automáticamente según longitud conversación
- **Planificación Dinámica**: Se ajusta a condiciones cambiantes
- **Integración Completa**: LangChain + CrewAI funcionando juntos

### Calidad de Implementación
- **Manejo de Errores**: Respuestas apropiadas a consultas fuera de alcance
- **UI Profesional**: Tema oscuro, interfaz pulida
- **Validación**: Scripts automatizados de testing
- **Documentación**: Completa y detallada

### Casos de Uso Organizacionales
- **Inventario**: "¿Cuánto stock de productos de limpieza hay en Las Condes?"
- **Turnos**: "¿Qué turnos tiene María en septiembre?"
- **Análisis**: Reportes automatizados con múltiples agentes
- **Planificación**: Estrategias que se adaptan a restricciones

---

## 🐛 Solución Rápida de Problemas

### Error: "Max retries exceeded"
**Solución**: La API no está corriendo
```powershell
.\iniciar_api.bat
# O manualmente: cd src/api && python app.py
```

### Error: "Incorrect API key"
**Solución**: Configurar token de GitHub
```powershell
$env:GITHUB_TOKEN="tu_token"
$env:OPENAI_API_KEY="tu_token"
```

### Error: Puerto ocupado
**Solución**: Cambiar puertos o matar procesos
```powershell
netstat -ano | findstr :8000
taskkill /PID [PID_NUMBER] /F
```

---

## 📁 Archivos Importantes

### Código Principal
- `src/agents/langchain_agent.py` - Agente individual (IL2.1)
- `src/agents/memory/advanced_memory.py` - Sistema memoria (IL2.2)
- `src/agents/crewai_orchestration.py` - Multi-agente (IL2.3)
- `src/agents/planning/adaptive_planning.py` - Planificación (IL2.3)

### Interfaces
- `src/api/app.py` - API FastAPI
- `app_streamlit.py` - Interfaz web
- `demo_api.py` - API demo inteligente

### Documentación
- `README.md` - Documentación técnica completa
- `INFORME_TECNICO.md` - Análisis académico
- `MEJORAS_FINALES.md` - Log de cambios recientes

### Validación
- `validar_sistema.py` - Testing automatizado
- `demo_flujos_automatizados.py` - Casos de uso
- `iniciar_api.bat` - Script de inicio

---

## ⏱️ Tiempo Estimado de Evaluación

- **Configuración inicial**: 3-5 minutos
- **Validación automatizada**: 2 minutos  
- **Pruebas funcionales**: 10-15 minutos
- **Revisión código/documentación**: 15-20 minutos
- **Total**: ~30-40 minutos

---

## 🎯 Resumen Ejecutivo

**CleanPro AI** es un sistema completo de agentes inteligentes que demuestra:

1. **IL2.1**: Agente funcional con 6 herramientas especializadas usando LangChain
2. **IL2.2**: Sistema de memoria híbrido que se adapta automáticamente  
3. **IL2.3**: Planificación adaptativa con CrewAI y estrategias dinámicas
4. **IL2.4**: Documentación completa e integración de todos los componentes

El sistema incluye validación automatizada, interfaz profesional, y casos de uso organizacionales reales que demuestran aplicabilidad práctica en automatización empresarial.

---

> **Contacto**: Para cualquier consulta durante la evaluación, referirse a la documentación técnica completa en README.md o INFORME_TECNICO.md.