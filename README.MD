# Les Papyrus de Héron : Visualiseur d'Algorithmes de Tri

![Concept Image](path/to/concept_image.png) ## Contexte Narratif

Dans le tumulte intellectuel de la Grande Bibliothèque d’Alexandrie, l'illustre Héron (Ier siècle apr. J.-C.) est consterné par le désordre des précieux papyrus. Inspirés par sa quête d'ordre, ce projet Python moderne utilise la puissance des algorithmes de tri et la magie visuelle de Pygame pour explorer et comparer différentes méthodes d'organisation, comme Héron aurait pu l'imaginer avec les outils d'aujourd'hui.

## Fonctionnalités

* **Algorithmes Implémentés :**
    * Tri par Sélection
    * Tri à Bulles
    * Tri par Insertion
    * Tri Fusion (Merge Sort)
    * Tri Rapide (Quick Sort)
    * Tri par Tas (Heap Sort)
    * Tri à Peigne (Comb Sort)
* **Interface Graphique (Pygame) :**
    * Menu principal intuitif pour la sélection des paramètres.
    * Visualisation en temps réel du processus de tri.
    * Plusieurs types de visualisations : Barres Verticales, Cercle de Couleurs, (autres à ajouter: Spirale, Grille).
    * Thèmes visuels personnalisables : Égyptien Antique, Futuriste High-Tech, Naturel Apaisant.
    * Animations fluides avec mise en évidence des comparaisons et échanges.
    * Contrôle interactif : Pause/Reprise, Vitesse ajustable, Pas-à-pas (si implémenté), Reset.
    * Statistiques en direct : Nombre de comparaisons, d'échanges, temps écoulé.
    * Effets sonores immersifs pour les actions clés.
* **Options de Configuration :**
    * Choix de l'algorithme de tri.
    * Sélection de la taille de la liste (Petite, Moyenne, Grande).
    * Choix du type de désordre initial (Aléatoire, Presque Triée, Inversée).
* **Analyse de Performance :** Mesure du temps d'exécution et comparaison basique (voir section dédiée).
* **Interface en Ligne de Commande :** Une version simplifiée (`main.py`) pour tester les tris sans l'interface graphique.

## Algorithmes Expliqués

*(Brève description de chaque algorithme, son principe de fonctionnement, et sa complexité temporelle moyenne/pire cas en notation Big O.)*

* **Tri par Sélection :** O(n²). Recherche le minimum et le place au début. Simple mais inefficace.
* **Tri à Bulles :** O(n²). Compare et échange les éléments adjacents. Généralement lent, sauf pour des listes presque triées (avec optimisation).
* **Tri par Insertion :** O(n²). Construit la liste triée un élément à la fois. Efficace pour les petites listes ou les listes presque triées.
* **Tri Fusion :** O(n log n). Diviser pour régner. Très efficace, stable, mais nécessite de la mémoire supplémentaire.
* **Tri Rapide :** O(n log n) en moyenne, O(n²) pire cas. Diviser pour régner avec pivot. Très rapide en pratique, mais non stable.
* **Tri par Tas :** O(n log n). Utilise une structure de données de tas. Efficace, pas stable, tri sur place.
* **Tri à Peigne :** Amélioration du tri à bulles, complexité proche de O(n log n) pour de nombreuses listes. Vise à éliminer les "tortues" (petits éléments en fin de liste).

## Installation et Utilisation

**Prérequis :**
* Python 3.7+
* Pip (gestionnaire de paquets Python)

**Installation :**

1.  **Cloner le dépôt :**
    ```bash
    git clone [https://github.com/VOTRE_NOM_UTILISATEUR/les-papyrus-de-heron.git](https://github.com/VOTRE_NOM_UTILISATEUR/les-papyrus-de-heron.git)
    cd les-papyrus-de-heron
    ```
2.  **Installer les dépendances :**
    ```bash
    pip install -r requirements.txt
    ```
    *(Créez le fichier `requirements.txt` avec `pygame` dedans)*

**Lancement :**

* **Visualiseur Graphique (Recommandé) :**
    ```bash
    python visualizer.py
    ```
    Utilisez la souris pour sélectionner les options dans le menu et cliquez sur "Commencer le Tri". Pendant le tri, utilisez les touches :
    * `ESPACE` : Pause / Reprendre
    * `HAUT` : Augmenter la vitesse
    * `BAS` : Diminuer la vitesse
    * `R` : Réinitialiser le tri avec les mêmes paramètres
    * `ESC` : Revenir au menu principal

* **Interface en Ligne de Commande :**
    ```bash
    python main.py
    ```
    Suivez les instructions dans le terminal pour choisir l'algorithme et la liste.

## Choix de Conception (Interface et Visualisation)

*(Expliquez ici pourquoi vous avez choisi certains aspects visuels, Pygame, la structure en générateur, les thèmes, etc.)*

* **Pygame :** Choisi pour sa flexibilité dans le dessin 2D et la gestion des événements, idéal pour une visualisation personnalisée.
* **Générateurs (`yield`) :** L'utilisation de générateurs dans `sorting.py` permet de découpler la logique de tri de la visualisation. Le visualiseur demande simplement l'étape suivante sans connaître les détails internes de l'algorithme, rendant l'ajout de nouveaux algorithmes plus facile.
* **Thèmes :** Pour offrir une expérience utilisateur riche et relier le projet au contexte narratif (Égyptien) tout en proposant des alternatives (Futuriste, Naturel).
* **Visualisations Multiples :** Proposer différentes manières de "voir" le tri (barres, cercle...) rend le concept plus tangible et intéressant d'un point de vue éducatif.
* **Effets Visuels/Sonores :** Visent à rendre l'expérience plus engageante et à fournir un retour immédiat sur les actions de l'algorithme (comparaison vs échange).

## Analyse des Performances

*(Présentez ici vos résultats. Un tableau comparatif serait idéal.)*

Des tests ont été effectués sur une machine [Votre Config CPU/RAM] avec des listes de tailles différentes (ex: 10, 50, 100, 500 éléments) et différents types de désordre initiaux.

| Algorithme         | Taille 50 (Aléatoire) | Taille 500 (Aléatoire) | Taille 500 (Presque Triée) | Taille 500 (Inversée) | Observations                                      |
|--------------------|-----------------------|------------------------|-----------------------------|-----------------------|---------------------------------------------------|
| Selection Sort     | ~X.XXX s              | ~Y.YYY s               | ~Y.YYY s                    | ~Y.YYY s              | Performances stables mais médiocres (O(n²)).       |
| Bubble Sort        | ~X.XXX s              | ~Y.YYY s               | ~Z.ZZZ s (rapide)           | ~Y.YYY s (lent)       | Lent, sauf si presque trié (avec optimisation). |
| Insertion Sort     | ~A.AAA s              | ~B.BBB s               | ~C.CCC s (très rapide)      | ~B.BBB s (lent)       | Bon pour petites listes ou presque triées.        |
| Merge Sort         | ~D.DDD s              | ~E.EEE s               | ~E.EEE s                    | ~E.EEE s              | Rapide et fiable (O(n log n)). Consommation mémoire. |
| Quick Sort         | ~D.DDD s              | ~E.EEE s               | ~E.EEE s                    | ~F.FFF s (lent si mauvais pivot) | Très rapide en moyenne. Sensible au pivot.      |
| Heap Sort          | ~D.DDD s              | ~E.EEE s               | ~E.EEE s                    | ~E.EEE s              | Rapide et fiable (O(n log n)), sur place.         |
| Comb Sort          | ~A.AAA s              | ~B.BBB s               | ~C.CCC s                    | ~B.BBB s              | Souvent plus rapide que Bubble/Insertion.         |

*(Remplacez X.XXX, etc. par vos mesures réelles. Ajoutez des commentaires sur quel algo est préférable dans quel scénario.)*

**Conclusions :**
* Pour les performances générales sur de grandes listes aléatoires, **Merge Sort, Heap Sort, et Quick Sort (en moyenne)** sont les meilleurs choix (O(n log n)).
* **Insertion Sort** est excellent pour les petites listes ou si les données sont déjà majoritairement triées.
* **Selection Sort** et **Bubble Sort** sont principalement éducatifs et à éviter pour des raisons de performance.
* **Comb Sort** offre une amélioration notable sur Bubble Sort.

*(Si la parallélisation est implémentée, ajoutez une section la comparant.)*

## Structure du Projet