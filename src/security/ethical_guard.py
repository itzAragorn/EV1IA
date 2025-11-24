"""
IL3.3: Guardián Ético
Sistema para asegurar comportamiento ético del agente
"""

import re
from typing import List, Dict, Optional
from dataclasses import dataclass
from ..observability.logger_config import get_logger

logger = get_logger(__name__)

@dataclass
class EthicalViolation:
    """Representa una violación ética detectada"""
    category: str
    severity: str  # low, medium, high, critical
    description: str
    matched_pattern: str

class EthicalGuard:
    """
    Guardián ético para el agente de IA
    Implementa IL3.3: Ética en Agentes de IA
    """
    
    # Categorías de contenido inapropiado
    UNETHICAL_PATTERNS = {
        'violencia': [
            r'hackear',
            r'atacar',
            r'destruir',
            r'da[ñn]ar',
            r'matar',
            r'herir',
            r'golpear'
        ],
        'ilegal': [
            r'drogas?\s+ilegales',
            r'robar',
            r'hurtar',
            r'estafar',
            r'falsificar',
            r'piratear',
            r'copyright\s+violation'
        ],
        'discriminacion': [
            r'racista',
            r'sexista',
            r'homof[oó]bico',
            r'xenof[oó]bico',
            r'discriminar',
            r'prejuicio'
        ],
        'privacidad': [
            r'datos\s+personales',
            r'información\s+privada',
            r'violar\s+privacidad',
            r'doxxing',
            r'espiar'
        ],
        'manipulacion': [
            r'manipular',
            r'enga[ñn]ar',
            r'mentir',
            r'fraude',
            r'estafa',
            r'phishing'
        ]
    }
    
    # Respuestas éticas predefinidas
    ETHICAL_RESPONSES = {
        'violencia': "No puedo proporcionar información que promueva la violencia o el daño a otros.",
        'ilegal': "No puedo ayudar con actividades ilegales. Le sugiero consultar con un profesional legal.",
        'discriminacion': "No apoyo ni promuevo contenido discriminatorio de ningún tipo.",
        'privacidad': "No puedo ayudar con actividades que violen la privacidad de las personas.",
        'manipulacion': "No puedo ayudar con prácticas engañosas o manipuladoras.",
        'general': "Esta solicitud va en contra de mis principios éticos y no puedo ayudar con ella."
    }
    
    def __init__(self):
        self.compiled_patterns = {
            category: [re.compile(pattern, re.IGNORECASE) for pattern in patterns]
            for category, patterns in self.UNETHICAL_PATTERNS.items()
        }
        self.violations_log: List[EthicalViolation] = []
    
    def check_input(self, text: str) -> Optional[EthicalViolation]:
        """
        Verifica si una entrada contiene contenido no ético
        
        Returns:
            EthicalViolation si se detecta, None si es ético
        """
        for category, patterns in self.compiled_patterns.items():
            for pattern in patterns:
                match = pattern.search(text)
                if match:
                    violation = EthicalViolation(
                        category=category,
                        severity='high',
                        description=f"Contenido de categoría '{category}' detectado",
                        matched_pattern=match.group(0)
                    )
                    
                    self.violations_log.append(violation)
                    logger.warning(
                        f"⚠️  Violación ética detectada: {category} - '{match.group(0)}'",
                        extra={'category': category, 'pattern': pattern.pattern}
                    )
                    
                    return violation
        
        return None
    
    def get_ethical_response(self, violation: EthicalViolation) -> str:
        """Obtiene una respuesta ética apropiada para una violación"""
        return self.ETHICAL_RESPONSES.get(violation.category, self.ETHICAL_RESPONSES['general'])
    
    def validate_and_respond(self, text: str) -> tuple[bool, Optional[str]]:
        """
        Valida entrada y retorna respuesta ética si es necesario
        
        Returns:
            (is_ethical, ethical_response): Tupla con validación y respuesta
        """
        violation = self.check_input(text)
        
        if violation:
            response = self.get_ethical_response(violation)
            logger.info(f"🛡️  Respuesta ética aplicada para categoría: {violation.category}")
            return False, response
        
        return True, None
    
    def get_violations_summary(self) -> Dict:
        """Obtiene un resumen de las violaciones detectadas"""
        from collections import Counter
        
        categories = [v.category for v in self.violations_log]
        
        return {
            'total_violations': len(self.violations_log),
            'by_category': dict(Counter(categories)),
            'recent_violations': [
                {
                    'category': v.category,
                    'severity': v.severity,
                    'description': v.description
                }
                for v in self.violations_log[-10:]  # Últimas 10
            ]
        }
    
    def is_appropriate_question(self, question: str) -> bool:
        """Verifica si una pregunta es apropiada"""
        violation = self.check_input(question)
        return violation is None
    
    def filter_response(self, response: str) -> str:
        """Filtra una respuesta del agente para asegurar contenido ético"""
        # Verificar si la respuesta contiene contenido inapropiado
        violation = self.check_input(response)
        
        if violation:
            logger.warning("⚠️  Respuesta del agente contiene contenido inapropiado, filtrando...")
            return "Lo siento, no puedo proporcionar esa información de manera apropiada."
        
        return response

# Instancia global del guardián ético
global_ethical_guard = EthicalGuard()
