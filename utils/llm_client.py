"""
Client LLM pour les appels à Anthropic Claude
"""
import os
from pathlib import Path
from typing import Generator, Optional
import anthropic
from dotenv import load_dotenv

# Charger les variables d'environnement depuis le fichier .env du projet
env_path = Path(__file__).parent.parent / '.env'
load_dotenv(env_path)


class LLMClient:
    """Client pour interagir avec l'API Anthropic Claude."""
    
    def __init__(self, model: str = "claude-sonnet-4-20250514"):
        """
        Initialise le client LLM.
        
        Args:
            model: Modèle Anthropic à utiliser
        """
        self.api_key = os.getenv("ANTHROPIC_API_KEY")
        if not self.api_key:
            raise ValueError("ANTHROPIC_API_KEY non trouvée dans les variables d'environnement")
        
        self.client = anthropic.Anthropic(api_key=self.api_key)
        self.model = model
    
    def generate(
        self,
        prompt: str,
        system_prompt: str = "",
        max_tokens: int = 4096,
        temperature: float = 0.7
    ) -> str:
        """
        Génère une réponse complète.
        
        Args:
            prompt: Le prompt utilisateur
            system_prompt: Le prompt système
            max_tokens: Nombre maximum de tokens
            temperature: Température de génération
            
        Returns:
            La réponse générée
        """
        messages = [{"role": "user", "content": prompt}]
        
        response = self.client.messages.create(
            model=self.model,
            max_tokens=max_tokens,
            system=system_prompt if system_prompt else "",
            messages=messages,
            temperature=temperature
        )
        
        return response.content[0].text
    
    def generate_stream(
        self,
        prompt: str,
        system_prompt: str = "",
        max_tokens: int = 4096,
        temperature: float = 0.7
    ) -> Generator[str, None, None]:
        """
        Génère une réponse en streaming.
        
        Args:
            prompt: Le prompt utilisateur
            system_prompt: Le prompt système
            max_tokens: Nombre maximum de tokens
            temperature: Température de génération
            
        Yields:
            Morceaux de texte au fur et à mesure
        """
        messages = [{"role": "user", "content": prompt}]
        
        with self.client.messages.stream(
            model=self.model,
            max_tokens=max_tokens,
            system=system_prompt if system_prompt else "",
            messages=messages,
            temperature=temperature
        ) as stream:
            for text in stream.text_stream:
                yield text
    
    def chat(
        self,
        messages: list,
        system_prompt: str = "",
        max_tokens: int = 4096,
        temperature: float = 0.7
    ) -> str:
        """
        Conversation multi-tours.
        
        Args:
            messages: Liste de messages [{"role": "user/assistant", "content": "..."}]
            system_prompt: Le prompt système
            max_tokens: Nombre maximum de tokens
            temperature: Température de génération
            
        Returns:
            La réponse générée
        """
        response = self.client.messages.create(
            model=self.model,
            max_tokens=max_tokens,
            system=system_prompt if system_prompt else "",
            messages=messages,
            temperature=temperature
        )
        
        return response.content[0].text
    
    def chat_stream(
        self,
        messages: list,
        system_prompt: str = "",
        max_tokens: int = 4096,
        temperature: float = 0.7
    ) -> Generator[str, None, None]:
        """
        Conversation multi-tours en streaming.
        
        Args:
            messages: Liste de messages
            system_prompt: Le prompt système
            max_tokens: Nombre maximum de tokens
            temperature: Température de génération
            
        Yields:
            Morceaux de texte au fur et à mesure
        """
        with self.client.messages.stream(
            model=self.model,
            max_tokens=max_tokens,
            system=system_prompt if system_prompt else "",
            messages=messages,
            temperature=temperature
        ) as stream:
            for text in stream.text_stream:
                yield text

