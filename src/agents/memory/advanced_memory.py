"""
Sistema de Memoria para Agentes
===============================
Implementa memoria conversacional de corto y largo plazo,
basado en los patrones aprendidos en IL2.2.
"""

import json
import os
from typing import Any, Dict, List, Optional
from datetime import datetime, timedelta
from langchain.memory import ConversationBufferMemory, ConversationBufferWindowMemory, ConversationSummaryMemory
from langchain.memory.chat_message_histories import FileChatMessageHistory
from langchain.schema import BaseMessage, HumanMessage, AIMessage
from langchain_openai import ChatOpenAI


class MemoriaAvanzada:
    """
    Sistema de memoria híbrido que combina diferentes estrategias:
    - Buffer completo para sesiones cortas
    - Ventana deslizante para conversaciones medianas  
    - Resumen para conversaciones largas
    """
    
    def __init__(self, session_id: str, max_buffer_size: int = 10, max_window_size: int = 5):
        self.session_id = session_id
        self.max_buffer_size = max_buffer_size
        self.max_window_size = max_window_size
        
        # Configurar LLM para resúmenes
        self.llm = ChatOpenAI(
            model="gpt-4o",
            temperature=0.1,
            openai_api_base=os.getenv("OPENAI_BASE_URL"),
            openai_api_key=os.getenv("OPENAI_API_KEY")
        )
        
        # Crear directorio de memoria
        self.memory_dir = os.path.join("memory", session_id)
        os.makedirs(self.memory_dir, exist_ok=True)
        
        # Inicializar sistemas de memoria
        self._setup_memory_systems()
        
        # Metadatos de sesión
        self.session_metadata = {
            "created_at": datetime.now().isoformat(),
            "last_accessed": datetime.now().isoformat(),
            "message_count": 0,
            "memory_strategy": "buffer"
        }
        
        self._load_session_metadata()
    
    def _setup_memory_systems(self):
        """Configura los diferentes sistemas de memoria."""
        
        # Historia de chat persistente
        history_file = os.path.join(self.memory_dir, "chat_history.json")
        self.chat_history = FileChatMessageHistory(history_file)
        
        # Buffer Memory - para conversaciones cortas
        self.buffer_memory = ConversationBufferMemory(
            chat_memory=self.chat_history,
            return_messages=True,
            memory_key="chat_history"
        )
        
        # Window Memory - para conversaciones medianas
        self.window_memory = ConversationBufferWindowMemory(
            chat_memory=self.chat_history,
            k=self.max_window_size,
            return_messages=True,
            memory_key="chat_history"
        )
        
        # Summary Memory - para conversaciones largas
        self.summary_memory = ConversationSummaryMemory(
            llm=self.llm,
            chat_memory=self.chat_history,
            return_messages=True,
            memory_key="chat_history"
        )
    
    def _load_session_metadata(self):
        """Carga metadatos de sesión existente."""
        metadata_file = os.path.join(self.memory_dir, "session_metadata.json")
        if os.path.exists(metadata_file):
            with open(metadata_file, 'r', encoding='utf-8') as f:
                saved_metadata = json.load(f)
                self.session_metadata.update(saved_metadata)
    
    def _save_session_metadata(self):
        """Guarda metadatos de sesión."""
        metadata_file = os.path.join(self.memory_dir, "session_metadata.json")
        self.session_metadata["last_accessed"] = datetime.now().isoformat()
        
        with open(metadata_file, 'w', encoding='utf-8') as f:
            json.dump(self.session_metadata, f, indent=2, ensure_ascii=False)
    
    def add_interaction(self, human_input: str, ai_response: str):
        """Añade una interacción a la memoria."""
        # Añadir a la historia de chat
        self.chat_history.add_user_message(human_input)
        self.chat_history.add_ai_message(ai_response)
        
        # Actualizar contador de mensajes
        self.session_metadata["message_count"] += 2
        
        # Determinar estrategia de memoria óptima
        self._update_memory_strategy()
        
        # Guardar metadatos actualizados
        self._save_session_metadata()
    
    def _update_memory_strategy(self):
        """Actualiza la estrategia de memoria según el número de mensajes."""
        message_count = self.session_metadata["message_count"]
        
        if message_count <= self.max_buffer_size * 2:
            self.session_metadata["memory_strategy"] = "buffer"
        elif message_count <= self.max_buffer_size * 4:
            self.session_metadata["memory_strategy"] = "window"  
        else:
            self.session_metadata["memory_strategy"] = "summary"
    
    def get_memory_context(self) -> Dict[str, Any]:
        """Obtiene el contexto de memoria apropiado según la estrategia actual."""
        strategy = self.session_metadata["memory_strategy"]
        
        if strategy == "buffer":
            return self.buffer_memory.load_memory_variables({})
        elif strategy == "window":
            return self.window_memory.load_memory_variables({})
        else:
            return self.summary_memory.load_memory_variables({})
    
    def get_memory_summary(self) -> str:
        """Obtiene un resumen de la memoria de la sesión."""
        context = self.get_memory_context()
        messages = context.get("chat_history", [])
        
        summary = f"""
## Resumen de Sesión: {self.session_id}

**Estrategia de memoria actual:** {self.session_metadata["memory_strategy"]}
**Mensajes totales:** {self.session_metadata["message_count"]}
**Creada:** {self.session_metadata["created_at"]}
**Último acceso:** {self.session_metadata["last_accessed"]}

**Contexto disponible:** {len(messages)} mensajes en memoria activa
"""
        
        if messages and len(messages) > 0:
            summary += f"\n**Última interacción:** {messages[-1].content[:100]}..."
        
        return summary
    
    def clear_memory(self):
        """Limpia toda la memoria de la sesión."""
        self.chat_history.clear()
        self.session_metadata["message_count"] = 0
        self.session_metadata["memory_strategy"] = "buffer"
        self._save_session_metadata()
    
    def export_conversation(self) -> Dict[str, Any]:
        """Exporta toda la conversación para backup o análisis."""
        messages = self.chat_history.messages
        
        return {
            "session_id": self.session_id,
            "metadata": self.session_metadata,
            "messages": [
                {
                    "type": type(msg).__name__,
                    "content": msg.content,
                    "timestamp": getattr(msg, 'timestamp', None)
                }
                for msg in messages
            ]
        }


class GestorMemoriaSesiones:
    """Gestor global de sesiones de memoria."""
    
    def __init__(self):
        self.sesiones_activas: Dict[str, MemoriaAvanzada] = {}
        self.base_dir = "memory"
        os.makedirs(self.base_dir, exist_ok=True)
    
    def get_session(self, session_id: str) -> MemoriaAvanzada:
        """Obtiene o crea una sesión de memoria."""
        if session_id not in self.sesiones_activas:
            self.sesiones_activas[session_id] = MemoriaAvanzada(session_id)
        
        return self.sesiones_activas[session_id]
    
    def list_sessions(self) -> List[str]:
        """Lista todas las sesiones disponibles."""
        if not os.path.exists(self.base_dir):
            return []
        
        return [d for d in os.listdir(self.base_dir) 
                if os.path.isdir(os.path.join(self.base_dir, d))]
    
    def delete_session(self, session_id: str):
        """Elimina una sesión de memoria."""
        import shutil
        
        # Remover de sesiones activas
        if session_id in self.sesiones_activas:
            del self.sesiones_activas[session_id]
        
        # Eliminar directorio de memoria
        session_dir = os.path.join(self.base_dir, session_id)
        if os.path.exists(session_dir):
            shutil.rmtree(session_dir)
    
    def cleanup_old_sessions(self, days_old: int = 30):
        """Limpia sesiones antigas basado en última fecha de acceso."""
        cutoff_date = datetime.now() - timedelta(days=days_old)
        
        for session_id in self.list_sessions():
            metadata_file = os.path.join(self.base_dir, session_id, "session_metadata.json")
            
            if os.path.exists(metadata_file):
                with open(metadata_file, 'r', encoding='utf-8') as f:
                    metadata = json.load(f)
                
                last_accessed = datetime.fromisoformat(metadata.get("last_accessed", ""))
                
                if last_accessed < cutoff_date:
                    print(f"Eliminando sesión antigua: {session_id}")
                    self.delete_session(session_id)


# Instancia global del gestor
memory_manager = GestorMemoriaSesiones()