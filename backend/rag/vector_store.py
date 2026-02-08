"""
Vector Store - ChromaDB integration for regulatory document retrieval
"""
from typing import List, Optional
from dataclasses import dataclass
import chromadb
from chromadb.config import Settings as ChromaSettings
from langchain_openai import OpenAIEmbeddings
import json
import os

from config import Settings


@dataclass
class RetrievedDocument:
    """A document retrieved from the vector store."""
    content: str
    reference: str
    article: Optional[str] = None
    section: Optional[str] = None
    score: float = 0.0


class VectorStore:
    """ChromaDB vector store for regulatory documents."""
    
    def __init__(self, settings: Settings):
        self.settings = settings
        self.client = None
        self.collection = None
        self.embeddings = None
        
    async def initialize(self):
        """Initialize the vector store and load documents."""
        # Initialize ChromaDB
        self.client = chromadb.Client(ChromaSettings(
            anonymized_telemetry=False,
            is_persistent=True,
            persist_directory=self.settings.chroma_persist_directory
        ))
        
        # Initialize OpenAI embeddings
        if self.settings.openai_api_key:
            self.embeddings = OpenAIEmbeddings(
                model=self.settings.openai_embedding_model,
                openai_api_key=self.settings.openai_api_key
            )
        
        # Get or create collection
        self.collection = self.client.get_or_create_collection(
            name="corep_regulations",
            metadata={"hnsw:space": "cosine"}
        )
        
        # Load sample data if collection is empty
        if self.collection.count() == 0:
            await self._load_sample_data()
    
    async def _load_sample_data(self):
        """Load sample regulatory documents into the vector store."""
        # Load PRA Rulebook samples
        data_dir = os.path.join(os.path.dirname(__file__), "..", "data")
        
        try:
            with open(os.path.join(data_dir, "pra_rulebook_sample.json"), "r") as f:
                pra_docs = json.load(f)
            
            with open(os.path.join(data_dir, "corep_instructions_c01.json"), "r") as f:
                corep_docs = json.load(f)
            
            all_docs = pra_docs + corep_docs
            
            if self.embeddings and all_docs:
                # Generate embeddings
                texts = [doc["content"] for doc in all_docs]
                embeddings = await self.embeddings.aembed_documents(texts)
                
                # Add to collection
                self.collection.add(
                    ids=[f"doc_{i}" for i in range(len(all_docs))],
                    embeddings=embeddings,
                    documents=texts,
                    metadatas=[{
                        "reference": doc.get("reference", ""),
                        "article": doc.get("article", ""),
                        "section": doc.get("section", "")
                    } for doc in all_docs]
                )
        except FileNotFoundError:
            # Sample data not yet created - will be populated later
            pass
    
    async def retrieve(
        self,
        query: str,
        scenario: Optional[str] = None,
        k: int = 5
    ) -> List[RetrievedDocument]:
        """Retrieve relevant documents for a query."""
        if not self.embeddings or not self.collection:
            return []
        
        # Combine query and scenario for better retrieval
        search_text = query
        if scenario:
            search_text = f"{query}\n\nScenario: {scenario}"
        
        # Generate query embedding
        query_embedding = await self.embeddings.aembed_query(search_text)
        
        # Search collection
        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=k,
            include=["documents", "metadatas", "distances"]
        )
        
        # Convert to RetrievedDocument objects
        docs = []
        if results and results["documents"]:
            for i, (doc, metadata, distance) in enumerate(zip(
                results["documents"][0],
                results["metadatas"][0],
                results["distances"][0]
            )):
                docs.append(RetrievedDocument(
                    content=doc,
                    reference=metadata.get("reference", f"Document {i+1}"),
                    article=metadata.get("article"),
                    section=metadata.get("section"),
                    score=1 - distance  # Convert distance to similarity score
                ))
        
        return docs
    
    async def add_document(self, content: str, reference: str, metadata: dict = None):
        """Add a document to the vector store."""
        if not self.embeddings or not self.collection:
            return
        
        embedding = await self.embeddings.aembed_documents([content])
        doc_id = f"doc_{self.collection.count()}"
        
        self.collection.add(
            ids=[doc_id],
            embeddings=embedding,
            documents=[content],
            metadatas=[{
                "reference": reference,
                **(metadata or {})
            }]
        )
