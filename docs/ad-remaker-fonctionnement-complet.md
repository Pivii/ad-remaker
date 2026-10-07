# Ad Remaker — Rapport complet de fonctionnement

**Version :** mise à jour le 7 octobre 2026 à 18:03 UTC  
**Périmètre :** architecture réelle de l’agent, outils actifs, services disponibles, Skill, données, validations et workflow opérationnel

---

## 1. Résumé exécutif

**Ad Remaker** est un agent IA spécialisé dans l’analyse et la recréation, pour une marque donnée, de concepts publicitaires concurrents présentant des signaux publics de performance.

Son rôle n’est pas de copier une annonce à l’identique ni de publier automatiquement. Il doit :

1. repérer des références crédibles ;
2. distinguer les faits, estimations et opinions ;
3. déconstruire leur mécanique créative ;
4. adapter cette mécanique au produit réel et à la marque ;
5. obtenir les validations nécessaires avant toute dépense ou action externe ;
6. contrôler la fidélité structurelle, la qualité et l’absence de traces du concurrent ;
7. livrer les créations ou un pack de production/lancement.

Architecture simplifiée :

```text
Demande utilisateur
      ↓
Modèle IA / agent Ad Remaker
      ↓
Règles du rôle + Skill spécialisée
      ↓
Contexte autorisé : mémoire, Company Brain, bases SQL
      ↓
Outils locaux ou appels MCP
      ↓
Résultats vérifiés et livrables
      ↓
Validation humaine avant action sensible
```

---

## 2. Les composants principaux

### 2.1 Le modèle IA

Le modèle interprète la demande, choisit une méthode, appelle les outils nécessaires et assemble les résultats.

Il travaille à partir :

- du message courant et de l’historique utile ;
- de son rôle d’Ad Remaker ;
- de la Skill applicable ;
- des préférences mémorisées ;
- des informations validées de l’entreprise ;
- des résultats renvoyés par les outils.

Le modèle peut expliquer sa méthode, ses critères et ses conclusions. Il ne restitue cependant pas mot pour mot ses consignes internes, ses secrets techniques ou un raisonnement privé détaillé.

### 2.2 MCP

**MCP** signifie *Model Context Protocol*. C’est une interface standardisée entre l’agent et des capacités externes.

Un serveur MCP peut exposer :

- des fonctions exécutables ;
- des applications ou API ;
- des ressources documentaires ;
- un navigateur ;
- un système de fichiers ;
- une base de données ;
- des opérations d’approbation ou de connexion sécurisée.

Un appel MCP contient des paramètres structurés. L’outil exécute l’action, puis renvoie un résultat que l’agent doit lire et vérifier. MCP fournit donc les « mains » et les sources de l’agent ; il ne remplace pas son jugement.

### 2.3 Les Skills

Une **Skill** est une procédure spécialisée et réutilisable. Elle indique comment effectuer une catégorie de travail : ordre des étapes, critères d’acceptation, contrôles, validations et règles de sécurité.

Différence entre les couches :

| Couche | Fonction |
|---|---|
| Modèle IA | Comprend, arbitre, rédige |
| Skill | Définit la méthode métier |
| MCP / outil | Exécute une capacité |
| Mémoire / Brain / SQL | Apporte ou conserve le contexte |
| Validation humaine | Autorise les actions sensibles |

### 2.4 Les plugins et services

Un plugin peut regrouper une Skill, des serveurs MCP et des intégrations applicatives. Lorsqu’un service externe est nécessaire, l’agent vérifie d’abord si une intégration prête à l’emploi existe.

Une connexion nécessitant OAuth, un token ou une clé passe par une interface sécurisée. Les mots de passe et clés ne doivent pas être demandés dans la conversation.

---

## 3. Skills réellement installées

La vérification en direct montre **7 Skills accessibles** : une Skill métier native et six Skills en lecture seule installées par des applications.

| Skill | Origine | Rôle principal |
|---|---|---|
| `winning-ad-remake-workflow` | Agent Ad Remaker | Workflow métier complet de recherche, remake, contrôle, approbation et lancement |
| `brandsearch-usage` | App Brandsearch | Recherche de marques, publicités, contenus organiques, emails et produits |
| `trendtrack-usage` | App TrendTrack | Intelligence e-commerce, boutiques Shopify, publicités Meta/TikTok et suivi concurrentiel |
| `higgsfield-usage` | App Higgsfield | Génération d’images, vidéos et personnages via Higgsfield |
| `kie-ai-usage` | App Kie.ai | Génération image, vidéo et audio avec de nombreux modèles |
| `pika-usage` | App Pika | Création et édition vidéo, image, audio et finitions |
| `fal-usage` | App fal.ai | Recherche et exécution de plus de 1 000 modèles génératifs |

Les six Skills d’applications sont **lisibles même lorsque leur MCP n’est pas authentifié**. Elles documentent la bonne méthode d’utilisation, mais ne donnent pas à elles seules accès aux outils.

### Winning-ad remake workflow

C’est la procédure métier centrale d’Ad Remaker. Une installation d’application peut donc fournir une Skill et une configuration MCP séparées. La Skill peut être présente alors que l’authentification ou les outils restent indisponibles.

Cette Skill métier impose le pipeline suivant.

#### Étape 1 — Trouver la référence

La source privilégiée prévue par la procédure est un outil de recherche publicitaire spécialisé. À défaut, l’agent utilise des bibliothèques publicitaires publiques pertinentes.

L’annonce concurrente sert uniquement de référence d’analyse. Elle n’est ni publiée ni promue.

#### Étape 2 — Évaluer les signaux

Les signaux possibles comprennent :

- durée de diffusion ;
- statut actif ;
- variantes observables ;
- placements ;
- engagement visible ;
- récurrence du concept chez l’annonceur.

Une longue diffusion peut indiquer qu’un concept mérite d’être étudié, mais ne prouve pas sa rentabilité. Toute donnée inférée est marquée **estimation** et tout jugement subjectif **opinion**.

Sont rejetés :

- les concepts déjà reproduits ;
- les références insuffisamment étayées ;
- les mauvais ajustements produit/audience ;
- les remakes qui paraîtraient manifestement artificiels.

#### Étape 3 — Déconstruire l’annonce

Pour une vidéo, les artefacts attendus peuvent inclure :

- cut list avec timestamps ;
- planche complète d’images ;
- planche des trois premières secondes ;
- clips muets plan par plan ;
- notes littérales par plan ;
- transcription ;
- analyse du rythme ;
- notes sur la voix et la musique.

Pour un visuel statique, la composition est cartographiée avec des zones x/y exprimées en pourcentage.

#### Étape 4 — Concevoir le remake

Le remake préserve au plus près :

- le type de hook ;
- la séquence ;
- le cadrage ;
- le rythme ;
- les transitions ;
- le timing des textes ;
- le format source.

Il remplace obligatoirement :

- produit et emballage concurrents ;
- marque et logo ;
- personnes ;
- voix ;
- musique ;
- témoignages et autres éléments identifiants.

Seules des allégations étayées sont admises. Il est interdit de fabriquer avis, résultats, rareté, recommandations, capacités ou témoignages.

Le plan doit employer idéalement **2 à 4 vraies photos produit** et proposer **deux castings de personnes clairement différentes**.

#### Étape 5 — Chiffrer la génération

Avant chaque lot payant, l’agent doit indiquer :

- nombre exact d’unités ;
- prix unitaire ;
- sous-total ;
- marge de reprise de 20 % ;
- total estimé ;
- devise ;
- solde disponible, s’il est accessible.

Un tarif incertain est signalé comme estimation. Aucune génération payante n’est lancée sans accord explicite.

#### Étape 6 — Générer uniquement le lot approuvé

La production doit préserver l’apparence réelle du produit. Sont rejetés :

- packaging déformé ;
- étiquette illisible ;
- anatomie ou mouvements invraisemblables ;
- fuite d’identité ;
- rendu IA peu convaincant.

Les nouvelles tentatives payantes exigent un nouveau chiffrage et une nouvelle validation.

#### Étape 7 — Contrôle qualité

La comparaison se fait plan par plan avec deux notes :

- fidélité structurelle : **minimum 8/10** ;
- qualité de production : **minimum 7/10**.

Le résultat échoue immédiatement s’il contient une trace du concurrent : nom, logo, packaging, produit, personne, voix, musique, watermark, sous-titre, métadonnée ou autre élément identifiable.

#### Étape 8 — Livraison

Chaque fichier créé doit être fourni sous forme consultable : analyses, prompts, photos retenues, rendus intermédiaires, finales et comparaisons.

Les décisions proposées sont explicites : approuver le lot, choisir la personne A ou B, demander des changements, approuver la finale ou arrêter.

#### Étape 9 — Préparer la campagne

Après validation finale, l’agent peut préparer une campagne avec, par défaut, un budget de **20 par jour en devise locale** et le nom :

```text
concurrent · angle · format · date
```

Si une intégration Meta est utilisée, les campagnes, ensembles et annonces doivent rester en pause et être revérifiés. Aucune activation, programmation de dépense ou dépense ne se fait sans autorisation séparée.

#### Étape 10 — Nettoyer la référence

Après approbation finale et confirmation que la référence n’est plus nécessaire, les fichiers locaux du concurrent peuvent être supprimés. Les analyses et les fichiers de la marque ne sont pas supprimés sans demande distincte.

---

## 4. État réel des outils et connexions

Cette section distingue ce qui est **actif maintenant**, ce qui est seulement **prévu par la Skill**, et ce qui existe dans le **catalogue mais n’est pas connecté**.

### 4.1 État des MCP externes

État constaté le **7 octobre 2026 à 18:03 UTC** :

| MCP | Connexion | Outils appelables | Diagnostic |
|---|---:|---:|---|
| **Kie.ai** | Connecté | **Oui — 39 outils** | Opérationnel |
| **TrendTrack** | Échec | Non | Jeton OAuth invalide |
| **Brandsearch** | Échec | Non | Bearer token manquant |
| **Higgsfield** | Échec | Non | Non autorisé |
| **Pika** | Échec | Non | Non autorisé |
| **fal.ai** | Échec | Non | Jeton invalide ou expiré |
| **Meta Ads** | Non observé dans le statut MCP | Non | Aucun MCP/outil Meta actif détecté |

L’installation a donc bien déposé plusieurs bundles et Skills, mais **Kie.ai est le seul service média externe opérationnel au moment du contrôle**.

Une application comporte des couches indépendantes :

```text
Bundle de l’application
├── Skill d’usage              peut être accessible
├── configuration MCP          peut être enregistrée
├── authentification           peut échouer
└── outils opérationnels       seulement si le MCP se connecte
```

La présence d’une Skill ne garantit ni une authentification valide ni l’accès aux données et crédits du service.

### 4.2 Outils natifs actifs : recherche et navigation

L’environnement de l’agent peut fournir :

- recherche web et découverte de sources ;
- lecture de pages statiques ;
- navigation sur des sites dynamiques ;
- téléchargement de fichiers ;
- captures d’écran ;
- inspection visuelle d’images ;
- lecture de ressources éventuellement exposées par un MCP.

Usage Ad Remaker : bibliothèques publicitaires publiques, pages produit, vérification de claims et collecte de preuves observables.

### 4.3 Outils natifs actifs : fichiers et livrables

- lecture et recherche de fichiers ;
- création et modification ciblée de fichiers ;
- consultation d’images locales ;
- publication d’un fichier ou dossier via une URL partageable ;
- retrait d’un fichier publié ;
- affichage de cartes de fichiers dans la conversation.

Usage : rapports Markdown, storyboards, scripts, prompts, exports, images, comparatifs et launch packs.

### 4.4 Création média réellement disponible

L’agent dispose d’un outil natif de **génération et d’édition d’images**.

Il dispose aussi, via **Kie.ai connecté**, de 39 outils spécialisés couvrant :

- **vidéo** : Seedance, Veo 3, Kling, Runway Aleph, Wan, Hailuo, HappyHorse, Grok Imagine, OmniHuman et animation Wan ;
- **image** : GPT Image 2, Seedream, Flux/Flux Kontext, Nano Banana, Midjourney, Qwen, Z-Image et Wan Image ;
- **audio** : ElevenLabs TTS et effets, génération musicale Suno ;
- **édition et finition** : upscale Topaz, suppression d’arrière-plan Recraft, reframing Ideogram, lip-sync Infinitalk, avatar Kling ;
- **opérations** : catalogue de modèles, préparation/soumission des générations, upload, suivi des tâches et récupération des sorties.

Les générations Kie.ai sont asynchrones et consomment les crédits du compte. Les fichiers d’entrée doivent être accessibles par URL ; les sorties expirantes doivent être téléchargées dans l’espace de travail si elles doivent être conservées.

Les outils Higgsfield, Pika et fal.ai ne sont pas encore appelables malgré leurs Skills installées, car leur authentification échoue.

La Skill recommande par défaut :

- **Seedance 2.5** pour la vidéo ;
- le dernier modèle **GPT Image** pour les visuels statiques ;
- le format de la source.

Seedance et GPT Image sont désormais accessibles via Kie.ai. Il reste toutefois obligatoire de vérifier le modèle exact, le tarif, le solde et d’obtenir un accord explicite avant toute génération payante.

### 4.5 Détail des applications média et recherche

| Service | Skill installée | Fonctions documentées | État des outils |
|---|---:|---|---|
| **Brandsearch** | Oui | 14 M+ boutiques et 400 M+ publicités, contenus et emails ; recherche, téléchargement et analyse créative | Bloqués par authentification |
| **TrendTrack** | Oui | Boutiques Shopify, Meta/TikTok, emails, favoris et Brandtracker | Bloqués par jeton invalide |
| **Higgsfield** | Oui | Images, vidéos et personnages ; Soul, Seedream, Kling, Veo, Sora, Cinema Studio, etc. | Bloqués par authentification |
| **Kie.ai** | Oui | Images, vidéos, audio et édition multi-modèles | **39 outils actifs** |
| **Pika** | Oui | Text/image-to-video, extension, lip-sync, image, audio, captions, trim, stitch et transitions | Bloqués par authentification |
| **fal.ai** | Oui | Recherche, inspection et exécution de plus de 1 000 modèles | Bloqués par jeton invalide/expiré |
| **Meta Ads** | Non détectée | Gestion et lecture des campagnes si installée | Aucun outil actif détecté |

Règles particulières issues des Skills :

- **TrendTrack** : chaque ligne retournée consomme un crédit ; commencer avec une petite limite et vérifier le solde.
- **Brandsearch** : `analyze_ad` et `transcribe_ad` consomment des crédits IA ; télécharger les créations plutôt que dépendre d’URL temporaires.
- **Higgsfield** : ne jamais répéter une soumission après un timeout ambigu, afin d’éviter une double facturation.
- **Kie.ai** : générer d’abord une seule variante et conserver localement les sorties utiles.
- **Pika** : annoncer modèle et durée avant le rendu ; réutiliser les actifs existants quand le prompt n’a pas changé.
- **fal.ai** : rechercher le modèle, inspecter son schéma, puis seulement lancer l’inférence.

### 4.6 Bases de données SQL

Deux espaces existent :

- une base privée propre à l’agent ;
- une base partagée entre agents d’un même espace de travail.

La base privée contient notamment une structure destinée aux gagnants publicitaires : marque, angle, format, date de démarrage, durée active, variantes, signal de croissance, score public, URL, explication et statut.

Des vues enregistrées peuvent afficher ces données sous forme de tableau, liste, galerie ou board.

### 4.7 Mémoire

La mémoire conserve certaines préférences ou décisions utiles entre les conversations. Elle n’est pas un journal exhaustif.

Préférences actuellement connues pour Dictus :

- recherche via bibliothèques publicitaires publiques gratuites plutôt que TrendTrack/Brandsearch ;
- livraison de packs d’instructions prêts à copier-coller plutôt que production via Higgsfield/Kie.ai ;
- livraison de launch packs plutôt que connexion directe à Meta Ads.

### 4.8 Company Brain

Le Company Brain est une base de connaissances validée humainement sur l’entreprise : offre, prix, clientèle, ton, concurrents, équipe et règles.

L’agent doit rechercher puis lire les pages pertinentes avant de produire un contenu dépendant de l’entreprise. Une correction n’est pas écrite automatiquement : elle est proposée pour validation.

**État actuel : le Company Brain est vide.** Par conséquent, les futures adaptations de marque devront s’appuyer sur les éléments fournis par l’utilisateur tant qu’aucune page n’aura été validée.

### 4.9 Gestion des Skills

Des outils permettent de :

- lister les Skills ;
- lire une Skill avant utilisation ;
- lire ses fichiers de référence ;
- proposer une nouvelle règle ou une modification ;
- créer ou éditer une Skill lorsque l’utilisateur le demande explicitement.

### 4.10 Catalogue et installation de services

Un catalogue de services peut être recherché avant de construire une intégration manuellement. Il peut proposer des connecteurs vers des applications tierces.

Quand une connexion requiert une authentification :

- l’agent prépare d’abord ce qui peut l’être ;
- il explique ce que la connexion débloque ;
- il présente une carte de connexion sécurisée ;
- il ne demande jamais de coller le secret dans le chat.

### 4.11 Approbations et questions

Des composants structurés permettent :

- de poser plusieurs questions de cadrage en une fois ;
- de demander une approbation explicite ;
- de demander des secrets via un formulaire masqué ;
- de suggérer des réponses rapides.

Les approbations sont utilisées pour les actions conséquentes ou irréversibles, notamment publication, envoi, dépense ou activation.

### 4.12 Planification

L’agent peut créer, lire, modifier, activer, désactiver ou supprimer des tâches planifiées.

Routine actuellement connue :

- **Dictus Monday ad winners** ;
- chaque lundi à 09:00 UTC ;
- prochaine exécution indiquée : 12 octobre 2026 à 09:00 UTC.

Une tâche planifiée est nécessaire lorsqu’un travail doit réellement reprendre plus tard : l’agent ne continue pas silencieusement après la fin d’un tour de conversation.

### 4.13 Collaboration multi-agent

L’environnement peut permettre à un agent principal de répartir des sous-tâches entre agents, puis d’assembler leurs résultats.

Dans la configuration actuelle, cette délégation n’est pas déclenchée automatiquement : elle n’est utilisée que si l’utilisateur ou une procédure applicable la demande explicitement.

---

## 5. Données, priorité des sources et traçabilité

Pour éviter les contradictions, l’ordre logique est :

1. faits validés du Company Brain ;
2. fichiers et informations explicitement fournis par l’utilisateur ;
3. préférences mémorisées ;
4. données structurées internes ;
5. sources externes vérifiables ;
6. estimations et opinion stratégique clairement étiquetées.

Le rapport final doit séparer :

- **fait observable** : directement vérifiable ;
- **estimation** : déduction approximative ;
- **opinion** : jugement professionnel ;
- **inconnu** : information non disponible.

L’agent ne doit pas prétendre connaître le ROAS, les dépenses ou la rentabilité d’un concurrent à partir d’une bibliothèque publique si ces données n’y figurent pas.

---

## 6. Sécurité et garde-fous

Principes essentiels :

- rien n’est publié, envoyé, activé ou dépensé sans accord explicite ;
- aucune génération payante hors du lot approuvé ;
- aucune relance payante silencieuse ;
- aucun mot de passe ou secret demandé dans le chat ;
- aucun claim non étayé ;
- aucun faux témoignage, faux résultat ou fausse rareté ;
- aucun élément identifiable du concurrent dans le rendu final ;
- aucun succès annoncé avant confirmation de l’outil ;
- tout échec bloquant est signalé clairement avec la suite nécessaire.

Créer un fichier local de travail n’est pas la même chose que publier une campagne. Publier un rapport pour que l’utilisateur puisse l’ouvrir ne diffuse pas une publicité et n’engage pas de budget média.

---

## 7. Fonctionnement concret sur une mission Dictus

Configuration opérationnelle actuelle :

```text
Bibliothèques publicitaires publiques
→ sélection et score de références
→ analyse créative détaillée
→ adaptation honnête à Dictus
→ storyboard + script + prompts
→ deux options de casting
→ estimation du lot média et approbation
→ production possible via Kie.ai
→ contrôle qualité à réception des rendus
→ approbation finale
→ launch pack
```

État opérationnel :

- les Skills TrendTrack et Brandsearch sont présentes, mais leurs outils restent bloqués par authentification ;
- Kie.ai est connecté et permet désormais une production directe image, vidéo et audio ;
- Higgsfield, Pika et fal.ai ont leurs Skills, mais leurs outils restent bloqués par authentification ;
- aucune Skill ni connexion Meta Ads active n’a été détectée ; le livrable publicitaire reste donc un launch pack ;
- les anciennes préférences Dictus restent mémorisées, mais la disponibilité technique de Kie.ai a changé ; aucune génération payante ne sera lancée sans un nouvel accord explicite.

### 7.1 Inventaire exact des 39 outils Kie.ai actifs

**Vidéo et animation** : `bytedance_seedance_video`, `veo3_generate_video`, `veo3_get_1080p_video`, `kling_video`, `runway_aleph_video`, `wan_video`, `wan_animate`, `hailuo_video`, `happyhorse_video`, `grok_imagine`, `omnihuman_video`, `kling_avatar`, `infinitalk_lip_sync`.

**Image** : `bytedance_seedream_image`, `gpt_image_2`, `flux2_image`, `flux_kontext_image`, `nano_banana_image`, `midjourney_generate`, `qwen_image`, `z_image`, `wan_image`, `gemini_omni`.

**Audio** : `elevenlabs_tts`, `elevenlabs_ttsfx`, `suno_generate_music`.

**Édition** : `topaz_upscale_image`, `recraft_remove_background`, `ideogram_reframe`.

**Gestion des médias et tâches** : `list_models`, `list_tasks`, `prepare_media_generation`, `submit_media_generation`, `get_task_status`, `wait_for_task`, `get_upload_url`, `upload_file`, `upload_widget`, `finalize_upload`.

---

## 7.2 Mode de secours — aucun outil externe connecté

Si l’utilisateur ne connecte **aucune application externe**, l’agent reste utilisable. Il bascule vers un workflow sans TrendTrack, Brandsearch, Higgsfield, Kie.ai, Pika, fal.ai ni Meta Ads.

| Besoin | Outil spécialisé normalement utilisé | Fallback sans connexion | Limite |
|---|---|---|---|
| Trouver des publicités | TrendTrack / Brandsearch | Bibliothèques publicitaires publiques gratuites, recherche web et navigation | Pas de métriques privées ni de preuve directe de rentabilité |
| Évaluer un gagnant | Données agrégées spécialisées | Signaux publics : ancienneté, statut actif, variantes, répétition du concept, placements et engagement visible | Les performances, dépenses et ROAS restent inconnus |
| Récupérer la création | Téléchargement via l’app | URL publique, téléchargement autorisé ou captures à des fins d’analyse | Certains médias peuvent être temporaires ou protégés |
| Analyser une vidéo | Analyse/transcription intégrée | Inspection locale, captures, découpage, transcription et analyse manuelle avec les outils natifs disponibles | Travail parfois moins automatisé |
| Créer une image | Higgsfield / Kie.ai / Pika / fal.ai | Générateur/éditeur d’images natif, si disponible dans la session | Choix de modèles et réglages plus limité |
| Créer une vidéo | Seedance, Kling, Veo, etc. | Storyboard, script, shot list, prompts, voix off, textes écran et instructions de montage prêts à copier-coller | L’agent ne rend pas la vidéo sans moteur vidéo accessible |
| Voix, musique et effets | ElevenLabs / Suno / Pika | Scripts, direction vocale, brief musical et liste d’effets | Aucun fichier audio généré sans moteur accessible |
| Publier sur Meta | Meta Ads | Launch pack manuel : structure, ciblage, copies, titres, CTA, budget, noms et checklist | L’utilisateur crée et lance lui-même la campagne |
| Stocker et suivre les résultats | Apps externes | Base SQL privée, fichiers et rapports partageables | Pas de synchronisation avec les comptes externes |

### Livrables possibles en mode sans connexion

- sélection argumentée de références publiques ;
- tableau de signaux publics avec séparation **fait / estimation / opinion / inconnu** ;
- analyse du hook et de la structure créative ;
- storyboard, cut list et plan de tournage ;
- script, voix off et textes à l’écran ;
- prompts prêts à coller dans l’outil choisi par l’utilisateur ;
- deux propositions de casting ;
- sélection recommandée de 2 à 4 photos produit ;
- brief de montage, musique, voix et sous-titres ;
- grille de contrôle qualité ;
- launch pack Meta entièrement manuel.

### Ce que le fallback ne prétend pas faire

Sans connexion, l’agent ne prétend pas accéder aux données privées, connaître le ROAS d’un concurrent, consommer les crédits d’un service, générer une vidéo via un moteur absent, ni créer ou activer une campagne Meta. Il montre ce qui est prêt et laisse l’utilisateur exécuter les étapes externes.

Le fallback est automatique : l’absence de connexion n’empêche donc pas de démarrer la recherche et la conception. Elle réduit surtout l’automatisation, l’accès aux données propriétaires et la production média directe.

## 8. Exemple de déroulement d’une demande

Demande : « Trouve une publicité concurrente intéressante et adapte-la à Dictus. »

1. Lecture de la Skill.
2. Consultation des préférences et du Company Brain.
3. Recherche dans les bibliothèques publiques.
4. Collecte d’URLs, dates, formats et variantes.
5. Score des signaux publics.
6. Sélection d’une référence et justification.
7. Déconstruction plan par plan.
8. Vérification des informations produit disponibles.
9. Rédaction du storyboard, script et textes écran.
10. Création de deux castings et sélection de 2 à 4 photos produit.
11. Livraison du pack de production.
12. Si une génération payante est possible : chiffrage et demande d’accord.
13. Comparaison du rendu à la source.
14. Validation des seuils 8/10 et 7/10, et contrôle zéro trace concurrente.
15. Approbation finale.
16. Préparation du launch pack.
17. Aucune activation média sans autorisation distincte.

---

## 9. Limites

- Les bibliothèques publiques ne révèlent généralement pas les performances financières réelles.
- Une annonce active depuis longtemps est un signal, pas une preuve absolue.
- La qualité d’une adaptation dépend des informations produit, visuels et claims disponibles.
- Une intégration non connectée ne peut pas être utilisée sur des données privées.
- Une Skill installée ne prouve pas que son MCP est authentifié.
- Les prix des outils de génération peuvent évoluer et doivent être vérifiés.
- Une création générée peut nécessiter plusieurs essais, chacun soumis au contrôle de dépense prévu.
- Le Company Brain vide limite l’autonomie sur les faits de marque.
- L’agent ne poursuit pas un travail en arrière-plan après la fin d’un échange, sauf tâche réellement planifiée.

---

## 10. Critère de fin d’une mission

Une mission est considérée comme terminée lorsque :

- tous les fichiers demandés sont accessibles ;
- le rendu final atteint au moins 8/10 en fidélité structurelle ;
- le rendu final atteint au moins 7/10 en qualité ;
- aucune trace du concurrent ne subsiste ;
- chaque action payante correspond à une approbation ;
- les éventuels éléments Meta ont été revérifiés en pause ;
- la référence concurrente locale a été supprimée si l’utilisateur l’a confirmé ;
- le livrable final et le launch pack ont été remis.

---

## 11. Formule synthétique

> **Le modèle décide, la Skill impose la méthode, MCP relie l’agent aux capacités, les données apportent le contexte, et l’utilisateur garde le contrôle des dépenses et des actions externes.**
