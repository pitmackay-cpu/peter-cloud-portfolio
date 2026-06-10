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
├── cisco_monitor.py          # Supervision SSH du Catalyst 1000 (Netmiko)
└── backup_infrastructure.sh  # Sauvegarde NPM + AdGuard via WireGuard
```

- **`cisco_monitor.py`** — connexion SSH au Catalyst 1000 (VLAN
  management), état des interfaces, détection des ports *down*.
  Démontre : fonctions, dataclasses, gestion d'exceptions, parsing.
- **`backup_infrastructure.sh`** — exécuté sur le VPS : archive les
  configurations NPM et AdGuard puis les réplique vers le serveur de
  sauvegarde du lab à travers le tunnel WireGuard.
  Démontre : `set -euo pipefail`, `trap`, logs horodatés, codes de retour.

---

## 6. Compétences et parcours

**Programmation & automatisation**
- **Python** : automatisation réseau (Netmiko), gestion d'erreurs,
  structuration en fonctions et classes.
- **Bash** : scripts d'exploitation robustes, cron, transferts sécurisés.
- **C** : bases solides acquises lors de la **Piscine de l'École 42**
  (2022) — pointeurs, gestion mémoire (`malloc`/`free`), algorithmique.
- **Go** : agent de déploiement multiplateforme du projet STARLAB.

**Systèmes & réseaux** (Titre Professionnel **TSSR**, niveau 5)
- Windows Server / Active Directory, Linux (Debian/Ubuntu), virtualisation
  (Proxmox, KVM, LXC), VLAN/OSPF, pare-feu/VPN/DMZ/PKI, PXE (FOG,
  netboot.xyz), stratégies de sauvegarde et PRA/PCA.

**Parcours**
- Spécialité **NSI** au Baccalauréat (algorithmique, Python).
- **Piscine École 42** (2022) — programmation C intensive.
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
