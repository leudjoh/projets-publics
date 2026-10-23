# Djodjo's Gallery — Retour d'expérience

**Refondre et sécuriser un site vitrine en vingt-cinq jours, avec une IA**

Geoffroy, alias Djodjo · en reconversion vers la cybersécurité (blue team) · octobre 2026

Site : [djos-galley.online](https://djos-galley.online) · Version PDF : [Djodjos-Gallery-retour-experience.pdf](Djodjos-Gallery-retour-experience.pdf)

![L'accueil du site avant et après la refonte, côte à côte](images/accueil-avant-apres.jpg)

## En bref

Djodjo's Gallery est le site vitrine de mes peintures : street art, lettrages graffiti, personnages, machines. Il ne vend rien. Il me sert aussi de terrain d'entraînement pour ma reconversion vers la cybersécurité.

Du 28 septembre au 22 octobre 2026, le site est passé de fichiers déposés à la main chez l'hébergeur à un projet versionné, déployé automatiquement, durci et relu. Le travail tient en **84 pull requests**, que j'ai toutes relues avant de les fusionner ou de les fermer. Dix-huit viennent du workflow d'ajout de toiles, deux de Dependabot ; les 64 autres ont été préparées avec **Claude (IA)**, l'assistant d'Anthropic.

L'essentiel de la refonte a été fait en **quinze jours**. Ce n'est pas fini : la suite, je compte en faire davantage « seul », guidé par l'IA.

| Indicateur | Avant | Après |
|---|---|---|
| Œuvres en ligne | 10, sans classement | 66, en six séries |
| Ajouter une toile | modifier le HTML à la main | déposer une photo, relire une pull request |
| Galerie sur téléphone (33 toiles) | 13,1 Mo | 2,4 Mo (−82 %) |
| En-têtes de sécurité HTTP | 0 | 6, version de PHP masquée |
| Ressources chargées chez un tiers | Google Fonts sur chaque page | aucune |
| Accessibilité | toiles hors d'atteinte au clavier, formulaire sans étiquettes | 0 problème détecté par l'outil axe |
| Adresses du site | `www` et adresse principale servies en double | une seule adresse (`301`), page 404 du site |

**Ce que le projet m'a fait pratiquer :** Git et GitHub (branches, pull requests, relecture), GitHub Actions, sécurité web (CSP, HSTS, en-têtes HTTP), sécurité de la chaîne d'approvisionnement, fuites d'information (OWASP WSTG), RGPD et pseudonymisation (HMAC), divulgation coordonnée (`security.txt`), accessibilité (axe, navigation au clavier), référencement (Search Console, redirections), lecture des en-têtes avec `curl`, règles Apache (`.htaccess`), travail encadré avec une IA.

> Le code du site est dans un dépôt privé. Les numéros de pull request (PR) servent de repères ; l'annexe les liste toutes.

## Le site lui-même

**Un en-tête qui dit ce que je fais** (PR #19). « Artiste peintre » devient « Street art & technoculture » : les machines que je peins, et la carrière tech que je vise.

![En-tête avant et après](images/entete-avant-apres.jpg)

**Un accueil qui raconte** (PR #24 à #27). Avant : une bannière fixe. Après : une accroche, « Chaque toile a son code. », un mur de toiles qui défile, les séries, une toile en gros plan, la bio, le contact.

![Structure de l'accueil : un écran avant, six blocs après](images/accueil-structure.jpg)

**Six séries, sans une ligne de code pour en ajouter une** (PR #22 et #23). Chaque série a son filtre et sa propre adresse. J'ai créé la série Persos seul, sans toucher au code.

![Le portfolio avant et après](images/portfolio-avant-apres.jpg)

**Des textes réécrits** (PR #36, #55 et #67). Un titre principal par page, une description pour Google qui commence par « street art », et pour chaque toile une description de ce qu'on voit. Avant, un lecteur d'écran lisait « fresque-1 ».

*Lecteur d'écran : logiciel qui lit la page à voix haute, pour les personnes aveugles ou malvoyantes.*

**Utilisable au clavier** (PR #38). La touche Tab sautait toutes les toiles, la visionneuse ne se fermait pas, le formulaire n'avait pas d'étiquettes. Tout est corrigé : zéro problème détecté par l'outil axe.

![Visionneuse ouverte au clavier, focus sur le bouton Fermer](images/lightbox-clavier.jpg)

**−82 % sur téléphone** (PR #7 et #29 à #31). Des miniatures, et le navigateur choisit la plus petite image qui suffit : la galerie passe de 13,1 à 2,4 Mo.

**Un bel aperçu quand on partage un lien** (PR #50 et #51). Titre, description et image s'affichent sur WhatsApp, LinkedIn ou Discord. L'image est symétrique : WhatsApp la découpe parfois en carré.

![Image d'aperçu affichée au partage d'un lien du site](images/apercu-partage.jpg)

## Le projet en sept temps

![Chronologie : fondations, refonte, durcissement, visibilité et revue, formulaire et finitions, livre d'or et mentions légales, revue et alerte](images/chronologie.png)

La frise donne l'ordre des étapes. Plus bas, le travail est rangé par thème : chaque sujet n'y est raconté qu'une fois, avec ses PR.

## Qui a fait quoi

Le pied de page du site dit « conçu, codé et sécurisé par Djodjo et Claude (IA) ». Voici le partage réel.

| Moi (Geoffroy) | Claude (IA) |
|---|---|
| Les objectifs, les priorités, la direction artistique ; « Street art & technoculture », les noms des séries Horizons et Électrons libres | Les diagnostics et quatre revues de code complètes |
| Le choix de la maquette ; la correction et la validation de tous les textes, dont ce que « Sous le capot » ne doit jamais dire | Les maquettes de l'accueil, les premiers jets des textes |
| Le dépôt et sa liaison avec l'hébergeur ; la relecture et la fusion de chaque pull request | Le code : HTML, CSS, JavaScript, PHP, Python, GitHub Actions |
| Les vérifications en ligne (`curl`, console du navigateur) et Search Console, vérifiée par DNS | Les tests avant chaque PR : navigateur automatisé (ordinateur et téléphone), Apache et PHP en local, outil axe |
| Les photos et les titres des toiles, le consentement, les descriptions Google, l'image de partage | La rédaction des pull requests et de `CLAUDE.md` |
| La série Persos, créée seul ; en exercice guidé, l'en-tête HSTS et la mesure de l'adresse réelle des visiteurs ; la clé secrète du formulaire, générée et installée par moi ; le ménage des branches | Le formulaire corrigé (PR #64), « Sous le capot » (PR #69 et #70), le livre d'or et les mentions légales (PR #72, #75 et #79), les suites de la quatrième revue (PR #80 et #82), la coupure de PHP (PR #83 et #84) |
| Les décisions : modération du livre d'or, menu, lien dans la bio, pseudonyme, durée de conservation, coordonnées de l'hébergeur | L'explication de chaque choix et de chaque erreur, les miennes comme les siennes |

## La méthode

1. **Diagnostiquer avant de proposer** : le code, les textes et les toiles sont relus d'abord.
2. **Montrer avant de coder** : maquettes avec les vraies toiles, captures avant chaque changement visuel.
3. **Écrire les textes à part**, les valider, puis les intégrer en une seule PR.
4. **Un sujet, une branche, une pull request**, testée sur ordinateur et sur téléphone.
5. **Un humain fusionne** : Claude n'a jamais poussé sur la branche principale.
6. **Vérifier en ligne après la fusion** : codes de réponse et en-têtes avec `curl -I`, console du navigateur, Search Console. C'est moi qui le fais.

**`CLAUDE.md`, la mémoire du projet.** Un fichier du dépôt où sont écrites les règles : aucun secret, rien chez un tiers, des commentaires publics sans détails internes, des tests avant chaque PR. L'IA le relit à chaque session : les garde-fous sont écrits une fois pour toutes. Chaque action de Claude est aussi notée dans un résumé de l'état du site, pour reprendre le travail ailleurs.

**Une IA, sans les clés.** Claude n'accède qu'au dépôt du site, sur autorisation, et ne fusionne rien. Ses propositions passent par la même relecture que n'importe quelle contribution. Ses erreurs sont dans les incidents : c'est la relecture qui les a rattrapées.

**L'IA n'est pas illimitée.** Claude s'utilise avec une limite d'usage hebdomadaire. J'ai épuisé la mienne en six jours : le 7 octobre après-midi, la jauge était à 100 %, et je n'ai plus eu accès à Claude avant sa remise à zéro, le lendemain à 13 h. C'était une erreur de ma part. J'ai mené en parallèle deux très longues conversations en réflexion étendue, un mode où Claude réfléchit plus longtemps avant de répondre, et consomme donc beaucoup plus. Je l'avais activé dans la première, et la seconde l'a gardé par défaut sans que je m'en aperçoive. Le contenu y a gagné en qualité, mais la limite a fondu. Depuis, je vérifie ce réglage à l'ouverture de chaque conversation. J'ai aussi gardé trois habitudes : une conversation par sujet, un résumé de l'état du site pour reprendre ailleurs sans tout relire, et des captures recadrées.

![Ma limite d'usage hebdomadaire de Claude : 100 %, épuisée en six jours](images/usage-claude-semaine.png)

**Ce que l'IA change pour moi.** J'ai découvert l'IA avec Claude, et c'est un compagnon de travail remarquable. En une semaine, j'ai fait ce qui m'aurait pris, selon mon estimation, deux mois à plein temps. Mais produire avec une IA est un travail en soi : il faut formuler, relire et vérifier. L'IA a aussi un revers : je codais moins moi-même, et j'avais l'impression de pouvoir m'en tirer avec quelques notions. Vu la vitesse à laquelle Claude écrit et teste du code, apprendre à coder m'a même paru inaccessible, et presque obsolète. C'est un piège quand on vise la cybersécurité, où il faut comprendre ce qu'on défend : le but n'est pas d'écrire aussi vite qu'une IA, mais de savoir lire et juger ce qu'elle écrit. J'ai donc gardé des exercices à faire seul, avec un simple indice : l'en-tête HSTS, puis l'adresse IP réelle des visiteurs du formulaire.

Pour sortir de ce piège pour de bon, j'ai mis en place des cours de Python avec Claude Code. Je travaille sur une machine virtuelle à laquelle je me connecte en SSH depuis Visual Studio Code : c'est moi qui écris le code dans l'éditeur, et Claude Code y joue le rôle de professeur. Dans ces cours, l'IA n'écrit pas à ma place : elle encadre mon apprentissage.

## Le travail, par thème

### 1. Publier sans risque

Chaque fusion sur la branche principale part en ligne. Rien n'y entre sans relecture, code comme toiles.

- **Un dépôt privé, un accès minimal.** Le site est public, pas son code ni son historique. L'hébergeur n'a accès qu'à ce dépôt, pas à tout mon compte. Aucun mot de passe dans Git.
- **Ajouter une toile sans toucher au code** (PR #12, #22 et #48). Je dépose une photo. Un robot la redimensionne, efface ses métadonnées (téléphone, date, GPS), la range dans sa série et me propose une pull request. Je relis, je fusionne.

    *Workflow GitHub Actions : une suite de tâches que GitHub exécute tout seul quand un événement se produit, ici l'arrivée d'une photo.*

- **Le robot traité comme un suspect** (PR #42, #49, #58 et #82). Il ouvre des fichiers venus de l'extérieur et peut écrire dans le dépôt. Il travaille donc en deux étapes. La première traite les photos sans droit d'écriture. La seconde vérifie le résultat fichier par fichier, et elle seule ouvre la pull request. Un faux JPEG, un fichier rendu exécutable, un raccourci vers un autre fichier : refusés.

    *Chaîne d'approvisionnement : tout le code des autres dont on dépend. Les outils du robot sont figés par empreinte : personne ne peut les remplacer en douce.*

- **Le code tiers sous surveillance** (PR #58). La bibliothèque d'envoi de mails du formulaire a maintenant sa version verrouillée.
- **Supprimer sans rien perdre.** J'ai fait le ménage des branches moi-même, dans le terminal. Une suppression en masse, essayée à blanc, aurait effacé ma branche de travail en cours. Depuis, je nomme ce que je supprime, et j'essaie à blanc d'abord.
- **Tester sur des branches jetables** (PR #41, #57 et #81). Le contrôle du robot a été attaqué avec dix-huit fichiers piégés : tous refusés.

![Le workflow d'ajout en deux jobs](images/workflow-securise.png)

*Réflexes : moindre privilège, zéro confiance, sécurité de la chaîne d'approvisionnement, validation des entrées en tout ou rien, secrets hors du dépôt, gestion des changements (84 PR en vingt-cinq jours).*

### 2. Durcir le serveur

Un serveur en dit souvent plus qu'il ne faut, et protège moins qu'on ne croit.

- **Moins de surface** (PR #8 et #9). Page par défaut supprimée, fichiers internes bloqués, liste des dossiers coupée. Ce qui n'est pas exposé ne s'attaque pas.
- **Des en-têtes qui protègent** (PR #39). Le navigateur ne charge que ce qui vient du site : un script injecté serait bloqué. Caméra, micro et position sont refusés. La version de PHP n'est plus annoncée.

    *En-têtes HTTP : des consignes invisibles que le serveur envoie avec chaque page. La CSP en est une : la liste des sources autorisées.*

- **HTTPS obligatoire, par paliers** (PR #40 et #54). L'en-tête HSTS oblige le navigateur à rester en HTTPS. Mal réglé, il rend un site injoignable pendant des mois. Alors : 60 secondes, puis une semaine, puis plus. J'ai trouvé la ligne moi-même, en exercice.
- **Google affichait encore l'ancien site** (PR #54). Le site répondait sous deux adresses, avec et sans `www`, et Google gardait une vieille copie de la première. Une balise peut lui suggérer la bonne adresse ; une redirection `301` la lui impose. J'ai choisi la redirection.

    *Redirection 301 : le serveur répond « cette page a déménagé pour de bon, voici sa nouvelle adresse ».*

- **Si une protection tombe, le site se ferme au lieu de s'ouvrir** (PR #56). Les règles du serveur étaient écrites sous condition : « si tel module est présent, applique ceci ». Module absent : règles ignorées, sans le moindre message. Testé sur un serveur local : des fichiers internes devenaient lisibles par tous. Désormais, un module manquant provoque une erreur visible, et rien ne fuit.

    *En sécurité, on parle de « défaillance sûre » : en cas de panne, on ferme plutôt qu'on n'ouvre.*

- **« Interdit » plutôt que « introuvable ».** Faire croire que les dossiers internes n'existent pas ? Non : ce serait de l'obscurité, pas de la protection. Et dans les journaux du serveur, un « accès interdit » sur un dossier interne signale clairement quelqu'un qui fouille.
- **Le dossier des images ne sert que des images** (PR #82). Tout autre fichier y est refusé, sans être exécuté. Un script glissé un jour par erreur ne tournerait pas.
- **Une faille critique, publiée avant son correctif** (PR #83 et #84). Le 20 octobre, deux failles de PHP permettant de prendre la main sur un serveur à distance ont été rendues publiques. Des attaques en masse étaient attendues. Je n'ai pas coupé le site : seulement PHP, dont seuls les deux formulaires dépendent. Le reste du site n'a pas bougé. Le lendemain, la version affichée par l'hébergeur n'avait pas changé. Elle ne prouvait rien : j'ai exigé une confirmation écrite avant de rouvrir.

    *PHP : le langage qui fait tourner les formulaires côté serveur.*

![Une adresse, une page : redirection www et page 404](images/www-et-404.jpg)

*Réflexes : défense en profondeur, changement prudent, défaillance sûre, penser à la détection, tester avant la production, lire les en-têtes HTTP, réduire la surface en attendant un correctif, vérifier un correctif plutôt qu'un numéro de version.*

### 3. Ne rien dire de trop

Une attaque commence par lire. Tout ce qui est public, un attaquant le lit aussi.

- **Des fichiers publics trop bavards** (PR #52 et #53). `robots.txt`, souvent le premier fichier qu'on ouvre pour reconnaître un site, citait des dossiers internes (erreur de Claude). Des commentaires du code nommaient des protections. Pas des failles : des indices gratuits. Tout est retiré, et une règle du projet l'interdit désormais.

    *`robots.txt` : un fichier public qui dit aux moteurs de recherche où aller et où ne pas aller.*

- **Un fichier de travail oublié en ligne** (14 octobre). Une liste de branches à supprimer, déposée à la racine du site. Rien de secret, mais une information gratuite. Repéré à la quatrième revue de code, retiré.
- **« Sous le capot » : expliquer sans dévoiler** (PR #69, #70 et #75). Une page qui dit aux visiteurs comment le site les protège, en principes seulement : aucun seuil, aucun nom de fichier. Le mot « sécurise » de ma bio y mène, pour qu'un recruteur la trouve.
- **Dire où signaler une faille.** Un fichier `security.txt`, au format standard, l'indique aux chercheurs en sécurité.
- **Ce document suit la même règle.** Des principes, jamais de réglages. On ne publie pas une faiblesse encore ouverte.

*Réflexes : limiter les fuites d'information, divulgation coordonnée.*

### 4. Les données des visiteurs

Chaque visite laisse une adresse IP. Chaque formulaire, ce que la personne écrit.

- **Rien chez un tiers** (PR #37). Les polices venaient de Google : chaque visite lui envoyait l'adresse du visiteur, sans son accord. Elles sont maintenant servies par le site.
- **Mesurer avant de corriger** (PR #64). La revue de code soupçonnait le formulaire de compter la mauvaise adresse. Claude m'a donné un indice, pas la réponse. J'ai mesuré, depuis le PC puis en 4G : fausse alerte. Mais la mesure a révélé un autre point, corrigé dans la même PR.
- **Pseudonymiser pour de vrai** (PR #64). Les adresses étaient gardées sous forme d'empreinte, sans clé. Or il n'existe que 4,3 milliards d'adresses IPv4 : on les essaie toutes en quelques minutes, et l'adresse d'origine réapparaît. J'ai tenté la correction trois fois, puis Claude l'a écrite et je l'ai relue. Désormais : empreinte à clé secrète, effacée quand elle ne sert plus, envois venus d'un autre site refusés, et un formulaire qui s'arrête plutôt que de tourner sans protection.

    *Empreinte : une suite de caractères calculée à partir d'une donnée. Impossible à « décalculer », mais on peut la retrouver en essayant toutes les valeurs possibles. Avec une clé secrète (HMAC), c'est impossible sans la clé.*

- **Un livre d'or sans risque** (PR #72). Codé par Claude, faute de temps, en m'expliquant chaque étape. Rien n'est publié automatiquement ni stocké sur le serveur : je reçois chaque message par e-mail et je publie ceux que j'accepte. Un message s'affiche comme du texte, jamais comme du code : un script collé dedans ne s'exécute pas. Le serveur revérifie tout et limite les envois.

    *XSS : une attaque qui glisse un script dans une page pour qu'il s'exécute chez les visiteurs suivants.*

- **Des tests d'abus qui trouvent un vrai bug.** Une trentaine de cas joués avant la fusion : l'ancien formulaire de contact plantait sur un champ envoyé sous forme de liste. Corrigé.
- **Une limite pour tout le site** (PR #80). Une seule personne disposant de nombreuses adresses pouvait noyer ma boîte mail. Le contact a maintenant, comme le livre d'or, une limite globale en plus de celle par visiteur.
- **Des mentions légales qui disent ce que fait le code** (PR #75 et #79). Je ne vends rien : la loi me permet de rester sous pseudonyme, si l'hébergeur connaît mon identité. Chaque donnée a son but, sa durée et ses droits. Une promesse d'effacement était plus ferme que le code : j'ai corrigé le texte, pas le code.

*Réflexes : minimisation des données, pseudonymisation, mesurer avant de conclure, sortie sûre, obligations légales et vie privée, dire ce que fait le code.*

## Incidents et leçons

| Ce qui s'est passé | Ce que j'en retiens |
|---|---|
| Une image remplacée revient dans son ancienne version, deux fois | Une image qui change, change de nom. Le robot l'applique désormais (PR #48) |
| Quatre corrections faites en direct sur la branche principale, par moi | La règle vaut pour moi aussi. Sans protection de branche (offre gratuite), seule la discipline protège |
| Des prénoms publiés, deux PR fusionnées trop vite | Une PR ouverte ne coûte rien. Une erreur en ligne ne s'efface jamais complètement |
| Deux toiles de personnes réelles, titrées par leur prénom | Pas de portrait sans accord : publier est irréversible |
| Des conflits de fusion en série | Mon éditeur reformatait tout à chaque sauvegarde. Je formate quand je le décide |
| Dix affirmations fausses (erreur de Claude) | Un constat se vérifie avant d'être présenté. Ma mesure a démenti une faille classée « élevée » (PR #64) |
| Une promesse de vie privée plus ferme que le code (erreur de Claude) | Chaque phrase d'une page de vie privée se vérifie dans le code (PR #79) |
| Une règle d'urgence trop large au premier jet (erreur de Claude) | Même pressé, on teste aussi ce qu'on ne vise pas. Le test local l'a attrapée avant la PR (#83) |
| Deux correctifs sur téléphone sans effet (erreur de Claude) | Mesurer sur l'appareil avant de corriger |
| Un fichier public citait des dossiers internes (erreur de Claude) | Un fichier public ne décrit jamais l'intérieur du site (PR #52) |
| Six erreurs d'organisation (erreur de Claude) | Vérifier l'état réel avant d'agir. Ces règles sont écrites dans `CLAUDE.md` (PR #71, #77 et #78) |

## La suite

L'essentiel est fait, mais ce n'est pas fini. La suite, je compte en faire davantage « seul », guidé par l'IA.

- **Retirer une toile par un workflow.** J'écris moi-même le workflow, en exercice guidé ; Claude écrit le script, que je relis et teste. Le script et la première étape sont faits.
- **Changer la toile mise en avant sur l'accueil**, sur le même modèle.
- **Attaquer moi-même le livre d'or**, en exercice : injection de script, envois en masse, champs trop longs.
- **Des contrôles automatiques dans les pull requests** : une toile sans vraie description, un message du livre d'or mal formé.
- **HSTS** : un mois, puis un an, avec une vérification à chaque palier.
- **Des mails authentifiés** (SPF, DKIM, DMARC), pour que personne ne puisse écrire au nom du domaine.
- **Tenir la durée de conservation annoncée** : trier régulièrement ma messagerie.
- **Des images plus justes** : toiles noires sur Android jusqu'au premier défilement, miniatures trop petites sur écran haute définition. Mesurer d'abord, corriger ensuite.

Me contacter : par le [formulaire du site](https://djos-galley.online/about.html).

## Annexe : les 84 pull requests

<details>
<summary>Afficher la liste</summary>

| PR | Date | Sujet | Résultat |
|---|---|---|---|
| #1 | 28/09 | Renomme peinture1.jpg en envie.jpg | fusionnée |
| #2 | 28/09 | Renomme les peintures 2 à 10 d'après leur titre | fusionnée |
| #3 | 28/09 | Supprime la barre de défilement de la page d'accueil | fusionnée |
| #4 | 28/09 | Adapte l'accueil et le menu aux petits écrans | fusionnée |
| #5 | 30/09 | Ajoute un CLAUDE.md | fusionnée |
| #6 | 02/10 | Corrige la galerie sur mobile et sous le menu | fusionnée |
| #7 | 02/10 | Remplace les photos par des versions optimisées | fusionnée |
| #8 | 02/10 | Supprime la page par défaut de l'hébergeur | fusionnée |
| #9 | 02/10 | Sécurise le dossier du code tiers et le formulaire de contact | fusionnée |
| #10 | 02/10 | Nettoie la feuille de style et le script | fusionnée |
| #11 | 02/10 | Fait du logo un lien vers l'accueil | fusionnée |
| #12 | 02/10 | Ajoute un workflow qui publie les peintures déposées dans un dossier de dépôt | fusionnée |
| #13 | 02/10 | Ajoute la peinture « Grafity » | fusionnée |
| #14 | 02/10 | Affiche le titre des peintures au survol et dans la lightbox | fusionnée |
| #15 | 03/10 | Ajoute 4 peintures | fusionnée |
| #16 | 03/10 | Mélange l'ordre des peintures à chaque visite | fusionnée |
| #17 | 03/10 | Affiche la galerie sur deux colonnes sur téléphone | fusionnée |
| #18 | — | Corrige les dimensions de quatre peintures dans la galerie | fermée sans fusion |
| #19 | 03/10 | Remplace « Artiste Peintre » par « Street art & technoculture » dans l'en-tête | fusionnée |
| #20 | 03/10 | Ajoute 4 peintures | fusionnée |
| #21 | 03/10 | Retire les quatre anciennes lignes de la galerie aux mauvaises dimensions | fusionnée |
| #22 | 03/10 | Ajoute les séries à la galerie et au workflow d'ajout | fusionnée |
| #23 | 03/10 | Range Vivre-Mourir dans Lettres et Essai dans Électrons libres | fusionnée |
| #24 | 03/10 | Refait l'accueil : mur de toiles, séries, zoom et bio (fusion 1) | fusionnée |
| #25 | 03/10 | Raconte l'histoire d'Arbre de vie dans le zoom de l'accueil | fusionnée |
| #26 | 03/10 | Retire les prénoms et resserre le texte du zoom sur Arbre de vie | fusionnée |
| #27 | 03/10 | Crédite Claude dans le pied de page de l'accueil | fusionnée |
| #28 | 03/10 | Ajoute 3 peintures | fusionnée |
| #29 | 03/10 | Accélère le chargement de la galerie avec des miniatures | fusionnée |
| #30 | 03/10 | Accélère l'affichage de la galerie sur téléphone | fusionnée |
| #31 | 03/10 | Place les peintures de la galerie sans animation | fusionnée |
| #32 | 03/10 | Ajoute 6 peintures | fusionnée |
| #33 | 03/10 | Ajoute 9 peintures | fusionnée |
| #34 | 03/10 | Ajoute la peinture « Space » | fusionnée |
| #35 | 03/10 | Retire une toile et en renomme une autre, faute d'accord des personnes représentées | fusionnée |
| #36 | 03/10 | Intègre les textes validés du site | fusionnée |
| #37 | 05/10 | Héberge les polices sur le site au lieu de Google Fonts | fusionnée |
| #38 | 05/10 | Rend la galerie et le formulaire accessibles, et corrige le lien piégé | fusionnée |
| #39 | 05/10 | Ajoute une politique de sécurité du contenu et masque la version de PHP | fusionnée |
| #40 | 05/10 | Oblige le navigateur à rester en HTTPS (HSTS), d'abord pour 60 secondes | fusionnée |
| #41 | — | Ajoute la peinture « Essai workflow » | fermée sans fusion |
| #42 | 05/10 | Sécurise le workflow d'ajout et garde le profil couleur des photos | fusionnée |
| #43 | 05/10 | Ajoute 6 peintures | fusionnée |
| #44 | — | Ajoute 6 peintures | fermée sans fusion |
| #45 | — | Workflow: Bump the actions group with 2 updates (Dependabot) | fermée sans fusion |
| #46 | 05/10 | Ajoute 19 peintures et remplace la photo de Taï Ji | fusionnée |
| #47 | 05/10 | Remplace la photo de Forum et vide le dossier de dépôt des photos déjà en ligne | fusionnée |
| #48 | 05/10 | Ajoute le remplacement automatique d'une peinture | fusionnée |
| #49 | 05/10 | Workflow: Bump the actions group with 2 updates (Dependabot) | fusionnée |
| #50 | 05/10 | Ajoute l'aperçu de partage et les bases du référencement | fusionnée |
| #51 | 05/10 | Passe l'aperçu de partage à une composition symétrique | fusionnée |
| #52 | 06/10 | Retire le commentaire de robots.txt | fusionnée |
| #53 | 06/10 | Retire des commentaires publics les indices sur l'intérieur du site | fusionnée |
| #54 | 06/10 | Redirige www vers le domaine principal, HSTS une semaine, page 404 | fusionnée |
| #55 | 06/10 | Remplace « peintre autodidacte » par « street art » dans les descriptions | fusionnée |
| #56 | 06/10 | Sort les règles du .htaccess des blocs IfModule (défaillance sûre) | fusionnée |
| #57 | — | Ajoute la peinture « Essai deux jobs » et remplace la photo de « Taï Ji » | fermée sans fusion |
| #58 | 06/10 | Workflow en deux jobs, liens symboliques refusés, suivi du code tiers | fusionnée |
| #59 | 06/10 | Garde « figuration libre » dans les textes (règle dans CLAUDE.md) | fusionnée |
| #60 | 06/10 | Ajoute 1 peinture | fusionnée |
| #61 | 06/10 | Ajoute 3 peintures | fusionnée |
| #62 | 06/10 | Ajoute la peinture « fresque-1 » | fusionnée |
| #63 | 06/10 | Ajoute la peinture « fresque-2 » | fusionnée |
| #64 | 07/10 | Protège le formulaire : clé secrète, origine et configuration | fusionnée |
| #65 | 07/10 | Ajoute 3 peintures | fusionnée |
| #66 | 07/10 | Ajoute la peinture « Château » | fusionnée |
| #67 | 08/10 | Décrit dix peintures et corrige cinq titres | fusionnée |
| #68 | 08/10 | Ajoute le pied de page au portfolio et à la page À propos | fusionnée |
| #69 | 08/10 | Ajoute la page « Sous le capot » et security.txt | fusionnée |
| #70 | 08/10 | Ajoute Sous le capot au menu et le lien vers le retour d'expérience | fusionnée |
| #71 | 08/10 | Ajoute la règle de suivi : état du site et retour d'expérience | fusionnée |
| #72 | 12/10 | Ajoute le livre d'or (modération a priori) et factorise le code des formulaires | fusionnée |
| #73 | 12/10 | Lie « sécurise » de la bio à Sous le capot | fusionnée dans une branche intermédiaire, reprise dans la #75 |
| #74 | 12/10 | Ajoute les mentions légales | fusionnée dans une branche intermédiaire, reprise dans la #75 |
| #75 | 12/10 | Livre d'or : messages avant le formulaire, lien de bio, mentions légales | fusionnée |
| #76 | 12/10 | Précise les mentions légales | fusionnée |
| #77 | 12/10 | CLAUDE.md : état du site en fin de session, feuille de route du retex, pièges de session | fusionnée |
| #78 | 13/10 | CLAUDE.md : corrige la feuille de route de ce document | fusionnée |
| #79 | 13/10 | Mentions légales : conservation, fondements, droits et promesses sur les adresses des visiteurs | fusionnée |
| #80 | 14/10 | Contact : limite du site, et longueurs du livre d'or comptées comme le serveur | fusionnée |
| #81 | — | Ajoute la peinture « Essai liste blanche » | fermée sans fusion |
| #82 | 14/10 | Workflow : liste blanche par type de changement, et le dossier des images ne sert que des JPEG | fusionnée |
| #83 | 21/10 | Met PHP à l'abri d'une faille critique annoncée | fusionnée |
| #84 | 22/10 | Rétablit PHP : retire la coupure temporaire | fusionnée |

</details>
