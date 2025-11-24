"""
IL3.3: Validador de Entradas
Sistema para validar y sanitizar entradas de usuario
"""

import re
from enum import Enum
from typing import Dict, List, Tuple, Any
from ..observability.logger_config import get_logger

logger = get_logger(__name__)

class SecurityLevel(Enum):
    """Niveles de seguridad para validación"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

class InputValidator:
    """
    Validador de entradas para seguridad del sistema
    Implementa IL3.3: Seguridad y Ética
    """
    
    # Patrones peligrosos que deben ser bloqueados
    DANGEROUS_PATTERNS = [
        r'<script[^>]*>.*?</script>',  # XSS
        r'javascript:',  # JavaScript injection
        r'on\w+\s*=',  # Event handlers
        r'eval\s*\(',  # eval() calls
        r'exec\s*\(',  # exec() calls
        r'__import__',  # Python imports
        r'open\s*\(',  # File operations
        r'os\.',  # OS operations
        r'subprocess',  # Subprocess execution
        r'\.\./|\.\.\\',  # Path traversal
        r';\s*rm\s+',  # Shell commands
        r';\s*del\s+',  # Delete commands
        r'DROP\s+TABLE',  # SQL injection
        r'DELETE\s+FROM',  # SQL injection
        r'UPDATE\s+.*SET',  # SQL injection
    ]
    
    # Palabras clave sensibles
    SENSITIVE_KEYWORDS = [
        'password', 'passwd', 'pwd', 'secret', 'token', 'api_key',
        'private_key', 'credential', 'auth', 'session_id'
    ]
    
    def __init__(self, security_level: SecurityLevel = SecurityLevel.MEDIUM):
        self.security_level = security_level
        self.blocked_patterns = [re.compile(pattern, re.IGNORECASE) for pattern in self.DANGEROUS_PATTERNS]
    
    def validate(self, text: str) -> Tuple[bool, str]:
        """
        Valida una entrada de texto
        
        Returns:
            (is_valid, message): Tupla con el resultado y mensaje
        """
        if not text:
            return False, "Entrada vacía"
        
        # Verificar longitud máxima
        if len(text) > 10000:
            logger.warning("🚨 Entrada demasiado larga rechazada")
            return False, "Entrada demasiado larga (máximo 10000 caracteres)"
        
        # Verificar patrones peligrosos
        for pattern in self.blocked_patterns:
            if pattern.search(text):
                logger.warning(f"🚨 Patrón peligroso detectado: {pattern.pattern}")
                return False, f"Patrón de seguridad detectado y bloqueado"
        
        # Verificar palabras sensibles (solo advertencia en nivel CRITICAL)
        if self.security_level == SecurityLevel.CRITICAL:
            for keyword in self.SENSITIVE_KEYWORDS:
                if keyword.lower() in text.lower():
                    logger.warning(f"⚠️  Palabra sensible detectada: {keyword}")
                    return False, f"Información sensible detectada en la entrada"
        
        return True, "Validación exitosa"
    
    def sanitize(self, text: str) -> str:
        """Sanitiza una entrada removiendo caracteres peligrosos"""
        # Remover caracteres de control
        sanitized = re.sub(r'[\x00-\x1f\x7f-\x9f]', '', text)
        
        # Escapar HTML
        sanitized = sanitized.replace('&', '&amp;')
        sanitized = sanitized.replace('<', '&lt;')
        sanitized = sanitized.replace('>', '&gt;')
        sanitized = sanitized.replace('"', '&quot;')
        sanitized = sanitized.replace("'", '&#x27;')
        
        return sanitized
    
    def validate_and_sanitize(self, text: str) -> Tuple[bool, str, str]:
        """
        Valida y sanitiza una entrada
        
        Returns:
            (is_valid, message, sanitized_text)
        """
        is_valid, message = self.validate(text)
        if not is_valid:
            return False, message, ""
        
        sanitized = self.sanitize(text)
        return True, message, sanitized
    
    def validate_sql_query(self, query: str) -> bool:
        """Valida que una consulta SQL no sea maliciosa"""
        dangerous_sql = [
            'DROP', 'DELETE', 'TRUNCATE', 'ALTER', 'CREATE',
            'INSERT', 'UPDATE', 'GRANT', 'REVOKE'
        ]
        
        query_upper = query.upper()
        for keyword in dangerous_sql:
            if keyword in query_upper:
                logger.warning(f"🚨 Palabra SQL peligrosa detectada: {keyword}")
                return False
        
        return True
    
    def safe_eval(self, expression: str) -> Tuple[bool, Any]:
        """
        Evalúa expresiones matemáticas de forma segura
        Implementa IL3.3: Seguridad
        """
        # Solo permitir caracteres seguros
        allowed = set('0123456789+-*/(). ')
        if not set(expression) <= allowed:
            logger.warning("🚨 Expresión con caracteres no permitidos")
            return False, "Expresión no permitida"
        
        try:
            result = eval(expression, {"__builtins__": {}}, {})
            return True, result
        except Exception as e:
            logger.error(f"❌ Error en evaluación segura: {str(e)}")
            return False, f"Error en la expresión: {str(e)}"

# Instancia global del validador
global_validator = InputValidator(SecurityLevel.MEDIUM)
