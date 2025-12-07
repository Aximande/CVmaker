"""
Client Supabase pour la persistance des données
"""
import os
from datetime import datetime
from typing import List, Dict, Optional
from pathlib import Path
from dotenv import load_dotenv

# Charger les variables d'environnement
env_path = Path(__file__).parent.parent / '.env'
load_dotenv(env_path)

# Configuration Supabase
SUPABASE_URL = os.getenv("SUPABASE_URL", "https://rsknfjcaazondtymiyrv.supabase.co")
SUPABASE_KEY = os.getenv("SUPABASE_KEY", "")


class SupabaseClient:
    """Client pour interagir avec Supabase."""
    
    def __init__(self):
        """Initialise le client Supabase."""
        try:
            from supabase import create_client, Client
            
            if not SUPABASE_KEY:
                raise ValueError("SUPABASE_KEY non trouvée dans les variables d'environnement")
            
            self.client: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
            self.enabled = True
        except ImportError:
            print("⚠️ Module supabase non installé. Utilisation du stockage local.")
            self.client = None
            self.enabled = False
        except Exception as e:
            print(f"⚠️ Erreur Supabase: {e}. Utilisation du stockage local.")
            self.client = None
            self.enabled = False
    
    # =========================================================================
    # CANDIDATURES
    # =========================================================================
    
    def save_candidature(
        self,
        titre_poste: str,
        entreprise: str,
        offre_texte: str = None,
        cv_adapte: str = None,
        lettre_motivation: str = None,
        preparation_entretien: str = None,
        analyse_compatibilite: str = None,
        notes: str = None
    ) -> Optional[Dict]:
        """
        Sauvegarde une candidature dans Supabase.
        
        Returns:
            Dict avec les données insérées ou None en cas d'erreur
        """
        if not self.enabled:
            return None
        
        try:
            data = {
                "titre_poste": titre_poste,
                "entreprise": entreprise,
                "offre_texte": offre_texte,
                "cv_adapte": cv_adapte,
                "lettre_motivation": lettre_motivation,
                "preparation_entretien": preparation_entretien,
                "analyse_compatibilite": analyse_compatibilite,
                "notes": notes,
                "statut": "en_cours"
            }
            
            result = self.client.table("candidatures").insert(data).execute()
            return result.data[0] if result.data else None
            
        except Exception as e:
            print(f"Erreur sauvegarde candidature: {e}")
            return None
    
    def get_candidatures(self, limit: int = 50) -> List[Dict]:
        """
        Récupère les candidatures depuis Supabase.
        
        Args:
            limit: Nombre max de candidatures à récupérer
            
        Returns:
            Liste des candidatures
        """
        if not self.enabled:
            return []
        
        try:
            result = self.client.table("candidatures") \
                .select("*") \
                .order("created_at", desc=True) \
                .limit(limit) \
                .execute()
            return result.data or []
            
        except Exception as e:
            print(f"Erreur récupération candidatures: {e}")
            return []
    
    def update_candidature_statut(self, candidature_id: str, statut: str) -> bool:
        """
        Met à jour le statut d'une candidature.
        
        Args:
            candidature_id: ID de la candidature
            statut: Nouveau statut ('en_cours', 'envoyee', 'entretien', 'refusee', 'acceptee')
            
        Returns:
            True si succès, False sinon
        """
        if not self.enabled:
            return False
        
        try:
            self.client.table("candidatures") \
                .update({"statut": statut, "updated_at": datetime.now().isoformat()}) \
                .eq("id", candidature_id) \
                .execute()
            return True
            
        except Exception as e:
            print(f"Erreur mise à jour statut: {e}")
            return False
    
    def delete_candidature(self, candidature_id: str) -> bool:
        """Supprime une candidature."""
        if not self.enabled:
            return False
        
        try:
            self.client.table("candidatures") \
                .delete() \
                .eq("id", candidature_id) \
                .execute()
            return True
            
        except Exception as e:
            print(f"Erreur suppression candidature: {e}")
            return False
    
    # =========================================================================
    # CHAT
    # =========================================================================
    
    def save_chat_message(self, role: str, content: str, session_id: str = "default") -> bool:
        """
        Sauvegarde un message de chat.
        
        Args:
            role: 'user' ou 'assistant'
            content: Contenu du message
            session_id: ID de session (par défaut 'default')
            
        Returns:
            True si succès
        """
        if not self.enabled:
            return False
        
        try:
            self.client.table("chat_messages").insert({
                "role": role,
                "content": content,
                "session_id": session_id
            }).execute()
            return True
            
        except Exception as e:
            print(f"Erreur sauvegarde message: {e}")
            return False
    
    def get_chat_messages(self, session_id: str = "default", limit: int = 100) -> List[Dict]:
        """
        Récupère les messages de chat.
        
        Args:
            session_id: ID de session
            limit: Nombre max de messages
            
        Returns:
            Liste des messages
        """
        if not self.enabled:
            return []
        
        try:
            result = self.client.table("chat_messages") \
                .select("*") \
                .eq("session_id", session_id) \
                .order("created_at", desc=False) \
                .limit(limit) \
                .execute()
            return result.data or []
            
        except Exception as e:
            print(f"Erreur récupération messages: {e}")
            return []
    
    def clear_chat_messages(self, session_id: str = "default") -> bool:
        """Efface tous les messages d'une session."""
        if not self.enabled:
            return False
        
        try:
            self.client.table("chat_messages") \
                .delete() \
                .eq("session_id", session_id) \
                .execute()
            return True
            
        except Exception as e:
            print(f"Erreur suppression messages: {e}")
            return False
    
    # =========================================================================
    # DOCUMENTS CHAT
    # =========================================================================
    
    def save_chat_document(self, filename: str, content: str, session_id: str = "default") -> bool:
        """Sauvegarde un document uploadé dans le chat."""
        if not self.enabled:
            return False
        
        try:
            # Vérifier si le document existe déjà
            existing = self.client.table("chat_documents") \
                .select("id") \
                .eq("session_id", session_id) \
                .eq("filename", filename) \
                .execute()
            
            if existing.data:
                # Mettre à jour le contenu existant
                self.client.table("chat_documents") \
                    .update({"content": content}) \
                    .eq("session_id", session_id) \
                    .eq("filename", filename) \
                    .execute()
            else:
                # Insérer nouveau document
                self.client.table("chat_documents").insert({
                    "filename": filename,
                    "content": content,
                    "session_id": session_id
                }).execute()
            return True
            
        except Exception as e:
            print(f"Erreur sauvegarde document: {e}")
            return False
    
    def get_chat_documents(self, session_id: str = "default") -> List[Dict]:
        """Récupère les documents d'une session de chat."""
        if not self.enabled:
            return []
        
        try:
            result = self.client.table("chat_documents") \
                .select("*") \
                .eq("session_id", session_id) \
                .order("created_at", desc=False) \
                .execute()
            return result.data or []
            
        except Exception as e:
            print(f"Erreur récupération documents: {e}")
            return []
    
    def delete_chat_document(self, doc_id: int) -> bool:
        """Supprime un document du chat."""
        if not self.enabled:
            return False
        
        try:
            self.client.table("chat_documents") \
                .delete() \
                .eq("id", doc_id) \
                .execute()
            return True
            
        except Exception as e:
            print(f"Erreur suppression document: {e}")
            return False
    
    def clear_chat_documents(self, session_id: str = "default") -> bool:
        """Efface tous les documents d'une session."""
        if not self.enabled:
            return False
        
        try:
            self.client.table("chat_documents") \
                .delete() \
                .eq("session_id", session_id) \
                .execute()
            return True
            
        except Exception as e:
            print(f"Erreur suppression documents: {e}")
            return False
    
    # =========================================================================
    # LINKEDIN POSTS
    # =========================================================================
    
    def save_linkedin_post(
        self,
        sujet: str,
        contenu: str,
        tone: str = None,
        publie: bool = False
    ) -> Optional[Dict]:
        """Sauvegarde un post LinkedIn généré."""
        if not self.enabled:
            return None
        
        try:
            data = {
                "sujet": sujet,
                "contenu": contenu,
                "tone": tone,
                "publie": publie
            }
            
            result = self.client.table("linkedin_posts").insert(data).execute()
            return result.data[0] if result.data else None
            
        except Exception as e:
            print(f"Erreur sauvegarde post LinkedIn: {e}")
            return None
    
    def get_linkedin_posts(self, limit: int = 20) -> List[Dict]:
        """Récupère les posts LinkedIn sauvegardés."""
        if not self.enabled:
            return []
        
        try:
            result = self.client.table("linkedin_posts") \
                .select("*") \
                .order("created_at", desc=True) \
                .limit(limit) \
                .execute()
            return result.data or []
            
        except Exception as e:
            print(f"Erreur récupération posts LinkedIn: {e}")
            return []
    
    def mark_post_published(self, post_id: int) -> bool:
        """Marque un post comme publié."""
        if not self.enabled:
            return False
        
        try:
            self.client.table("linkedin_posts") \
                .update({"publie": True, "date_publication": datetime.now().isoformat()}) \
                .eq("id", post_id) \
                .execute()
            return True
            
        except Exception as e:
            print(f"Erreur mise à jour post: {e}")
            return False
    
    # =========================================================================
    # CANDIDATURES EVENTS (TRACKING)
    # =========================================================================
    
    def add_candidature_event(
        self,
        candidature_id: str,
        type_event: str,
        description: str = None,
        date_event: str = None,
        rappel_date: str = None
    ) -> Optional[Dict]:
        """
        Ajoute un événement à une candidature.
        
        Args:
            candidature_id: UUID de la candidature
            type_event: Type d'événement (envoi, relance, entretien_tel, etc.)
            description: Description optionnelle
            date_event: Date de l'événement (défaut: maintenant)
            rappel_date: Date de rappel optionnelle
        """
        if not self.enabled:
            return None
        
        try:
            data = {
                "candidature_id": candidature_id,
                "type_event": type_event,
                "description": description
            }
            
            if date_event:
                data["date_event"] = date_event
            if rappel_date:
                data["rappel_date"] = rappel_date
            
            result = self.client.table("candidatures_events").insert(data).execute()
            return result.data[0] if result.data else None
            
        except Exception as e:
            print(f"Erreur ajout événement: {e}")
            return None
    
    def get_candidature_events(self, candidature_id: str) -> List[Dict]:
        """Récupère tous les événements d'une candidature."""
        if not self.enabled:
            return []
        
        try:
            result = self.client.table("candidatures_events") \
                .select("*") \
                .eq("candidature_id", candidature_id) \
                .order("date_event", desc=True) \
                .execute()
            return result.data or []
            
        except Exception as e:
            print(f"Erreur récupération événements: {e}")
            return []
    
    def get_upcoming_reminders(self, days: int = 7) -> List[Dict]:
        """
        Récupère les rappels à venir dans les X prochains jours.
        
        Args:
            days: Nombre de jours à regarder
            
        Returns:
            Liste des événements avec rappel
        """
        if not self.enabled:
            return []
        
        try:
            from datetime import timedelta
            
            now = datetime.now()
            end_date = now + timedelta(days=days)
            
            result = self.client.table("candidatures_events") \
                .select("*, candidatures(titre_poste, entreprise)") \
                .gte("rappel_date", now.isoformat()) \
                .lte("rappel_date", end_date.isoformat()) \
                .order("rappel_date", desc=False) \
                .execute()
            return result.data or []
            
        except Exception as e:
            print(f"Erreur récupération rappels: {e}")
            return []
    
    # =========================================================================
    # EMAIL TEMPLATES
    # =========================================================================
    
    def get_email_templates(self) -> List[Dict]:
        """Récupère tous les templates d'emails."""
        if not self.enabled:
            return []
        
        try:
            result = self.client.table("email_templates") \
                .select("*") \
                .order("type_template") \
                .execute()
            return result.data or []
            
        except Exception as e:
            print(f"Erreur récupération templates: {e}")
            return []
    
    def get_email_template_by_type(self, type_template: str) -> Optional[Dict]:
        """Récupère un template par son type."""
        if not self.enabled:
            return None
        
        try:
            result = self.client.table("email_templates") \
                .select("*") \
                .eq("type_template", type_template) \
                .limit(1) \
                .execute()
            return result.data[0] if result.data else None
            
        except Exception as e:
            print(f"Erreur récupération template: {e}")
            return None
    
    def save_custom_template(
        self,
        nom: str,
        sujet: str,
        contenu: str,
        variables: List[str] = None
    ) -> Optional[Dict]:
        """Sauvegarde un template personnalisé."""
        if not self.enabled:
            return None
        
        try:
            data = {
                "nom": nom,
                "type_template": "personnalise",
                "sujet": sujet,
                "contenu": contenu,
                "variables": variables or []
            }
            
            result = self.client.table("email_templates").insert(data).execute()
            return result.data[0] if result.data else None
            
        except Exception as e:
            print(f"Erreur sauvegarde template: {e}")
            return None
    
    # =========================================================================
    # CV PERSONNALISÉS
    # =========================================================================
    
    def save_cv_personnalise(
        self,
        titre_offre: str,
        entreprise: str,
        offre_texte: str,
        customizations: Dict,
        html_content: str,
        chat_history: List[Dict] = None,
        candidature_id: int = None
    ) -> Optional[Dict]:
        """
        Sauvegarde un CV personnalisé dans Supabase.
        
        Args:
            titre_offre: Titre du poste
            entreprise: Nom de l'entreprise
            offre_texte: Texte de l'offre d'emploi
            customizations: Dict des personnalisations (accroche, qualites, competences)
            html_content: HTML du CV généré
            chat_history: Historique des modifications
            candidature_id: ID de la candidature liée (optionnel)
        """
        if not self.enabled:
            return None
        
        try:
            import json
            
            data = {
                "titre_offre": titre_offre,
                "entreprise": entreprise,
                "offre_texte": offre_texte[:5000] if offre_texte else None,  # Limiter la taille
                "customizations": json.dumps(customizations) if customizations else None,
                "html_content": html_content,
                "chat_history": json.dumps(chat_history) if chat_history else None,
                "candidature_id": candidature_id,
                "version": 1
            }
            
            result = self.client.table("cv_personnalises").insert(data).execute()
            return result.data[0] if result.data else None
            
        except Exception as e:
            print(f"Erreur sauvegarde CV personnalisé: {e}")
            return None
    
    def get_cv_personnalises(self, limit: int = 20) -> List[Dict]:
        """Récupère les CV personnalisés récents."""
        if not self.enabled:
            return []
        
        try:
            result = self.client.table("cv_personnalises") \
                .select("*") \
                .order("created_at", desc=True) \
                .limit(limit) \
                .execute()
            return result.data or []
            
        except Exception as e:
            print(f"Erreur récupération CV personnalisés: {e}")
            return []
    
    def get_cv_personnalise(self, cv_id: int) -> Optional[Dict]:
        """Récupère un CV personnalisé par son ID."""
        if not self.enabled:
            return None
        
        try:
            result = self.client.table("cv_personnalises") \
                .select("*") \
                .eq("id", cv_id) \
                .limit(1) \
                .execute()
            return result.data[0] if result.data else None
            
        except Exception as e:
            print(f"Erreur récupération CV: {e}")
            return None
    
    def update_cv_personnalise(
        self,
        cv_id: int,
        customizations: Dict = None,
        html_content: str = None,
        chat_history: List[Dict] = None
    ) -> bool:
        """Met à jour un CV personnalisé existant."""
        if not self.enabled:
            return False
        
        try:
            import json
            
            data = {}
            if customizations is not None:
                data["customizations"] = json.dumps(customizations)
            if html_content is not None:
                data["html_content"] = html_content
            if chat_history is not None:
                data["chat_history"] = json.dumps(chat_history)
            
            # Incrémenter la version
            current = self.get_cv_personnalise(cv_id)
            if current:
                data["version"] = current.get("version", 1) + 1
            
            self.client.table("cv_personnalises") \
                .update(data) \
                .eq("id", cv_id) \
                .execute()
            return True
            
        except Exception as e:
            print(f"Erreur mise à jour CV: {e}")
            return False
    
    def delete_cv_personnalise(self, cv_id: int) -> bool:
        """Supprime un CV personnalisé."""
        if not self.enabled:
            return False
        
        try:
            self.client.table("cv_personnalises") \
                .delete() \
                .eq("id", cv_id) \
                .execute()
            return True
            
        except Exception as e:
            print(f"Erreur suppression CV: {e}")
            return False
    
    def get_cvs_for_candidature(self, candidature_id: str) -> List[Dict]:
        """Récupère les CV personnalisés liés à une candidature."""
        if not self.enabled:
            return []
        
        try:
            result = self.client.table("cv_personnalises") \
                .select("id, titre_offre, version, created_at") \
                .eq("candidature_id", candidature_id) \
                .order("created_at", desc=True) \
                .execute()
            return result.data or []
            
        except Exception as e:
            print(f"Erreur récupération CV candidature: {e}")
            return []
    
    # =========================================================================
    # STATISTIQUES
    # =========================================================================
    
    def get_candidatures_stats(self) -> Dict:
        """Récupère les statistiques des candidatures."""
        if not self.enabled:
            return {}
        
        try:
            # Récupérer toutes les candidatures
            result = self.client.table("candidatures") \
                .select("statut") \
                .execute()
            
            candidatures = result.data or []
            
            stats = {
                "total": len(candidatures),
                "en_cours": sum(1 for c in candidatures if c.get("statut") == "en_cours"),
                "envoyees": sum(1 for c in candidatures if c.get("statut") == "envoyee"),
                "entretiens": sum(1 for c in candidatures if c.get("statut") == "entretien"),
                "refusees": sum(1 for c in candidatures if c.get("statut") == "refusee"),
                "acceptees": sum(1 for c in candidatures if c.get("statut") == "acceptee")
            }
            
            return stats
            
        except Exception as e:
            print(f"Erreur statistiques: {e}")
            return {}


# Instance globale (singleton)
_supabase_client = None


def get_supabase_client() -> SupabaseClient:
    """Retourne l'instance unique du client Supabase."""
    global _supabase_client
    if _supabase_client is None:
        _supabase_client = SupabaseClient()
    return _supabase_client

