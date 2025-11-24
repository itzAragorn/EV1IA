"""
IL3.2: Rastreador de Conversaciones
Sistema para rastrear el flujo de conversaciones del agente
"""

from typing import Dict, List, Optional
from dataclasses import dataclass, field
from datetime import datetime
import json
from pathlib import Path
from ..observability.logger_config import get_logger

logger = get_logger(__name__)

@dataclass
class ConversationTurn:
    """Representa un turno de conversación"""
    turn_id: int
    timestamp: float
    user_message: str
    agent_response: str
    tools_used: List[str] = field(default_factory=list)
    duration: float = 0.0
    metadata: Dict = field(default_factory=dict)
    
    def to_dict(self) -> dict:
        return {
            'turn_id': self.turn_id,
            'timestamp': self.timestamp,
            'datetime': datetime.fromtimestamp(self.timestamp).isoformat(),
            'user_message': self.user_message,
            'agent_response': self.agent_response,
            'tools_used': self.tools_used,
            'duration': self.duration,
            'metadata': self.metadata
        }

@dataclass
class Conversation:
    """Representa una conversación completa"""
    conversation_id: str
    start_time: float
    end_time: Optional[float] = None
    turns: List[ConversationTurn] = field(default_factory=list)
    metadata: Dict = field(default_factory=dict)
    
    @property
    def total_duration(self) -> Optional[float]:
        if self.end_time:
            return self.end_time - self.start_time
        return None
    
    @property
    def turn_count(self) -> int:
        return len(self.turns)
    
    def to_dict(self) -> dict:
        return {
            'conversation_id': self.conversation_id,
            'start_time': self.start_time,
            'start_datetime': datetime.fromtimestamp(self.start_time).isoformat(),
            'end_time': self.end_time,
            'end_datetime': datetime.fromtimestamp(self.end_time).isoformat() if self.end_time else None,
            'total_duration': self.total_duration,
            'turn_count': self.turn_count,
            'turns': [turn.to_dict() for turn in self.turns],
            'metadata': self.metadata
        }

class ConversationTracker:
    """
    Rastreador de conversaciones para análisis de interacciones
    Implementa IL3.2: Análisis de Trazabilidad
    """
    
    def __init__(self):
        self.conversations: Dict[str, Conversation] = {}
        
    def start_conversation(self, conversation_id: str, **metadata) -> Conversation:
        """Inicia el rastreo de una nueva conversación"""
        import time
        
        conversation = Conversation(
            conversation_id=conversation_id,
            start_time=time.time(),
            metadata=metadata
        )
        self.conversations[conversation_id] = conversation
        
        logger.info(f"💬 Iniciando rastreo de conversación: {conversation_id}")
        return conversation
    
    def add_turn(
        self,
        conversation_id: str,
        user_message: str,
        agent_response: str,
        tools_used: List[str] = None,
        duration: float = 0.0,
        **metadata
    ):
        """Agrega un turno a una conversación"""
        import time
        
        if conversation_id not in self.conversations:
            self.start_conversation(conversation_id)
        
        conversation = self.conversations[conversation_id]
        turn_id = len(conversation.turns) + 1
        
        turn = ConversationTurn(
            turn_id=turn_id,
            timestamp=time.time(),
            user_message=user_message,
            agent_response=agent_response,
            tools_used=tools_used or [],
            duration=duration,
            metadata=metadata
        )
        
        conversation.turns.append(turn)
        
        logger.debug(f"  📝 Turno {turn_id} agregado a conversación {conversation_id}")
    
    def end_conversation(self, conversation_id: str):
        """Finaliza el rastreo de una conversación"""
        import time
        
        if conversation_id in self.conversations:
            conversation = self.conversations[conversation_id]
            conversation.end_time = time.time()
            
            logger.info(
                f"✅ Conversación finalizada: {conversation_id} - "
                f"{conversation.turn_count} turnos, {conversation.total_duration:.2f}s"
            )
    
    def get_conversation(self, conversation_id: str) -> Optional[Conversation]:
        """Obtiene una conversación por ID"""
        return self.conversations.get(conversation_id)
    
    def get_all_conversations(self) -> List[Conversation]:
        """Obtiene todas las conversaciones"""
        return list(self.conversations.values())
    
    def get_summary(self) -> Dict:
        """Genera un resumen de todas las conversaciones"""
        all_convs = self.get_all_conversations()
        
        total_turns = sum(c.turn_count for c in all_convs)
        completed_durations = [c.total_duration for c in all_convs if c.total_duration]
        
        # Herramientas más usadas
        all_tools = []
        for conv in all_convs:
            for turn in conv.turns:
                all_tools.extend(turn.tools_used)
        
        from collections import Counter
        tool_usage = dict(Counter(all_tools).most_common(10))
        
        return {
            'total_conversations': len(all_convs),
            'total_turns': total_turns,
            'avg_turns_per_conversation': total_turns / len(all_convs) if all_convs else 0,
            'avg_conversation_duration': sum(completed_durations) / len(completed_durations) if completed_durations else 0,
            'most_used_tools': tool_usage
        }
    
    def save_conversations(self, filepath: str):
        """Guarda las conversaciones a un archivo JSON"""
        path = Path(filepath)
        path.parent.mkdir(parents=True, exist_ok=True)
        
        data = {
            'timestamp': datetime.now().isoformat(),
            'summary': self.get_summary(),
            'conversations': [c.to_dict() for c in self.get_all_conversations()]
        }
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        logger.info(f"💾 Conversaciones guardadas en: {filepath}")

# Instancia global del rastreador
global_conversation_tracker = ConversationTracker()
