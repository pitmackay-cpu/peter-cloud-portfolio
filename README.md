# peter-cloud.com — Home Lab & Infrastructure auto-hébergée

> Infrastructure personnelle complète — hyperviseur, switch managé Cisco,
> VPS public, VPN site-à-site — administrée sous mon propre domaine exposé
> sur Internet. Ce dépôt regroupe les scripts (Python / Bash) et la
> documentation qui pilotent cette infrastructure.

![Statut](https://img.shields.io/badge/lab-actif-success)
![Python](https://img.shields.io/badge/Python-3.11-blue)
![Bash](https://img.shields.io/badge/Bash-5.x-green)
![Ubuntu](https://img.shields.io/badge/VPS-Ubuntu%2024.04-orange)

🌐 **Démonstration en ligne : [peter-cloud.com](https://peter-cloud.com)**

---

## 1. Objectif du dépôt

1. **Pratiquer** le métier d'administrateur systèmes/réseaux dans des
   conditions de production réelles : domaine public, certificats TLS,
   VPN site-à-site, segmentation VLAN, sauvegardes hors-site.
2. **Démontrer une démarche d'ingénierie** : code structuré, gestion des
   erreurs, journalisation, documentation — au-delà de la configuration
   d'équipements.

---

## 2. Topologie réseau réelle

```
                        INTERNET
                            │
                  ┌─────────┴─────────┐
                  │     Cloudflare    │  CDN · WAF · DNS proxy · anti-DDoS
                  └─────────┬─────────┘
                            │
              ┌─────────────┴──────────────┐
              │   VPS — Ubuntu 24.04 LTS    │
              │  Nginx Proxy Manager (TLS)  │
              │  AdGuard Home (DoH/DoT)     │
              │  peter-cloud.com (site)     │
              └─────────────┬──────────────┘
                            │  WireGuard VPN (site-à-site)
              ┌─────────────┴──────────────┐
              │        LAB LOCAL            │
              │                             │
              │  Cisco Catalyst 1000 (24p)  │
              │  VLAN10 LAN · VLAN20 SRV    │
              │  VLAN30 DMZ · VLAN40 IoT    │
              │  VLAN99 MGMT · STP · ACL    │
              │            │                │
              │  Routeur interne            │
              │  (inter-VLAN, OSPF)         │
              │            │                │
              │  Proxmox VE (Ryzen 5 3600,  │
              │  16 GB RAM, KVM/LXC) :      │
              │   ├─ Windows Server (AD,    │
              │   │   DNS, DHCP, GPO)       │
              │   ├─ pfSense (FW, IDS/IPS)  │
              │   ├─ FOG (PXE, masters)     │
              │   ├─ Debian 12 (web, SSH)   │
              │   ├─ Sauvegardes (PRA/PCA)  │
              │   └─ Supervision (logs)     │
              └─────────────────────────────┘
```

---

## 3. Services en production

| Service | URL | Rôle |
|---|---|---|
| **Nginx Proxy Manager** | proxy.peter-cloud.com | Reverse proxy, TLS Let's Encrypt, access lists |
| **AdGuard Home** | dns.peter-cloud.com | DNS filtrant, DNS-over-HTTPS, blocklists |
| **Homarr** | homarr.peter-cloud.com | Tableau de bord de supervision centralisée |
| **netboot.xyz** | boot.peter-cloud.com | Boot réseau PXE, déploiement d'OS à distance |
| **STARLAB** | starlab.peter-cloud.com | Déploiement logiciel auto-hébergé — agent **Go** multiplateforme, 85+ paquets |

Le domaine est administré via Cloudflare : enregistrements A/CNAME/TXT,
SPF, DKIM, DNSSEC.

---

## 4. Sécurité et séparation des environnements

- **Cloudflare en frontal** : l'adresse d'origine du VPS n'est jamais
  exposée publiquement ; WAF et protection DDoS en amont.
- **Cloisonnement VLAN** : cinq VLANs (LAN, serveurs, DMZ, IoT, management)
  sur le Catalyst 1000, avec STP, port security et ACL.
- **pfSense** : pare-feu et IDS/IPS entre les segments, DMZ dédiée.
- **WireGuard site-à-site** : seul lien entre le VPS public et le lab
  local — aucun service du lab n'est directement exposé.
- **Séparation des environnements** : mes projets personnels sont hébergés
  sur un VPS financé et administré personnellement, distinct de tout
  équipement d'un établissement — données, accès et cycle de vie restent
  sous mon entière responsabilité.
- **Sauvegardes hors-site** : configurations critiques archivées et
  répliquées à travers le tunnel WireGuard, avec rotation (stratégie
  alignée sur les recommandations PRA/PCA du référentiel TSSR).
- **Accès** : clés SSH uniquement, moindre privilège, recommandations ANSSI.

---

## 5. Contenu du dépôt

```
.
├── README.md
├── LICENSE
├── .gitignore
│
│   # — Exemples C (programme ADSILLH) —
├── Makefile                  # Compilation séparée (.c -> .o -> exécutable)
├── pile.h                    # Interface : type + prototypes (modularité)
├── pile.c                    # Implémentation de la pile
├── main.c                    # Démo : structures, contrôle, printf, fonctions
├── linked_list.c             # Pointeurs, malloc/free, algo (École 42)
│
│   # — Exemples Python (programme ADSILLH) —
├── python_fondamentaux.py    # Listes, tuples, chaînes, fonctions, exceptions
├── algo_lineaire_vs_quadratique.py  # O(n) vs O(n²), mesure de temps
│
│   # — Automatisation de l'infrastructure —
├── cisco_monitor.py          # Supervision SSH du Catalyst 1000 (Netmiko)
└── backup_infrastructure.sh  # Sauvegarde NPM + AdGuard via WireGuard
```

**Exemples C**

- **`pile.h` / `pile.c` / `main.c` / `Makefile`** — pile (LIFO) d'entiers en
  C, organisée en modules : l'interface (`pile.h`) est séparée de
  l'implémentation (`pile.c`), et le `Makefile` montre la compilation
  séparée (`.c` → `.o` → exécutable). Démontre : variables, structures de
  contrôle, fonctions, `printf`, `struct`, modularité (`.h`/`.o`).
- **`linked_list.c`** — liste chaînée : renversement *en place* par
  manipulation de pointeurs, libération mémoire sans fuite. Compile avec
  `gcc -Wall -Wextra -Werror`. Pointeurs, `malloc`/`free`, algorithmique
  (Piscine École 42).

**Exemples Python**

- **`python_fondamentaux.py`** — relevé de notes : listes, tuples, chaînes
  de caractères, fonctions, structures de contrôle, rattrapage
  d'exceptions (`try`/`except`).
- **`algo_lineaire_vs_quadratique.py`** — comparaison concrète d'un
  algorithme linéaire `O(n)` (une boucle) et quadratique `O(n²)` (deux
  boucles imbriquées), avec mesure du temps d'exécution.

**Automatisation de l'infrastructure**

- **`cisco_monitor.py`** — connexion SSH au Catalyst 1000 (VLAN
  management), état des interfaces, détection des ports *down*.
  Démontre : fonctions, dataclasses, gestion d'exceptions, parsing.
- **`backup_infrastructure.sh`** — exécuté sur le VPS : archive les
  configurations NPM et AdGuard puis les réplique vers le serveur de
  sauvegarde du lab à travers le tunnel WireGuard.
  Démontre : `set -euo pipefail`, `trap`, logs horodatés, codes de retour.

---

## 6. Compétences en programmation — preuves vérifiables

Ce dépôt a été constitué pour documenter, de façon concrète et consultable,
mes compétences en programmation (C, Python, Bash) appliquées à une
infrastructure réelle. Chaque compétence renvoie à un élément vérifiable.

| Compétence | Preuve dans ce dépôt | Origine de la compétence |
|---|---|---|
| **C** — pointeurs, mémoire, algo | [`linked_list.c`](./linked_list.c) (compile `-Wall -Wextra -Werror`) | Piscine **École 42 Angoulême** (2022) |
| **Python** — automatisation | [`cisco_monitor.py`](./cisco_monitor.py) (Netmiko, classes, exceptions) | Spécialité **NSI** au Bac + projets perso |
| **Bash** — exploitation | [`backup_infrastructure.sh`](./backup_infrastructure.sh) (`set -euo pipefail`, logs) | Module scripts **TSSR** + home lab |
| **Go** — projet applicatif | Projet **STARLAB** (agent multiplateforme) — voir ci-dessous | Développement personnel |

> **STARLAB** est mon projet le plus complet : une plateforme de déploiement
> logiciel auto-hébergée (agent **Go** multiplateforme, serveur/API, client
> self-service, application iOS), en production sur `starlab.peter-cloud.com`.
> C'est la démonstration la plus aboutie de ma logique de programmation.

### Correspondance avec les prérequis du programme ADSILLH

Les exemples ci-dessus couvrent directement les notions listées dans les
prérequis de la licence :

| Prérequis ADSILLH | Démontré dans |
|---|---|
| C — variables, `if`/`for`/`while`, fonctions, `printf`, structures | `pile.h`, `pile.c`, `main.c` |
| C — modularité : compilation séparée `.o`, interface `.h` | `Makefile`, `pile.h` |
| Python — variables, structures de contrôle, fonctions | `python_fondamentaux.py` |
| Python — listes, tuples, chaînes de caractères | `python_fondamentaux.py` |
| Python — rattrapage d'exceptions | `python_fondamentaux.py` |
| Algorithmique — linéaire `O(n)` vs quadratique `O(n²)` | `algo_lineaire_vs_quadratique.py` |
| Compilation vs interprétation (C compilé / Python interprété) | l'ensemble du dépôt |

**Systèmes & réseaux** (Titre Professionnel **TSSR**, niveau 5) : Windows
Server / Active Directory, Linux (Debian/Ubuntu), virtualisation (Proxmox,
KVM, LXC), VLAN/OSPF, pare-feu/VPN/DMZ/PKI, PXE (FOG, netboot.xyz),
sauvegardes et PRA/PCA — le tout mis en œuvre dans le home lab décrit plus haut.

**Parcours & attestations**
- Spécialité **NSI** au Baccalauréat (algorithmique, Python).
- **Piscine de l'École 42 Angoulême** (2022) — programmation C intensive
  (pointeurs, gestion mémoire, algorithmique).
- **TP TSSR** — stage au **laboratoire Pprime (ISAE-ENSMA, Poitiers)** :
  maintenance de parc, infrastructure réseau académique, support.
- Certifications : **Cisco Networking Basics**, **ANSSI** (hygiène
  informatique), **CNIL** (atelier RGPD).

---

## 7. Évolutions prévues

Environnement d'exercices isolé sur `lab.peter-cloud.com`, approche
*Infrastructure as Code* (Ansible), supervision Prometheus + Grafana,
CI sur les scripts (pytest, shellcheck).

---

*Peter Mackay — [peter-cloud.com](https://peter-cloud.com) · Candidature L3 Pro ADSILLH, Bordeaux.*
