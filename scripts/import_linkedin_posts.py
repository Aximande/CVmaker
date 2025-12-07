"""
Script pour importer les posts LinkedIn existants de Valérie dans Supabase
"""
import json
import os
import sys
from pathlib import Path

# Ajouter le répertoire parent au path
sys.path.insert(0, str(Path(__file__).parent.parent))

from dotenv import load_dotenv

# Charger le .env
env_path = Path(__file__).parent.parent / '.env'
load_dotenv(env_path)

# Configuration Supabase
SUPABASE_URL = os.getenv("SUPABASE_URL", "https://rsknfjcaazondtymiyrv.supabase.co")
SUPABASE_KEY = os.getenv("SUPABASE_KEY", "")

if not SUPABASE_KEY:
    print("❌ SUPABASE_KEY non trouvée dans .env")
    sys.exit(1)

from supabase import create_client

def main():
    client = create_client(SUPABASE_URL, SUPABASE_KEY)
    
    # Charger les posts LinkedIn
    json_path = Path(__file__).parent.parent / 'docMaman/dataset_linkedin-profile-posts_2025-12-06_11-28-56-790.json'
    
    with open(json_path, 'r', encoding='utf-8') as f:
        posts = json.load(f)
    
    print(f"📊 {len(posts)} posts trouvés dans le fichier")
    
    # Filtrer les posts de Valérie (auteur)
    valerie_posts = []
    for post in posts:
        author = post.get('author', {})
        if author.get('username') == 'valeriejasica':
            valerie_posts.append(post)
    
    print(f"✅ {len(valerie_posts)} posts de Valérie identifiés")
    
    # Importer les posts
    imported = 0
    skipped = 0
    
    for post in valerie_posts:
        try:
            # Extraire les infos
            text = post.get('text', '')
            if not text or len(text) < 10:
                skipped += 1
                continue
            
            # Extraire le sujet (première ligne ou premiers mots)
            first_line = text.split('\n')[0]
            sujet = first_line[:100] if len(first_line) > 100 else first_line
            sujet = sujet.strip()
            
            # Si le sujet est trop court, utiliser les premiers 50 caractères du texte
            if len(sujet) < 10:
                sujet = text[:50].replace('\n', ' ').strip() + "..."
            
            posted_at = post.get('posted_at', {})
            original_date = posted_at.get('date', '')
            
            stats = post.get('stats', {})
            post_type_raw = post.get('post_type', 'regular')
            
            # Mapper le type
            if post_type_raw == 'regular':
                post_type = 'imported_original'
            elif post_type_raw == 'quote':
                post_type = 'imported_quote'
            elif post_type_raw == 'repost':
                post_type = 'imported_repost'
            else:
                post_type = 'imported_original'
            
            has_media = post.get('media') is not None
            linkedin_url = post.get('url', '')
            
            # Préparer les données
            data = {
                'sujet': sujet,
                'contenu': text,
                'post_type': post_type,
                'linkedin_url': linkedin_url,
                'stats': stats,
                'has_media': has_media,
                'publie': True,  # Ces posts sont déjà publiés
                'date_publication': original_date if original_date else None
            }
            
            # Insérer dans Supabase
            result = client.table('linkedin_posts').insert(data).execute()
            imported += 1
            print(f"  ✓ Importé: {sujet[:60]}...")
            
        except Exception as e:
            print(f"  ❌ Erreur: {e}")
    
    print(f"\n{'='*50}")
    print(f"🎉 IMPORT TERMINÉ")
    print(f"   ✅ {imported} posts importés")
    print(f"   ⏭️ {skipped} posts ignorés (trop courts)")
    print(f"{'='*50}")


if __name__ == "__main__":
    main()

