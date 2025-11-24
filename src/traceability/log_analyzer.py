"""
IL3.2: Analizador de Logs
Sistema para analizar y extraer insights de logs
"""

import re
from typing import List, Dict, Any, Optional
from pathlib import Path
from datetime import datetime
from collections import Counter
from ..observability.logger_config import get_logger

logger = get_logger(__name__)

class LogAnalyzer:
    """
    Analizador de logs para trazabilidad
    Implementa IL3.2: Análisis de Trazabilidad y Logs
    """
    
    def __init__(self, log_file: str):
        self.log_file = Path(log_file)
        self.entries: List[Dict[str, Any]] = []
        
    def parse_log_line(self, line: str) -> Optional[Dict[str, Any]]:
        """Parsea una línea de log"""
        # Formato: timestamp | logger | level | function:line | message
        pattern = r'(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2},\d{3}) \| ([\w.]+) \| (\w+) \| ([\w]+):(\d+) \| (.+)'
        match = re.match(pattern, line)
        
        if match:
            timestamp_str, logger_name, level, function, line_no, message = match.groups()
            return {
                'timestamp': timestamp_str,
                'logger': logger_name,
                'level': level,
                'function': function,
                'line': int(line_no),
                'message': message
            }
        return None
    
    def load_logs(self):
        """Carga y parsea el archivo de logs"""
        if not self.log_file.exists():
            logger.warning(f"Archivo de log no encontrado: {self.log_file}")
            return
            
        with open(self.log_file, 'r', encoding='utf-8') as f:
            for line in f:
                entry = self.parse_log_line(line.strip())
                if entry:
                    self.entries.append(entry)
        
        logger.info(f"📄 Cargadas {len(self.entries)} entradas de log")
    
    def get_errors(self) -> List[Dict[str, Any]]:
        """Obtiene todos los errores del log"""
        return [e for e in self.entries if e['level'] == 'ERROR']
    
    def get_warnings(self) -> List[Dict[str, Any]]:
        """Obtiene todas las advertencias del log"""
        return [e for e in self.entries if e['level'] == 'WARNING']
    
    def get_by_level(self, level: str) -> List[Dict[str, Any]]:
        """Obtiene entradas por nivel"""
        return [e for e in self.entries if e['level'] == level]
    
    def get_by_function(self, function: str) -> List[Dict[str, Any]]:
        """Obtiene entradas por función"""
        return [e for e in self.entries if e['function'] == function]
    
    def get_level_distribution(self) -> Dict[str, int]:
        """Obtiene la distribución de niveles de log"""
        return dict(Counter(e['level'] for e in self.entries))
    
    def get_function_distribution(self) -> Dict[str, int]:
        """Obtiene la distribución de funciones que generan logs"""
        return dict(Counter(e['function'] for e in self.entries))
    
    def search_pattern(self, pattern: str) -> List[Dict[str, Any]]:
        """Busca un patrón en los mensajes"""
        regex = re.compile(pattern, re.IGNORECASE)
        return [e for e in self.entries if regex.search(e['message'])]
    
    def get_summary(self) -> Dict[str, Any]:
        """Genera un resumen del análisis de logs"""
        return {
            'total_entries': len(self.entries),
            'errors': len(self.get_errors()),
            'warnings': len(self.get_warnings()),
            'level_distribution': self.get_level_distribution(),
            'top_functions': dict(Counter(e['function'] for e in self.entries).most_common(10))
        }
    
    def print_summary(self):
        """Imprime un resumen del análisis"""
        summary = self.get_summary()
        
        print("\n" + "=" * 60)
        print("📊 RESUMEN DE ANÁLISIS DE LOGS")
        print("=" * 60)
        print(f"Total de entradas: {summary['total_entries']}")
        print(f"Errores: {summary['errors']}")
        print(f"Advertencias: {summary['warnings']}")
        print("\n📈 Distribución por nivel:")
        for level, count in summary['level_distribution'].items():
            print(f"  {level}: {count}")
        print("\n🔝 Top 10 funciones:")
        for func, count in summary['top_functions'].items():
            print(f"  {func}: {count}")
        print("=" * 60 + "\n")
