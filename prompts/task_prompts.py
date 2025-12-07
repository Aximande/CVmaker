"""
Prompts de tâches spécifiques pour chaque fonctionnalité
"""

PROMPT_ANALYSE_OFFRE = """Analyse cette offre d'emploi et extrais les informations clés :

<offre_emploi>
{offre}
</offre_emploi>

Fournis une analyse structurée avec :

1. **INFORMATIONS GÉNÉRALES**
   - Intitulé du poste
   - Entreprise/Structure
   - Localisation
   - Type de contrat
   - Date limite de candidature

2. **COMPÉTENCES REQUISES**
   - Compétences techniques (liste)
   - Compétences comportementales (liste)
   - Expérience demandée

3. **MOTS-CLÉS À REPRENDRE**
   - Liste des termes importants à intégrer dans le CV et la lettre

4. **POINTS D'ATTENTION**
   - Éléments spécifiques à ne pas manquer
   - Critères éliminatoires potentiels

5. **AVANTAGES DU POSTE**
   - Ce qui rend ce poste attractif"""

PROMPT_OPTIMISER_CV = """Tu vas adapter le CV de Valérie pour cette offre d'emploi spécifique.

<cv_actuel>
{cv}
</cv_actuel>

<offre_emploi>
{offre}
</offre_emploi>

ÉTAPE 1 - ANALYSE (dans ta réflexion) :
- Identifie les compétences clés demandées
- Repère les correspondances dans le CV de Valérie
- Note les mots-clés à reprendre absolument

ÉTAPE 2 - CV OPTIMISÉ :
Fournis un CV restructuré et adapté avec :

**ACCROCHE PERSONNALISÉE** (adaptée à CE poste)

**COMPÉTENCES CLÉS** (réorganisées selon les priorités de l'offre)

**EXPÉRIENCES PROFESSIONNELLES** (avec mise en avant des plus pertinentes)

**FORMATION**

**STAGES CIP** (si pertinents pour le poste)

**ATOUTS DIFFÉRENCIANTS**

ÉTAPE 3 - RECOMMANDATIONS :
- Ce qui a été mis en avant et pourquoi
- Points forts de la candidature
- Conseils supplémentaires"""

PROMPT_LETTRE_MOTIVATION = """Rédige une lettre de motivation percutante pour Valérie.

<cv>
{cv}
</cv>

<offre_emploi>
{offre}
</offre_emploi>

{contexte_supplementaire}

CONSIGNES :
1. Accroche qui capte l'attention (PAS "Suite à votre annonce...")
2. Paragraphe démontrant la valeur ajoutée (avec exemples concrets du CV)
3. Paragraphe sur l'alignement avec la structure et le poste
4. Conclusion avec appel à l'action confiant

FOURNIS :
1. **LA LETTRE COMPLÈTE** (prête à envoyer)

2. **3 VARIANTES D'ACCROCHE** :
   - Angle résultat/impact
   - Angle passion/engagement
   - Angle problème/solution

3. **POINTS DE VIGILANCE** :
   - Ce qu'il ne faut pas dire
   - Formulations à éviter"""

PROMPT_PREPARATION_ENTRETIEN = """Prépare Valérie pour un entretien d'embauche pour ce poste.

<cv>
{cv}
</cv>

<offre_emploi>
{offre}
</offre_emploi>

Type d'entretien : {type_entretien}

FOURNIS :

## 1. ANALYSE DU RECRUTEUR
- Ce qu'il cherche vraiment
- Ses inquiétudes probables sur le profil de Valérie
- Les signaux d'alerte qu'il guettera

## 2. QUESTIONS PROBABLES (15 questions)

### Questions classiques (5)
Pour chaque question :
- La question
- L'intention réelle du recruteur
- Structure de réponse recommandée
- Réponse suggérée pour Valérie

### Questions comportementales STAR (5)
Pour chaque question :
- La question
- Situation idéale à utiliser depuis le parcours de Valérie
- Réponse modèle complète

### Questions pièges (5)
Pour chaque question :
- La question
- L'erreur courante à éviter
- Approche recommandée
- Réponse suggérée

## 3. QUESTIONS À POSER AU RECRUTEUR (8)
- 3 sur le poste et les attentes concrètes
- 3 sur l'équipe et la culture
- 2 sur l'évolution et les perspectives
(Explique ce que chaque question révèle stratégiquement)

## 4. GESTION DES POINTS SENSIBLES
Pour chaque point (âge, reconversion, parcours varié) :
- Reformulation positive
- Exemple concret qui neutralise l'objection
- Phrase de transition vers un point fort"""

PROMPT_ANALYSE_COMPATIBILITE = """Analyse la compatibilité entre le profil de Valérie et cette offre.

<cv>
{cv}
</cv>

<offre_emploi>
{offre}
</offre_emploi>

FOURNIS :

## 1. MATRICE DE COMPATIBILITÉ

| Critère | Score /10 | Justification |
|---------|-----------|---------------|
| Compétences techniques requises | | |
| Compétences comportementales | | |
| Niveau d'expérience attendu | | |
| Adéquation sectorielle | | |
| Formation/Diplômes | | |
| Localisation | | |

**Score global : X/60**

## 2. VERDICT

🔵 [CANDIDATURE HAUTEMENT RECOMMANDÉE / RECOMMANDÉE AVEC PRÉPARATION / POSSIBLE MAIS RISQUÉE / DÉCONSEILLÉE]

Justification en 3 phrases.

## 3. ANALYSE DES ÉCARTS

Pour chaque écart identifié :
- Nature de l'écart
- Gravité (bloquant / surmontable / négligeable)
- Stratégie de compensation

## 4. ARGUMENTS DE CANDIDATURE

Si candidature recommandée :
- 5 arguments massue à utiliser
- Angle de différenciation unique
- Narratif de candidature à adopter

## 5. PLAN D'ACTION

Actions concrètes pour optimiser cette candidature."""

PROMPT_COACH_CONVERSATION = """Tu es le coach emploi de Valérie. Elle te pose cette question :

<question>
{question}
</question>

Contexte de Valérie :
{cv}

{contexte_supplementaire}

Réponds de manière :
- Bienveillante mais directe
- Orientée action
- Avec des exemples concrets quand pertinent
- En tutoyant Valérie"""

PROMPT_ADAPTER_CV_TEMPLATE = """Analyse cette offre d'emploi et propose des personnalisations COMPLÈTES pour le CV de Valérie.

<offre_emploi>
{offre}
</offre_emploi>

CV actuel de Valérie :
{cv}

Tu dois proposer des adaptations PRÉCISES pour personnaliser son CV à cette offre.

FOURNIS TA RÉPONSE AU FORMAT JSON STRICT :

```json
{{
    "accroche": "Nouvelle accroche personnalisée pour cette offre (2-3 phrases max, avec des <span class='accroche-highlight'>mots clés</span> en gras)",
    "qualites": ["Qualité1", "Qualité2", "Qualité3", "Qualité4"],
    "competences_prioritaires": [
        "Compétence la plus pertinente pour cette offre",
        "Deuxième compétence pertinente",
        "Troisième compétence",
        "Quatrième compétence",
        "Cinquième compétence"
    ],
    "mots_cles_offre": ["mot1", "mot2", "mot3"],
    "conseil_personnalisation": "Conseil court sur ce qu'il faut mettre en avant"
}}
```

RÈGLES :
1. L'accroche doit reprendre les mots-clés de l'offre tout en restant authentique à Valérie
2. Les qualités doivent être choisies parmi : Déterminée, Engagée, Résiliente, Fédératrice, Polyvalente, Organisée, Proactive, Empathique
3. Les compétences prioritaires doivent être reformulées si besoin pour matcher l'offre
4. Limite-toi à 5 compétences prioritaires maximum
5. RÉPONDS UNIQUEMENT AVEC LE JSON, rien d'autre"""


PROMPT_MODIFIER_CV_COMPLET = """Tu es un expert en adaptation de CV. Le CV de Valérie a été personnalisé et l'utilisateur demande une modification.

<cv_donnees_actuelles>
{cv_data}
</cv_donnees_actuelles>

<offre_emploi>
{offre}
</offre_emploi>

<demande_modification>
{demande}
</demande_modification>

Applique la modification demandée. Tu peux modifier N'IMPORTE QUELLE partie du CV si c'est pertinent :
- Accroche
- Qualités
- Compétences (reformuler, réordonner)
- Expériences (reformuler les postes, mettre en avant certaines)
- Stages (reformuler les missions)
- Bénévolat
- Centres d'intérêt

RÉPONDS UNIQUEMENT AVEC UN JSON VALIDE contenant les champs modifiés :

```json
{{
    "accroche": "Accroche modifiée si nécessaire (avec <span class='accroche-highlight'>mots clés</span> en gras)",
    "qualites": ["Qualité1", "Qualité2", "Qualité3", "Qualité4"],
    "competences": [
        "Compétence 1",
        "Compétence 2",
        "etc..."
    ],
    "experiences": [
        {{"entreprise": "Nom", "poste": "Intitulé reformulé", "dates": "Dates"}},
        ...
    ],
    "stages": [
        {{"lieu": "Nom", "mission": "Mission reformulée", "dates": "Dates"}},
        ...
    ],
    "benevolat": [
        {{"evenement": "Nom", "role": "Rôle reformulé"}},
        ...
    ],
    "interets": [
        {{"titre": "Titre", "detail": "Détail"}},
        ...
    ],
    "mots_cles_offre": ["mot1", "mot2"],
    "modification_appliquee": "Description précise de ce qui a été modifié",
    "sections_modifiees": ["accroche", "competences", "experiences"]
}}
```

RÈGLES :
1. Ne modifie QUE ce qui est demandé + ce qui est directement lié
2. Garde les autres sections identiques (copie-les telles quelles)
3. Pour les expériences, garde TOUTES les expériences mais reformule si demandé
4. Sois précis dans "modification_appliquee" pour expliquer les changements
5. RÉPONDS UNIQUEMENT AVEC LE JSON, rien d'autre"""


PROMPT_LINKEDIN_POST = """Rédige un post LinkedIn pour Valérie sur le sujet suivant :

<sujet>
{sujet}
</sujet>

<contexte>
{contexte}
</contexte>

Profil de Valérie pour contexte :
{cv}

CONSIGNES DE STYLE (basées sur ses posts existants) :
1. Accroche percutante avec emoji fort (💥, 💫, ✨)
2. Contextualisation personnelle (son rôle, pourquoi elle en parle)
3. Corps structuré avec bullet points (▶️ ou •)
4. Mise en avant des valeurs humaines et soft skills
5. Section pour taguer des personnes/organisations (à personnaliser)
6. Bloc de 6-10 hashtags pertinents en fin de post

HASHTAGS À CONSIDÉRER :
#InsertionProfessionnelle #SportEtInsertion #Inclusion #FranceTravail 
#SocioSport #LesClubsSportifsEngagés #Triathlon #ImpactSocial
#StadeVersLEmploi #ParaTriathlon #EspritClub

LONGUEUR : 1000-1500 caractères idéalement

FOURNIS :
1. **LE POST COMPLET** (prêt à copier-coller sur LinkedIn)

2. **VERSION ALTERNATIVE** avec un angle différent

3. **SUGGESTIONS D'IMAGES** à accompagner le post

4. **MEILLEUR MOMENT POUR PUBLIER** selon le sujet"""

