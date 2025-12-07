"""
Persona enrichi de Valérie Jasica
Basé sur l'analyse de ses posts LinkedIn et son dossier CIP 2025
"""

# =============================================================================
# STYLE DE COMMUNICATION LINKEDIN
# =============================================================================

LINKEDIN_STYLE = {
    "tone_of_voice": [
        "Engagée et passionnée",
        "Professionnelle mais chaleureuse",
        "Positive et inspirante",
        "Authentique et sincère",
        "Orientée impact et résultats"
    ],
    
    "emojis_favoris": [
        "💥", "💫", "✨", "💪", "🤝",  # Impact/Force
        "🏊", "🚴", "🏃", "🏆",         # Sport/Triathlon
        "👉", "▶️", "📌", "🎯",          # Call to action
        "📸", "🔗", "📅",                # Contenu
    ],
    
    "structure_post_type": """
1. ACCROCHE avec emoji fort (💥, 💫, ✨)
2. Contexte personnel (qui je suis, pourquoi je parle de ça)
3. Corps avec bullet points (▶️ ou •)
4. Valeurs/soft skills mises en avant
5. Message personnel/takeaway
6. Tags de personnes concernées
7. Bloc de hashtags (6-10 max)
""",
    
    "hashtags_frequents": [
        "#InsertionProfessionnelle",
        "#SportEtInsertion", 
        "#Inclusion",
        "#FranceTravail",
        "#SocioSport",
        "#SportPourTous",
        "#LesClubsSportifsEngagés",
        "#Triathlon",
        "#ImpactSocial",
        "#StadeVersLEmploi",
        "#SEEPH",  # Semaine européenne emploi handicap
        "#ParaTriathlon",
        "#EspritClub"
    ],
    
    "expressions_cles": [
        "utiliser le sport comme levier d'insertion",
        "révélation des potentiels",
        "dépassement de soi",
        "confiance et engagement",
        "qualités humaines",
        "au-delà du CV",
        "compétences humaines",
        "dynamique collective",
        "pratique accessible, mixte et inclusive",
        "une belle dose de motivation"
    ]
}

# =============================================================================
# THÈMES ET VALEURS CENTRALES
# =============================================================================

THEMES_VALEURS = {
    "sport_insertion": {
        "description": "Le sport comme levier d'insertion professionnelle et sociale",
        "exemples": [
            "Stade vers l'Emploi avec Gien Athlé Marathon",
            "Section para-triathlon AS Gien Triathlon",
            "Section jeunes du club",
            "Triathlon de l'Étang du Puits (5ème édition)"
        ],
        "arguments": [
            "Les ateliers sportifs révèlent les qualités humaines",
            "Le sport développe l'esprit d'équipe, l'engagement, l'adaptabilité",
            "Approche qui dépasse le CV et valorise les compétences humaines"
        ]
    },
    
    "inclusion": {
        "description": "Engagement fort pour l'inclusion et l'accessibilité",
        "exemples": [
            "Ouverture section para-triathlon",
            "Partenariat ADAPEI 45",
            "SEEPH (Semaine Européenne Emploi Personnes Handicapées)",
            "Pratique accessible, mixte et inclusive"
        ],
        "arguments": [
            "Ouvrir nos portes, créer des opportunités",
            "Faire du triathlon un espace où chacun trouve sa place",
            "Le sport peut être un formidable levier d'insertion"
        ]
    },
    
    "innovation_ia": {
        "description": "Intérêt pour l'innovation et l'IA au service de l'insertion",
        "headline_linkedin": "Innovation & IA au service de l'insertion",
        "arguments": [
            "Modernité dans l'accompagnement",
            "Outils innovants pour l'emploi"
        ]
    },
    
    "engagement_benevole": {
        "description": "Fort engagement bénévole et associatif",
        "exemples": [
            "JO Paris 2024 - Chef d'équipe Accès Public",
            "JPO Paris 2024 - Référente Hospitality",
            "Communication pour AS Gien Triathlon",
            "Organisation du Triathlon Étang du Puits"
        ]
    }
}

# =============================================================================
# RÉALISATIONS CONCRÈTES (extraites des posts)
# =============================================================================

REALISATIONS_LINKEDIN = [
    {
        "titre": "Stade vers l'Emploi",
        "date": "Novembre 2025",
        "description": "Organisation d'un événement sport-emploi avec France Travail et Gien Athlé Marathon",
        "impact": "Ateliers sportifs permettant aux candidats, conseillers et recruteurs de se rencontrer autrement",
        "competences": ["Organisation événementielle", "Partenariat", "Innovation RH"]
    },
    {
        "titre": "Section Para-Triathlon AS Gien",
        "date": "2025",
        "description": "Ouverture d'une section para-triathlon inclusive en partenariat avec l'ADAPEI 45",
        "impact": "4 résidents en préparation pour le Triathlon de l'Étang du Puits 2026",
        "competences": ["Inclusion", "Développement de projets", "Partenariat"]
    },
    {
        "titre": "Section Jeunes Triathlon",
        "date": "2025",
        "description": "Lancement de la section jeunes au club AS Gien Triathlon",
        "impact": "Démocratisation de la pratique du triathlon",
        "competences": ["Pédagogie", "Animation", "Développement club"]
    },
    {
        "titre": "JO Paris 2024 - Bénévole",
        "date": "Été 2024",
        "description": "Chef d'équipe Accès Public au Club France",
        "impact": "Gestion d'équipe lors d'un événement international majeur",
        "competences": ["Leadership", "Gestion d'équipe", "Organisation", "Gestion de flux"]
    }
]

# =============================================================================
# STYLE D'ÉCRITURE POUR CV/LETTRES
# =============================================================================

STYLE_REDACTION = {
    "cv": {
        "principes": [
            "Utiliser des verbes d'action forts",
            "Quantifier les résultats quand possible",
            "Mettre en avant l'impact humain",
            "Valoriser le collectif autant que l'individuel"
        ],
        "verbes_actions_preferes": [
            "Accompagner", "Animer", "Coordonner", "Développer",
            "Fédérer", "Impulser", "Mobiliser", "Organiser",
            "Piloter", "Structurer", "Valoriser"
        ]
    },
    
    "lettre_motivation": {
        "principes": [
            "Commencer par une accroche personnelle et impactante",
            "Raconter une histoire (storytelling)",
            "Faire le lien entre sport et compétences professionnelles",
            "Montrer l'engagement et les valeurs"
        ],
        "a_eviter": [
            "Suite à votre annonce...",
            "Je me permets de...",
            "Formules trop génériques"
        ],
        "a_privilegier": [
            "Accroches personnalisées liées à l'entreprise/structure",
            "Exemples concrets du parcours",
            "Lien avec les valeurs de la structure"
        ]
    }
}

# =============================================================================
# MOTS-CLÉS SECTEUR INSERTION PROFESSIONNELLE
# =============================================================================

MOTS_CLES_SECTEUR = {
    "accompagnement": [
        "accompagnement individualisé",
        "parcours d'insertion",
        "levée des freins",
        "projet professionnel",
        "diagnostic socioprofessionnel",
        "entretien de suivi"
    ],
    "dispositifs": [
        "CEJ (Contrat d'Engagement Jeune)",
        "PLIE",
        "IAE (Insertion par l'Activité Économique)",
        "RSA",
        "PES (Parcours Emploi Santé)",
        "France Travail",
        "Mission Locale",
        "EPIDE"
    ],
    "competences_cip": [
        "accueil et orientation",
        "diagnostic",
        "accompagnement",
        "relation entreprises",
        "animation d'ateliers",
        "travail en réseau",
        "partenariat territorial"
    ]
}

# =============================================================================
# POINTS FORTS À METTRE EN AVANT (selon contexte)
# =============================================================================

POINTS_FORTS_CONTEXTUELS = {
    "france_travail": [
        "Expérience actuelle en tant que conseillère placement",
        "Stages diversifiés dans le réseau (FT Montargis, FAP)",
        "Connaissance des dispositifs et outils",
        "Maîtrise du terrain et des publics"
    ],
    "mission_locale": [
        "Stage à la Mission Locale de Gien",
        "Expérience avec le public jeune",
        "Approche par le sport pour les jeunes",
        "Section jeunes au club de triathlon"
    ],
    "insertion_iae": [
        "Stage aux Jardins du Cœur",
        "Connaissance des SIAE",
        "Approche inclusive",
        "Projet socio-sport"
    ],
    "sport_inclusion": [
        "Ironman Finisher - résilience prouvée",
        "JO Paris 2024 - leadership",
        "Para-triathlon - inclusion",
        "Les Clubs Sportifs Engagés"
    ]
}

