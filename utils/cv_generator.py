"""
Générateur de CV HTML → PDF pour Valérie Jasica
Permet de personnaliser le CV en fonction de chaque offre d'emploi
"""
import os
import io
import re
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional
import base64


# ============================================================================
# DONNÉES DE BASE DE VALÉRIE (template par défaut)
# ============================================================================

VALERIE_DATA_BASE = {
    "nom": "VALÉRIE JASICA",
    "titre_professionnel": "Conseillère en Insertion Professionnelle",
    "email": "valerie.jasica67@gmail.com",
    "telephone": "06 09 91 41 86",
    "linkedin": "Valerie_Jasica",
    "localisation": "COULLONS 45720",
    
    # Zone personnalisable selon l'offre
    "accroche": """<span class="accroche-highlight">Redonner confiance</span>, ouvrir des perspectives et accompagner chaque personne, en valorisant ses ressources et en <span class="accroche-highlight">facilitant son insertion sociale et professionnelle durable.</span>""",
    
    # Zone personnalisable
    "qualites": ["Déterminée", "Engagée", "Résiliente", "Fédératrice"],
    
    # Zone personnalisable - ordre selon l'offre
    "competences": [
        "Accueillir, informer et orienter les usagers",
        "Réaliser des entretiens individuels de diagnostic",
        "Identifier les freins et rédiger des synthèses",
        "Orienter vers les dispositifs adaptés",
        "Construire des projets professionnels individualisés",
        "Soutenir l'accès et le maintien en emploi",
        "Animer un portefeuille, promotion de profil",
        "Concevoir et animer des ateliers collectifs",
        "Développer le travail en réseau et partenariat",
        "Prospecter et accompagner les employeurs"
    ],
    
    "experiences": [
        {"entreprise": "France Travail", "poste": "Conseillère placement", "dates": "Juillet 2024 - Présent"},
        {"entreprise": "Greenfield", "poste": "Assistante commerciale", "dates": "2020 – 2023"},
        {"entreprise": "Hexis", "poste": "Chargée Relation Clients ADV", "dates": "2013 – 2020"},
        {"entreprise": "EDF Photowatt", "poste": "Attachée commerciale", "dates": "2010 – 2012"},
        {"entreprise": "Cherry Rocher", "poste": "Adjointe du Directeur Commercial", "dates": "2008 – 2009"},
        {"entreprise": "Armée Djibouti", "poste": "Chargée de Communication", "dates": "2005 – 2007"},
        {"entreprise": "Arpège MasterK", "poste": "Assistante de direction", "dates": "2001 – 2004"},
        {"entreprise": "STEF TFE", "poste": "Assistante de Direction/DAF", "dates": "1999 – 2001"},
        {"entreprise": "CIRFO Centre de Formation", "poste": "Référente administrative", "dates": "1995 – 1997"},
    ],
    
    "formations": [
        {"titre": "Titre Professionnel CIP", "etablissement": "AFPA Issoudun", "dates": "2024 – 2025"},
        {"titre": "BTS Assistante de direction", "etablissement": "Ilfar Montpellier", "dates": "1991"},
        {"titre": "BAC A2 Littéraire", "etablissement": "Lycée St François de Sales", "dates": "1987"},
    ],
    
    "stages": [
        {"lieu": "France Travail Montargis", "mission": "Relation entreprises", "dates": "22/04 – 23/05/25"},
        {"lieu": "FAP Montargis", "mission": "Suivi RSA – PES", "dates": "10/02 – 7/03/25"},
        {"lieu": "GEIQ SPORT PACA", "mission": "Accompagnement alternants", "dates": "3/12 – 20/12/24"},
        {"lieu": "EPIDE Bourges", "mission": "Accompagnement jeunes", "dates": "2/07 – 12/07/24"},
        {"lieu": "Les Jardins du Cœur Gien", "mission": "Insertion SIAE", "dates": "15/05 – 22/05/24"},
        {"lieu": "Mission Locale Gien", "mission": "Accompagnement jeunes", "dates": "22/04 – 26/04/24"},
    ],
    
    "benevolat": [
        {"evenement": "JO Paris 2024", "role": "Chef d'équipe Accès Public – Club France"},
        {"evenement": "JPO Paris 2024", "role": "Référente Hospitality – Forum Sport"},
    ],
    
    "interets": [
        {"titre": "Triathlon compétition", "detail": "Finisher Ironman Embrunman"},
        {"titre": "Communication club", "detail": "AS Gien Triathlon"},
        {"titre": "Projet socio-sport", "detail": "Les Clubs Sportifs Engagés"},
    ],
    
    # Section optionnelle Communication/Événementiel
    "section_communication": True,
    "competences_com": [
        "Accueillir, informer et conseiller les clients",
        "Organisation d'événements : salons, job dating, forums",
        "Animation de réseau et créations des publications",
        "Assurer le suivi administratif et le reporting"
    ],
}


def get_photo_base64(photo_path: str = None) -> str:
    """Convertit la photo en base64 pour l'inclure dans le HTML."""
    if photo_path is None:
        photo_path = Path(__file__).parent.parent / "docMaman" / "photomaman.jpeg"
    
    try:
        with open(photo_path, "rb") as f:
            data = f.read()
        return f"data:image/jpeg;base64,{base64.b64encode(data).decode()}"
    except:
        return ""


def render_template(data: Dict) -> str:
    """
    Génère le HTML du CV à partir des données.
    Utilise un mini moteur de template maison.
    """
    template_path = Path(__file__).parent.parent / "templates" / "cv_template.html"
    
    with open(template_path, "r", encoding="utf-8") as f:
        html = f.read()
    
    # Ajouter la photo en base64
    data["photo_url"] = get_photo_base64()
    
    # Remplacer les variables simples {{variable}}
    for key, value in data.items():
        if isinstance(value, str):
            html = html.replace(f"{{{{{key}}}}}", value)
    
    # Traiter les listes (sections répétées)
    # Format: {{#liste}}...{{/liste}}
    
    # Qualités (liste simple)
    if "qualites" in data:
        qualites_html = ""
        for q in data["qualites"]:
            qualites_html += f'<span class="qualite">{q}</span>\n'
        html = re.sub(r'\{\{#qualites\}\}.*?\{\{/qualites\}\}', qualites_html, html, flags=re.DOTALL)
    
    # Compétences (liste simple)
    if "competences" in data:
        comp_html = ""
        for c in data["competences"]:
            comp_html += f'<div class="competence-item">{c}</div>\n'
        html = re.sub(r'\{\{#competences\}\}.*?\{\{/competences\}\}', comp_html, html, flags=re.DOTALL)
    
    # Compétences communication (section optionnelle)
    if data.get("section_communication") and "competences_com" in data:
        # Générer le HTML des compétences com
        comp_com_html = ""
        for c in data["competences_com"]:
            comp_com_html += f'<div class="competence-item">{c}</div>\n'
        
        # Remplacer les compétences dans la section
        html = re.sub(r'\{\{#competences_com\}\}.*?\{\{/competences_com\}\}', comp_com_html, html, flags=re.DOTALL)
        
        # Supprimer les balises de section (garder le contenu)
        html = html.replace('{{#section_communication}}', '')
        html = html.replace('{{/section_communication}}', '')
    else:
        # Supprimer toute la section communication si pas activée
        html = re.sub(r'\{\{#section_communication\}\}.*?\{\{/section_communication\}\}', '', html, flags=re.DOTALL)
    
    # Expériences
    if "experiences" in data:
        exp_html = ""
        for exp in data["experiences"]:
            exp_html += f'''
            <div class="experience-item">
                <div>
                    <div class="exp-entreprise">{exp["entreprise"]}</div>
                    <div class="exp-poste">{exp["poste"]}</div>
                </div>
                <div class="exp-dates">{exp["dates"]}</div>
            </div>
            '''
        html = re.sub(r'\{\{#experiences\}\}.*?\{\{/experiences\}\}', exp_html, html, flags=re.DOTALL)
    
    # Formations
    if "formations" in data:
        form_html = ""
        for f in data["formations"]:
            form_html += f'''
            <div class="formation-item">
                <div class="formation-dates">{f["dates"]}</div>
                <div class="formation-titre">{f["titre"]}</div>
                <div class="formation-lieu">{f["etablissement"]}</div>
            </div>
            '''
        html = re.sub(r'\{\{#formations\}\}.*?\{\{/formations\}\}', form_html, html, flags=re.DOTALL)
    
    # Stages
    if "stages" in data:
        stages_html = ""
        for s in data["stages"]:
            stages_html += f'''
            <div class="stage-item">
                <div class="stage-dates">{s["dates"]}</div>
                <div class="stage-lieu">{s["lieu"]}</div>
                <div class="stage-mission">{s["mission"]}</div>
            </div>
            '''
        html = re.sub(r'\{\{#stages\}\}.*?\{\{/stages\}\}', stages_html, html, flags=re.DOTALL)
    
    # Bénévolat
    if "benevolat" in data:
        ben_html = ""
        for b in data["benevolat"]:
            ben_html += f'''
            <div class="benevolat-item">
                <div class="benevolat-event">{b["evenement"]}</div>
                <div>{b["role"]}</div>
            </div>
            '''
        html = re.sub(r'\{\{#benevolat\}\}.*?\{\{/benevolat\}\}', ben_html, html, flags=re.DOTALL)
    
    # Intérêts
    if "interets" in data:
        int_html = ""
        for i in data["interets"]:
            detail = f" – {i['detail']}" if i.get("detail") else ""
            int_html += f'''
            <div class="interet-item">
                <span class="interet-highlight">{i["titre"]}</span>{detail}
            </div>
            '''
        html = re.sub(r'\{\{#interets\}\}.*?\{\{/interets\}\}', int_html, html, flags=re.DOTALL)
    
    return html


def generate_cv_html(customizations: Dict = None) -> str:
    """
    Génère le HTML du CV avec personnalisations optionnelles.
    
    Args:
        customizations: Dict avec les éléments à personnaliser
            - accroche: Nouvelle accroche
            - qualites: Liste de qualités réordonnées
            - competences: Liste de compétences réordonnées
            - experiences_highlight: Liste d'entreprises à mettre en premier
            
    Returns:
        HTML complet du CV
    """
    data = VALERIE_DATA_BASE.copy()
    
    if customizations:
        # Accroche personnalisée
        if "accroche" in customizations:
            data["accroche"] = customizations["accroche"]
        
        # Qualités réordonnées
        if "qualites" in customizations:
            data["qualites"] = customizations["qualites"]
        
        # Compétences réordonnées/filtrées
        if "competences" in customizations:
            data["competences"] = customizations["competences"]
        
        # Réordonner les expériences si nécessaire
        if "experiences_order" in customizations:
            order = customizations["experiences_order"]
            # Réordonner selon les indices fournis
            data["experiences"] = [data["experiences"][i] for i in order if i < len(data["experiences"])]
    
    return render_template(data)


def generate_cv_pdf(customizations: Dict = None) -> io.BytesIO:
    """
    Génère un PDF du CV.
    
    Args:
        customizations: Personnalisations à appliquer
        
    Returns:
        BytesIO contenant le PDF
    """
    html = generate_cv_html(customizations)
    
    try:
        from weasyprint import HTML, CSS
        
        buffer = io.BytesIO()
        HTML(string=html).write_pdf(buffer)
        buffer.seek(0)
        return buffer
        
    except ImportError:
        # Fallback : retourner le HTML si weasyprint n'est pas installé
        raise ImportError("weasyprint n'est pas installé. Installez-le avec: pip install weasyprint")


def preview_cv_html(customizations: Dict = None) -> str:
    """
    Génère une prévisualisation HTML du CV.
    Utile pour l'affichage dans Streamlit avec st.components.html()
    """
    return generate_cv_html(customizations)


# ============================================================================
# FONCTION D'ADAPTATION AUTOMATIQUE
# ============================================================================

def adapt_cv_for_offer(
    offer_analysis: Dict,
    llm_suggestions: Dict = None
) -> Dict:
    """
    Adapte le CV en fonction de l'analyse d'une offre d'emploi.
    
    Args:
        offer_analysis: Analyse de l'offre (mots-clés, compétences recherchées)
        llm_suggestions: Suggestions du LLM pour personnalisation
        
    Returns:
        Dict de personnalisations pour generate_cv_html()
    """
    customizations = {}
    
    if llm_suggestions:
        # Utiliser les suggestions du LLM
        if "accroche" in llm_suggestions:
            customizations["accroche"] = llm_suggestions["accroche"]
        
        if "qualites" in llm_suggestions:
            customizations["qualites"] = llm_suggestions["qualites"]
        
        if "competences_prioritaires" in llm_suggestions:
            # Réordonner les compétences selon les priorités
            prioritaires = llm_suggestions["competences_prioritaires"]
            autres = [c for c in VALERIE_DATA_BASE["competences"] if c not in prioritaires]
            customizations["competences"] = prioritaires + autres
    
    return customizations


if __name__ == "__main__":
    # Test : générer le CV par défaut
    html = generate_cv_html()
    
    output_path = Path(__file__).parent.parent / "exports" / "cv_preview.html"
    output_path.parent.mkdir(exist_ok=True)
    
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html)
    
    print(f"✅ CV HTML généré : {output_path}")

