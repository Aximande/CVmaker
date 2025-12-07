"""
Contextes personnalisés pré-définis pour Valérie Jasica
Basés sur son CV, dossier CIP, et posts LinkedIn
Ces éléments enrichissent automatiquement les lettres de motivation
"""

# ============================================================================
# CONTEXTES PRÉ-DÉFINIS - Sélectionnables par l'utilisateur
# ============================================================================

CONTEXTES_LETTRE_MOTIVATION = {
    # === PARCOURS & RECONVERSION ===
    "reconversion": {
        "label": "🔄 Reconversion réussie",
        "categorie": "Parcours",
        "texte": """Après 25 ans d'expérience dans le commerce et la relation client, j'ai entrepris une reconversion professionnelle 
mûrement réfléchie vers l'insertion professionnelle. Mon bilan de compétences approfondi (FAP 45 Montargis, 2024) 
a révélé des valeurs profondes centrées sur l'humain et l'accompagnement. J'ai obtenu mon Titre Professionnel 
de Conseillère en Insertion Professionnelle en 2025 (AFPA Issoudun), validant ainsi cette nouvelle orientation.""",
        "mots_cles": ["reconversion", "expérience", "maturité", "bilan de compétences"]
    },
    
    "experience_terrain": {
        "label": "📋 Expérience terrain diversifiée (6 stages CIP)",
        "categorie": "Parcours",
        "texte": """Ma formation CIP m'a permis de réaliser 6 stages dans des structures variées, me donnant une vision 
complète du métier : France Travail (relation entreprises), FAP Montargis (suivi RSA/PES), GEIQ Sport PACA 
(accompagnement alternants sport), EPIDE Bourges (accompagnement jeunes en difficulté), Les Jardins du Cœur 
(insertion SIAE), et Mission Locale de Gien (accompagnement jeunes). Cette diversité m'a permis de développer 
une adaptabilité et une compréhension fine des différents publics et dispositifs.""",
        "mots_cles": ["stages", "terrain", "France Travail", "diversité", "publics"]
    },
    
    "competences_transferables": {
        "label": "💼 Compétences transférables (25 ans commercial/ADV)",
        "categorie": "Parcours",
        "texte": """Mes 25 années en relation client, ADV et commerce m'ont dotée de compétences directement transférables : 
gestion de portefeuilles, sens de l'écoute et du conseil, organisation rigoureuse, capacité à travailler sous pression, 
et maîtrise des outils numériques. Cette expérience me permet d'accompagner efficacement les demandeurs d'emploi 
dans leur relation avec les entreprises, car je connais les attentes des recruteurs.""",
        "mots_cles": ["commercial", "relation client", "ADV", "compétences transférables"]
    },
    
    # === ENGAGEMENT SPORTIF ===
    "ironman": {
        "label": "🏃 Finisher Ironman Embrunman",
        "categorie": "Sport & Valeurs",
        "texte": """Ma pratique du triathlon et l'aboutissement de l'Ironman Embrunman (3,8km natation, 188km vélo, 42km course) 
illustrent ma détermination, ma résilience et ma capacité à atteindre des objectifs ambitieux sur le long terme. 
Ces qualités sont essentielles dans l'accompagnement des personnes vers l'emploi, où la persévérance et le dépassement 
de soi sont au cœur du processus.""",
        "mots_cles": ["triathlon", "Ironman", "résilience", "dépassement", "objectifs"]
    },
    
    "jo_paris_2024": {
        "label": "🏅 Bénévole JO Paris 2024 - Chef d'équipe",
        "categorie": "Sport & Valeurs",
        "texte": """Mon engagement comme Chef d'équipe Accès Public au Club France lors des JO Paris 2024 a renforcé ma conviction 
que le sport est un formidable levier d'insertion. Cette expérience m'a permis de coordonner une équipe de bénévoles, 
d'accueillir un public international, et de créer des contacts précieux avec des acteurs de l'insertion par le sport 
comme le GEIQ Sport PACA. Cet engagement illustre mes valeurs de service, de fédération et d'inclusion.""",
        "mots_cles": ["JO", "Paris 2024", "bénévolat", "chef d'équipe", "coordination"]
    },
    
    "sport_insertion": {
        "label": "⚽ Le sport comme levier d'insertion",
        "categorie": "Sport & Valeurs",
        "texte": """Je suis convaincue que le sport est un puissant levier d'insertion professionnelle. Il développe l'estime de soi, 
la persévérance, l'esprit d'équipe et la capacité à se fixer des objectifs. Mon implication dans le projet socio-sportif 
"Les Clubs Sportifs Engagés" avec l'AS Gien Triathlon vise à faire du sport un tremplin vers l'emploi. Je connais 
les dispositifs comme "Stade vers l'Emploi" et j'ai tissé un réseau avec la FFTri, le CROS Centre Val de Loire et l'ANS.""",
        "mots_cles": ["sport", "insertion", "socio-sportif", "Stade vers l'Emploi", "inclusion"]
    },
    
    # === VALEURS & VISION ===
    "vision_accompagnement": {
        "label": "❤️ Vision humaine de l'accompagnement",
        "categorie": "Valeurs",
        "texte": """Ma vision de l'accompagnement place l'humain au centre : chaque personne possède des ressources et des compétences 
à valoriser, au-delà de ce qui apparaît sur un CV. Mon rôle est de redonner confiance, d'ouvrir des perspectives 
et de faciliter une insertion sociale et professionnelle durable. Je crois en l'importance d'un accompagnement 
personnalisé qui prend en compte la globalité de la personne, ses freins comme ses leviers.""",
        "mots_cles": ["accompagnement", "humain", "confiance", "personnalisé", "ressources"]
    },
    
    "engagement_inclusion": {
        "label": "🤝 Engagement pour l'inclusion",
        "categorie": "Valeurs",
        "texte": """L'inclusion est au cœur de mon engagement professionnel. Je suis sensibilisée aux problématiques d'accessibilité 
et d'accompagnement des publics éloignés de l'emploi. Mon expérience aux JO et Jeux Paralympiques de Paris 2024 
m'a permis de côtoyer des personnes en situation de handicap et de comprendre l'importance de l'adaptation 
des parcours. Je suis formée à l'accompagnement de publics variés : jeunes, seniors, RSA, personnes en situation de handicap.""",
        "mots_cles": ["inclusion", "handicap", "accessibilité", "publics fragiles", "adaptation"]
    },
    
    # === DISPONIBILITÉ & MOBILITÉ ===
    "disponibilite_immediate": {
        "label": "📅 Disponibilité immédiate",
        "categorie": "Pratique",
        "texte": """Je suis disponible immédiatement pour prendre mes fonctions et m'investir pleinement dans ce nouveau poste.""",
        "mots_cles": ["disponible", "immédiat"]
    },
    
    "mobilite_loiret": {
        "label": "🚗 Mobilité Loiret / Centre-Val de Loire",
        "categorie": "Pratique",
        "texte": """Résidant à Coullons (45), je suis mobile sur l'ensemble du département du Loiret et de la région Centre-Val de Loire. 
Je dispose d'un véhicule personnel et suis habituée aux déplacements professionnels.""",
        "mots_cles": ["mobilité", "Loiret", "Centre-Val de Loire", "véhicule"]
    },
    
    # === FRANCE TRAVAIL SPÉCIFIQUE ===
    "connaissance_france_travail": {
        "label": "🏛️ Connaissance de France Travail",
        "categorie": "Spécifique",
        "texte": """J'ai déjà travaillé au sein de France Travail en tant que Conseillère placement (depuis juillet 2024) et j'ai effectué 
un stage de 5 semaines en relation entreprises à France Travail Montargis. Je connais donc l'organisation, les outils, 
les procédures et les valeurs de l'institution. Cette expérience me permet d'être rapidement opérationnelle.""",
        "mots_cles": ["France Travail", "Pôle Emploi", "conseillère placement", "opérationnelle"]
    },
    
    "reseau_partenarial": {
        "label": "🔗 Réseau partenarial développé",
        "categorie": "Spécifique",
        "texte": """Au fil de mes stages et de mes engagements, j'ai développé un solide réseau partenarial : France Travail, 
FAP 45 Montargis, Mission Locale, GEIQ Sport PACA, EPIDE, structures SIAE, clubs sportifs engagés, FFTri, 
CROS Centre Val de Loire, ANS, Comité Olympique et Paralympique. Ce réseau est un atout pour accompagner 
efficacement les bénéficiaires vers les bonnes ressources et partenaires.""",
        "mots_cles": ["réseau", "partenaires", "institutions", "maillage territorial"]
    },
}

# ============================================================================
# CONTEXTES PAR CATÉGORIE (pour affichage groupé)
# ============================================================================

def get_contextes_par_categorie():
    """Retourne les contextes groupés par catégorie."""
    categories = {}
    for key, ctx in CONTEXTES_LETTRE_MOTIVATION.items():
        cat = ctx["categorie"]
        if cat not in categories:
            categories[cat] = []
        categories[cat].append((key, ctx))
    return categories


def get_contexte_texte(keys: list) -> str:
    """
    Compile les textes des contextes sélectionnés en un bloc cohérent.
    
    Args:
        keys: Liste des clés de contextes sélectionnés
        
    Returns:
        Texte compilé pour enrichir le prompt
    """
    if not keys:
        return ""
    
    textes = []
    for key in keys:
        if key in CONTEXTES_LETTRE_MOTIVATION:
            textes.append(CONTEXTES_LETTRE_MOTIVATION[key]["texte"])
    
    return "\n\n".join(textes)


def get_mots_cles(keys: list) -> list:
    """Retourne tous les mots-clés des contextes sélectionnés."""
    mots_cles = []
    for key in keys:
        if key in CONTEXTES_LETTRE_MOTIVATION:
            mots_cles.extend(CONTEXTES_LETTRE_MOTIVATION[key]["mots_cles"])
    return list(set(mots_cles))


# ============================================================================
# CONTEXTES RECOMMANDÉS PAR TYPE DE POSTE
# ============================================================================

RECOMMANDATIONS_PAR_POSTE = {
    "france_travail": {
        "label": "France Travail / Pôle Emploi",
        "contextes_recommandes": ["connaissance_france_travail", "experience_terrain", "vision_accompagnement", "competences_transferables"],
        "description": "Postes de conseiller(e) chez France Travail"
    },
    "mission_locale": {
        "label": "Mission Locale",
        "contextes_recommandes": ["experience_terrain", "vision_accompagnement", "sport_insertion", "engagement_inclusion"],
        "description": "Accompagnement des jeunes 16-25 ans"
    },
    "structure_insertion": {
        "label": "Structure d'insertion (SIAE, GEIQ...)",
        "contextes_recommandes": ["experience_terrain", "vision_accompagnement", "sport_insertion", "reseau_partenarial"],
        "description": "Structures d'insertion par l'activité économique"
    },
    "sport_insertion": {
        "label": "Insertion par le sport",
        "contextes_recommandes": ["sport_insertion", "jo_paris_2024", "ironman", "engagement_inclusion"],
        "description": "Structures utilisant le sport comme levier"
    },
    "collectivite": {
        "label": "Collectivité territoriale",
        "contextes_recommandes": ["reconversion", "competences_transferables", "vision_accompagnement", "reseau_partenarial"],
        "description": "Services emploi des collectivités"
    },
}


def get_contextes_recommandes_pour_offre(offre_text: str) -> list:
    """
    Analyse l'offre et suggère les contextes les plus pertinents.
    
    Args:
        offre_text: Texte de l'offre d'emploi
        
    Returns:
        Liste des clés de contextes recommandés
    """
    offre_lower = offre_text.lower()
    recommandes = set()
    
    # Détection France Travail
    if "france travail" in offre_lower or "pôle emploi" in offre_lower or "pole emploi" in offre_lower:
        recommandes.update(RECOMMANDATIONS_PAR_POSTE["france_travail"]["contextes_recommandes"])
    
    # Détection Mission Locale
    if "mission locale" in offre_lower or "jeunes" in offre_lower:
        recommandes.update(RECOMMANDATIONS_PAR_POSTE["mission_locale"]["contextes_recommandes"])
    
    # Détection insertion par le sport
    if "sport" in offre_lower or "geiq" in offre_lower:
        recommandes.update(RECOMMANDATIONS_PAR_POSTE["sport_insertion"]["contextes_recommandes"])
    
    # Détection SIAE / insertion
    if "siae" in offre_lower or "insertion" in offre_lower or "accompagnement" in offre_lower:
        recommandes.update(RECOMMANDATIONS_PAR_POSTE["structure_insertion"]["contextes_recommandes"])
    
    # Contextes par défaut si rien de spécifique
    if not recommandes:
        recommandes = {"reconversion", "experience_terrain", "vision_accompagnement"}
    
    # Toujours ajouter la disponibilité
    recommandes.add("disponibilite_immediate")
    
    return list(recommandes)

