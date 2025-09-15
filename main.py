# main.py
import random
from sorting import SORTING_ALGORITHMS_TIMED, generate_list # Utilise les versions timées ici

def main():
    print("Bienvenue aux Papyrus de Héron - Triage en Ligne de Commande")
    print("----------------------------------------------------------")

    # Choix de l'algorithme
    print("Algorithmes disponibles :")
    algo_names = list(SORTING_ALGORITHMS_TIMED.keys())
    for i, name in enumerate(algo_names):
        print(f"{i + 1}. {name}")

    while True:
        try:
            choice = int(input(f"Choisissez un algorithme (1-{len(algo_names)}): "))
            if 1 <= choice <= len(algo_names):
                algo_name = algo_names[choice - 1]
                sort_function = SORTING_ALGORITHMS_TIMED[algo_name]
                break
            else:
                print("Choix invalide.")
        except ValueError:
            print("Veuillez entrer un nombre.")

    # Choix de la liste
    print("\nOptions pour la liste :")
    print("1. Entrer la liste manuellement (nombres séparés par des espaces)")
    print("2. Générer une liste aléatoire")

    list_data = []
    while True:
        try:
            list_choice = int(input("Choisissez une option (1-2): "))
            if list_choice == 1:
                list_str = input("Entrez les nombres (flottants ou entiers) séparés par des espaces: ")
                list_data = [float(x) for x in list_str.split()]
                if list_data:
                    break
                else:
                    print("Liste vide, veuillez entrer des nombres.")
            elif list_choice == 2:
                size = int(input("Taille de la liste générée (ex: 10): "))
                min_val = float(input("Valeur minimale (ex: 0.0): "))
                max_val = float(input("Valeur maximale (ex: 100.0): "))
                if size > 0:
                    list_data = generate_list(size, min_val, max_val)
                    break
                else:
                    print("La taille doit être positive.")
            else:
                print("Choix invalide.")
        except ValueError:
            print("Entrée invalide. Assurez-vous d'entrer des nombres corrects.")

    # Affichage et Tri
    print("\nListe originale :")
    print(list_data)

    print(f"\nTri en cours avec {algo_name}...")
    
    # Copie pour ne pas modifier l'originale si la fonction de tri le fait in-place
    list_to_sort = list_data[:] 
    
    # Appelle la fonction (version timée qui imprime aussi les stats)
    sorted_list = sort_function(list_to_sort) 

    print("\nListe triée :")
    print(sorted_list)
    print("\n----------------------------------------------------------")


if __name__ == "__main__":
    main()