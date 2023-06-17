# Recosanté pour Home Assistant

Composant pour exposer les niveaux/épisodes de pollution, pollens, index UV, vigilance météo prévus pour le jour même pour une commune ainsi que son potentiel radon.

Données fournies par Recosanté et les agences régionales (ATMO, RNSA, Météo France, IRSN...).  
Voir https://recosante.beta.gouv.fr/ pour l'accès web.

L'intégration expose les données d'Recosanté pour une commune donnée.  
Les données exposées sont :
- Niveau de pollution
  - Dioxyde d'azote (NO<sub>2</sub>)
  - Ozone (O<sub>3</sub>)
  - Particules fines <2.5 µm (Pm25)
  - Particules fines <10 µm (Pm10)
  - Dioxyde de soufre (SO<sub>2</sub>)
  - Niveau global (indice ATMO de la qualité de l'air)
- Vigilance Météo
- Épisode de pollution
  - Dioxyde de soufre (SO<sub>2</sub>)
  - Ozone (O<sub>3</sub>)
  - Dioxyde d'azote (NO<sub>2</sub>)
  - Particules fines <10 µm (Pm10)
- Potentiel Radon
- Risque d’allergie aux pollens
  - Noisetier
  - Aulne
  - Peuplier
  - Saule
  - Frêne
  - Charme
  - Bouleau
  - Platane
  - Chêne
  - Olivier
  - Tilleul
  - Châtaignier
  - Rumex (Oseille)
  - Graminées
  - Plantain
  - Urticacées
  - Armoises
  - Ambroisies
  - Niveau global d'allergie aux pollens
- Indice UV

## Installation

Utilisez [HACS](https://hacs.xyz/).  
[![Ouvrez votre instance Home Assistant et ouvrez un référentiel dans la boutique communautaire Home Assistant.](https://my.home-assistant.io/badges/hacs_repository.svg)](https://my.home-assistant.io/redirect/hacs_repository/?owner=geckoflume&repository=hass-recosante&category=integration)

## Configuration

### Configuration dans Home Assistant

La méthode de configuration consiste à utiliser l'interface utilisateur.

Il faut tout d'abord saisir le code postal de la commune dont on souhaite obtenir les données.

![image info](/img/location.png)
>**Note :**
>L'API se base sur le code INSEE. La récupération du code INSEE se fait via l'intégration, mais il peut y avoir plusieurs communes (donc plusieurs codes INSEE) pour un même code postal. Dans ce cas, une étape supplémentaire demande de préciser la commune (sélectionnable dans une liste) pour ne récupérer qu'un code INSEE.
>**Note :**
>L'API se base sur le code INSEE. La récupération du code INSEE se fait via l'intégration, mais il peut y avoir plusieurs communes (donc plusieurs codes INSEE) pour un même code postal. Dans ce cas, une étape supplémentaire demande de préciser la commune (sélectionnable dans une liste) pour ne récupérer qu'un code INSEE.

![image info](/img/multiloc.png)

### Données

Les informations présentées sont les niveaux de pollution sur une échelle de 1 (Bon) à 5 (Trés Mauvais).

Le libellé du niveau est présent sous forme d'attribut du sensor. Sont également présents dans les attributs, la date et heure (UTC) de la mise à jour des données par Recosanté. **Les données sont mises à jour une fois par jour par Recosanté.**

![image info](/img/attributs.png)
