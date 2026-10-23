# projets-publics

**Mes projets publics d'apprentissage, en reconversion vers la cybersécurité.**

Je m'appelle Geoffroy (alias Djodjo). Après plusieurs métiers techniques — mécanique auto, électroménager, milieu hospitalier — je me reconvertis dans l'informatique, avec un objectif clair : la **cybersécurité**, d'abord en **blue team** (défense, détection, durcissement), puis le **pentest**.

Ce dépôt rassemble les travaux que je peux rendre publics. Je m'entraîne sur un homelab, sur Hack The Box et Let's Defend, et je cherche en particulier à bien articuler **IA et cybersécurité** : me servir de l'IA pour aller plus vite sans cesser de comprendre ce que je défends. Plusieurs projets ici ont été construits avec l'assistant d'Anthropic (Claude), et je le dis à chaque fois, avec le partage réel du travail.

> C'est un dépôt vivant. Il va **évoluer** au fil de mon apprentissage : des projets s'ajouteront, d'autres seront repris ou corrigés. Ce que vous voyez est un instantané, pas un état final.

## Ce qu'il y a dedans

| Dossier | Projet | Domaine |
|---|---|---|
| [`Rust/brutect`](Rust/brutect/README.md) | Détecteur de force brute SSH dans un `auth.log` | Blue team / forensique |
| [`djodjos-gallery-retex`](djodjos-gallery-retex/README.md) | Retour d'expérience : refondre et sécuriser un site vitrine en 25 jours, avec une IA | Sécurité web, DevSecOps |
| [`Python`](Python) | Outils réseau écrits ou réécrits pour apprendre | Réseau / offensif (apprentissage) |
| [`PowerShell`](PowerShell) | Scripts d'administration Windows et Active Directory | Admin système / AD |
| [`AWS`](AWS) | Modèle d'infrastructure haute disponibilité (IaC) | Cloud / réseau |

### `Rust/brutect` — détecter la force brute SSH

Un outil en ligne de commande qui lit un journal d'authentification Linux (`auth.log`) et répond à trois questions : quelles IP ont tenté de deviner un mot de passe SSH, quels comptes elles ont visés, et si l'une a fini par se connecter (compromission probable). Analyse a posteriori, utile pour un exercice de forensique, un CTF ou le contrôle de son propre serveur. Binaire Linux x86_64 fourni avec son empreinte `sha256`. Développé en Rust, un langage que je ne connaissais pas, avec Claude dans le rôle d'exécutant et moi dans celui de Product Owner. **Détails et mode d'emploi : [`Rust/brutect/README.md`](Rust/brutect/README.md).** Sous licence [MIT](Rust/brutect/LICENSE).

### `djodjos-gallery-retex` — retour d'expérience sécurité web

Le récit complet de la refonte et du durcissement de mon site vitrine ([djos-galley.online](https://djos-galley.online)) : 84 pull requests en 25 jours, toutes relues avant fusion. En-têtes de sécurité (CSP, HSTS), sécurité de la chaîne d'approvisionnement (workflow GitHub Actions en deux jobs, actions épinglées par empreinte), pseudonymisation RGPD (HMAC), divulgation coordonnée (`security.txt`), accessibilité, et la gestion d'une faille critique PHP annoncée avant son correctif. Le code du site est privé ; ce dossier en est le retour d'expérience, avec le partage réel du travail entre l'IA et moi, et la liste des incidents et des leçons. **À lire : [`djodjos-gallery-retex/README.md`](djodjos-gallery-retex/README.md)** (version [PDF](djodjos-gallery-retex/Djodjos-Gallery-retour-experience.pdf) également).

### `Python` — outils réseau

Des outils écrits ou réécrits pour comprendre les protocoles de l'intérieur :

- **`netcat.py`** — une reconstruction de `netcat` en Python (écoute, connexion, exécution de commandes), un classique pour apprendre les sockets et le fonctionnement d'un bind/reverse shell.
- **`SSH EXEC SRV CLT/`** — un serveur et un client SSH interactifs (PTY) écrits avec Paramiko, réécrits pour gérer plusieurs clients, l'authentification par clé et un hachage de mot de passe renforcé. Le serveur exécute les commandes qu'il reçoit : à utiliser **uniquement en environnement contrôlé**.
- **`smbserver.py`** — l'exemple de serveur SMB du projet [Impacket](https://github.com/fortra/impacket) (Fortra), conservé ici comme support d'apprentissage. Ce fichier n'est pas de moi : il garde son en-tête et sa licence d'origine.

### `PowerShell` — administration Windows et Active Directory

Des scripts à menu écrits pendant ma formation :

- **`Menu-crea-AD.ps1`** — création de machines virtuelles Hyper-V (Windows Server 2022 Core) pour monter un lab.
- **`menuUSERetOU-JP.ps1`** — création en masse d'utilisateurs, d'OU et de groupes Active Directory à partir d'un fichier CSV, et des dossiers personnels associés.

### `AWS` — infrastructure haute disponibilité

**`template-infra-ha.yaml`** — un modèle CloudFormation (infrastructure as code) : un VPC avec quatre sous-réseaux (deux publics, deux privés sur deux zones de disponibilité), deux instances EC2 derrière un load balancer. Un exercice de réseau cloud et de reproductibilité d'une infra.

## Un mot sur l'usage

Certains de ces projets (le netcat, le serveur SSH, le serveur SMB) sont des **outils d'apprentissage**. Ils sont destinés à l'étude et à des tests sur mes propres machines ou avec autorisation explicite. Les utiliser contre un système sans accord est illégal.

## Me contacter

Par le [formulaire de mon site](https://djos-galley.online/about.html).
