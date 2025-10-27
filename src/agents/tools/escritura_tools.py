"""
Herramientas de Escritura y Análisis para Agentes
================================================
Implementa herramientas especializadas para generar reportes,
análisis de datos y documentación organizacional.
"""

import os
import json
import pandas as pd
from datetime import datetime
from typing import Any, Dict, List
from langchain.tools import BaseTool
from pydantic import BaseModel, Field


class ReportInput(BaseModel):
    """Input schema para generar reportes."""
    titulo: str = Field(description="Título del reporte")
    contenido: str = Field(description="Contenido principal del reporte")
    tipo: str = Field(default="general", description="Tipo de reporte: general, inventario, turnos, analisis")
    incluir_fecha: bool = Field(default=True, description="Incluir fecha y hora en el reporte")


class DataAnalysisInput(BaseModel):
    """Input schema para análisis de datos."""
    dataset: str = Field(description="Nombre del dataset a analizar: inventory_las_condes o turnos_septiembre")
    tipo_analisis: str = Field(description="Tipo de análisis: resumen, estadisticas, tendencias")


class EscrituraReporteTool(BaseTool):
    """Herramienta para generar reportes estructurados."""
    
    name: str = "escritura_reporte"
    description: str = """
    Genera reportes estructurados y documentos organizacionales.
    Útil para crear informes de inventario, análisis de turnos,
    reportes ejecutivos, y documentación técnica.
    """
    args_schema = ReportInput
    
    def _run(self, titulo: str, contenido: str, tipo: str = "general", incluir_fecha: bool = True) -> str:
        """Genera un reporte estructurado."""
        try:
            # Preparar header del reporte
            header = f"# {titulo}\n\n"
            
            if incluir_fecha:
                fecha_actual = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                header += f"**Fecha de generación:** {fecha_actual}\n"
                header += f"**Tipo de reporte:** {tipo.title()}\n\n"
            
            # Estructurar contenido según el tipo
            if tipo == "inventario":
                reporte = self._formato_inventario(header, contenido)
            elif tipo == "turnos":
                reporte = self._formato_turnos(header, contenido)
            elif tipo == "analisis":
                reporte = self._formato_analisis(header, contenido)
            else:
                reporte = header + contenido
            
            # Guardar reporte en archivo
            filename = f"reporte_{tipo}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
            filepath = os.path.join("reports", filename)
            
            # Crear directorio si no existe
            os.makedirs("reports", exist_ok=True)
            
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(reporte)
            
            return f"Reporte generado exitosamente:\n{reporte}\n\n**Archivo guardado en:** {filepath}"
            
        except Exception as e:
            return f"Error generando reporte: {str(e)}"
    
    def _formato_inventario(self, header: str, contenido: str) -> str:
        """Formatea reporte de inventario."""
        return f"""{header}
## Resumen Ejecutivo
{contenido}

## Análisis de Inventario
- **Estado general:** Se requiere análisis detallado
- **Recomendaciones:** Basadas en los datos disponibles
- **Próximos pasos:** Definir según hallazgos

## Conclusiones
{contenido}

---
*Generado automáticamente por el Sistema de Agentes CleanPro*
"""
    
    def _formato_turnos(self, header: str, contenido: str) -> str:
        """Formatea reporte de turnos."""
        return f"""{header}
## Análisis de Turnos

### Resumen
{contenido}

### Distribución de Turnos
- **Datos analizados:** Septiembre 2024
- **Observaciones:** Según patrones identificados

### Recomendaciones
- Optimizar distribución según demanda
- Considerar ajustes por eficiencia

---
*Reporte generado por Sistema de Gestión CleanPro*
"""
    
    def _formato_analisis(self, header: str, contenido: str) -> str:
        """Formatea reporte de análisis."""
        return f"""{header}
## Análisis de Datos

### Metodología
{contenido}

### Hallazgos Principales
- **Tendencias identificadas**
- **Patrones relevantes**
- **Anomalías detectadas**

### Recomendaciones Estratégicas
- Acciones inmediatas
- Mejoras a mediano plazo
- Monitoreo continuo

---
*Análisis realizado por IA CleanPro*
"""
    
    async def _arun(self, titulo: str, contenido: str, tipo: str = "general", incluir_fecha: bool = True) -> str:
        return self._run(titulo, contenido, tipo, incluir_fecha)


class AnalisisDatosTool(BaseTool):
    """Herramienta para análisis automatizado de datasets."""
    
    name: str = "analisis_datos"
    description: str = """
    Realiza análisis automatizado de los datasets disponibles.
    Puede analizar datos de inventario y turnos, generar estadísticas,
    identificar tendencias y crear resúmenes ejecutivos.
    """
    args_schema = DataAnalysisInput
    
    def _run(self, dataset: str, tipo_analisis: str) -> str:
        """Ejecuta análisis de datos."""
        try:
            # Mapear datasets disponibles
            datasets_disponibles = {
                "inventory_las_condes": "data/inventory_las_condes.csv",
                "turnos_septiembre": "data/turnos_septiembre.csv"
            }
            
            if dataset not in datasets_disponibles:
                return f"Dataset '{dataset}' no disponible. Datasets disponibles: {list(datasets_disponibles.keys())}"
            
            filepath = datasets_disponibles[dataset]
            
            if not os.path.exists(filepath):
                return f"Archivo de datos no encontrado: {filepath}"
            
            # Cargar y analizar datos
            df = pd.read_csv(filepath)
            
            if tipo_analisis == "resumen":
                return self._generar_resumen(df, dataset)
            elif tipo_analisis == "estadisticas":
                return self._generar_estadisticas(df, dataset)
            elif tipo_analisis == "tendencias":
                return self._analizar_tendencias(df, dataset)
            else:
                return self._analisis_general(df, dataset)
                
        except Exception as e:
            return f"Error en análisis de datos: {str(e)}"
    
    def _generar_resumen(self, df: pd.DataFrame, dataset: str) -> str:
        """Genera resumen del dataset."""
        resumen = f"""
## Resumen del Dataset: {dataset}

**Dimensiones:** {df.shape[0]} filas × {df.shape[1]} columnas

**Columnas disponibles:**
{chr(10).join([f"- {col}" for col in df.columns])}

**Primeras 5 filas:**
{df.head().to_string()}

**Información general:**
- Valores faltantes: {df.isnull().sum().sum()}
- Tipos de datos: {dict(df.dtypes)}
"""
        return resumen
    
    def _generar_estadisticas(self, df: pd.DataFrame, dataset: str) -> str:
        """Genera estadísticas descriptivas."""
        stats = f"""
## Estadísticas Descriptivas: {dataset}

**Estadísticas numéricas:**
{df.describe().to_string()}

**Valores únicos por columna:**
{chr(10).join([f"- {col}: {df[col].nunique()} valores únicos" for col in df.columns])}
"""
        return stats
    
    def _analizar_tendencias(self, df: pd.DataFrame, dataset: str) -> str:
        """Analiza tendencias en los datos."""
        tendencias = f"""
## Análisis de Tendencias: {dataset}

**Patrones identificados:**
- Dataset contiene {df.shape[0]} registros
- {df.shape[1]} variables analizadas
- Distribución de datos por columna disponible

**Recomendaciones:**
- Realizar análisis más profundo con visualizaciones
- Considerar análisis temporal si hay fechas
- Evaluar correlaciones entre variables
"""
        return tendencias
    
    def _analisis_general(self, df: pd.DataFrame, dataset: str) -> str:
        """Análisis general del dataset."""
        return f"""
## Análisis General: {dataset}

**Estructura de datos:**
- Filas: {df.shape[0]}
- Columnas: {df.shape[1]}
- Memoria utilizada: {df.memory_usage(deep=True).sum()} bytes

**Calidad de datos:**
- Completitud: {((df.shape[0] * df.shape[1] - df.isnull().sum().sum()) / (df.shape[0] * df.shape[1]) * 100):.1f}%
- Valores únicos totales: {sum([df[col].nunique() for col in df.columns])}
"""
    
    async def _arun(self, dataset: str, tipo_analisis: str) -> str:
        return self._run(dataset, tipo_analisis)


def get_escritura_tools() -> List[BaseTool]:
    """Factory function para crear herramientas de escritura y análisis."""
    return [
        EscrituraReporteTool(),
        AnalisisDatosTool()
    ]