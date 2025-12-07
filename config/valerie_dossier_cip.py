"""
Informations extraites du Dossier CIP de Valérie Jasica (2025)
Ce dossier de 72 pages documente sa formation et ses stages pour l'obtention du titre CIP
"""

# =============================================================================
# PARCOURS DE RECONVERSION
# =============================================================================

PARCOURS_RECONVERSION = {
    "declencheur": "Bilan de compétences approfondi avec FAP 45 (Mme Delphine Bisson)",
    "motivation": "Travail d'introspection révélant des valeurs profondes où l'humain est au cœur de l'action",
    "validation": "3 PMSMP (Périodes de Mise en Situation en Milieu Professionnel)",
    "passions": ["Sport", "Social"],
    "projet_phare": "Insertion socio-sportive - faire du sport un levier d'insertion",
    "tournant": "Bénévolat JO/JPO Paris 2024 - rencontre avec le Comité Paralympique puis GEIQ Sport PACA"
}

# =============================================================================
# STAGES CIP DÉTAILLÉS
# =============================================================================

STAGES_CIP = [
    {
        "structure": "GEIQ SPORT PACA",
        "type": "Groupement d'Employeurs pour l'Insertion et la Qualification",
        "lieu": "Cabriès, Bouches-du-Rhône",
        "periode": "2 au 20 décembre 2024",
        "tutrice": "Emilie Barthès",
        "missions": [
            "Découverte du métier de CIP dans le mouvement sportif",
            "Identification et analyse des partenaires et institutions",
            "Appréhension du maillage territorial",
            "Entretiens d'accueil et de suivi",
            "Accompagnement vers l'emploi dans le secteur sportif"
        ],
        "apprentissages": [
            "Rôle du CIP dans le secteur sportif",
            "Fonctionnement d'un GEIQ",
            "Accompagnement des alternants vers le BPJEPS",
            "Travail en réseau avec institutions sportives"
        ],
        "contexte": "92 contrats d'apprentissage, 63 structures adhérentes, 80% d'insertion"
    },
    {
        "structure": "FAP - Formation Accueil Promotion",
        "lieu": "Montargis (45)",
        "periode": "10 au 27 février 2025",
        "tutrice": "Delphine Bisson",
        "missions": [
            "Accompagnement des bénéficiaires du RSA (CCP2)",
            "Diagnostic socioprofessionnel",
            "Entretiens individuels de suivi",
            "Travail sur les freins à l'emploi"
        ],
        "apprentissages": [
            "Accompagnement du public RSA",
            "Levée des freins périphériques",
            "Travail en partenariat avec les services sociaux"
        ]
    },
    {
        "structure": "France Travail Montargis",
        "lieu": "Montargis (45)",
        "periode": "21 avril au 23 mai 2025",
        "tuteur": "Christophe Frot (Équipe Entreprise Pro)",
        "missions": [
            "Découverte des missions relation entreprises",
            "Accompagnement des employeurs",
            "Prospection entreprises",
            "Appui technique au recrutement",
            "Facilitation de l'intégration des salariés"
        ],
        "apprentissages": [
            "Relation entreprises France Travail",
            "Prospection et fidélisation employeurs",
            "Matching offre/demande",
            "Services aux entreprises"
        ]
    }
]

# =============================================================================
# COMPÉTENCES VALIDÉES (référentiel CIP)
# =============================================================================

COMPETENCES_CIP = {
    "CCP1": {
        "intitule": "Accueillir pour analyser la demande des personnes et poser les bases d'un diagnostic partagé",
        "competences": [
            "Informer une personne ou un groupe sur les ressources en matière d'insertion",
            "Analyser la demande de la personne et poser les bases d'un diagnostic partagé",
            "Exercer une veille informationnelle, technique et prospective pour adapter son activité",
            "Travailler en équipe, en réseau et dans un cadre partenarial"
        ]
    },
    "CCP2": {
        "intitule": "Accompagner les personnes dans leur parcours d'insertion sociale et professionnelle",
        "competences": [
            "Contractualiser et suivre avec la personne son parcours d'insertion professionnelle",
            "Accompagner une personne à l'élaboration de son projet professionnel",
            "Concevoir et préparer des ateliers thématiques favorisant l'insertion professionnelle",
            "Animer des ateliers thématiques favorisant l'insertion"
        ]
    },
    "CCP3": {
        "intitule": "Mettre en œuvre une offre de services auprès des employeurs",
        "competences": [
            "Déployer dans une démarche de projet des actions de prospection avec les employeurs",
            "Apporter un appui technique aux employeurs en matière de recrutement",
            "Faciliter l'intégration et le maintien du salarié dans son environnement professionnel"
        ]
    }
}

# =============================================================================
# ATELIERS CONÇUS ET ANIMÉS
# =============================================================================

ATELIERS_ANIMES = [
    {
        "titre": "Techniques de Recherche d'Emploi (TRE)",
        "contenu": ["CV", "Lettre de motivation", "Outils numériques", "Préparation entretiens"],
        "public": "Demandeurs d'emploi"
    },
    {
        "titre": "Préparation aux entretiens d'embauche",
        "contenu": ["Simulation", "Communication non-verbale", "Questions types"],
        "public": "Alternants GEIQ Sport"
    }
]

# =============================================================================
# PARTENAIRES RENCONTRÉS
# =============================================================================

PARTENAIRES_FORMATION = {
    "institutions_sportives": [
        "Comité National Olympique et Sportif Français (CNOSF)",
        "Comité Paralympique et Sportif Français (CPSF)",
        "DRAJES (Direction Régionale Académique Jeunesse Engagement Sport)",
        "CROS Centre-Val de Loire",
        "ANS (Agence Nationale du Sport)",
        "Fédération Française de Triathlon"
    ],
    "structures_insertion": [
        "France Travail (Orléans, Montargis, Gien)",
        "Mission Locale Gien",
        "FAP 45 Montargis",
        "ADAPEI 45",
        "Les Clubs Sportifs Engagés"
    ],
    "geiq": [
        "GEIQ Sport PACA",
        "GEIQ Sport et Loisirs Centre-Val de Loire (en création avril 2024)"
    ]
}

# =============================================================================
# PROJET SOCIO-SPORTIF STRUCTURANT
# =============================================================================

PROJET_SOCIO_SPORTIF = {
    "vision": "Faire du sport un levier d'estime de soi, de mobilisation, de montée en compétences et d'accès à l'emploi",
    "territoire_cible": "Centre-Val de Loire",
    "actions_concretes": [
        "Transposition du modèle GEIQ Sport PACA en Centre-Val de Loire",
        "Création de la section para-triathlon AS Gien avec ADAPEI 45",
        "Organisation du Triathlon inclusif Étang du Puits",
        "Participation aux dispositifs 'Stade vers l'Emploi'",
        "Animation de la section jeunes triathlon"
    ],
    "partenaires_mobilises": [
        "Les Clubs Sportifs Engagés (réseau national)",
        "AS Gien Triathlon",
        "GEIQ Sport et Loisirs Centre-Val de Loire",
        "France Travail Gien",
        "Fédération Française de Triathlon"
    ]
}

# =============================================================================
# TEXTE FORMATÉ POUR LES PROMPTS LLM
# =============================================================================

DOSSIER_CIP_RESUME = """
## DOSSIER DE FORMATION CIP - VALÉRIE JASICA (2025)

### PARCOURS DE RECONVERSION
Après 25+ ans d'expérience professionnelle (relation client, gestion administrative, événementiel), 
Valérie a entrepris une reconversion mûrie vers le métier de Conseillère en Insertion Professionnelle.

**Déclencheur** : Bilan de compétences avec FAP 45 révélant des valeurs centrées sur l'humain
**Validation** : 3 PMSMP confirmant l'intérêt pour ce métier
**Tournant** : JO/JPO Paris 2024 - rencontre avec le mouvement sportif et l'insertion

### STAGES RÉALISÉS

**1. GEIQ SPORT PACA** (Décembre 2024)
- Découverte du métier de CIP dans le secteur sportif
- Accompagnement d'alternants vers le BPJEPS
- Taux d'insertion : 80%

**2. FAP Montargis** (Février 2025)
- Accompagnement bénéficiaires RSA
- Diagnostic socioprofessionnel
- Levée des freins à l'emploi

**3. France Travail Montargis** (Avril-Mai 2025)
- Relations entreprises
- Prospection employeurs
- Appui au recrutement

### COMPÉTENCES VALIDÉES (Titre CIP)
- CCP1 : Accueil et diagnostic partagé
- CCP2 : Accompagnement parcours d'insertion
- CCP3 : Offre de services aux employeurs

### PROJET STRUCTURANT : INSERTION SOCIO-SPORTIVE
Vision : "Faire du sport un levier d'estime de soi, de mobilisation et d'accès à l'emploi"

Actions concrètes :
- Section para-triathlon AS Gien avec ADAPEI 45
- Triathlon inclusif Étang du Puits (5ème édition prévue juin 2026)
- Événements "Stade vers l'Emploi" avec France Travail
- Réseau "Les Clubs Sportifs Engagés"

### RÉSEAU PARTENARIAL
Institutions : CNOSF, CPSF, DRAJES, CROS, ANS, FFTri
Insertion : France Travail, Missions Locales, ADAPEI, FAP
Sportif : GEIQ Sport, AS Gien Triathlon, Clubs Sportifs Engagés
"""

