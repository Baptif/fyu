# F*yu — appli de suivi de musculation (Android)

Appli mobile en une seule page HTML/CSS/JS vanilla (`www/index.html`), emballée en APK avec Capacitor 6.
Pas de framework, pas de build web : on édite `www/index.html` directement.

## Structure
- `www/index.html` : toute l'appli (vues, styles, logique). Source de vérité.
- `capacitor.config.json`, `package.json` : configuration Capacitor (appId `com.fyu.app`).
- `resources/icon-512.png` + `scripts/make_icons.py` : icônes de lancement (Pillow), appliquées après `npx cap add android`.
- `.github/workflows/build-apk.yml` (à placer à la main depuis `build-apk.workflow.yml`, voir ci-dessous) : compile un APK debug sur GitHub Actions (artifact `fyu-apk`).
- `android/` est généré (ignoré par git) : `npx cap add android`.

## Commandes
- Générer et compiler en local (Node 20, Java 17, Android SDK) :
  `npm install && npx cap add android && python scripts/make_icons.py && npx cap sync android && cd android && ./gradlew assembleDebug`
- Après une modification de `www/` : `npx cap sync android`.
- Test rapide dans un navigateur : servir `www/` (ex. `npx serve www`) et émuler un mobile ~390 px de large.

## Données et architecture
- Persistance : `localStorage`, clé `fonte_data_v1` (objet `data` : sessions, current, schedule[7], profile, settings{accentColor, customRest, breathOff, showMuscles, dropPct}, programs[], exercises[]). Migrations dans `loadData()`.
- Modèles : programme `{id, name, exercises:[{name,sets}], color}` ; `schedule[0..6]` (lundi = 0) = id de programme ou null ; séance `{date, name, duration, note, sets:[{ex,reps,weight}]}` (série unilatérale : `repsR` en plus ; série dégressive : `drop:true, of:<sid de la série>`, les séries normales ont un `sid`) (la plus récente en premier) ; catalogue `data.exercises=[{name, group, unilateral?}]` avec groupes Push / Pull / Legs / Autre.
- Niveaux : XP calculée depuis les séances (100 / séance + 10 / série (20 max) + 50 si la précédente date de 1 à 3 jours ; palier 250 + 50 × niveau). La streak (jours consécutifs) est une stat séparée.
- Navigation : `showView(id, btn)` ; `main` est le conteneur qui défile. En mode séance, `body.session-mode` masque le menu du bas et l'en-tête.
- Pas de `alert()/confirm()` : utiliser `askConfirm()` et `showToast()`.
- Échapper tout texte utilisateur avec `esc()`.

## Fonctions de séance (mode séance)
- Menu du bas propre au mode séance : Chrono / Tracking / Notes. Chrono : repos (préréglages + perso), chrono libre, courbe de respiration (6 resp./min, rythme rapide sur la fin).
- Carte d'exercice : icône du muscle (`muscleIcon`, option dans Paramètres), menu « ⋯ » (superset avec un autre exercice, unilatéral, dégressif sur une série choisie, retirer).
- Superset : `ss` sur les exercices de `sessionExercises` (séance en cours uniquement). Dégressif : sous-lignes liées à une série par `sid`; elles comptent dans le tonnage, pas dans le nombre de séries (`nMain()`).
- Fin de séance : récap plein écran (`buildRecap`).

## Design
- Thème sombre unique, ton « motivation / rage » (sobre, tranchant, pas enjoué). Jetons CSS dans `:root` : `--bg #15171B`, `--surface`, `--accent #D8A94E` (réglable dans Paramètres), `--teal`, `--danger`.
- Polices : Space Grotesk (titres, chiffres) + Inter (texte).
- Respecter `prefers-reduced-motion`. Pensé pour ~390 px de large.
- Langue de l'interface : français.

## Idées à venir
- Restaurer la séance en cours (et le chrono) après un rechargement.
- Gérer le bouton retour Android.

## Mise en place du workflow GitHub (une fois)
Le fichier est livré à la racine sous `build-apk.workflow.yml`. Le déplacer à `.github/workflows/build-apk.yml` :
`mkdir -p .github/workflows && git mv build-apk.workflow.yml .github/workflows/build-apk.yml` (ou `mv` avant le premier commit).
