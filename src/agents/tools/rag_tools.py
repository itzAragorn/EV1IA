"""
Herramientas de Consulta RAG para Agentes
========================================
Implementa herramientas especializadas para consultar información usando RAG,
integradas con el sistema de vectorstore existente.
"""

import os
from typing import Any, Dict
from langchain.tools import BaseTool
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from pydantic import BaseModel, Field


class RAGQueryInput(BaseModel):
    """Input schema para la herramienta de consulta RAG."""
    query: str = Field(description="Pregunta o consulta para buscar en la base de conocimientos")
    max_results: int = Field(default=4, description="Número máximo de resultados a recuperar")


class RAGConsultaTool(BaseTool):
    """Herramienta para realizar consultas RAG sobre la base de conocimientos."""
    
    name: str = "rag_consulta"
    description: str = """
    Consulta la base de conocimientos de CleanPro usando RAG.
    Útil para buscar información sobre inventario, turnos, políticas de empresa,
    procedimientos de limpieza, o cualquier información almacenada en la base de datos.
    """
    args_schema = RAGQueryInput
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._setup_retriever()
    
    def _setup_retriever(self):
        """Configura el retriever RAG."""
        try:
            # Configurar embeddings
            self.embeddings = OpenAIEmbeddings(
                openai_api_base=os.getenv("OPENAI_EMBEDDINGS_URL"),
                openai_api_key=os.getenv("OPENAI_API_KEY"),
                model="text-embedding-3-small"
            )
            
            # Configurar vectorstore
            chroma_dir = "./.chroma_db"
            self.vectorstore = Chroma(
                persist_directory=chroma_dir, 
                embedding_function=self.embeddings
            )
            
        except Exception as e:
            print(f"Error configurando RAG retriever: {e}")
            self.vectorstore = None
    
    def _run(self, query: str, max_results: int = 4) -> str:
        """Ejecuta la consulta RAG."""
        if not self.vectorstore:
            return "Error: No se pudo acceder a la base de conocimientos."
        
        try:
            # Realizar búsqueda de similitud
            docs = self.vectorstore.similarity_search(query, k=max_results)
            
            if not docs:
                return f"No se encontró información relevante para: '{query}'"
            
            # Compilar resultados
            resultados = []
            for i, doc in enumerate(docs, 1):
                contenido = doc.page_content[:500]  # Limitar contenido
                metadata = doc.metadata
                source = metadata.get('source', 'Fuente desconocida')
                
                resultados.append(f"Resultado {i}:\nFuente: {source}\nContenido: {contenido}\n")
            
            return "\n".join(resultados)
            
        except Exception as e:
            return f"Error realizando consulta RAG: {str(e)}"
    
    async def _arun(self, query: str, max_results: int = 4) -> str:
        """Versión asíncrona de la herramienta."""
        return self._run(query, max_results)


def get_rag_consulta_tool() -> RAGConsultaTool:
    """Factory function para crear la herramienta de consulta RAG."""
    return RAGConsultaTool()