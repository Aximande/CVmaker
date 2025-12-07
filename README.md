# 🎯 JobCoach IA - Assistant Recherche d'Emploi

Application Streamlit propulsée par Claude (Anthropic) pour accompagner la recherche d'emploi de manière personnalisée.

![Python](https://img.shields.io/badge/Python-3.9+-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-red)
![Claude](https://img.shields.io/badge/LLM-Claude%20Sonnet-purple)

## ✨ Fonctionnalités

### 🚀 Génération Express
Génère en un clic CV adapté + Lettre de motivation + Préparation entretien pour une offre d'emploi.

### 🎨 CV Personnalisé
- Template HTML/CSS professionnel
- Personnalisation automatique via IA selon l'offre
- **Chat itératif** pour affiner le CV
- Export PDF/HTML

### ✉️ Lettre de Motivation
Génération de lettres personnalisées avec le style et les valeurs du candidat.

### 🎤 Préparation Entretien
Questions probables, réponses suggérées, points forts à valoriser.

### 💼 Générateur de Posts LinkedIn
Création de posts LinkedIn dans le style du candidat.

### 💬 Coach IA
Chatbot conversationnel pour conseils de carrière et questions diverses.

### 📚 Suivi des Candidatures
Dashboard complet avec :
- Statistiques
- Timeline des événements
- Rappels
- Liaison avec les CV générés

## 🛠️ Installation locale

```bash
# Cloner le repo
git clone https://github.com/Aximande/CVmaker.git
cd CVmaker

# Créer l'environnement virtuel
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou venv\Scripts\activate  # Windows

# Installer les dépendances
pip install -r requirements.txt

# Configurer les variables d'environnement
cp .env.example .env
# Éditer .env avec vos clés API

# Lancer l'application
streamlit run app.py
```

## 🔑 Configuration

Créez un fichier `.env` avec :

```env
ANTHROPIC_API_KEY=votre_cle_anthropic
SUPABASE_URL=votre_url_supabase
SUPABASE_KEY=votre_cle_supabase
```

## 🚀 Déploiement sur Streamlit Share

1. Forkez ce repo ou pushé votre code
2. Allez sur [share.streamlit.io](https://share.streamlit.io)
3. Connectez votre repo GitHub
4. Dans **Advanced settings** → **Secrets**, ajoutez :
   ```toml
   ANTHROPIC_API_KEY = "votre_cle"
   SUPABASE_URL = "votre_url"
   SUPABASE_KEY = "votre_cle"
   ```
5. Déployez !

## 📁 Structure du projet

```
CVmaker/
├── app.py                 # Application principale
├── config/                # Configuration et profil
├── prompts/               # Prompts pour le LLM
├── templates/             # Templates HTML
├── utils/                 # Utilitaires (LLM, PDF, Supabase)
├── docMaman/              # Documents de référence
├── requirements.txt       # Dépendances Python
└── README.md
```

## 🔒 Sécurité

- Les clés API ne sont JAMAIS commitées
- Utilisez les Secrets de Streamlit Share pour le déploiement
- Les données sont stockées dans Supabase (base de données sécurisée)

## 📄 License

MIT License - Libre d'utilisation et de modification.

---

Développé avec ❤️ pour accompagner la recherche d'emploi.

