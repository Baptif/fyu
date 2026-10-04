# F*yu — APK Android via GitHub

GitHub compile l'APK pour toi, gratuitement. Rien à installer sur ton ordinateur.

## Une seule fois
1. Crée un compte sur github.com (gratuit) puis un **nouveau dépôt** (privé ou public), par exemple `fyu`.
2. Sur la page du dépôt vide : **uploading an existing file**, puis glisse **tout le contenu de ce dossier**
   (y compris le dossier caché `.github` — voir plus bas si tu ne le vois pas).
3. Valide avec **Commit changes**.

## Récupérer l'APK
1. Onglet **Actions** du dépôt → le workflow « Build APK Android » se lance tout seul (≈ 5 à 8 min).
2. Quand il est vert ✅ : clique dessus → section **Artifacts** en bas → **fyu-apk** (zip contenant `app-debug.apk`).
3. Envoie l'APK sur ton téléphone (câble, Drive, mail…), ouvre-le et autorise
   « Installer des applis inconnues » pour l'application utilisée. Android peut afficher un avertissement
   (APK de test non signé pour le Play Store) : c'est normal.

## Mettre à jour l'appli
Remplace `www/index.html` dans le dépôt (Add file → Upload files) : une nouvelle compilation démarre.
Installe le nouvel APK par-dessus l'ancien : tes données sont conservées.

## Le dossier `.github` n'apparaît pas ?
Les dossiers commençant par un point sont cachés sur Mac (⌘ + Maj + .) et Windows (Affichage → Éléments masqués).
Alternative : sur GitHub, **Add file → Create new file**, tape `.github/workflows/build-apk.yml` comme nom
et colle le contenu du fichier.

## Sur ordinateur (optionnel)
Avec Node 20, Java 17 et Android Studio : `npm install && npx cap add android && python3 scripts/make_icons.py && npx cap sync android && cd android && ./gradlew assembleDebug`
