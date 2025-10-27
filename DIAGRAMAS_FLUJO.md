# 🔄 Diagramas de Flujo - Sistema CleanPro AI

Este documento contiene los diagramas de flujo detallados del sistema CleanPro AI, mostrando cómo interactúan todos los componentes desde la perspectiva del usuario hasta la generación de respuestas.

---

## 📊 Flujo Principal del Sistema

```mermaid
flowchart TD
    %% Inicio del proceso
    Start([👤 Usuario accede al sistema]) --> Check{🔍 Sistema validado?}
    Check --> |No| Validate[⚡ validar_sistema.py]
    Validate --> Setup[🔧 Configuración automática]
    Setup --> Check
    
    Check --> |Sí| UI[🖥️ Interfaz Streamlit<br/>localhost:8501]
    
    %% Selección de modo
    UI --> Mode{🎯 Selección de Modo}
    Mode --> |Individual| Path1[🤖 Agente Individual]
    Mode --> |Multi-Agente| Path2[👥 Sistema CrewAI]  
    Mode --> |Planificación| Path3[📋 Planificación Adaptativa]
    
    %% Flujo Agente Individual (IL2.1)
    Path1 --> Input1[📝 Entrada del usuario]
    Input1 --> Memory1{🧠 Análisis Memoria}
    Memory1 --> |≤10 mensajes| Buffer[💾 Buffer Memory]
    Memory1 --> |11-50 mensajes| Window[🪟 Window Memory]
    Memory1 --> |>50 mensajes| Summary[📄 Summary Memory]
    
    Buffer --> Context1[📋 Contexto preparado]
    Window --> Context1
    Summary --> Context1
    
    Context1 --> LangChain[🔗 LangChain Agent]
    LangChain --> ToolSelect{🛠️ Selección Herramientas}
    
    %% Herramientas disponibles
    ToolSelect --> |Consulta datos| RAG[🗃️ RAG Consulta]
    ToolSelect --> |Generar reporte| Report[📊 Escritura Reporte]
    ToolSelect --> |Analizar información| Analysis[📈 Análisis Datos]
    ToolSelect --> |Tomar decisión| Decision[🧠 Razonamiento]
    ToolSelect --> |Crear plan| Planning[📋 Planificación]
    ToolSelect --> |Adaptar contexto| Adaptation[🔄 Adaptación]
    
    %% API Demo Inteligente
    RAG --> API1[🎭 demo_api.py]
    API1 --> NLP[🧠 Procesamiento NLP]
    NLP --> |stock=inventario| Synonym[📝 Detección Sinónimos]
    NLP --> |Las Condes| Location[📍 Reconocimiento Ubicación]
    NLP --> |Fuera alcance| Limit[⚠️ Manejo Limitaciones]
    
    Synonym --> Response1[📤 Respuesta Contextual]
    Location --> Response1
    Limit --> Response1
    
    %% Flujo Multi-Agente (IL2.3)
    Path2 --> Input2[📝 Entrada del usuario]
    Input2 --> CrewCoord[👨‍💼 Coordinador CrewAI]
    CrewCoord --> TaskDist{📋 Distribución Tareas}
    
    TaskDist --> Researcher[🔍 Agente Investigador]
    TaskDist --> Analyst[📊 Agente Analista]  
    TaskDist --> Writer[📝 Agente Documentador]
    
    Researcher --> Research[🔍 Investigación de datos]
    Analyst --> Analyze[📊 Análisis profundo]
    Writer --> Document[📝 Documentación]
    
    Research --> Collab[🤝 Colaboración]
    Analyze --> Collab
    Document --> Collab
    
    Collab --> Response2[📤 Respuesta Colaborativa]
    
    %% Flujo Planificación Adaptativa (IL2.3)
    Path3 --> Input3[📝 Entrada del usuario]
    Input3 --> PlanEngine[⚙️ Motor Planificación]
    PlanEngine --> ContextAnalysis{📋 Análisis Contexto}
    
    ContextAnalysis --> Resources[💾 Recursos Disponibles]
    ContextAnalysis --> TimeConst[⏰ Restricciones Tiempo]
    ContextAnalysis --> UserFeed[🔄 Feedback Usuario]
    
    Resources --> Adapt1{🔄 Adaptación?}
    TimeConst --> Adapt1
    UserFeed --> Adapt1
    
    Adapt1 --> |Sí| Replan[🔄 Re-planificación]
    Adapt1 --> |No| Execute[⚡ Ejecución Plan]
    
    Replan --> Execute
    Execute --> Response3[📤 Respuesta Adaptativa]
    
    %% Convergencia de respuestas
    Response1 --> Format{📋 Formateo}
    Response2 --> Format
    Response3 --> Format
    Report --> Format
    Analysis --> Format
    Decision --> Format
    Planning --> Format
    Adaptation --> Format
    
    Format --> UI_Display[🎨 Presentación UI]
    UI_Display --> |Tema oscuro| Visual[🌙 Estilo Visual]
    Visual --> End([✅ Respuesta mostrada al usuario])
    
    %% Estilos
    classDef startEnd fill:#4A90E2,stroke:#2E5C8A,stroke-width:3px,color:#fff
    classDef process fill:#50C878,stroke:#2E7D5F,stroke-width:2px,color:#fff
    classDef decision fill:#FFB347,stroke:#CC8A37,stroke-width:2px,color:#fff
    classDef tool fill:#DA70D6,stroke:#B85AA6,stroke-width:2px,color:#fff
    classDef api fill:#FF6B6B,stroke:#CC5555,stroke-width:2px,color:#fff
    classDef agent fill:#20B2AA,stroke:#177A7A,stroke-width:2px,color:#fff
    
    class Start,End startEnd
    class UI,Input1,Input2,Input3,Context1,Response1,Response2,Response3,Format,UI_Display,Visual process
    class Check,Mode,Memory1,ToolSelect,TaskDist,ContextAnalysis,Adapt1 decision
    class RAG,Report,Analysis,Decision,Planning,Adaptation tool
    class API1,NLP,Synonym,Location,Limit api
    class Path1,Path2,Path3,LangChain,CrewCoord,PlanEngine,Researcher,Analyst,Writer agent
```

---

## 🧠 Flujo de Gestión de Memoria (IL2.2)

```mermaid
flowchart TD
    Start([📝 Nueva consulta]) --> CheckSession{🔍 Sesión existente?}
    
    CheckSession --> |No| CreateSession[🆕 Crear sesión nueva]
    CheckSession --> |Sí| LoadSession[📂 Cargar sesión existente]
    
    CreateSession --> InitMemory[💾 Inicializar memoria]
    LoadSession --> CountMsgs{📊 Contar mensajes}
    
    InitMemory --> BufferMode[🔵 Modo Buffer Memory]
    
    CountMsgs --> |≤ 10 mensajes| BufferMode
    CountMsgs --> |11-50 mensajes| WindowMode[🟡 Modo Window Memory]  
    CountMsgs --> |> 50 mensajes| SummaryMode[🔴 Modo Summary Memory]
    
    BufferMode --> ProcessBuffer[📋 Mantener todos los mensajes]
    WindowMode --> ProcessWindow[🪟 Ventana deslizante de 5 mensajes]
    SummaryMode --> ProcessSummary[📄 Resumir mensajes antiguos]
    
    ProcessBuffer --> StoreBuffer[💾 Almacenar en JSON]
    ProcessWindow --> StoreWindow[💾 Almacenar ventana + histórico]
    ProcessSummary --> StoreSummary[💾 Almacenar resumen + recientes]
    
    StoreBuffer --> Context[📋 Preparar contexto]
    StoreWindow --> Context
    StoreSummary --> Context
    
    Context --> Agent[🤖 Enviar a agente]
    Agent --> Response[📤 Generar respuesta]
    Response --> SaveResponse[💾 Guardar respuesta]
    
    SaveResponse --> CheckSize{📏 Revisar tamaño}
    CheckSize --> |Crece| Transition{🔄 ¿Cambiar modo?}
    CheckSize --> |OK| End([✅ Finalizar])
    
    Transition --> |Buffer → Window| SwitchWindow[🔄 Cambiar a Window]
    Transition --> |Window → Summary| SwitchSummary[🔄 Cambiar a Summary]
    Transition --> |No cambio| End
    
    SwitchWindow --> ProcessWindow
    SwitchSummary --> ProcessSummary
    
    %% Estilos
    classDef memory fill:#FFB347,stroke:#CC8A37,stroke-width:2px,color:#fff
    classDef process fill:#50C878,stroke:#2E7D5F,stroke-width:2px,color:#fff
    classDef decision fill:#DA70D6,stroke:#B85AA6,stroke-width:2px,color:#fff
    classDef storage fill:#87CEEB,stroke:#5F9EA0,stroke-width:2px,color:#fff
    
    class BufferMode,WindowMode,SummaryMode,ProcessBuffer,ProcessWindow,ProcessSummary memory
    class CreateSession,LoadSession,InitMemory,Context,Agent,Response,SwitchWindow,SwitchSummary process
    class CheckSession,CountMsgs,CheckSize,Transition decision
    class StoreBuffer,StoreWindow,StoreSummary,SaveResponse storage
```

---

## 🎭 Flujo API Demo Inteligente

```mermaid
flowchart TD
    APICall([📞 Llamada API]) --> ParseQuery[🔍 Parsear consulta]
    ParseQuery --> NLPProcess[🧠 Procesamiento NLP]
    
    NLPProcess --> DetectIntent{🎯 Detectar intención}
    
    DetectIntent --> |Inventario| InventoryFlow[📦 Flujo Inventario]
    DetectIntent --> |Turnos| ShiftFlow[👥 Flujo Turnos]
    DetectIntent --> |Otro| GenericFlow[❓ Flujo Genérico]
    
    %% Flujo Inventario
    InventoryFlow --> CheckSynonyms{📝 Verificar sinónimos}
    CheckSynonyms --> |stock, inventario, productos| SynonymMatch[✅ Sinónimo detectado]
    CheckSynonyms --> |Otros términos| NoMatch[❌ No reconocido]
    
    SynonymMatch --> CheckLocation{📍 Verificar ubicación}
    CheckLocation --> |Las Condes| LocationMatch[✅ Ubicación válida]
    CheckLocation --> |Otra ubicación| InvalidLocation[❌ Ubicación inválida]
    
    LocationMatch --> DataLookup[🔍 Consultar datos CSV]
    DataLookup --> FormatResponse[📋 Formatear respuesta]
    
    InvalidLocation --> LimitationResponse[⚠️ Respuesta limitación]
    NoMatch --> LimitationResponse
    
    %% Flujo Turnos
    ShiftFlow --> CheckEmployee{👤 Verificar empleado}
    CheckEmployee --> |Nombre válido| EmployeeFound[✅ Empleado encontrado]
    CheckEmployee --> |Nombre inválido| EmployeeNotFound[❌ Empleado no encontrado]
    
    EmployeeFound --> CheckMonth{📅 Verificar mes}
    CheckMonth --> |Septiembre| ValidMonth[✅ Mes disponible]
    CheckMonth --> |Otro mes| InvalidMonth[❌ Mes no disponible]
    
    ValidMonth --> ShiftLookup[🔍 Consultar turnos CSV]
    ShiftLookup --> FormatShiftResponse[📋 Formatear respuesta turnos]
    
    EmployeeNotFound --> ShiftLimitation[⚠️ Empleado no encontrado]
    InvalidMonth --> ShiftLimitation
    
    %% Flujo Genérico
    GenericFlow --> GenericLimitation[⚠️ Consulta fuera de alcance]
    
    %% Convergencia
    FormatResponse --> ResponseJSON[📤 JSON Response]
    LimitationResponse --> ResponseJSON
    FormatShiftResponse --> ResponseJSON
    ShiftLimitation --> ResponseJSON
    GenericLimitation --> ResponseJSON
    
    ResponseJSON --> LogInteraction[📝 Log interacción]
    LogInteraction --> Return([🔄 Retornar respuesta])
    
    %% Estilos
    classDef apiNode fill:#FF6B6B,stroke:#CC5555,stroke-width:2px,color:#fff
    classDef nlpNode fill:#20B2AA,stroke:#177A7A,stroke-width:2px,color:#fff
    classDef dataNode fill:#50C878,stroke:#2E7D5F,stroke-width:2px,color:#fff
    classDef limitNode fill:#FFB347,stroke:#CC8A37,stroke-width:2px,color:#fff
    classDef decisionNode fill:#DA70D6,stroke:#B85AA6,stroke-width:2px,color:#fff
    
    class APICall,Return apiNode
    class NLPProcess,ParseQuery,SynonymMatch,LocationMatch,EmployeeFound,ValidMonth nlpNode
    class DataLookup,ShiftLookup,FormatResponse,FormatShiftResponse,ResponseJSON,LogInteraction dataNode
    class LimitationResponse,ShiftLimitation,GenericLimitation,InvalidLocation,InvalidMonth,NoMatch,EmployeeNotFound limitNode
    class DetectIntent,CheckSynonyms,CheckLocation,CheckEmployee,CheckMonth decisionNode
```

---

## 👥 Flujo CrewAI Multi-Agente (IL2.3)

```mermaid
flowchart TD
    CrewStart([🚀 Inicio CrewAI]) --> TaskReceive[📝 Recibir tarea]
    TaskReceive --> CrewCoordinator[👨‍💼 Coordinador de Crew]
    
    CrewCoordinator --> DefineRoles[🎭 Definir roles y responsabilidades]
    DefineRoles --> AssignTasks[📋 Asignar tareas específicas]
    
    AssignTasks --> ResearcherTask[🔍 Tarea: Investigación]
    AssignTasks --> AnalystTask[📊 Tarea: Análisis]
    AssignTasks --> WriterTask[📝 Tarea: Documentación]
    
    %% Agente Investigador
    ResearcherTask --> ResearchAgent[🔍 Agente Investigador]
    ResearchAgent --> DataGathering[📚 Recolección de datos]
    DataGathering --> SourceValidation[✅ Validación de fuentes]
    SourceValidation --> ResearchReport[📊 Reporte investigación]
    
    %% Agente Analista
    AnalystTask --> AnalystAgent[📊 Agente Analista]
    AnalystAgent --> DataAnalysis[🔬 Análisis de datos]
    DataAnalysis --> PatternRecognition[🔍 Reconocimiento patrones]
    PatternRecognition --> AnalysisReport[📈 Reporte análisis]
    
    %% Agente Documentador
    WriterTask --> WriterAgent[📝 Agente Documentador]
    WriterAgent --> ContentStructuring[📋 Estructuración contenido]
    ContentStructuring --> Documentation[📄 Documentación]
    Documentation --> QualityReview[✅ Revisión calidad]
    
    %% Colaboración entre agentes
    ResearchReport --> Collaboration[🤝 Espacio Colaboración]
    AnalysisReport --> Collaboration
    QualityReview --> Collaboration
    
    Collaboration --> KnowledgeSharing[🔄 Intercambio conocimiento]
    KnowledgeSharing --> ConflictResolution{⚖️ ¿Conflictos?}
    
    ConflictResolution --> |Sí| Mediation[🤝 Mediación]
    ConflictResolution --> |No| Integration[🔗 Integración resultados]
    
    Mediation --> Negotiation[💬 Negociación entre agentes]
    Negotiation --> Integration
    
    Integration --> QualityAssurance[🛡️ Aseguramiento calidad]
    QualityAssurance --> FinalValidation{✅ ¿Validación OK?}
    
    FinalValidation --> |No| Revision[🔄 Revisión y mejora]
    FinalValidation --> |Sí| CrewResult[🎯 Resultado final Crew]
    
    Revision --> KnowledgeSharing
    CrewResult --> DeliveryFormat[📦 Formato entrega]
    DeliveryFormat --> CrewEnd([✅ Entrega completada])
    
    %% Estilos
    classDef coordinator fill:#4A90E2,stroke:#2E5C8A,stroke-width:2px,color:#fff
    classDef researcher fill:#50C878,stroke:#2E7D5F,stroke-width:2px,color:#fff  
    classDef analyst fill:#FFB347,stroke:#CC8A37,stroke-width:2px,color:#fff
    classDef writer fill:#DA70D6,stroke:#B85AA6,stroke-width:2px,color:#fff
    classDef collaboration fill:#20B2AA,stroke:#177A7A,stroke-width:2px,color:#fff
    classDef quality fill:#FF6B6B,stroke:#CC5555,stroke-width:2px,color:#fff
    
    class CrewCoordinator,DefineRoles,AssignTasks coordinator
    class ResearcherTask,ResearchAgent,DataGathering,SourceValidation,ResearchReport researcher
    class AnalystTask,AnalystAgent,DataAnalysis,PatternRecognition,AnalysisReport analyst  
    class WriterTask,WriterAgent,ContentStructuring,Documentation,QualityReview writer
    class Collaboration,KnowledgeSharing,Mediation,Negotiation,Integration collaboration
    class QualityAssurance,FinalValidation,Revision,CrewResult,DeliveryFormat quality
```

---

## 📋 Flujo Planificación Adaptativa (IL2.3)

```mermaid
flowchart TD
    PlanStart([📋 Inicio Planificación]) --> ReceiveGoal[🎯 Recibir objetivo]
    ReceiveGoal --> ContextAssessment[📊 Evaluación contexto]
    
    ContextAssessment --> ResourceAnalysis[💾 Análisis recursos]
    ContextAssessment --> TimeAnalysis[⏰ Análisis temporal]
    ContextAssessment --> ConstraintAnalysis[🚧 Análisis restricciones]
    
    ResourceAnalysis --> ResourceAvailable{💾 ¿Recursos suficientes?}
    TimeAnalysis --> TimeAvailable{⏰ ¿Tiempo suficiente?}
    ConstraintAnalysis --> ConstraintManageable{🚧 ¿Restricciones manejables?}
    
    ResourceAvailable --> |Sí| PlanStrategy[📋 Estrategia planificación]
    ResourceAvailable --> |No| ResourceAdaptation[🔄 Adaptación recursos]
    
    TimeAvailable --> |Sí| PlanStrategy
    TimeAvailable --> |No| TimeAdaptation[🔄 Adaptación temporal]
    
    ConstraintManageable --> |Sí| PlanStrategy
    ConstraintManageable --> |No| ConstraintAdaptation[🔄 Adaptación restricciones]
    
    ResourceAdaptation --> AdaptationStrategy[🔄 Estrategia adaptativa]
    TimeAdaptation --> AdaptationStrategy
    ConstraintAdaptation --> AdaptationStrategy
    
    AdaptationStrategy --> ReassessContext[🔄 Re-evaluar contexto]
    ReassessContext --> PlanStrategy
    
    PlanStrategy --> CreatePlan[📋 Crear plan inicial]
    CreatePlan --> ValidatePlan[✅ Validar plan]
    
    ValidatePlan --> PlanValid{✅ ¿Plan válido?}
    PlanValid --> |No| AdjustPlan[🔧 Ajustar plan]
    PlanValid --> |Sí| ExecutePlan[⚡ Ejecutar plan]
    
    AdjustPlan --> ValidatePlan
    
    ExecutePlan --> MonitorExecution[👁️ Monitorear ejecución]
    MonitorExecution --> CheckProgress{📊 ¿Progreso OK?}
    
    CheckProgress --> |Sí| ContinueExecution[▶️ Continuar ejecución]
    CheckProgress --> |No| DetectIssue[⚠️ Detectar problema]
    
    DetectIssue --> IssueType{🔍 Tipo de problema?}
    IssueType --> |Recursos| ResourceIssue[💾 Problema recursos]
    IssueType --> |Tiempo| TimeIssue[⏰ Problema tiempo]
    IssueType --> |Calidad| QualityIssue[🎯 Problema calidad]
    
    ResourceIssue --> AdaptiveResponse[🔄 Respuesta adaptativa]
    TimeIssue --> AdaptiveResponse
    QualityIssue --> AdaptiveResponse
    
    AdaptiveResponse --> Replan[🔄 Re-planificar]
    Replan --> ExecutePlan
    
    ContinueExecution --> CheckCompletion{🏁 ¿Completado?}
    CheckCompletion --> |No| MonitorExecution
    CheckCompletion --> |Sí| EvaluateResults[📊 Evaluar resultados]
    
    EvaluateResults --> ResultsSatisfactory{✅ ¿Resultados OK?}
    ResultsSatisfactory --> |No| ImprovementPlan[🔧 Plan mejoras]
    ResultsSatisfactory --> |Sí| PlanComplete[🎉 Plan completado]
    
    ImprovementPlan --> Replan
    PlanComplete --> DocumentLessons[📝 Documentar lecciones]
    DocumentLessons --> PlanEnd([✅ Finalizar planificación])
    
    %% Estilos
    classDef planning fill:#4A90E2,stroke:#2E5C8A,stroke-width:2px,color:#fff
    classDef analysis fill:#50C878,stroke:#2E7D5F,stroke-width:2px,color:#fff
    classDef adaptation fill:#FFB347,stroke:#CC8A37,stroke-width:2px,color:#fff
    classDef execution fill:#DA70D6,stroke:#B85AA6,stroke-width:2px,color:#fff
    classDef monitoring fill:#20B2AA,stroke:#177A7A,stroke-width:2px,color:#fff
    classDef issue fill:#FF6B6B,stroke:#CC5555,stroke-width:2px,color:#fff
    
    class ReceiveGoal,PlanStrategy,CreatePlan,ValidatePlan,ExecutePlan,PlanComplete planning
    class ContextAssessment,ResourceAnalysis,TimeAnalysis,ConstraintAnalysis,ReassessContext analysis
    class ResourceAdaptation,TimeAdaptation,ConstraintAdaptation,AdaptationStrategy,AdaptiveResponse,Replan adaptation
    class ContinueExecution,CheckCompletion,EvaluateResults,ImprovementPlan execution
    class MonitorExecution,CheckProgress,DocumentLessons monitoring
    class DetectIssue,IssueType,ResourceIssue,TimeIssue,QualityIssue issue
```

---

## 🎨 Leyenda de Colores

- 🔵 **Azul**: Puntos de inicio/fin y coordinación
- 🟢 **Verde**: Procesos y operaciones principales  
- 🟡 **Amarillo**: Decisiones y análisis
- 🟣 **Morado**: Herramientas y utilidades
- 🔴 **Rojo**: APIs y interfaces externas
- 🟦 **Azul Claro**: Agentes y componentes inteligentes

---

## 📝 Notas Técnicas

1. **Memoria Adaptativa**: El sistema cambia automáticamente entre Buffer, Window y Summary según el número de mensajes.
2. **API Inteligente**: El demo_api.py incluye procesamiento NLP para detectar sinónimos y ubicaciones.
3. **CrewAI Colaborativo**: Los agentes trabajan en conjunto con mediación automática de conflictos.
4. **Planificación Dinámica**: Se adapta a cambios en recursos, tiempo y restricciones en tiempo real.
5. **Validación Automática**: Scripts de testing validan todos los componentes antes de la ejecución.