"""
🎯 Assistant Recherche d'Emploi - Valérie Jasica
Application Streamlit pour optimiser la recherche d'emploi
"""

import streamlit as st
import json
import os
import re
from datetime import datetime
from pathlib import Path

# Configuration de la page - DOIT être en premier
st.set_page_config(
    page_title="Assistant Emploi - Valérie",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Imports locaux
from config.valerie_profile import PROFIL_VALERIE, CV_TEXTE_COMPLET
from prompts.system_prompts import (
    SYSTEM_PROMPT_GENERAL,
    SYSTEM_PROMPT_CV,
    SYSTEM_PROMPT_LETTRE,
    SYSTEM_PROMPT_ENTRETIEN,
    SYSTEM_PROMPT_ANALYSE,
    SYSTEM_PROMPT_COACH,
    SYSTEM_PROMPT_LINKEDIN
)
from prompts.task_prompts import (
    PROMPT_ANALYSE_OFFRE,
    PROMPT_OPTIMISER_CV,
    PROMPT_LETTRE_MOTIVATION,
    PROMPT_PREPARATION_ENTRETIEN,
    PROMPT_ANALYSE_COMPATIBILITE,
    PROMPT_COACH_CONVERSATION,
    PROMPT_LINKEDIN_POST,
    PROMPT_ADAPTER_CV_TEMPLATE,
    PROMPT_MODIFIER_CV_COMPLET
)
from utils.llm_client import LLMClient
from utils.pdf_parser import extract_text_from_pdf
from utils.supabase_client import get_supabase_client

# ============================================================================
# STYLES CSS PERSONNALISÉS
# ============================================================================

def load_custom_css():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');
    
    /* Variables globales */
    :root {
        --primary: #2563eb;
        --primary-dark: #1d4ed8;
        --secondary: #7c3aed;
        --accent: #06b6d4;
        --success: #10b981;
        --warning: #f59e0b;
        --error: #ef4444;
        --bg-dark: #0f172a;
        --bg-card: #1e293b;
        --text-primary: #f1f5f9;
        --text-secondary: #94a3b8;
        --border: #334155;
    }
    
    /* Reset et base */
    .stApp {
        background: linear-gradient(135deg, #0f172a 0%, #1e1b4b 50%, #0f172a 100%);
        font-family: 'DM Sans', sans-serif;
    }
    
    /* Header personnalisé */
    .main-header {
        background: linear-gradient(90deg, rgba(37, 99, 235, 0.1) 0%, rgba(124, 58, 237, 0.1) 100%);
        border: 1px solid rgba(124, 58, 237, 0.3);
        border-radius: 16px;
        padding: 2rem;
        margin-bottom: 2rem;
        backdrop-filter: blur(10px);
    }
    
    .main-header h1 {
        background: linear-gradient(90deg, #60a5fa, #a78bfa, #06b6d4);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 2.5rem;
        font-weight: 700;
        margin: 0;
    }
    
    .main-header p {
        color: #94a3b8;
        font-size: 1.1rem;
        margin: 0.5rem 0 0 0;
    }
    
    /* Cards de fonctionnalités */
    .feature-card {
        background: rgba(30, 41, 59, 0.8);
        border: 1px solid rgba(71, 85, 105, 0.5);
        border-radius: 16px;
        padding: 1.5rem;
        margin: 0.5rem 0;
        transition: all 0.3s ease;
        backdrop-filter: blur(10px);
    }
    
    .feature-card:hover {
        border-color: rgba(124, 58, 237, 0.5);
        transform: translateY(-2px);
        box-shadow: 0 10px 40px rgba(124, 58, 237, 0.2);
    }
    
    .feature-card h3 {
        color: #f1f5f9;
        font-size: 1.2rem;
        margin: 0 0 0.5rem 0;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    
    .feature-card p {
        color: #94a3b8;
        font-size: 0.9rem;
        margin: 0;
    }
    
    /* Badges de statut */
    .status-badge {
        display: inline-flex;
        align-items: center;
        padding: 0.25rem 0.75rem;
        border-radius: 9999px;
        font-size: 0.75rem;
        font-weight: 600;
    }
    
    .status-excellent {
        background: rgba(16, 185, 129, 0.2);
        color: #34d399;
        border: 1px solid rgba(16, 185, 129, 0.3);
    }
    
    .status-good {
        background: rgba(6, 182, 212, 0.2);
        color: #22d3ee;
        border: 1px solid rgba(6, 182, 212, 0.3);
    }
    
    .status-warning {
        background: rgba(245, 158, 11, 0.2);
        color: #fbbf24;
        border: 1px solid rgba(245, 158, 11, 0.3);
    }
    
    .status-alert {
        background: rgba(239, 68, 68, 0.2);
        color: #f87171;
        border: 1px solid rgba(239, 68, 68, 0.3);
    }
    
    /* Score de compatibilité */
    .score-container {
        background: rgba(30, 41, 59, 0.9);
        border: 1px solid rgba(71, 85, 105, 0.5);
        border-radius: 16px;
        padding: 2rem;
        text-align: center;
        margin: 1rem 0;
    }
    
    .score-number {
        font-size: 4rem;
        font-weight: 700;
        background: linear-gradient(90deg, #60a5fa, #a78bfa);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    
    .score-label {
        color: #94a3b8;
        font-size: 1rem;
        margin-top: 0.5rem;
    }
    
    /* Sidebar personnalisée */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1e293b 0%, #0f172a 100%);
        border-right: 1px solid rgba(71, 85, 105, 0.3);
    }
    
    [data-testid="stSidebar"] .stMarkdown h1,
    [data-testid="stSidebar"] .stMarkdown h2,
    [data-testid="stSidebar"] .stMarkdown h3 {
        color: #f1f5f9;
    }
    
    /* Boutons personnalisés */
    .stButton > button {
        background: linear-gradient(90deg, #2563eb, #7c3aed) !important;
        color: #ffffff !important;
        border: none !important;
        border-radius: 12px;
        padding: 0.75rem 1.5rem;
        font-weight: 600;
        font-family: 'DM Sans', sans-serif;
        transition: all 0.3s ease;
        text-shadow: 0 1px 2px rgba(0, 0, 0, 0.2);
    }
    
    .stButton > button:hover {
        background: linear-gradient(90deg, #1d4ed8, #6d28d9) !important;
        color: #ffffff !important;
        box-shadow: 0 10px 40px rgba(124, 58, 237, 0.3);
        transform: translateY(-2px);
    }
    
    .stButton > button:active,
    .stButton > button:focus {
        color: #ffffff !important;
    }
    
    /* Text areas */
    .stTextArea > div > div > textarea {
        background: rgba(30, 41, 59, 0.8);
        border: 1px solid rgba(71, 85, 105, 0.5);
        border-radius: 12px;
        color: #f1f5f9;
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.9rem;
    }
    
    .stTextArea > div > div > textarea:focus {
        border-color: #7c3aed;
        box-shadow: 0 0 0 3px rgba(124, 58, 237, 0.2);
    }
    
    /* Tabs personnalisés */
    .stTabs [data-baseweb="tab-list"] {
        background: rgba(30, 41, 59, 0.5);
        border-radius: 12px;
        padding: 0.5rem;
        gap: 0.5rem;
    }
    
    .stTabs [data-baseweb="tab"] {
        background: transparent;
        color: #e2e8f0 !important;
        border-radius: 8px;
        padding: 0.75rem 1.5rem;
        font-weight: 500;
    }
    
    .stTabs [data-baseweb="tab"]:hover {
        background: rgba(124, 58, 237, 0.2);
        color: #ffffff !important;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(90deg, #2563eb, #7c3aed) !important;
        color: #ffffff !important;
        font-weight: 600;
    }
    
    /* Labels et textes généraux */
    .stMarkdown, .stMarkdown p, .stMarkdown li {
        color: #e2e8f0;
    }
    
    .stMarkdown h1, .stMarkdown h2, .stMarkdown h3, .stMarkdown h4 {
        color: #f8fafc !important;
    }
    
    /* Labels des inputs */
    .stTextArea label, .stTextInput label, .stSelectbox label, .stFileUploader label {
        color: #e2e8f0 !important;
        font-weight: 500;
    }
    
    /* Placeholder text */
    .stTextArea textarea::placeholder, .stTextInput input::placeholder {
        color: #94a3b8 !important;
    }
    
    /* Download button */
    .stDownloadButton > button {
        background: linear-gradient(90deg, #10b981, #06b6d4) !important;
        color: #ffffff !important;
        border: none !important;
        font-weight: 600;
    }
    
    .stDownloadButton > button:hover {
        background: linear-gradient(90deg, #059669, #0891b2) !important;
        color: #ffffff !important;
    }
    
    /* Expanders */
    .streamlit-expanderHeader {
        background: rgba(30, 41, 59, 0.8);
        border: 1px solid rgba(71, 85, 105, 0.5);
        border-radius: 12px;
        color: #f1f5f9;
        font-weight: 600;
    }
    
    .streamlit-expanderContent {
        background: rgba(30, 41, 59, 0.5);
        border: 1px solid rgba(71, 85, 105, 0.3);
        border-top: none;
        border-radius: 0 0 12px 12px;
    }
    
    /* Résultats générés */
    .generated-content {
        background: rgba(30, 41, 59, 0.9);
        border: 1px solid rgba(16, 185, 129, 0.3);
        border-radius: 16px;
        padding: 2rem;
        margin: 1rem 0;
    }
    
    .generated-content h2 {
        color: #34d399;
        font-size: 1.3rem;
        margin-bottom: 1rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    
    /* Profil card */
    .profile-card {
        background: linear-gradient(135deg, rgba(37, 99, 235, 0.1) 0%, rgba(124, 58, 237, 0.1) 100%);
        border: 1px solid rgba(124, 58, 237, 0.3);
        border-radius: 16px;
        padding: 1.5rem;
        margin: 1rem 0;
    }
    
    .profile-name {
        font-size: 1.5rem;
        font-weight: 700;
        color: #f1f5f9;
        margin: 0;
    }
    
    .profile-title {
        color: #a78bfa;
        font-size: 1rem;
        margin: 0.25rem 0 0 0;
    }
    
    /* Metrics personnalisés */
    [data-testid="stMetricValue"] {
        color: #60a5fa;
        font-size: 2rem;
        font-weight: 700;
    }
    
    [data-testid="stMetricLabel"] {
        color: #94a3b8;
    }
    
    /* Chat messages */
    .chat-message {
        padding: 1rem 1.5rem;
        border-radius: 16px;
        margin: 0.5rem 0;
        max-width: 85%;
    }
    
    .chat-user {
        background: linear-gradient(90deg, #2563eb, #7c3aed);
        color: white;
        margin-left: auto;
    }
    
    .chat-assistant {
        background: rgba(30, 41, 59, 0.9);
        border: 1px solid rgba(71, 85, 105, 0.5);
        color: #f1f5f9;
    }
    
    /* Divider */
    hr {
        border: none;
        height: 1px;
        background: linear-gradient(90deg, transparent, rgba(124, 58, 237, 0.5), transparent);
        margin: 2rem 0;
    }
    
    /* Animation de loading */
    @keyframes pulse {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.5; }
    }
    
    .loading {
        animation: pulse 2s ease-in-out infinite;
    }
    
    /* Scrollbar personnalisée */
    ::-webkit-scrollbar {
        width: 8px;
        height: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: #1e293b;
        border-radius: 4px;
    }
    
    ::-webkit-scrollbar-thumb {
        background: #475569;
        border-radius: 4px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: #64748b;
    }
    
    /* File uploader */
    [data-testid="stFileUploader"] {
        background: rgba(30, 41, 59, 0.5);
        border: 2px dashed rgba(124, 58, 237, 0.3);
        border-radius: 16px;
        padding: 1rem;
    }
    
    /* Select box */
    .stSelectbox > div > div {
        background: rgba(30, 41, 59, 0.8);
        border: 1px solid rgba(71, 85, 105, 0.5);
        border-radius: 12px;
        color: #f1f5f9;
    }
    
    /* Info boxes */
    .stAlert {
        background: rgba(30, 41, 59, 0.9);
        border-radius: 12px;
    }
    
    /* Profile photo styling */
    [data-testid="stSidebar"] img {
        border-radius: 50%;
        border: 3px solid rgba(124, 58, 237, 0.5);
        box-shadow: 0 4px 20px rgba(124, 58, 237, 0.3);
        transition: all 0.3s ease;
    }
    
    [data-testid="stSidebar"] img:hover {
        border-color: #a78bfa;
        transform: scale(1.05);
        box-shadow: 0 8px 30px rgba(124, 58, 237, 0.4);
    }
    
    /* Banner image styling */
    .main img:first-of-type {
        border-radius: 16px;
        margin-bottom: 1rem;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
    }
    
    /* Motivation quote */
    .motivation-quote {
        background: linear-gradient(135deg, rgba(124, 58, 237, 0.1) 0%, rgba(6, 182, 212, 0.1) 100%);
        border-left: 4px solid #a78bfa;
        padding: 1rem 1.5rem;
        border-radius: 0 12px 12px 0;
        margin: 1rem 0;
        font-style: italic;
        color: #e2e8f0;
    }
    </style>
    """, unsafe_allow_html=True)


# ============================================================================
# INITIALISATION DES ÉTATS
# ============================================================================

def init_session_state():
    """Initialise les états de session Streamlit."""
    defaults = {
        'current_page': 'accueil',
        'offre_actuelle': '',
        'cv_adapte': '',
        'lettre_motivation': '',
        'preparation_entretien': '',
        'analyse_compatibilite': '',
        'chat_messages': [],
        'historique_candidatures': [],
        'llm_client': None
    }
    
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value
    
    # Initialiser le client LLM
    if st.session_state.llm_client is None:
        try:
            st.session_state.llm_client = LLMClient()
        except ValueError as e:
            st.error(f"⚠️ Erreur de configuration : {e}")
            st.stop()


def get_llm():
    """Récupère le client LLM."""
    return st.session_state.llm_client


# ============================================================================
# FONCTIONS UTILITAIRES
# ============================================================================

def save_candidature(titre_poste: str, entreprise: str, data: dict):
    """Sauvegarde une candidature (Supabase + local fallback)."""
    # Essayer Supabase d'abord
    supabase = get_supabase_client()
    if supabase.enabled:
        result = supabase.save_candidature(
            titre_poste=titre_poste,
            entreprise=entreprise,
            offre_texte=data.get('offre'),
            cv_adapte=data.get('cv_adapte'),
            lettre_motivation=data.get('lettre_motivation'),
            preparation_entretien=data.get('preparation_entretien'),
            analyse_compatibilite=data.get('analyse'),
            notes=data.get('notes')
        )
        if result:
            return result
    
    # Fallback local
    candidature = {
        'id': datetime.now().strftime('%Y%m%d_%H%M%S'),
        'created_at': datetime.now().isoformat(),
        'titre_poste': titre_poste,
        'entreprise': entreprise,
        **data
    }
    st.session_state.historique_candidatures.append(candidature)
    
    # Sauvegarder dans un fichier
    history_dir = Path('data/historique')
    history_dir.mkdir(parents=True, exist_ok=True)
    
    file_path = history_dir / f"{candidature['id']}.json"
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(candidature, f, ensure_ascii=False, indent=2)
    
    return candidature
    
    return candidature


def load_historique():
    """Charge l'historique des candidatures (Supabase + local fallback)."""
    # Essayer Supabase d'abord
    supabase = get_supabase_client()
    if supabase.enabled:
        candidatures = supabase.get_candidatures(limit=50)
        if candidatures:
            # Convertir le format pour compatibilité
            for c in candidatures:
                c['date'] = datetime.fromisoformat(c['created_at'].replace('Z', '+00:00')).strftime('%d/%m/%Y %H:%M') if c.get('created_at') else ''
                c['offre'] = c.get('offre_texte')
                c['analyse'] = c.get('analyse_compatibilite')
            return candidatures
    
    # Fallback local
    history_dir = Path('data/historique')
    if not history_dir.exists():
        return []
    
    candidatures = []
    for file in sorted(history_dir.glob('*.json'), reverse=True):
        with open(file, 'r', encoding='utf-8') as f:
            candidatures.append(json.load(f))
    
    return candidatures


# ============================================================================
# COMPOSANTS UI
# ============================================================================

def render_header():
    """Affiche le header principal avec le bandeau triathlon."""
    # Bandeau triathlon en haut
    st.image(
        "docMaman/tribandeau.jpeg",
        use_container_width=True
    )
    
    st.markdown("""
    <div class="main-header">
        <h1>🎯 Assistant Recherche d'Emploi</h1>
        <p>Valérie, optimisons ensemble ta candidature avec l'intelligence artificielle</p>
        <p style="font-size: 0.85rem; color: #a78bfa; margin-top: 0.5rem;">
            🏊 Finisher Ironman Embrunman • 🏃 Déterminée • 💪 Résiliente
        </p>
    </div>
    """, unsafe_allow_html=True)


def render_sidebar():
    """Affiche la sidebar avec le profil et la navigation."""
    with st.sidebar:
        # Photo de profil et titre
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.image(
                "docMaman/photomaman.jpeg",
                width=120
            )
        
        st.markdown("""
        <div style="text-align: center; padding: 0.5rem 0;">
            <h2 style="margin: 0; color: #f1f5f9; font-size: 1.3rem;">JobCoach IA</h2>
            <p style="color: #a78bfa; font-size: 0.85rem; margin: 0.25rem 0 0 0;">🎯 Pour Valérie</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Profil rapide avec style amélioré
        st.markdown("""
        <div class="profile-card" style="text-align: center;">
            <p class="profile-name" style="font-size: 1.2rem;">Valérie Jasica</p>
            <p class="profile-title" style="font-size: 0.9rem;">Conseillère en Insertion Professionnelle</p>
            <p style="color: #94a3b8; font-size: 0.75rem; margin-top: 0.5rem;">
                🏆 Finisher Ironman • 🥇 JO Paris 2024
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        # Statistiques rapides
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Expérience", "25+ ans")
        with col2:
            st.metric("Titre CIP", "2025 ✓")
        
        st.markdown("---")
        
        # Navigation
        st.markdown("### 📍 Navigation")
        
        pages = {
            'accueil': ('🏠', 'Accueil'),
            'cv_perso': ('🎨', 'CV Personnalisé'),
            'lettre': ('✉️', 'Lettre de motivation'),
            'entretien': ('🎤', 'Préparer un entretien'),
            'linkedin': ('💼', 'Posts LinkedIn'),
            'coach': ('💬', 'Coach IA'),
            'historique': ('📚', 'Mes candidatures')
        }
        
        for page_id, (icon, label) in pages.items():
            if st.button(f"{icon} {label}", key=f"nav_{page_id}", use_container_width=True):
                st.session_state.current_page = page_id
                st.rerun()
        
        st.markdown("---")
        
        # Atouts différenciants
        with st.expander("✨ Mes atouts clés", expanded=False):
            for atout in PROFIL_VALERIE['atouts_differenciants'][:4]:
                st.markdown(f"• {atout}")


def render_accueil():
    """Page d'accueil avec les fonctionnalités."""
    render_header()
    
    st.markdown("### 👋 Bienvenue Valérie !")
    st.markdown("""
    Cet assistant est conçu **spécialement pour toi** pour t'aider dans ta recherche d'emploi. 
    Il connaît ton parcours, tes compétences et tes atouts uniques.
    """)
    
    # Citation motivante personnalisée
    st.markdown("""
    <div class="motivation-quote">
        "Celle qui a terminé l'Embrunman sait que rien n'est impossible. 
        Chaque candidature est une nouvelle ligne de départ. 🏊‍♀️🚴‍♀️🏃‍♀️"
    </div>
    """, unsafe_allow_html=True)
    
    # Fonctionnalités principales en grille
    st.markdown("### 🚀 Que veux-tu faire aujourd'hui ?")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="feature-card">
            <h3>🎨 CV Personnalisé</h3>
            <p>Génère un CV adapté à chaque offre avec template pro + chat itératif</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Créer mon CV", key="btn_cv_perso"):
            st.session_state.current_page = 'cv_perso'
            st.rerun()
        
        st.markdown("""
        <div class="feature-card">
            <h3>✉️ Lettre de motivation</h3>
            <p>Crée une lettre percutante et personnalisée pour chaque candidature</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Rédiger ma lettre", key="btn_lettre"):
            st.session_state.current_page = 'lettre'
            st.rerun()
        
        st.markdown("""
        <div class="feature-card">
            <h3>💬 Coach IA</h3>
            <p>Discute avec ton coach personnel pour toutes tes questions</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Parler au coach", key="btn_coach"):
            st.session_state.current_page = 'coach'
            st.rerun()
    
    with col2:
        st.markdown("""
        <div class="feature-card">
            <h3>🎤 Préparer un entretien</h3>
            <p>Anticipe les questions et prépare des réponses percutantes</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Préparer l'entretien", key="btn_entretien"):
            st.session_state.current_page = 'entretien'
            st.rerun()
        
        st.markdown("""
        <div class="feature-card">
            <h3>💼 Posts LinkedIn</h3>
            <p>Génère des posts LinkedIn dans ton style pour booster ta visibilité</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Créer un post", key="btn_linkedin"):
            st.session_state.current_page = 'linkedin'
            st.rerun()
        
        st.markdown("""
        <div class="feature-card">
            <h3>📚 Mes candidatures</h3>
            <p>Suivi complet de tes candidatures avec rappels et statistiques</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Voir mes candidatures", key="btn_historique"):
            st.session_state.current_page = 'historique'
            st.rerun()
    
    st.markdown("---")
    
    # Rappel des atouts
    st.markdown("### 💪 Rappel de tes points forts")
    
    cols = st.columns(3)
    atouts = [
        ("🏆", "Ironman Finisher", "Résilience exceptionnelle"),
        ("🥇", "JO Paris 2024", "Leadership prouvé"),
        ("🎓", "Titre CIP 2025", "Formation récente"),
        ("💼", "25+ ans expérience", "Expertise relationnelle"),
        ("🤝", "6 stages diversifiés", "Connaissance du terrain"),
        ("🏃", "Projet socio-sport", "Engagement social")
    ]
    
    for i, (icon, titre, desc) in enumerate(atouts):
        with cols[i % 3]:
            st.markdown(f"""
            <div style="text-align: center; padding: 1rem; background: rgba(30, 41, 59, 0.5); border-radius: 12px; margin: 0.5rem 0;">
                <div style="font-size: 2rem;">{icon}</div>
                <div style="color: #f1f5f9; font-weight: 600; margin: 0.5rem 0;">{titre}</div>
                <div style="color: #94a3b8; font-size: 0.85rem;">{desc}</div>
            </div>
            """, unsafe_allow_html=True)


def render_express():
    """Page de génération express - Tout en 1 clic."""
    st.markdown("## 🚀 Génération Express")
    st.markdown("**Génère en un clic** : Analyse + CV adapté + Lettre de motivation + Préparation entretien")
    
    st.markdown("""
    <div class="motivation-quote">
        ⚡ Gagne du temps ! Colle une offre d'emploi et je génère TOUT pour toi automatiquement.
    </div>
    """, unsafe_allow_html=True)
    
    # Input de l'offre
    tab1, tab2 = st.tabs(["📝 Coller le texte", "📎 Uploader un PDF"])
    
    with tab1:
        offre_text = st.text_area(
            "Colle l'offre d'emploi complète ici",
            height=250,
            placeholder="Colle le contenu complet de l'offre d'emploi...\n\nPlus l'offre est détaillée, meilleurs seront les résultats !",
            key="express_offre_text"
        )
    
    with tab2:
        uploaded_file = st.file_uploader(
            "Uploade un fichier PDF",
            type=['pdf'],
            key="express_pdf_upload"
        )
        if uploaded_file:
            offre_text = extract_text_from_pdf(uploaded_file)
            st.success("✅ PDF extrait avec succès !")
            with st.expander("Voir le texte extrait"):
                st.text(offre_text[:2000] + "..." if len(offre_text) > 2000 else offre_text)
    
    # Options
    with st.expander("⚙️ Options de personnalisation (optionnel)"):
        col1, col2 = st.columns(2)
        with col1:
            ton_lettre = st.selectbox(
                "Ton de la lettre",
                options=["Professionnel et engagé", "Dynamique et enthousiaste", "Sobre et factuel"],
                index=0,
                key="express_ton"
            )
        with col2:
            type_entretien = st.selectbox(
                "Type d'entretien prévu",
                options=["Entretien RH", "Entretien manager", "Jury/Commission", "Non précisé"],
                index=3,
                key="express_type"
            )
        
        contexte_perso = st.text_area(
            "Contexte personnel (motivation particulière, disponibilité...)",
            placeholder="Ex: Disponible immédiatement, très motivée par la mission sociale de cette structure...",
            height=80,
            key="express_contexte"
        )
    
    # Bouton de génération
    if st.button("🚀 GÉNÉRER TOUT EN 1 CLIC", type="primary", use_container_width=True):
        if offre_text and len(offre_text.strip()) > 50:
            st.session_state.offre_actuelle = offre_text
            
            # Initialiser les résultats
            results = {
                'offre': offre_text,
                'analyse': None,
                'cv': None,
                'lettre': None,
                'entretien': None
            }
            
            llm = get_llm()
            
            # Progress bar
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            # 1. ANALYSE DE COMPATIBILITÉ
            status_text.markdown("### 🔍 Étape 1/4 : Analyse de compatibilité...")
            progress_bar.progress(10)
            
            with st.spinner("Analyse en cours..."):
                prompt = PROMPT_ANALYSE_COMPATIBILITE.format(
                    cv=CV_TEXTE_COMPLET,
                    offre=offre_text
                )
                results['analyse'] = llm.generate(
                    prompt=prompt,
                    system_prompt=SYSTEM_PROMPT_ANALYSE,
                    max_tokens=3000
                )
            progress_bar.progress(25)
            
            # 2. CV ADAPTÉ
            status_text.markdown("### 📄 Étape 2/4 : Adaptation du CV...")
            
            with st.spinner("Optimisation du CV..."):
                prompt = PROMPT_OPTIMISER_CV.format(
                    cv=CV_TEXTE_COMPLET,
                    offre=offre_text
                )
                results['cv'] = llm.generate(
                    prompt=prompt,
                    system_prompt=SYSTEM_PROMPT_CV,
                    max_tokens=5000
                )
            progress_bar.progress(50)
            
            # 3. LETTRE DE MOTIVATION
            status_text.markdown("### ✉️ Étape 3/4 : Rédaction de la lettre...")
            
            with st.spinner("Rédaction de la lettre..."):
                contexte_prompt = f"""
Contexte personnel : {contexte_perso if contexte_perso else "Non spécifié"}
Ton souhaité : {ton_lettre}
"""
                prompt = PROMPT_LETTRE_MOTIVATION.format(
                    cv=CV_TEXTE_COMPLET,
                    offre=offre_text,
                    contexte_supplementaire=contexte_prompt
                )
                results['lettre'] = llm.generate(
                    prompt=prompt,
                    system_prompt=SYSTEM_PROMPT_LETTRE,
                    max_tokens=3500
                )
            progress_bar.progress(75)
            
            # 4. PRÉPARATION ENTRETIEN
            status_text.markdown("### 🎤 Étape 4/4 : Préparation de l'entretien...")
            
            with st.spinner("Préparation de l'entretien..."):
                prompt = PROMPT_PREPARATION_ENTRETIEN.format(
                    cv=CV_TEXTE_COMPLET,
                    offre=offre_text,
                    type_entretien=type_entretien
                )
                results['entretien'] = llm.generate(
                    prompt=prompt,
                    system_prompt=SYSTEM_PROMPT_ENTRETIEN,
                    max_tokens=5000
                )
            progress_bar.progress(100)
            
            # Sauvegarder dans session
            st.session_state.cv_adapte = results['cv']
            st.session_state.lettre_motivation = results['lettre']
            st.session_state.preparation_entretien = results['entretien']
            st.session_state.analyse_compatibilite = results['analyse']
            
            status_text.markdown("### ✅ Génération terminée !")
            
            st.success("🎉 **Tout est prêt !** Tu peux maintenant consulter les résultats ci-dessous.")
            
            # Afficher les résultats dans des tabs
            st.markdown("---")
            st.markdown("## 📋 Résultats de la génération")
            
            tabs = st.tabs(["📊 Analyse", "📄 CV Adapté", "✉️ Lettre", "🎤 Entretien"])
            
            with tabs[0]:
                st.markdown("### 📊 Analyse de compatibilité")
                st.markdown(results['analyse'])
            
            with tabs[1]:
                st.markdown("### 📄 CV Optimisé")
                st.markdown(results['cv'])
                
                # Exports CV
                col_a, col_b = st.columns(2)
                with col_a:
                    st.download_button(
                        "📥 TXT",
                        data=results['cv'],
                        file_name=f"CV_Valerie_{datetime.now().strftime('%Y%m%d')}.txt",
                        mime="text/plain"
                    )
                with col_b:
                    try:
                        from utils.document_generator import generate_cv_docx
                        cv_docx = generate_cv_docx(results['cv'])
                        st.download_button(
                            "📥 WORD",
                            data=cv_docx,
                            file_name=f"CV_Valerie_{datetime.now().strftime('%Y%m%d')}.docx",
                            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
                        )
                    except Exception as e:
                        st.warning(f"Export DOCX non disponible: {e}")
            
            with tabs[2]:
                st.markdown("### ✉️ Lettre de motivation")
                st.markdown(results['lettre'])
                
                # Exports Lettre
                col_a, col_b = st.columns(2)
                with col_a:
                    st.download_button(
                        "📥 TXT",
                        data=results['lettre'],
                        file_name=f"LM_Valerie_{datetime.now().strftime('%Y%m%d')}.txt",
                        mime="text/plain"
                    )
                with col_b:
                    try:
                        from utils.document_generator import generate_lettre_docx
                        lettre_docx = generate_lettre_docx(results['lettre'])
                        st.download_button(
                            "📥 WORD",
                            data=lettre_docx,
                            file_name=f"LM_Valerie_{datetime.now().strftime('%Y%m%d')}.docx",
                            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
                        )
                    except Exception as e:
                        st.warning(f"Export DOCX non disponible: {e}")
            
            with tabs[3]:
                st.markdown("### 🎤 Préparation entretien")
                st.markdown(results['entretien'])
                
                # Exports Préparation
                col_a, col_b = st.columns(2)
                with col_a:
                    st.download_button(
                        "📥 TXT",
                        data=results['entretien'],
                        file_name=f"Entretien_Valerie_{datetime.now().strftime('%Y%m%d')}.txt",
                        mime="text/plain"
                    )
                with col_b:
                    try:
                        from utils.document_generator import generate_preparation_docx
                        prep_docx = generate_preparation_docx(results['entretien'], "Candidature")
                        st.download_button(
                            "📥 WORD",
                            data=prep_docx,
                            file_name=f"Entretien_Valerie_{datetime.now().strftime('%Y%m%d')}.docx",
                            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
                        )
                    except Exception as e:
                        st.warning(f"Export DOCX non disponible: {e}")
            
            # Bouton de sauvegarde avec formulaire
            st.markdown("---")
            st.markdown("### 💾 Sauvegarder cette candidature")
            st.info("💡 **Astuce** : Sauvegarde pour retrouver tous tes documents dans le dashboard 'Mes candidatures'")
            
            with st.expander("📝 Informations de la candidature", expanded=True):
                col_save1, col_save2 = st.columns(2)
                with col_save1:
                    titre_save_express = st.text_input("Titre du poste", value="", placeholder="Ex: Conseiller(e) en Insertion Professionnelle", key="express_titre_save")
                with col_save2:
                    entreprise_save_express = st.text_input("Entreprise", value="", placeholder="Ex: France Travail", key="express_entreprise_save")
            
            col1, col2 = st.columns(2)
            with col1:
                if st.button("💾 Sauvegarder cette candidature", type="primary", use_container_width=True):
                    titre = titre_save_express if titre_save_express else "Candidature Express"
                    entreprise = entreprise_save_express if entreprise_save_express else "Non spécifié"
                    result = save_candidature(
                        titre_poste=titre,
                        entreprise=entreprise,
                        data={
                            'cv_adapte': results['cv'],
                            'lettre_motivation': results['lettre'],
                            'preparation_entretien': results['entretien'],
                            'analyse': results['analyse'],
                            'offre': offre_text
                        }
                    )
                    if result:
                        st.success("✅ Candidature sauvegardée avec succès !")
                        st.info("💡 Tu peux retrouver cette candidature dans **'📚 Mes candidatures'** pour suivre son évolution")
                    else:
                        st.warning("⚠️ Sauvegarde locale uniquement (Supabase non disponible)")
            
            with col2:
                # Export complet
                full_export = f"""
CANDIDATURE GÉNÉRÉE LE {datetime.now().strftime('%d/%m/%Y à %H:%M')}
{'='*60}

ANALYSE DE COMPATIBILITÉ
{'-'*40}
{results['analyse']}

{'='*60}
CV ADAPTÉ
{'-'*40}
{results['cv']}

{'='*60}
LETTRE DE MOTIVATION
{'-'*40}
{results['lettre']}

{'='*60}
PRÉPARATION ENTRETIEN
{'-'*40}
{results['entretien']}
"""
                st.download_button(
                    "📥 Télécharger TOUT",
                    data=full_export,
                    file_name=f"Candidature_Complete_Valerie_{datetime.now().strftime('%Y%m%d')}.txt",
                    mime="text/plain",
                    use_container_width=True
                )
        else:
            st.warning("⚠️ Merci de coller une offre d'emploi valide (au moins 50 caractères)")


def render_analyser_offre():
    """Page d'analyse d'une offre d'emploi."""
    st.markdown("## 🔍 Analyser une offre d'emploi")
    st.markdown("Colle le texte de l'offre ou uploade un PDF pour obtenir une analyse détaillée.")
    
    # Input de l'offre
    tab1, tab2 = st.tabs(["📝 Coller le texte", "📎 Uploader un PDF"])
    
    with tab1:
        offre_text = st.text_area(
            "Colle l'offre d'emploi ici",
            height=300,
            placeholder="Colle le contenu complet de l'offre d'emploi...",
            key="offre_text_input"
        )
    
    with tab2:
        uploaded_file = st.file_uploader(
            "Uploade un fichier PDF",
            type=['pdf'],
            key="offre_pdf_upload"
        )
        if uploaded_file:
            offre_text = extract_text_from_pdf(uploaded_file)
            st.success("✅ PDF extrait avec succès !")
            with st.expander("Voir le texte extrait"):
                st.text(offre_text[:2000] + "..." if len(offre_text) > 2000 else offre_text)
    
    if st.button("🔍 Analyser cette offre", type="primary", use_container_width=True):
        if offre_text and len(offre_text.strip()) > 50:
            st.session_state.offre_actuelle = offre_text
            
            with st.spinner("🤖 Analyse en cours..."):
                llm = get_llm()
                
                # Analyse de compatibilité
                prompt = PROMPT_ANALYSE_COMPATIBILITE.format(
                    cv=CV_TEXTE_COMPLET,
                    offre=offre_text
                )
                
                result = llm.generate(
                    prompt=prompt,
                    system_prompt=SYSTEM_PROMPT_ANALYSE,
                    max_tokens=4096
                )
                
                st.session_state.analyse_compatibilite = result
            
            st.markdown("---")
            st.markdown("### 📊 Résultat de l'analyse")
            st.markdown(result)
            
            # Actions rapides
            st.markdown("---")
            st.markdown("### ⚡ Actions rapides")
            col1, col2, col3 = st.columns(3)
            
            with col1:
                if st.button("📄 Adapter mon CV", use_container_width=True):
                    st.session_state.current_page = 'cv'
                    st.rerun()
            with col2:
                if st.button("✉️ Créer la lettre", use_container_width=True):
                    st.session_state.current_page = 'lettre'
                    st.rerun()
            with col3:
                if st.button("🎤 Préparer l'entretien", use_container_width=True):
                    st.session_state.current_page = 'entretien'
                    st.rerun()
        else:
            st.warning("⚠️ Merci de coller une offre d'emploi valide (au moins 50 caractères)")


def render_optimiser_cv():
    """Page d'optimisation du CV."""
    st.markdown("## 📄 Optimiser mon CV")
    st.markdown("Génère une version de ton CV adaptée à une offre spécifique.")
    
    # Vérifier si une offre est déjà chargée
    if st.session_state.offre_actuelle:
        st.success("✅ Une offre est déjà chargée. Tu peux la modifier ci-dessous.")
    
    offre_text = st.text_area(
        "Offre d'emploi ciblée",
        value=st.session_state.offre_actuelle,
        height=250,
        placeholder="Colle l'offre d'emploi pour laquelle tu veux adapter ton CV...",
        key="cv_offre_input"
    )
    
    # Options supplémentaires
    with st.expander("⚙️ Options de personnalisation"):
        accent_experience = st.multiselect(
            "Expériences à mettre particulièrement en avant",
            options=[exp['poste'] + " - " + exp['entreprise'] for exp in PROFIL_VALERIE['experiences']],
            default=[]
        )
        
        points_specifiques = st.text_area(
            "Points spécifiques à mentionner (optionnel)",
            placeholder="Ex: Disponibilité immédiate, mobilité géographique...",
            height=100
        )
    
    if st.button("🚀 Générer le CV optimisé", type="primary", use_container_width=True):
        if offre_text and len(offre_text.strip()) > 50:
            st.session_state.offre_actuelle = offre_text
            
            with st.spinner("🤖 Optimisation du CV en cours..."):
                llm = get_llm()
                
                prompt = PROMPT_OPTIMISER_CV.format(
                    cv=CV_TEXTE_COMPLET,
                    offre=offre_text
                )
                
                # Ajouter le contexte supplémentaire si fourni
                if points_specifiques:
                    prompt += f"\n\nPoints supplémentaires à intégrer :\n{points_specifiques}"
                
                result = llm.generate(
                    prompt=prompt,
                    system_prompt=SYSTEM_PROMPT_CV,
                    max_tokens=6000
                )
                
                st.session_state.cv_adapte = result
            
            st.markdown("---")
            st.markdown("### ✨ CV Optimisé")
            
            st.markdown("""
            <div class="generated-content">
                <h2>📄 Ton CV adapté à cette offre</h2>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown(result)
            
            # Options de sauvegarde
            st.markdown("---")
            col1, col2 = st.columns(2)
            with col1:
                if st.button("💾 Sauvegarder cette candidature", use_container_width=True):
                    save_candidature(
                        titre_poste="Poste extrait de l'offre",
                        entreprise="À définir",
                        data={'cv_adapte': result, 'offre': offre_text}
                    )
                    st.success("✅ Candidature sauvegardée !")
            
            with col2:
                st.download_button(
                    "📥 Télécharger en texte",
                    data=result,
                    file_name=f"CV_Valerie_Jasica_{datetime.now().strftime('%Y%m%d')}.txt",
                    mime="text/plain",
                    use_container_width=True
                )
        else:
            st.warning("⚠️ Merci de coller une offre d'emploi valide")


def render_lettre_motivation():
    """Page de génération de lettre de motivation avec contextes pré-définis."""
    from config.valerie_contextes import (
        CONTEXTES_LETTRE_MOTIVATION, 
        get_contextes_par_categorie, 
        get_contexte_texte,
        get_contextes_recommandes_pour_offre
    )
    
    st.markdown("## ✉️ Lettre de motivation")
    st.markdown("Génère une lettre de motivation percutante et ultra-personnalisée.")
    
    # Vérifier si une offre est déjà chargée
    if st.session_state.offre_actuelle:
        st.success("✅ Une offre est déjà chargée.")
    
    offre_text = st.text_area(
        "Offre d'emploi ciblée",
        value=st.session_state.offre_actuelle,
        height=180,
        placeholder="Colle l'offre d'emploi...",
        key="lettre_offre_input"
    )
    
    # =========================================================================
    # CONTEXTES PRÉ-DÉFINIS + PERSONNALISÉS
    # =========================================================================
    st.markdown("---")
    st.markdown("""
    <div style="background: linear-gradient(135deg, rgba(16, 185, 129, 0.15) 0%, rgba(6, 182, 212, 0.15) 100%);
                border-radius: 12px; padding: 15px; margin-bottom: 15px; border-left: 4px solid #10b981;">
        <h4 style="margin: 0 0 8px 0; color: #34d399;">✨ Contextes personnalisés pré-chargés</h4>
        <p style="margin: 0; font-size: 0.9rem; color: #94a3b8;">
            Sélectionne les éléments de ton parcours à mettre en avant dans ta lettre.<br/>
            <strong>Ces informations sont issues de ton CV, ton dossier CIP et tes posts LinkedIn.</strong>
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Charger les contextes personnalisés depuis Supabase
    supabase = get_supabase_client()
    custom_contextes = {}
    if supabase.enabled:
        custom_contextes_list = supabase.get_custom_contextes()
        for ctx in custom_contextes_list:
            custom_contextes[ctx['cle']] = {
                'id': ctx['id'],
                'label': f"✏️ {ctx['label']}",
                'categorie': ctx['categorie'],
                'texte': ctx['texte'],
                'mots_cles': ctx.get('mots_cles', []),
                'is_custom': True
            }
    
    # Fusionner les contextes par défaut et personnalisés
    all_contextes = {**CONTEXTES_LETTRE_MOTIVATION, **custom_contextes}
    
    # Déterminer les contextes recommandés si une offre est présente
    contextes_recommandes = []
    if offre_text and len(offre_text.strip()) > 50:
        contextes_recommandes = get_contextes_recommandes_pour_offre(offre_text)
        st.info(f"💡 **Suggestions automatiques basées sur l'offre :** {len(contextes_recommandes)} contextes pré-sélectionnés")
    
    # Initialiser les sélections dans session_state
    if 'lettre_contextes_selectionnes' not in st.session_state:
        st.session_state.lettre_contextes_selectionnes = contextes_recommandes if contextes_recommandes else []
    
    # Organiser les contextes par catégorie (incluant les personnalisés)
    categories = {}
    for key, ctx in all_contextes.items():
        cat = ctx.get("categorie", "Autre")
        if cat not in categories:
            categories[cat] = []
        categories[cat].append((key, ctx))
    
    selected_contextes = []
    selected_custom_ids = []  # Pour gérer la suppression
    
    # Créer les colonnes pour les catégories
    col_left, col_right = st.columns(2)
    
    categories_list = list(categories.items())
    for i, (cat_name, cat_contextes) in enumerate(categories_list):
        with col_left if i % 2 == 0 else col_right:
            with st.expander(f"📁 {cat_name}", expanded=(cat_name in ["Parcours", "Sport & Valeurs"])):
                for key, ctx in cat_contextes:
                    is_recommended = key in contextes_recommandes
                    default_value = is_recommended or key in st.session_state.lettre_contextes_selectionnes
                    is_custom = ctx.get('is_custom', False)
                    
                    # Ajouter une icône ✨ si recommandé
                    label = ctx["label"]
                    if is_recommended:
                        label = f"{label} ✨"
                    
                    # Layout pour contextes personnalisés (avec bouton suppression)
                    if is_custom:
                        ctx_col1, ctx_col2 = st.columns([5, 1])
                        with ctx_col1:
                            if st.checkbox(label, value=default_value, key=f"ctx_{key}"):
                                selected_contextes.append(key)
                        with ctx_col2:
                            if st.button("🗑️", key=f"del_{key}", help="Supprimer ce contexte"):
                                if supabase.delete_custom_contexte(ctx['id']):
                                    st.success("Contexte supprimé !")
                                    st.rerun()
                    else:
                        if st.checkbox(label, value=default_value, key=f"ctx_{key}"):
                            selected_contextes.append(key)
    
    # Mettre à jour la session
    st.session_state.lettre_contextes_selectionnes = selected_contextes
    
    # Afficher un résumé des contextes sélectionnés
    if selected_contextes:
        st.markdown(f"**{len(selected_contextes)} contexte(s) sélectionné(s)** pour enrichir ta lettre")
    
    # =========================================================================
    # AJOUTER UN NOUVEAU CONTEXTE PERSONNALISÉ
    # =========================================================================
    with st.expander("➕ Ajouter un nouveau contexte personnalisé", expanded=False):
        st.markdown("""
        <div style="font-size: 0.85rem; color: #94a3b8; margin-bottom: 10px;">
            Crée un nouveau contexte qui sera sauvegardé et réutilisable pour toutes tes lettres.
        </div>
        """, unsafe_allow_html=True)
        
        new_ctx_col1, new_ctx_col2 = st.columns(2)
        with new_ctx_col1:
            new_label = st.text_input("Titre du contexte", placeholder="Ex: Mon expérience associative", key="new_ctx_label")
        with new_ctx_col2:
            new_categorie = st.selectbox(
                "Catégorie",
                options=["Parcours", "Sport & Valeurs", "Valeurs", "Pratique", "Spécifique", "Autre"],
                key="new_ctx_cat"
            )
        
        new_texte = st.text_area(
            "Contenu du contexte",
            placeholder="Décris en quelques phrases ce que tu veux mettre en avant...",
            height=100,
            key="new_ctx_texte"
        )
        
        if st.button("💾 Sauvegarder ce contexte", type="primary"):
            if new_label and new_texte:
                if supabase.enabled:
                    # Générer une clé unique
                    import re
                    cle = re.sub(r'[^a-z0-9_]', '_', new_label.lower().replace(' ', '_'))[:30]
                    cle = f"custom_{cle}_{datetime.now().strftime('%Y%m%d%H%M%S')}"
                    
                    result = supabase.save_custom_contexte(
                        cle=cle,
                        label=new_label,
                        categorie=new_categorie,
                        texte=new_texte
                    )
                    if result:
                        st.success(f"✅ Contexte '{new_label}' sauvegardé !")
                        st.rerun()
                    else:
                        st.error("Erreur lors de la sauvegarde")
                else:
                    st.warning("⚠️ Supabase non configuré. Les contextes personnalisés ne seront pas persistés.")
            else:
                st.warning("Merci de remplir le titre et le contenu")
    
    # Contexte SUPPLÉMENTAIRE libre (pour usage ponctuel)
    st.markdown("---")
    st.markdown("### 📝 Contexte ponctuel (non sauvegardé)")
    contexte_libre = st.text_area(
        "Ajoute des éléments spécifiques pour CETTE lettre uniquement",
        placeholder="Ex: Tu connais quelqu'un dans l'entreprise, tu as visité leurs locaux, tu as une motivation très spécifique pour CE poste...",
        height=80,
        key="lettre_contexte_libre"
    )
    
    # Style de lettre
    st.markdown("---")
    st.markdown("### 🎨 Style de la lettre")
    col1, col2 = st.columns(2)
    with col1:
        ton = st.selectbox(
            "Ton de la lettre",
            options=["Professionnel et engagé", "Dynamique et enthousiaste", "Sobre et factuel"],
            index=0
        )
    with col2:
        longueur = st.selectbox(
            "Longueur souhaitée",
            options=["Standard (1 page)", "Courte (3/4 page)", "Développée"],
            index=0
        )
    
    # Bouton de génération
    if st.button("✨ Générer la lettre", type="primary", use_container_width=True):
        if offre_text and len(offre_text.strip()) > 50:
            st.session_state.offre_actuelle = offre_text
            
            with st.spinner("🤖 Rédaction de la lettre en cours..."):
                llm = get_llm()
                
                # Compiler les contextes sélectionnés (défaut + personnalisés)
                textes_contextes = []
                for key in selected_contextes:
                    if key in CONTEXTES_LETTRE_MOTIVATION:
                        textes_contextes.append(CONTEXTES_LETTRE_MOTIVATION[key]["texte"])
                    elif key in custom_contextes:
                        textes_contextes.append(custom_contextes[key]["texte"])
                
                contexte_compile = "\n\n".join(textes_contextes)
                
                # Construire le contexte complet
                contexte_prompt = f"""
=== CONTEXTE PERSONNEL RICHE DE VALÉRIE ===
(Ces éléments sont vérifiés et issus de son parcours réel)

{contexte_compile if contexte_compile else "Aucun contexte pré-défini sélectionné."}

=== ÉLÉMENTS SUPPLÉMENTAIRES ===
{contexte_libre if contexte_libre else "Aucun élément supplémentaire."}

=== STYLE SOUHAITÉ ===
Ton : {ton}
Longueur : {longueur}

INSTRUCTIONS IMPORTANTES :
- Utilise les contextes personnels ci-dessus pour enrichir la lettre de façon NATURELLE
- Ne liste pas ces éléments, intègre-les subtilement dans l'argumentaire
- La lettre doit être authentique et refléter la personnalité de Valérie
- Fais ressortir sa reconversion réussie et sa maturité professionnelle
"""
                
                prompt = PROMPT_LETTRE_MOTIVATION.format(
                    cv=CV_TEXTE_COMPLET,
                    offre=offre_text,
                    contexte_supplementaire=contexte_prompt
                )
                
                result = llm.generate(
                    prompt=prompt,
                    system_prompt=SYSTEM_PROMPT_LETTRE,
                    max_tokens=8096
                )
                
                st.session_state.lettre_motivation = result
            
            st.markdown("---")
            st.markdown("### ✨ Ta lettre de motivation")
            
            # Afficher les contextes utilisés
            if selected_contextes:
                with st.expander("📌 Contextes utilisés pour cette lettre", expanded=False):
                    for key in selected_contextes:
                        if key in CONTEXTES_LETTRE_MOTIVATION:
                            ctx = CONTEXTES_LETTRE_MOTIVATION[key]
                            st.markdown(f"• **{ctx['label']}**")
            
            st.markdown(result)
            
            # Options
            st.markdown("---")
            col1, col2, col3 = st.columns(3)
            with col1:
                st.download_button(
                    "📥 Télécharger TXT",
                    data=result,
                    file_name=f"LM_Valerie_Jasica_{datetime.now().strftime('%Y%m%d')}.txt",
                    mime="text/plain",
                    use_container_width=True
                )
            with col2:
                try:
                    from utils.document_generator import generate_lettre_docx
                    docx_buffer = generate_lettre_docx(result)
                    st.download_button(
                        "📥 Télécharger WORD",
                        data=docx_buffer,
                        file_name=f"LM_Valerie_Jasica_{datetime.now().strftime('%Y%m%d')}.docx",
                        mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                        use_container_width=True
                    )
                except Exception:
                    pass
            with col3:
                if st.button("🔄 Regénérer", use_container_width=True):
                    st.rerun()
        else:
            st.warning("⚠️ Merci de coller une offre d'emploi valide (au moins 50 caractères)")


def render_preparation_entretien():
    """Page de préparation à l'entretien."""
    st.markdown("## 🎤 Préparer un entretien")
    st.markdown("Anticipe les questions et prépare des réponses percutantes.")
    
    # Vérifier si une offre est déjà chargée
    if st.session_state.offre_actuelle:
        st.success("✅ Une offre est déjà chargée.")
    
    offre_text = st.text_area(
        "Offre d'emploi pour laquelle tu as un entretien",
        value=st.session_state.offre_actuelle,
        height=200,
        placeholder="Colle l'offre d'emploi...",
        key="entretien_offre_input"
    )
    
    # Type d'entretien
    col1, col2 = st.columns(2)
    with col1:
        type_entretien = st.selectbox(
            "Type d'entretien",
            options=[
                "Entretien RH (premier contact)",
                "Entretien manager/opérationnel",
                "Entretien de validation finale",
                "Entretien téléphonique",
                "Entretien visio",
                "Jury / Commission"
            ],
            index=0
        )
    with col2:
        duree = st.selectbox(
            "Durée prévue",
            options=["30 minutes", "45 minutes", "1 heure", "Plus d'1 heure", "Non précisé"],
            index=4
        )
    
    # Informations supplémentaires
    with st.expander("📋 Informations complémentaires"):
        nom_recruteur = st.text_input("Nom du recruteur (si connu)")
        points_preparation = st.text_area(
            "Points spécifiques sur lesquels tu veux te préparer",
            placeholder="Ex: Comment justifier mon parcours varié ? Comment parler de ma reconversion ?"
        )
    
    if st.button("🎯 Préparer l'entretien", type="primary", use_container_width=True):
        if offre_text and len(offre_text.strip()) > 50:
            st.session_state.offre_actuelle = offre_text
            
            with st.spinner("🤖 Préparation de l'entretien en cours..."):
                llm = get_llm()
                
                prompt = PROMPT_PREPARATION_ENTRETIEN.format(
                    cv=CV_TEXTE_COMPLET,
                    offre=offre_text,
                    type_entretien=type_entretien
                )
                
                if points_preparation:
                    prompt += f"\n\nPoints spécifiques à préparer :\n{points_preparation}"
                
                result = llm.generate(
                    prompt=prompt,
                    system_prompt=SYSTEM_PROMPT_ENTRETIEN,
                    max_tokens=6000
                )
                
                st.session_state.preparation_entretien = result
            
            st.markdown("---")
            st.markdown("### 🎤 Ta préparation complète")
            
            st.markdown(result)
            
            # Options
            st.markdown("---")
            st.download_button(
                "📥 Télécharger la préparation",
                data=result,
                file_name=f"Prep_Entretien_Valerie_{datetime.now().strftime('%Y%m%d')}.txt",
                mime="text/plain",
                use_container_width=True
            )
        else:
            st.warning("⚠️ Merci de coller une offre d'emploi valide")


def save_chat_history():
    """Sauvegarde l'historique du chat (Supabase + local fallback)."""
    supabase = get_supabase_client()
    
    # Note: Avec Supabase, on sauvegarde message par message
    # Cette fonction est conservée pour le fallback local
    chat_dir = Path('data/chat')
    chat_dir.mkdir(parents=True, exist_ok=True)
    
    with open(chat_dir / 'chat_history.json', 'w', encoding='utf-8') as f:
        json.dump({
            'messages': st.session_state.chat_messages,
            'uploaded_docs': st.session_state.get('chat_uploaded_docs', []),
            'last_updated': datetime.now().isoformat()
        }, f, ensure_ascii=False, indent=2)


def save_chat_message_to_db(role: str, content: str):
    """Sauvegarde un seul message dans Supabase."""
    supabase = get_supabase_client()
    if supabase.enabled:
        supabase.save_chat_message(role=role, content=content)


def save_chat_document_to_db(filename: str, content: str):
    """Sauvegarde un document dans Supabase."""
    supabase = get_supabase_client()
    if supabase.enabled:
        supabase.save_chat_document(filename=filename, content=content)


def load_chat_history():
    """Charge l'historique du chat (Supabase + local fallback)."""
    supabase = get_supabase_client()
    
    # Essayer Supabase d'abord
    if supabase.enabled:
        messages = supabase.get_chat_messages(limit=100)
        docs = supabase.get_chat_documents()
        
        if messages or docs:
            # Convertir au format attendu
            formatted_messages = [
                {"role": m["role"], "content": m["content"]}
                for m in messages
            ]
            formatted_docs = [
                {"name": d["filename"], "content": d["content"], "id": d["id"]}
                for d in docs
            ]
            return formatted_messages, formatted_docs
    
    # Fallback local
    chat_file = Path('data/chat/chat_history.json')
    if chat_file.exists():
        with open(chat_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
            return data.get('messages', []), data.get('uploaded_docs', [])
    return [], []


def clear_chat_from_db():
    """Efface le chat de Supabase."""
    supabase = get_supabase_client()
    if supabase.enabled:
        supabase.clear_chat_messages()
        supabase.clear_chat_documents()


def render_cv_personnalise():
    """Page de génération de CV personnalisé HTML → PDF avec chat itératif."""
    render_header()
    
    st.markdown("## 🎨 CV Personnalisé")
    
    # Initialiser les états de session
    if 'cv_chat_history' not in st.session_state:
        st.session_state.cv_chat_history = []
    if 'cv_current_data' not in st.session_state:
        st.session_state.cv_current_data = None
    if 'cv_offre_text' not in st.session_state:
        st.session_state.cv_offre_text = ""
    if 'cv_modifications_history' not in st.session_state:
        st.session_state.cv_modifications_history = []
    if 'cv_version' not in st.session_state:
        st.session_state.cv_version = 0
    
    # === WORKFLOW EN 3 ÉTAPES ===
    
    # Indicateur de progression
    step = 1
    if st.session_state.cv_current_data:
        step = 2
    if st.session_state.cv_version > 1:
        step = 3
    
    st.markdown(f"""
    <div style="display: flex; gap: 10px; margin-bottom: 20px;">
        <div style="flex: 1; padding: 10px; border-radius: 8px; text-align: center;
                    background: {'rgba(16, 185, 129, 0.3)' if step >= 1 else 'rgba(100, 100, 100, 0.2)'};">
            <div style="font-size: 1.5rem;">1️⃣</div>
            <div style="font-size: 0.8rem; color: {'#10b981' if step >= 1 else '#6b7280'};">Coller l'offre</div>
        </div>
        <div style="flex: 1; padding: 10px; border-radius: 8px; text-align: center;
                    background: {'rgba(16, 185, 129, 0.3)' if step >= 2 else 'rgba(100, 100, 100, 0.2)'};">
            <div style="font-size: 1.5rem;">2️⃣</div>
            <div style="font-size: 0.8rem; color: {'#10b981' if step >= 2 else '#6b7280'};">CV généré</div>
        </div>
        <div style="flex: 1; padding: 10px; border-radius: 8px; text-align: center;
                    background: {'rgba(16, 185, 129, 0.3)' if step >= 3 else 'rgba(100, 100, 100, 0.2)'};">
            <div style="font-size: 1.5rem;">3️⃣</div>
            <div style="font-size: 0.8rem; color: {'#10b981' if step >= 3 else '#6b7280'};">Affiné</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # === ÉTAPE 1: INPUT OFFRE ===
    if not st.session_state.cv_current_data:
        st.markdown("### 📋 Étape 1 : Colle l'offre d'emploi")
        
        tab1, tab2 = st.tabs(["📝 Coller le texte", "📎 Uploader un PDF"])
        
        with tab1:
            offre_text = st.text_area(
                "Offre d'emploi",
                height=200,
                placeholder="Colle ici le contenu complet de l'offre d'emploi...\n\nPlus l'offre est détaillée, meilleure sera la personnalisation !",
                key="cv_perso_offre_input"
            )
        
        with tab2:
            uploaded_file = st.file_uploader("Fichier PDF de l'offre", type=['pdf'], key="cv_perso_pdf")
            if uploaded_file:
                offre_text = extract_text_from_pdf(uploaded_file)
                st.success("✅ PDF extrait avec succès !")
                with st.expander("Voir le texte extrait"):
                    st.text(offre_text[:1000] + "..." if len(offre_text) > 1000 else offre_text)
        
        col1, col2 = st.columns([2, 1])
        with col1:
            if st.button("🎨 Générer mon CV personnalisé", type="primary", use_container_width=True):
                if offre_text and len(offre_text.strip()) > 50:
                    st.session_state.cv_offre_text = offre_text
                    with st.spinner("🔄 Analyse de l'offre et personnalisation du CV..."):
                        generate_initial_cv(offre_text)
                    st.rerun()
                else:
                    st.warning("⚠️ L'offre est trop courte. Colle au moins le descriptif du poste.")
        
        with col2:
            if st.button("👁️ Voir mon CV actuel", use_container_width=True):
                st.session_state.show_default_cv = True
        
        # Afficher le CV par défaut si demandé
        if st.session_state.get('show_default_cv'):
            st.markdown("---")
            st.markdown("### 📄 Mon CV actuel (non personnalisé)")
            try:
                from utils.cv_generator import generate_cv_html
                default_html = generate_cv_html()
                import streamlit.components.v1 as components
                components.html(default_html, height=700, scrolling=True)
            except Exception as e:
                st.error(f"Erreur: {e}")
    
    else:
        # === ÉTAPE 2 & 3: CV GÉNÉRÉ + AFFINAGE ===
        
        # Layout en 2 colonnes
        col_left, col_right = st.columns([1, 1.3])
        
        with col_left:
            # === PANNEAU DE MODIFICATIONS ===
            st.markdown("### ✏️ Modifier le CV")
            
            # Résumé des modifications actuelles
            if st.session_state.get('cv_customizations'):
                cust = st.session_state.cv_customizations
                
                st.markdown(f"""
                <div style="background: rgba(99, 102, 241, 0.1); border-radius: 12px; padding: 15px; margin-bottom: 15px; border: 1px solid rgba(99, 102, 241, 0.3);">
                    <div style="font-size: 0.85rem; color: #a5b4fc; margin-bottom: 5px;">📊 Version {st.session_state.cv_version}</div>
                    <div style="font-size: 0.9rem;"><strong>Mots-clés détectés:</strong> {', '.join(cust.get('mots_cles_offre', ['Non défini']))}</div>
                </div>
                """, unsafe_allow_html=True)
            
            # === HISTORIQUE DES MODIFICATIONS ===
            if st.session_state.cv_modifications_history:
                with st.expander(f"📜 Historique ({len(st.session_state.cv_modifications_history)} modification(s))", expanded=False):
                    for i, modif in enumerate(reversed(st.session_state.cv_modifications_history)):
                        st.markdown(f"""
                        <div style="background: rgba(30, 41, 59, 0.5); border-radius: 8px; padding: 10px; margin-bottom: 8px; border-left: 3px solid #6366f1;">
                            <div style="font-size: 0.75rem; color: #94a3b8;">v{len(st.session_state.cv_modifications_history) - i}</div>
                            <div style="font-size: 0.85rem;">{modif.get('demande', 'Génération initiale')}</div>
                            <div style="font-size: 0.75rem; color: #10b981; margin-top: 5px;">✓ {modif.get('resultat', 'Appliqué')}</div>
                        </div>
                        """, unsafe_allow_html=True)
            
            st.markdown("---")
            
            # === SUGGESTIONS RAPIDES ===
            st.markdown("**💡 Suggestions rapides:**")
            
            suggestions = [
                ("🎯 Accroche percutante", "Rends l'accroche plus percutante et dynamique, avec des verbes d'action qui correspondent à l'offre"),
                ("💼 Expériences adaptées", "Reformule les intitulés de mes expériences professionnelles pour mieux correspondre aux termes de l'offre"),
                ("🏃 + Sport & JO", "Ajoute ou valorise mon engagement sportif (Ironman, JO Paris 2024) dans les intérêts et le bénévolat"),
                ("📝 Compétences CIP", "Reformule toutes les compétences pour correspondre au référentiel CIP et aux attentes de l'offre"),
                ("📋 Stages pertinents", "Reformule mes missions de stage pour les rendre plus pertinentes par rapport à cette offre"),
                ("🎓 Formation mise en avant", "Mets en valeur ma formation CIP 2025 et mes certifications récentes"),
                ("🤝 Soft skills", "Accentue mes compétences relationnelles dans l'accroche et les expériences"),
                ("🎯 Centres d'intérêt ciblés", "Adapte mes centres d'intérêt pour qu'ils résonnent avec la culture de l'entreprise")
            ]
            
            cols = st.columns(2)
            for i, (label, prompt) in enumerate(suggestions):
                with cols[i % 2]:
                    if st.button(label, key=f"sugg_{i}", use_container_width=True):
                        apply_cv_feedback(prompt)
                        st.rerun()
            
            st.markdown("---")
            
            # === MODIFICATION PERSONNALISÉE ===
            st.markdown("**✍️ Ou demande une modification spécifique:**")
            
            feedback = st.text_area(
                "Ta demande",
                height=80,
                placeholder="Ex: Change l'accroche pour mentionner mon projet socio-sportif...",
                key="cv_feedback_input"
            )
            
            col_a, col_b = st.columns(2)
            with col_a:
                if st.button("✨ Appliquer", type="primary", use_container_width=True, disabled=not feedback):
                    if feedback:
                        apply_cv_feedback(feedback)
                        st.rerun()
            
            with col_b:
                if st.button("🔄 Recommencer", use_container_width=True):
                    st.session_state.cv_chat_history = []
                    st.session_state.cv_current_data = None
                    st.session_state.cv_html_preview = None
                    st.session_state.cv_customizations = None
                    st.session_state.cv_modifications_history = []
                    st.session_state.cv_version = 0
                    st.rerun()
            
            st.markdown("---")
            
            # === AJUSTEMENT DENSITÉ POUR PDF 1 PAGE ===
            st.markdown("### 📐 Ajuster la densité (pour tenir sur 1 page)")
            
            from utils.cv_generator import get_density_recommendation, render_template, get_density_values
            
            # Obtenir la recommandation automatique
            cv_data = st.session_state.cv_current_data
            if cv_data:
                preset_name, recommended_density, explanation = get_density_recommendation(cv_data)
                
                # Afficher l'explication
                st.markdown(f"""
                <div style="background: rgba(251, 191, 36, 0.15); border-radius: 8px; padding: 10px; margin-bottom: 10px; font-size: 0.9rem;">
                    {explanation}
                </div>
                """, unsafe_allow_html=True)
                
                # Initialiser la densité dans session_state
                if 'cv_density' not in st.session_state:
                    st.session_state.cv_density = recommended_density
                
                # Slider de densité
                density = st.slider(
                    "Densité du CV",
                    min_value=0,
                    max_value=100,
                    value=st.session_state.cv_density,
                    help="0 = Ultra compact (tout petit), 100 = Espacé (grand)",
                    key="density_slider"
                )
                
                # Labels sous le slider
                col_labels = st.columns(4)
                with col_labels[0]:
                    st.caption("🔴 Ultra compact")
                with col_labels[1]:
                    st.caption("🟠 Compact")
                with col_labels[2]:
                    st.caption("🟢 Normal")
                with col_labels[3]:
                    st.caption("🔵 Espacé")
                
                # Bouton pour appliquer la nouvelle densité
                if density != st.session_state.cv_density:
                    if st.button("🔄 Appliquer la nouvelle densité", type="secondary", use_container_width=True):
                        st.session_state.cv_density = density
                        # Régénérer le HTML avec la nouvelle densité
                        new_html = render_template(cv_data, density=density)
                        st.session_state.cv_html_preview = new_html
                        st.success("✅ Densité mise à jour !")
                        st.rerun()
            
            st.markdown("---")
            
            # === TÉLÉCHARGEMENT ===
            st.markdown("### 📥 Télécharger")
            
            # Utiliser la densité actuelle pour générer les fichiers
            current_density = st.session_state.get('cv_density', 50)
            html_for_download = st.session_state.cv_html_preview
            
            dl_col1, dl_col2 = st.columns(2)
            
            with dl_col1:
                st.download_button(
                    "📄 Télécharger HTML",
                    data=html_for_download,
                    file_name=f"CV_Valerie_v{st.session_state.cv_version}_{datetime.now().strftime('%Y%m%d')}.html",
                    mime="text/html",
                    use_container_width=True
                )
            
            with dl_col2:
                # Essayer weasyprint, sinon proposer une alternative
                pdf_generated = False
                try:
                    from weasyprint import HTML
                    import io
                    
                    pdf_buffer = io.BytesIO()
                    HTML(string=html_for_download).write_pdf(pdf_buffer)
                    pdf_buffer.seek(0)
                    
                    st.download_button(
                        "📑 Télécharger PDF",
                        data=pdf_buffer,
                        file_name=f"CV_Valerie_v{st.session_state.cv_version}_{datetime.now().strftime('%Y%m%d')}.pdf",
                        mime="application/pdf",
                        use_container_width=True
                    )
                    pdf_generated = True
                except Exception as e:
                    pass
                
                if not pdf_generated:
                    st.info("💡 **Pour obtenir un PDF:** Télécharge le HTML, ouvre-le dans ton navigateur, puis Imprimer → Enregistrer en PDF")
            
            st.markdown("---")
            
            # === SAUVEGARDE ===
            st.markdown("### 💾 Sauvegarder")
            
            with st.expander("Sauvegarder ce CV", expanded=False):
                save_col1, save_col2 = st.columns(2)
                with save_col1:
                    titre_save = st.text_input("Titre du poste", value="Conseiller(e) en Insertion", key="cv_save_titre")
                with save_col2:
                    entreprise_save = st.text_input("Entreprise", value="France Travail", key="cv_save_entreprise")
                
                lier_candidature = st.checkbox("🔗 Créer/lier à une candidature", value=True, key="cv_lier_candidature")
                
                if st.button("💾 Sauvegarder", type="primary", use_container_width=True):
                    save_cv_to_supabase(
                        titre=titre_save,
                        entreprise=entreprise_save,
                        candidature_id=None,
                        create_candidature=lier_candidature
                    )
        
        # === COLONNE DROITE: PREVIEW + ÉDITION MANUELLE ===
        with col_right:
            st.markdown("### 📄 Aperçu du CV")
            
            # Onglets: Aperçu / Édition manuelle
            tab_preview, tab_edit = st.tabs(["👁️ Aperçu", "✏️ Édition manuelle"])
            
            with tab_preview:
                # Afficher les personnalisations actuelles de façon claire
                if st.session_state.get('cv_customizations'):
                    cust = st.session_state.cv_customizations
                    
                    with st.expander("🔍 Personnalisations actuelles", expanded=False):
                        st.markdown("**📝 Accroche:**")
                        accroche = cust.get('accroche', 'Non définie')
                        accroche_clean = accroche.replace("<span class='accroche-highlight'>", "**").replace("</span>", "**")
                        st.markdown(f"> {accroche_clean}")
                        
                        col_q, col_c = st.columns(2)
                        with col_q:
                            st.markdown("**✨ Qualités:**")
                            for q in cust.get('qualites', []):
                                st.markdown(f"• {q}")
                        
                        with col_c:
                            st.markdown("**💪 Compétences:**")
                            for c in cust.get('competences_prioritaires', [])[:5]:
                                st.markdown(f"• {c}")
                
                # Preview HTML du CV
                if st.session_state.get('cv_html_preview'):
                    import streamlit.components.v1 as components
                    components.html(st.session_state.cv_html_preview, height=700, scrolling=True)
                else:
                    st.warning("Erreur: Aucun aperçu disponible")
            
            with tab_edit:
                st.markdown("""
                <div style="background: rgba(251, 191, 36, 0.15); border-radius: 8px; padding: 12px; margin-bottom: 15px; border-left: 3px solid #fbbf24;">
                    <strong>✏️ Mode édition manuelle</strong><br/>
                    <span style="font-size: 0.85rem;">Modifie TOUT le CV ci-dessous, puis clique sur "Appliquer" pour régénérer.</span>
                </div>
                """, unsafe_allow_html=True)
                
                if st.session_state.get('cv_current_data'):
                    cv_data = st.session_state.cv_current_data
                    cust = st.session_state.cv_customizations or {}
                    
                    # Sous-onglets pour chaque section
                    edit_tabs = st.tabs(["📝 Accroche", "💪 Compétences", "💼 Expériences", "🎓 Formation", "📋 Stages", "🤝 Bénévolat", "🎯 Intérêts"])
                    
                    # === ONGLET ACCROCHE & QUALITÉS ===
                    with edit_tabs[0]:
                        st.markdown("**📝 Accroche** (utilise `**mot**` pour mettre en gras)")
                        
                        accroche_edit = cust.get('accroche', cv_data.get('accroche', ''))
                        accroche_edit = accroche_edit.replace("<span class='accroche-highlight'>", "**").replace("</span>", "**")
                        
                        new_accroche = st.text_area(
                            "Accroche",
                            value=accroche_edit,
                            height=100,
                            key="edit_accroche",
                            label_visibility="collapsed"
                        )
                        
                        st.markdown("**✨ Qualités** (4 max)")
                        qualites_actuelles = cv_data.get('qualites', ['Déterminée', 'Engagée', 'Résiliente', 'Fédératrice'])
                        
                        qualites_dispo = [
                            "Déterminée", "Engagée", "Résiliente", "Fédératrice", 
                            "Polyvalente", "Organisée", "Proactive", "Empathique",
                            "Dynamique", "Rigoureuse", "Adaptable", "Créative",
                            "Autonome", "Collaborative", "Persévérante", "Bienveillante"
                        ]
                        
                        new_qualites = st.multiselect(
                            "Qualités",
                            options=qualites_dispo + [q for q in qualites_actuelles if q not in qualites_dispo],
                            default=qualites_actuelles[:4],
                            max_selections=4,
                            key="edit_qualites",
                            label_visibility="collapsed"
                        )
                        
                        qualite_custom = st.text_input("+ Qualité personnalisée", key="edit_qualite_custom")
                        if qualite_custom and len(new_qualites) < 4:
                            new_qualites.append(qualite_custom)
                    
                    # === ONGLET COMPÉTENCES ===
                    with edit_tabs[1]:
                        st.markdown("**💪 Compétences principales** (affichées en premier)")
                        
                        competences_actuelles = cv_data.get('competences', [])
                        
                        new_competences = []
                        for i, comp in enumerate(competences_actuelles[:10]):
                            new_comp = st.text_input(
                                f"Compétence {i+1}",
                                value=comp,
                                key=f"edit_comp_{i}"
                            )
                            if new_comp:
                                new_competences.append(new_comp)
                        
                        # Ajouter une nouvelle compétence
                        new_comp_add = st.text_input("➕ Ajouter une compétence", key="edit_comp_new", placeholder="Nouvelle compétence...")
                        if new_comp_add:
                            new_competences.append(new_comp_add)
                    
                    # === ONGLET EXPÉRIENCES ===
                    with edit_tabs[2]:
                        st.markdown("**💼 Expériences professionnelles**")
                        
                        experiences = cv_data.get('experiences', [])
                        new_experiences = []
                        
                        for i, exp in enumerate(experiences):
                            with st.expander(f"{exp.get('entreprise', 'Expérience')} - {exp.get('poste', '')}", expanded=i==0):
                                col1, col2 = st.columns(2)
                                with col1:
                                    entreprise = st.text_input("Entreprise", value=exp.get('entreprise', ''), key=f"edit_exp_ent_{i}")
                                    poste = st.text_input("Poste", value=exp.get('poste', ''), key=f"edit_exp_poste_{i}")
                                with col2:
                                    dates = st.text_input("Dates", value=exp.get('dates', ''), key=f"edit_exp_dates_{i}")
                                    supprimer = st.checkbox("🗑️ Supprimer", key=f"edit_exp_del_{i}")
                                
                                if not supprimer and entreprise:
                                    new_experiences.append({
                                        'entreprise': entreprise,
                                        'poste': poste,
                                        'dates': dates
                                    })
                        
                        # Ajouter une expérience
                        with st.expander("➕ Ajouter une expérience"):
                            col1, col2 = st.columns(2)
                            with col1:
                                new_ent = st.text_input("Entreprise", key="edit_exp_new_ent")
                                new_poste = st.text_input("Poste", key="edit_exp_new_poste")
                            with col2:
                                new_dates = st.text_input("Dates", key="edit_exp_new_dates")
                            if new_ent and new_poste:
                                new_experiences.insert(0, {'entreprise': new_ent, 'poste': new_poste, 'dates': new_dates})
                    
                    # === ONGLET FORMATIONS ===
                    with edit_tabs[3]:
                        st.markdown("**🎓 Formations**")
                        
                        formations = cv_data.get('formations', [])
                        new_formations = []
                        
                        for i, form in enumerate(formations):
                            col1, col2, col3 = st.columns([2, 2, 1])
                            with col1:
                                titre = st.text_input("Diplôme", value=form.get('titre', ''), key=f"edit_form_titre_{i}")
                            with col2:
                                etab = st.text_input("Établissement", value=form.get('etablissement', ''), key=f"edit_form_etab_{i}")
                            with col3:
                                dates = st.text_input("Année", value=form.get('dates', ''), key=f"edit_form_dates_{i}")
                            
                            if titre:
                                new_formations.append({'titre': titre, 'etablissement': etab, 'dates': dates})
                    
                    # === ONGLET STAGES ===
                    with edit_tabs[4]:
                        st.markdown("**📋 Stages CIP**")
                        
                        stages = cv_data.get('stages', [])
                        new_stages = []
                        
                        for i, stage in enumerate(stages):
                            col1, col2, col3 = st.columns([2, 2, 1])
                            with col1:
                                lieu = st.text_input("Lieu", value=stage.get('lieu', ''), key=f"edit_stage_lieu_{i}")
                            with col2:
                                mission = st.text_input("Mission", value=stage.get('mission', ''), key=f"edit_stage_mission_{i}")
                            with col3:
                                dates = st.text_input("Dates", value=stage.get('dates', ''), key=f"edit_stage_dates_{i}")
                            
                            if lieu:
                                new_stages.append({'lieu': lieu, 'mission': mission, 'dates': dates})
                    
                    # === ONGLET BÉNÉVOLAT ===
                    with edit_tabs[5]:
                        st.markdown("**🤝 Missions de bénévolat**")
                        
                        benevolat = cv_data.get('benevolat', [])
                        new_benevolat = []
                        
                        for i, ben in enumerate(benevolat):
                            col1, col2 = st.columns(2)
                            with col1:
                                event = st.text_input("Événement", value=ben.get('evenement', ''), key=f"edit_ben_event_{i}")
                            with col2:
                                role = st.text_input("Rôle", value=ben.get('role', ''), key=f"edit_ben_role_{i}")
                            
                            if event:
                                new_benevolat.append({'evenement': event, 'role': role})
                        
                        # Ajouter
                        col1, col2 = st.columns(2)
                        with col1:
                            new_event = st.text_input("➕ Nouvel événement", key="edit_ben_new_event")
                        with col2:
                            new_role = st.text_input("Rôle", key="edit_ben_new_role")
                        if new_event:
                            new_benevolat.append({'evenement': new_event, 'role': new_role})
                    
                    # === ONGLET INTÉRÊTS ===
                    with edit_tabs[6]:
                        st.markdown("**🎯 Centres d'intérêt**")
                        
                        interets = cv_data.get('interets', [])
                        new_interets = []
                        
                        for i, inter in enumerate(interets):
                            col1, col2 = st.columns(2)
                            with col1:
                                titre = st.text_input("Intérêt", value=inter.get('titre', ''), key=f"edit_int_titre_{i}")
                            with col2:
                                detail = st.text_input("Détail", value=inter.get('detail', ''), key=f"edit_int_detail_{i}")
                            
                            if titre:
                                new_interets.append({'titre': titre, 'detail': detail})
                    
                    st.markdown("---")
                    
                    # === BOUTON APPLIQUER TOUTES LES MODIFICATIONS ===
                    if st.button("✅ Appliquer toutes mes modifications", type="primary", use_container_width=True):
                        apply_full_manual_edits(
                            accroche=new_accroche,
                            qualites=new_qualites,
                            competences=new_competences,
                            experiences=new_experiences,
                            formations=new_formations,
                            stages=new_stages,
                            benevolat=new_benevolat,
                            interets=new_interets
                        )
                        st.rerun()
                    
                    st.caption("💡 Toutes tes modifications seront appliquées au CV et ajoutées à l'historique.")
                
                else:
                    st.info("Génère d'abord un CV pour pouvoir l'éditer manuellement.")


def generate_initial_cv(offre_text: str):
    """Génère la première version du CV adapté."""
    try:
        import json
        from utils.cv_generator import VALERIE_DATA_BASE, render_template, get_density_recommendation
        
        llm = get_llm()
        
        prompt = PROMPT_ADAPTER_CV_TEMPLATE.format(
            offre=offre_text,
            cv=CV_TEXTE_COMPLET
        )
        
        result = llm.generate(
            prompt=prompt,
            system_prompt=SYSTEM_PROMPT_CV,
            max_tokens=2000
        )
        
        # Parser le JSON
        json_match = re.search(r'```json\s*(.*?)\s*```', result, re.DOTALL)
        json_str = json_match.group(1) if json_match else result
        customizations = json.loads(json_str)
        
        # Appliquer les personnalisations
        cv_data = VALERIE_DATA_BASE.copy()
        
        if "accroche" in customizations:
            cv_data["accroche"] = customizations["accroche"]
        if "qualites" in customizations:
            cv_data["qualites"] = customizations["qualites"][:4]
        if "competences_prioritaires" in customizations:
            prioritaires = customizations["competences_prioritaires"]
            autres = [c for c in VALERIE_DATA_BASE["competences"] if c not in prioritaires]
            cv_data["competences"] = prioritaires[:5] + autres[:5]
        
        # Calculer la densité recommandée automatiquement
        preset_name, recommended_density, _ = get_density_recommendation(cv_data)
        st.session_state.cv_density = recommended_density
        
        # Générer le HTML avec la densité appropriée
        html = render_template(cv_data, density=recommended_density)
        
        # Sauvegarder dans session state
        st.session_state.cv_html_preview = html
        st.session_state.cv_customizations = customizations
        st.session_state.cv_current_data = cv_data
        st.session_state.cv_version = 1
        st.session_state.cv_modifications_history = [{
            'version': 1,
            'demande': 'Génération initiale basée sur l\'offre',
            'resultat': f"Mots-clés détectés: {', '.join(customizations.get('mots_cles_offre', []))}"
        }]
        st.session_state.cv_chat_history = []
        
    except Exception as e:
        st.error(f"❌ Erreur: {e}")


def apply_cv_feedback(feedback: str):
    """Applique un feedback utilisateur pour modifier TOUT le CV."""
    try:
        import json
        from utils.cv_generator import VALERIE_DATA_BASE, render_template
        
        llm = get_llm()
        
        # Récupérer les données actuelles du CV
        cv_data = st.session_state.cv_current_data or VALERIE_DATA_BASE.copy()
        
        # Construire le contexte avec toutes les données du CV
        cv_data_str = json.dumps({
            'accroche': cv_data.get('accroche', ''),
            'qualites': cv_data.get('qualites', []),
            'competences': cv_data.get('competences', []),
            'experiences': cv_data.get('experiences', []),
            'stages': cv_data.get('stages', []),
            'benevolat': cv_data.get('benevolat', []),
            'interets': cv_data.get('interets', [])
        }, ensure_ascii=False, indent=2)
        
        # Utiliser le nouveau prompt complet
        prompt = PROMPT_MODIFIER_CV_COMPLET.format(
            cv_data=cv_data_str,
            offre=st.session_state.cv_offre_text[:3000],
            demande=feedback
        )
        
        result = llm.generate(
            prompt=prompt,
            system_prompt=SYSTEM_PROMPT_CV,
            max_tokens=4000
        )
        
        # Parser le JSON
        json_match = re.search(r'```json\s*(.*?)\s*```', result, re.DOTALL)
        json_str = json_match.group(1) if json_match else result
        new_data = json.loads(json_str)
        
        # Appliquer TOUTES les modifications au cv_data
        if "accroche" in new_data:
            cv_data["accroche"] = new_data["accroche"]
        if "qualites" in new_data:
            cv_data["qualites"] = new_data["qualites"][:4]
        if "competences" in new_data:
            cv_data["competences"] = new_data["competences"]
        if "experiences" in new_data:
            cv_data["experiences"] = new_data["experiences"]
        if "stages" in new_data:
            cv_data["stages"] = new_data["stages"]
        if "benevolat" in new_data:
            cv_data["benevolat"] = new_data["benevolat"]
        if "interets" in new_data:
            cv_data["interets"] = new_data["interets"]
        
        # Générer le HTML avec la densité actuelle
        current_density = st.session_state.get('cv_density', 50)
        html = render_template(cv_data, density=current_density)
        
        # Incrémenter la version
        st.session_state.cv_version = st.session_state.get('cv_version', 1) + 1
        
        # Ajouter à l'historique des modifications
        sections_modifiees = new_data.get('sections_modifiees', [])
        modification_msg = new_data.get('modification_appliquee', 'Modifications appliquées')
        
        # Mettre à jour les customizations
        new_customizations = {
            'accroche': cv_data.get('accroche', ''),
            'qualites': cv_data.get('qualites', []),
            'competences_prioritaires': cv_data.get('competences', [])[:5],
            'mots_cles_offre': new_data.get('mots_cles_offre', []),
            'modification_appliquee': modification_msg,
            'sections_modifiees': sections_modifiees
        }
        
        if 'cv_modifications_history' not in st.session_state:
            st.session_state.cv_modifications_history = []
        
        st.session_state.cv_modifications_history.append({
            'version': st.session_state.cv_version,
            'demande': feedback,
            'resultat': modification_msg
        })
        
        # Mettre à jour le session state
        st.session_state.cv_html_preview = html
        st.session_state.cv_customizations = new_customizations
        st.session_state.cv_current_data = cv_data
        
    except json.JSONDecodeError as e:
        st.error("❌ Erreur de parsing. Réessaie avec une demande plus simple.")
    except Exception as e:
        st.error(f"❌ Erreur: {str(e)}")


def apply_full_manual_edits(
    accroche: str,
    qualites: list,
    competences: list,
    experiences: list,
    formations: list,
    stages: list,
    benevolat: list,
    interets: list
):
    """Applique TOUTES les modifications manuelles de l'utilisateur au CV."""
    try:
        from utils.cv_generator import VALERIE_DATA_BASE, render_template
        
        # Convertir l'accroche (remplacer **mot** par les spans HTML)
        accroche_html = accroche
        accroche_html = re.sub(r'\*\*(.+?)\*\*', r"<span class='accroche-highlight'>\1</span>", accroche_html)
        
        # Construire le nouveau cv_data complet
        cv_data = VALERIE_DATA_BASE.copy()
        
        # Appliquer toutes les modifications
        cv_data["accroche"] = accroche_html
        cv_data["qualites"] = qualites[:4] if qualites else cv_data.get('qualites', [])
        cv_data["competences"] = competences if competences else cv_data.get('competences', [])
        cv_data["experiences"] = experiences if experiences else cv_data.get('experiences', [])
        cv_data["formations"] = formations if formations else cv_data.get('formations', [])
        cv_data["stages"] = stages if stages else cv_data.get('stages', [])
        cv_data["benevolat"] = benevolat if benevolat else cv_data.get('benevolat', [])
        cv_data["interets"] = interets if interets else cv_data.get('interets', [])
        
        # Générer le HTML avec la densité actuelle
        current_density = st.session_state.get('cv_density', 50)
        html = render_template(cv_data, density=current_density)
        
        # Mettre à jour les customizations
        current_cust = st.session_state.cv_customizations or {}
        new_customizations = {
            **current_cust,
            'accroche': accroche_html,
            'qualites': qualites[:4],
            'competences_prioritaires': competences[:5] if competences else [],
            'modification_appliquee': 'Édition manuelle complète'
        }
        
        # Incrémenter la version
        st.session_state.cv_version = st.session_state.get('cv_version', 1) + 1
        
        # Ajouter à l'historique
        if 'cv_modifications_history' not in st.session_state:
            st.session_state.cv_modifications_history = []
        
        # Compter les sections modifiées
        sections_modifiees = []
        if accroche: sections_modifiees.append("accroche")
        if qualites: sections_modifiees.append("qualités")
        if competences: sections_modifiees.append("compétences")
        if experiences: sections_modifiees.append("expériences")
        if formations: sections_modifiees.append("formations")
        if stages: sections_modifiees.append("stages")
        if benevolat: sections_modifiees.append("bénévolat")
        if interets: sections_modifiees.append("intérêts")
        
        st.session_state.cv_modifications_history.append({
            'version': st.session_state.cv_version,
            'demande': '✏️ Édition manuelle complète',
            'resultat': f"Sections modifiées: {', '.join(sections_modifiees)}"
        })
        
        # Mettre à jour le session state
        st.session_state.cv_html_preview = html
        st.session_state.cv_customizations = new_customizations
        st.session_state.cv_current_data = cv_data
        
        st.success("✅ Toutes les modifications ont été appliquées !")
        
    except Exception as e:
        st.error(f"❌ Erreur: {str(e)}")


def save_cv_to_supabase(titre: str = None, entreprise: str = None, candidature_id: str = None, create_candidature: bool = False):
    """Sauvegarde le CV personnalisé actuel dans Supabase."""
    try:
        supabase = get_supabase_client()
        
        offre_text = st.session_state.get('cv_offre_text', '')
        customizations = st.session_state.get('cv_customizations', {})
        
        # Utiliser les valeurs fournies ou détecter automatiquement
        if not titre:
            titre = customizations.get('mots_cles_offre', ['CV Personnalisé'])[0] if customizations.get('mots_cles_offre') else "CV Personnalisé"
        
        if not entreprise:
            entreprise = "Non spécifié"
            if "france travail" in offre_text.lower():
                entreprise = "France Travail"
        
        # Créer une nouvelle candidature si demandé
        if create_candidature:
            candidature_result = supabase.save_candidature(
                titre_poste=titre,
                entreprise=entreprise,
                offre_texte=offre_text,
                cv_adapte=st.session_state.get('cv_html_preview', ''),
                notes="CV créé via CV Personnalisé"
            )
            if candidature_result:
                candidature_id = candidature_result.get('id')
                st.info(f"📋 Nouvelle candidature créée : {titre}")
        
        # Sauvegarder le CV
        result = supabase.save_cv_personnalise(
            titre_offre=titre,
            entreprise=entreprise,
            offre_texte=offre_text,
            customizations=customizations,
            html_content=st.session_state.get('cv_html_preview', ''),
            chat_history=st.session_state.get('cv_chat_history', []),
            candidature_id=candidature_id
        )
        
        if result:
            st.session_state.cv_saved_id = result.get('id')
            msg = f"✅ CV sauvegardé ! (ID: {result.get('id')})"
            if candidature_id:
                msg += f" • Lié à la candidature"
            st.success(msg)
        else:
            st.warning("⚠️ Sauvegarde non disponible (Supabase désactivé)")
            
    except Exception as e:
        st.error(f"❌ Erreur sauvegarde: {e}")


def render_saved_cvs():
    """Affiche les CV personnalisés sauvegardés."""
    try:
        supabase = get_supabase_client()
        cvs = supabase.get_cv_personnalises(limit=10)
        
        if not cvs:
            st.info("Aucun CV sauvegardé pour le moment")
            return
        
        for cv in cvs:
            col1, col2, col3 = st.columns([3, 1, 1])
            
            with col1:
                titre = cv.get('titre_offre', 'Sans titre')
                entreprise = cv.get('entreprise', '')
                date = cv.get('created_at', '')[:10] if cv.get('created_at') else ''
                version = cv.get('version', 1)
                
                st.markdown(f"**{titre}** - {entreprise}")
                st.caption(f"📅 {date} • v{version}")
            
            with col2:
                if st.button("📂 Charger", key=f"load_cv_{cv['id']}", use_container_width=True):
                    load_saved_cv(cv)
                    st.rerun()
            
            with col3:
                if st.button("🗑️", key=f"del_cv_{cv['id']}", use_container_width=True):
                    supabase.delete_cv_personnalise(cv['id'])
                    st.rerun()
            
            st.markdown("---")
            
    except Exception as e:
        st.error(f"Erreur: {e}")


def load_saved_cv(cv_data: dict):
    """Charge un CV sauvegardé dans la session."""
    import json
    
    try:
        # Charger les customizations
        customizations = cv_data.get('customizations')
        if isinstance(customizations, str):
            customizations = json.loads(customizations)
        
        # Charger l'historique du chat
        chat_history = cv_data.get('chat_history')
        if isinstance(chat_history, str):
            chat_history = json.loads(chat_history)
        
        # Régénérer le HTML si nécessaire
        html_content = cv_data.get('html_content', '')
        
        if not html_content and customizations:
            from utils.cv_generator import VALERIE_DATA_BASE, render_template
            
            cv_data_template = VALERIE_DATA_BASE.copy()
            if "accroche" in customizations:
                cv_data_template["accroche"] = customizations["accroche"]
            if "qualites" in customizations:
                cv_data_template["qualites"] = customizations["qualites"][:4]
            if "competences_prioritaires" in customizations:
                prioritaires = customizations["competences_prioritaires"]
                autres = [c for c in VALERIE_DATA_BASE["competences"] if c not in prioritaires]
                cv_data_template["competences"] = prioritaires[:5] + autres[:5]
            
            html_content = render_template(cv_data_template)
        
        # Mettre à jour le session state
        st.session_state.cv_html_preview = html_content
        st.session_state.cv_customizations = customizations or {}
        st.session_state.cv_chat_history = chat_history or []
        st.session_state.cv_offre_text = cv_data.get('offre_texte', '')
        st.session_state.cv_current_data = True
        st.session_state.cv_saved_id = cv_data.get('id')
        
        st.success(f"✅ CV chargé: {cv_data.get('titre_offre', 'Sans titre')}")
        
    except Exception as e:
        st.error(f"Erreur chargement: {e}")


def render_linkedin():
    """Page de génération de posts LinkedIn."""
    render_header()
    
    st.markdown("## 💼 Générateur de Posts LinkedIn")
    st.markdown("""
    Crée des posts LinkedIn percutants qui reflètent ton style unique et renforcent ton personal branding 
    dans le domaine de l'insertion professionnelle et du socio-sport.
    """)
    
    # Thèmes suggérés basés sur son profil
    st.markdown("### 🎯 Thèmes suggérés")
    
    themes_suggeres = [
        "🏃 Retour d'expérience sur un événement sport-emploi",
        "🌟 Partage d'une réussite d'accompagnement",
        "💡 Réflexion sur l'insertion professionnelle",
        "🤝 Mise en avant d'un partenariat ou collaboration",
        "🏆 Actualité du club de triathlon",
        "📚 Apprentissage ou formation récente",
        "🎯 Témoignage inspirant d'un parcours"
    ]
    
    cols = st.columns(3)
    selected_theme = None
    for i, theme in enumerate(themes_suggeres):
        with cols[i % 3]:
            if st.button(theme, key=f"theme_{i}", use_container_width=True):
                selected_theme = theme
    
    st.markdown("---")
    
    # Formulaire de création
    st.markdown("### ✍️ Créer ton post")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        sujet = st.text_input(
            "📌 Sujet du post",
            value=selected_theme.replace("🏃 ", "").replace("🌟 ", "").replace("💡 ", "").replace("🤝 ", "").replace("🏆 ", "").replace("📚 ", "").replace("🎯 ", "") if selected_theme else "",
            placeholder="Ex: Mon expérience au Stade vers l'Emploi de novembre"
        )
        
        contexte = st.text_area(
            "📝 Contexte et détails (optionnel)",
            placeholder="Ajoute des détails spécifiques : événement, personnes impliquées, résultats, ressenti...",
            height=150
        )
    
    with col2:
        st.markdown("#### 💫 Ton style LinkedIn")
        st.markdown("""
        <div style="background: rgba(124, 58, 237, 0.1); padding: 1rem; border-radius: 10px; font-size: 0.85rem;">
        <b>Emojis favoris :</b><br/>
        💥 💫 ✨ 💪 🤝 🏊 🚴 🏃<br/><br/>
        <b>Hashtags récurrents :</b><br/>
        #InsertionProfessionnelle<br/>
        #SportEtInsertion<br/>
        #Inclusion<br/>
        #FranceTravail<br/>
        #SocioSport
        </div>
        """, unsafe_allow_html=True)
        
        # Options de style
        st.markdown("#### ⚙️ Options")
        tone = st.selectbox(
            "Ton du post",
            ["Inspirant", "Informatif", "Personnel", "Professionnel", "Célébration"]
        )
        longueur = st.selectbox(
            "Longueur",
            ["Optimal (1000-1500 car.)", "Court (< 800 car.)", "Long (> 1500 car.)"]
        )
    
    # Bouton de génération
    if st.button("✨ Générer le post LinkedIn", type="primary", use_container_width=True):
        if not sujet:
            st.warning("⚠️ Merci d'indiquer le sujet du post")
        else:
            with st.spinner("💫 Création de ton post LinkedIn..."):
                try:
                    client = LLMClient()
                    
                    prompt = PROMPT_LINKEDIN_POST.format(
                        sujet=sujet,
                        contexte=f"{contexte}\n\nTon souhaité: {tone}\nLongueur: {longueur}" if contexte else f"Ton souhaité: {tone}\nLongueur: {longueur}",
                        cv=CV_TEXTE_COMPLET
                    )
                    
                    result = client.generate(
                        prompt=prompt,
                        system_prompt=SYSTEM_PROMPT_LINKEDIN,
                        max_tokens=3000
                    )
                    
                    st.session_state.linkedin_result = result
                    
                except Exception as e:
                    st.error(f"❌ Erreur lors de la génération : {str(e)}")
    
    # Affichage du résultat
    if 'linkedin_result' in st.session_state and st.session_state.linkedin_result:
        st.markdown("---")
        st.markdown("### 📱 Ton post LinkedIn")
        
        # Afficher le résultat dans un container stylisé
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, rgba(10, 102, 194, 0.1) 0%, rgba(30, 41, 59, 0.9) 100%); 
                    border: 1px solid rgba(10, 102, 194, 0.3); border-radius: 12px; padding: 1.5rem; margin-bottom: 1rem;">
            <div style="display: flex; align-items: center; gap: 0.5rem; margin-bottom: 1rem;">
                <img src="https://content.linkedin.com/content/dam/me/business/en-us/amp/brand-site/v2/bg/LI-Bug.svg.original.svg" 
                     style="width: 24px; height: 24px;" />
                <span style="color: #0a66c2; font-weight: 600;">LinkedIn</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown(st.session_state.linkedin_result)
        
        # Boutons d'action
        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button("📋 Copier le post", use_container_width=True):
                st.info("💡 Sélectionne et copie le texte ci-dessus")
        with col2:
            if st.button("🔄 Régénérer", use_container_width=True):
                del st.session_state.linkedin_result
                st.rerun()
        with col3:
            if st.button("💾 Sauvegarder", use_container_width=True):
                supabase = get_supabase_client()
                
                # Sauvegarder dans Supabase si disponible
                if supabase.enabled:
                    result = supabase.save_linkedin_post(
                        sujet=sujet,
                        contenu=st.session_state.linkedin_result,
                        tone=tone
                    )
                    if result:
                        st.success("✅ Post sauvegardé dans Supabase !")
                    else:
                        st.error("❌ Erreur lors de la sauvegarde")
                else:
                    # Fallback session state
                    if 'linkedin_posts' not in st.session_state:
                        st.session_state.linkedin_posts = []
                    st.session_state.linkedin_posts.append({
                        'date': datetime.now().isoformat(),
                        'sujet': sujet,
                        'contenu': st.session_state.linkedin_result
                    })
                    st.success("✅ Post sauvegardé !")
    
    # Historique des posts (depuis Supabase ou session)
    st.markdown("---")
    supabase = get_supabase_client()
    
    if supabase.enabled:
        saved_posts = supabase.get_linkedin_posts(limit=10)
    else:
        saved_posts = st.session_state.get('linkedin_posts', [])
    
    if saved_posts:
        with st.expander("📚 Historique de mes posts", expanded=False):
            for post in saved_posts:
                date_str = post.get('created_at', post.get('date', ''))[:10] if post.get('created_at') or post.get('date') else ''
                publie_badge = "✅ Publié" if post.get('publie') else "📝 Brouillon"
                
                st.markdown(f"**{post.get('sujet', 'Sans sujet')}** - {date_str} | {publie_badge}")
                
                with st.container():
                    st.markdown(post.get('contenu', '')[:300] + "..." if len(post.get('contenu', '')) > 300 else post.get('contenu', ''))
                    
                    # Bouton pour marquer comme publié
                    if supabase.enabled and not post.get('publie') and post.get('id'):
                        if st.button(f"✅ Marquer comme publié", key=f"publish_{post.get('id')}"):
                            if supabase.mark_post_published(post.get('id')):
                                st.success("Marqué comme publié !")
                                st.rerun()
                
                st.markdown("---")


def render_coach():
    """Page de conversation avec le coach IA - Version améliorée avec streaming et PDF."""
    st.markdown("## 💬 Ton Coach IA Personnel")
    st.markdown("Pose-moi toutes tes questions sur ta recherche d'emploi ! Tu peux aussi m'envoyer des documents PDF à analyser.")
    
    # Initialiser l'historique du chat si nécessaire
    if 'chat_initialized' not in st.session_state:
        loaded_messages, loaded_docs = load_chat_history()
        if loaded_messages:
            st.session_state.chat_messages = loaded_messages
            st.session_state.chat_uploaded_docs = loaded_docs
        st.session_state.chat_initialized = True
    
    if 'chat_uploaded_docs' not in st.session_state:
        st.session_state.chat_uploaded_docs = []
    
    # Layout en 2 colonnes : chat principal + panneau latéral
    col_chat, col_docs = st.columns([3, 1])
    
    with col_docs:
        st.markdown("### 📎 Documents")
        
        # Upload de PDF
        uploaded_pdf = st.file_uploader(
            "Ajouter un PDF",
            type=['pdf'],
            key="chat_pdf_upload",
            help="Upload une offre d'emploi ou tout autre document à analyser"
        )
        
        if uploaded_pdf:
            # Extraire le texte du PDF
            pdf_text = extract_text_from_pdf(uploaded_pdf)
            if pdf_text and len(pdf_text) > 50:
                doc_info = {
                    'name': uploaded_pdf.name,
                    'content': pdf_text[:10000],  # Limiter la taille
                    'date': datetime.now().strftime('%H:%M')
                }
                # Éviter les doublons
                if not any(d['name'] == doc_info['name'] for d in st.session_state.chat_uploaded_docs):
                    st.session_state.chat_uploaded_docs.append(doc_info)
                    # Sauvegarder dans Supabase + local
                    save_chat_document_to_db(uploaded_pdf.name, pdf_text[:10000])
                    save_chat_history()
                    st.success(f"✅ {uploaded_pdf.name} ajouté !")
        
        # Liste des documents uploadés
        if st.session_state.chat_uploaded_docs:
            st.markdown("**Documents en contexte :**")
            for i, doc in enumerate(st.session_state.chat_uploaded_docs):
                col1, col2 = st.columns([4, 1])
                with col1:
                    st.markdown(f"📄 {doc['name'][:20]}...")
                with col2:
                    if st.button("❌", key=f"remove_doc_{i}"):
                        st.session_state.chat_uploaded_docs.pop(i)
                        save_chat_history()
                        st.rerun()
        
        st.markdown("---")
        
        # Suggestions de questions
        st.markdown("### 💡 Questions rapides")
        suggestions = [
            "Comment valoriser ma reconversion ?",
            "Mes 3 meilleurs arguments ?",
            "Reformule mon accroche",
            "Analyse ce document",
            "Prépare-moi pour l'entretien",
            "Points faibles à anticiper"
        ]
        
        for suggestion in suggestions:
            if st.button(suggestion, key=f"sugg_{suggestion[:10]}", use_container_width=True):
                st.session_state.chat_messages.append({
                    "role": "user",
                    "content": suggestion
                })
                st.rerun()
    
    with col_chat:
        # Container pour les messages avec hauteur fixe et scroll
        chat_container = st.container(height=500)
        
        with chat_container:
            # Message de bienvenue si chat vide
            if not st.session_state.chat_messages:
                st.markdown("""
                <div style="text-align: center; padding: 2rem; color: #94a3b8;">
                    <div style="font-size: 3rem; margin-bottom: 1rem;">👋</div>
                    <p style="font-size: 1.1rem;">Salut Valérie ! Je suis ton coach personnel.</p>
                    <p>Tu peux me poser toutes tes questions sur ta recherche d'emploi.</p>
                    <p style="font-size: 0.9rem; margin-top: 1rem;">
                        💡 <em>Tu peux aussi uploader des PDF (offres d'emploi, fiches de poste) pour que je les analyse !</em>
                    </p>
                </div>
                """, unsafe_allow_html=True)
            
            # Afficher les messages
            for i, msg in enumerate(st.session_state.chat_messages):
                if msg["role"] == "user":
                    with st.chat_message("user", avatar="👩"):
                        st.markdown(msg["content"])
                else:
                    with st.chat_message("assistant", avatar="🤖"):
                        st.markdown(msg["content"])
        
        # Traiter le dernier message si c'est un message utilisateur sans réponse
        if st.session_state.chat_messages and st.session_state.chat_messages[-1]["role"] == "user":
            llm = get_llm()
            
            # Construire le contexte avec les documents uploadés
            docs_context = ""
            if st.session_state.chat_uploaded_docs:
                docs_context = "\n\n--- DOCUMENTS FOURNIS PAR VALÉRIE ---\n"
                for doc in st.session_state.chat_uploaded_docs:
                    docs_context += f"\n📄 {doc['name']}:\n{doc['content'][:5000]}\n"
                docs_context += "\n--- FIN DES DOCUMENTS ---\n"
            
            # Construire l'historique pour le contexte
            messages = []
            for msg in st.session_state.chat_messages[-12:]:  # Garder les 12 derniers
                messages.append({
                    "role": msg["role"],
                    "content": msg["content"]
                })
            
            # Générer la réponse en streaming
            system = SYSTEM_PROMPT_COACH + f"\n\nCV de Valérie :\n{CV_TEXTE_COMPLET}" + docs_context
            
            with st.chat_message("assistant", avatar="🤖"):
                response_placeholder = st.empty()
                full_response = ""
                
                # Streaming de la réponse
                for chunk in llm.chat_stream(
                    messages=messages,
                    system_prompt=system,
                    max_tokens=3000
                ):
                    full_response += chunk
                    response_placeholder.markdown(full_response + "▌")
                
                response_placeholder.markdown(full_response)
            
            # Sauvegarder la réponse
            st.session_state.chat_messages.append({
                "role": "assistant",
                "content": full_response
            })
            # Sauvegarder dans Supabase + local
            save_chat_message_to_db("assistant", full_response)
            save_chat_history()
            st.rerun()
        
        # Zone d'input en bas
        st.markdown("---")
        
        # Input avec chat_input pour une meilleure UX
        user_input = st.chat_input("Pose ta question ici...", key="chat_input_main")
        
        if user_input:
            st.session_state.chat_messages.append({
                "role": "user",
                "content": user_input
            })
            # Sauvegarder dans Supabase + local
            save_chat_message_to_db("user", user_input)
            save_chat_history()
            st.rerun()
        
        # Boutons d'action
        col1, col2, col3 = st.columns(3)
        with col1:
            if st.session_state.chat_messages:
                if st.button("🗑️ Effacer le chat", use_container_width=True):
                    st.session_state.chat_messages = []
                    st.session_state.chat_uploaded_docs = []
                    # Effacer de Supabase + local
                    clear_chat_from_db()
                    save_chat_history()
                    st.rerun()
        with col2:
            if st.session_state.chat_messages:
                # Export de la conversation
                chat_export = "\n\n".join([
                    f"{'VALÉRIE' if m['role'] == 'user' else 'COACH IA'}: {m['content']}"
                    for m in st.session_state.chat_messages
                ])
                st.download_button(
                    "📥 Exporter",
                    data=chat_export,
                    file_name=f"conversation_{datetime.now().strftime('%Y%m%d_%H%M')}.txt",
                    mime="text/plain",
                    use_container_width=True
                )
        with col3:
            if st.session_state.chat_uploaded_docs:
                st.markdown(f"📎 {len(st.session_state.chat_uploaded_docs)} doc(s)")


def render_historique():
    """Page d'historique des candidatures avec tracking et dashboard."""
    render_header()
    
    st.markdown("## 📚 Suivi des Candidatures")
    
    # Explication du fonctionnement
    with st.expander("ℹ️ Comment ça fonctionne ?", expanded=False):
        st.markdown("""
        **🔄 Synchronisation automatique :**
        
        Toutes tes candidatures sont automatiquement synchronisées ici quand tu :
        - ✅ Sauvegardes un **CV Personnalisé** (avec option de liaison)
        - ✅ Sauvegardes une **Lettre de motivation** ou **Préparation entretien**
        
        **📊 Dashboard :**
        - Vois tes statistiques en temps réel
        - Suis l'évolution de chaque candidature
        - Ajoute des événements (relances, entretiens, etc.)
        - Définis des rappels
        
        **💡 Astuce :** Les CV personnalisés liés à une candidature apparaissent dans l'onglet CV de chaque candidature.
        """)
    
    supabase = get_supabase_client()
    
    # =========================================================================
    # DASHBOARD STATISTIQUES
    # =========================================================================
    
    if supabase.enabled:
        stats = supabase.get_candidatures_stats()
        
        st.markdown("### 📊 Dashboard")
        
        cols = st.columns(6)
        
        metrics = [
            ("Total", stats.get("total", 0), "📋"),
            ("En cours", stats.get("en_cours", 0), "⏳"),
            ("Envoyées", stats.get("envoyees", 0), "📤"),
            ("Entretiens", stats.get("entretiens", 0), "🎤"),
            ("Refusées", stats.get("refusees", 0), "❌"),
            ("Acceptées", stats.get("acceptees", 0), "✅")
        ]
        
        for col, (label, value, icon) in zip(cols, metrics):
            with col:
                st.markdown(f"""
                <div style="background: rgba(30, 41, 59, 0.8); padding: 1rem; border-radius: 10px; text-align: center;">
                    <div style="font-size: 1.5rem;">{icon}</div>
                    <div style="font-size: 1.8rem; font-weight: 700; color: #60a5fa;">{value}</div>
                    <div style="font-size: 0.75rem; color: #94a3b8;">{label}</div>
                </div>
                """, unsafe_allow_html=True)
        
        # Rappels à venir
        reminders = supabase.get_upcoming_reminders(days=7)
        if reminders:
            st.markdown("### ⏰ Rappels à venir (7 jours)")
            for reminder in reminders:
                candidature_info = reminder.get("candidatures", {})
                rappel_date = reminder.get("rappel_date", "")[:10] if reminder.get("rappel_date") else "Non défini"
                st.warning(f"📅 **{rappel_date}** - {reminder.get('type_event', '')} : {candidature_info.get('titre_poste', '')} @ {candidature_info.get('entreprise', '')}")
        
        st.markdown("---")
    
    # =========================================================================
    # LISTE DES CANDIDATURES
    # =========================================================================
    
    # Charger les candidatures
    if supabase.enabled:
        candidatures = supabase.get_candidatures(limit=50)
    else:
        candidatures = load_historique()
    
    if not candidatures:
        st.info("📭 Aucune candidature sauvegardée pour le moment.")
        st.markdown("Utilise les outils de génération (CV, lettre, etc.) puis sauvegarde tes candidatures !")
        return
    
    # Filtres
    col1, col2 = st.columns([1, 3])
    with col1:
        filtre_statut = st.selectbox(
            "Filtrer par statut",
            ["Tous", "en_cours", "envoyee", "entretien", "refusee", "acceptee"],
            format_func=lambda x: {
                "Tous": "📋 Tous",
                "en_cours": "⏳ En cours",
                "envoyee": "📤 Envoyée",
                "entretien": "🎤 Entretien",
                "refusee": "❌ Refusée",
                "acceptee": "✅ Acceptée"
            }.get(x, x)
        )
    
    # Filtrer si nécessaire
    if filtre_statut != "Tous":
        candidatures = [c for c in candidatures if c.get("statut") == filtre_statut]
    
    st.markdown(f"### 📁 {len(candidatures)} candidature(s)")
    
    for cand in candidatures:
        cand_id = cand.get("id")
        titre = cand.get('titre_poste', 'Sans titre')
        entreprise = cand.get('entreprise', 'Non précisée')
        statut = cand.get('statut', 'en_cours')
        date_creation = cand.get('created_at', cand.get('date', ''))[:10] if cand.get('created_at') or cand.get('date') else ''
        
        # Badge de statut
        statut_badges = {
            "en_cours": ("⏳ En cours", "#f59e0b"),
            "envoyee": ("📤 Envoyée", "#3b82f6"),
            "entretien": ("🎤 Entretien", "#8b5cf6"),
            "refusee": ("❌ Refusée", "#ef4444"),
            "acceptee": ("✅ Acceptée", "#10b981")
        }
        badge_text, badge_color = statut_badges.get(statut, ("❓ Inconnu", "#6b7280"))
        
        with st.expander(f"**{titre}** - {entreprise} | {badge_text} | {date_creation}"):
            
            # Onglets de la candidature
            tabs = st.tabs(["📊 Suivi", "📄 CV", "✉️ Lettre", "🎤 Entretien", "✉️ Emails"])
            
            # TAB SUIVI
            with tabs[0]:
                col1, col2 = st.columns([1, 2])
                
                with col1:
                    # Changer le statut
                    new_statut = st.selectbox(
                        "Statut",
                        ["en_cours", "envoyee", "entretien", "refusee", "acceptee"],
                        index=["en_cours", "envoyee", "entretien", "refusee", "acceptee"].index(statut) if statut in ["en_cours", "envoyee", "entretien", "refusee", "acceptee"] else 0,
                        key=f"statut_{cand_id}",
                        format_func=lambda x: statut_badges.get(x, (x, ""))[0]
                    )
                    
                    if new_statut != statut and supabase.enabled:
                        if st.button("💾 Mettre à jour", key=f"update_statut_{cand_id}"):
                            if supabase.update_candidature_statut(cand_id, new_statut):
                                st.success("✅ Statut mis à jour !")
                                st.rerun()
                
                with col2:
                    # Ajouter un événement
                    st.markdown("**Ajouter un événement**")
                    
                    event_type = st.selectbox(
                        "Type",
                        ["envoi", "relance", "appel", "entretien_tel", "entretien_physique", "entretien_video", "test_technique", "reponse_negative", "reponse_positive", "offre", "note"],
                        format_func=lambda x: {
                            "envoi": "📤 Envoi candidature",
                            "relance": "🔄 Relance",
                            "appel": "📞 Appel",
                            "entretien_tel": "📱 Entretien téléphonique",
                            "entretien_physique": "🏢 Entretien physique",
                            "entretien_video": "💻 Entretien vidéo",
                            "test_technique": "📝 Test technique",
                            "reponse_negative": "❌ Réponse négative",
                            "reponse_positive": "✅ Réponse positive",
                            "offre": "🎉 Offre reçue",
                            "note": "📌 Note"
                        }.get(x, x),
                        key=f"event_type_{cand_id}"
                    )
                    
                    event_desc = st.text_input("Description", key=f"event_desc_{cand_id}", placeholder="Ex: Échangé avec Mme Dupont, RDV prévu le...")
                    
                    col_a, col_b = st.columns(2)
                    with col_a:
                        rappel = st.checkbox("Définir un rappel", key=f"rappel_check_{cand_id}")
                    with col_b:
                        if rappel:
                            rappel_date = st.date_input("Date de rappel", key=f"rappel_date_{cand_id}")
                    
                    if st.button("➕ Ajouter l'événement", key=f"add_event_{cand_id}"):
                        if supabase.enabled:
                            rappel_iso = rappel_date.isoformat() if rappel and 'rappel_date' in dir() else None
                            result = supabase.add_candidature_event(
                                candidature_id=cand_id,
                                type_event=event_type,
                                description=event_desc if event_desc else None,
                                rappel_date=rappel_iso
                            )
                            if result:
                                st.success("✅ Événement ajouté !")
                                st.rerun()
                            else:
                                st.error("❌ Erreur lors de l'ajout")
                
                # Timeline des événements
                if supabase.enabled and cand_id:
                    events = supabase.get_candidature_events(cand_id)
                    if events:
                        st.markdown("---")
                        st.markdown("**📅 Historique**")
                        for event in events:
                            event_date = event.get("date_event", "")[:10] if event.get("date_event") else ""
                            event_icon = {
                                "envoi": "📤", "relance": "🔄", "appel": "📞",
                                "entretien_tel": "📱", "entretien_physique": "🏢",
                                "entretien_video": "💻", "test_technique": "📝",
                                "reponse_negative": "❌", "reponse_positive": "✅",
                                "offre": "🎉", "note": "📌"
                            }.get(event.get("type_event"), "•")
                            
                            desc = f" - {event.get('description')}" if event.get('description') else ""
                            st.markdown(f"{event_icon} **{event_date}** : {event.get('type_event', '')}{desc}")
            
            # TAB CV
            with tabs[1]:
                # Afficher les CV personnalisés liés
                if supabase.enabled and cand_id:
                    cvs_lies = supabase.get_cvs_for_candidature(cand_id)
                    
                    if cvs_lies:
                        st.markdown("**🎨 CV Personnalisés liés:**")
                        for cv_lie in cvs_lies:
                            cv_col1, cv_col2, cv_col3 = st.columns([3, 1, 1])
                            with cv_col1:
                                st.markdown(f"📄 {cv_lie.get('titre_offre', 'Sans titre')} (v{cv_lie.get('version', 1)})")
                            with cv_col2:
                                cv_date = cv_lie.get('created_at', '')[:10] if cv_lie.get('created_at') else ''
                                st.caption(cv_date)
                            with cv_col3:
                                if st.button("👁️", key=f"view_cv_{cv_lie['id']}_{cand_id}"):
                                    # Charger et afficher le CV
                                    cv_full = supabase.get_cv_personnalise(cv_lie['id'])
                                    if cv_full and cv_full.get('html_content'):
                                        st.session_state[f'show_cv_popup_{cv_lie["id"]}'] = True
                        
                        # Afficher le popup du CV si demandé
                        for cv_lie in cvs_lies:
                            if st.session_state.get(f'show_cv_popup_{cv_lie["id"]}'):
                                cv_full = supabase.get_cv_personnalise(cv_lie['id'])
                                if cv_full and cv_full.get('html_content'):
                                    import streamlit.components.v1 as components
                                    components.html(cv_full['html_content'], height=600, scrolling=True)
                                    if st.button("Fermer", key=f"close_cv_{cv_lie['id']}"):
                                        st.session_state[f'show_cv_popup_{cv_lie["id"]}'] = False
                                        st.rerun()
                        
                        st.markdown("---")
                
                # Afficher aussi le CV texte classique
                if cand.get('cv_adapte'):
                    with st.expander("📝 CV texte (ancien format)", expanded=False):
                        st.markdown(cand['cv_adapte'])
                elif not cvs_lies:
                    st.info("Pas de CV généré pour cette candidature")
                    if st.button("🎨 Créer un CV personnalisé", key=f"create_cv_{cand_id}"):
                        st.session_state.current_page = 'cv_perso'
                        st.rerun()
            
            # TAB LETTRE
            with tabs[2]:
                if cand.get('lettre_motivation'):
                    st.markdown(cand['lettre_motivation'])
                else:
                    st.info("Pas de lettre générée pour cette candidature")
            
            # TAB ENTRETIEN
            with tabs[3]:
                if cand.get('preparation_entretien'):
                    st.markdown(cand['preparation_entretien'])
                else:
                    st.info("Pas de préparation d'entretien pour cette candidature")
            
            # TAB EMAILS
            with tabs[4]:
                st.markdown("**📧 Générer un email**")
                
                # Charger les templates
                templates = []
                if supabase.enabled:
                    templates = supabase.get_email_templates()
                
                if templates:
                    template_choice = st.selectbox(
                        "Choisir un template",
                        templates,
                        format_func=lambda t: t.get("nom", "Sans nom"),
                        key=f"template_{cand_id}"
                    )
                    
                    if template_choice:
                        # Variables du template
                        variables = template_choice.get("variables", [])
                        var_values = {}
                        
                        st.markdown("**Variables à personnaliser :**")
                        for var in variables:
                            default_value = ""
                            if var == "poste":
                                default_value = titre
                            elif var == "entreprise":
                                default_value = entreprise
                            
                            var_values[var] = st.text_input(
                                f"{var}",
                                value=default_value,
                                key=f"var_{var}_{cand_id}"
                            )
                        
                        if st.button("📝 Générer l'email", key=f"gen_email_{cand_id}"):
                            sujet = template_choice.get("sujet", "")
                            contenu = template_choice.get("contenu", "")
                            
                            # Remplacer les variables
                            for var, value in var_values.items():
                                sujet = sujet.replace(f"{{{var}}}", value)
                                contenu = contenu.replace(f"{{{var}}}", value)
                            
                            st.markdown("---")
                            st.markdown(f"**Sujet :** {sujet}")
                            st.markdown("**Contenu :**")
                            st.text_area("", value=contenu, height=300, key=f"email_result_{cand_id}")
                else:
                    st.info("Aucun template disponible. Les templates seront disponibles avec Supabase activé.")


# ============================================================================
# MAIN
# ============================================================================

def main():
    """Point d'entrée principal de l'application."""
    # Charger les styles
    load_custom_css()
    
    # Initialiser les états
    init_session_state()
    
    # Afficher la sidebar
    render_sidebar()
    
    # Router vers la bonne page
    pages = {
        'accueil': render_accueil,
        'cv_perso': render_cv_personnalise,
        'lettre': render_lettre_motivation,
        'entretien': render_preparation_entretien,
        'linkedin': render_linkedin,
        'coach': render_coach,
        'historique': render_historique
    }
    
    current_page = st.session_state.current_page
    if current_page in pages:
        pages[current_page]()
    else:
        render_accueil()


if __name__ == "__main__":
    main()

