# sorting.py
import random
import time # Pour l'analyse de performance basique

def _measure_time(func):
    """Décorateur simple pour mesurer le temps d'exécution."""
    def wrapper(*args, **kwargs):
        start_time = time.perf_counter()
        # Exécute le générateur jusqu'à la fin pour obtenir le résultat final et les stats
        gen = func(*args, **kwargs)
        final_state = None
        comparisons = 0
        swaps = 0
        try:
            while True:
                state = next(gen)
                # Dans une utilisation réelle pour la visu, on traiterait 'state' ici
                # Pour la mesure de temps, on capture juste les dernières stats
                final_state = state[0] # La liste triée
                comparisons = state[3] if len(state) > 3 else comparisons
                swaps = state[4] if len(state) > 4 else swaps
        except StopIteration:
            pass # Le générateur est épuisé

        end_time = time.perf_counter()
        execution_time = end_time - start_time
        print(f"Algorithme: {func.__name__}")
        print(f"Temps d'exécution: {execution_time:.6f} secondes")
        print(f"Comparaisons: {comparisons}")
        print(f"Échanges: {swaps}")
        # Retourne la liste triée pour la version CLI
        return final_state
    return wrapper

# --- Implémentations des Générateurs de Tri ---

# Chaque fonction doit yield au moins:
# yield list_state, compared_indices, swapped_indices, comparison_count, swap_count

def selection_sort(arr):
    """Tri par sélection. Yield l'état après chaque swap."""
    n = len(arr)
    comparisons = 0
    swaps = 0
    for i in range(n):
        min_idx = i
        for j in range(i + 1, n):
            comparisons += 1
            yield arr, (i, j), (), comparisons, swaps # Comparaison
            if arr[j] < arr[min_idx]:
                min_idx = j
        
        if min_idx != i:
            arr[i], arr[min_idx] = arr[min_idx], arr[i]
            swaps += 1
            yield arr, (), (i, min_idx), comparisons, swaps # Swap
        # Optionnel: yield après chaque passage externe pour marquer la partie triée
        yield arr, (), (), comparisons, swaps 
    yield arr, (), (), comparisons, swaps # État final

def bubble_sort(arr):
    """Tri à bulles. Yield l'état après chaque comparaison et swap."""
    n = len(arr)
    comparisons = 0
    swaps = 0
    for i in range(n):
        swapped_in_pass = False
        for j in range(0, n - i - 1):
            comparisons += 1
            yield arr, (j, j + 1), (), comparisons, swaps # Comparaison
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                swaps += 1
                swapped_in_pass = True
                yield arr, (), (j, j + 1), comparisons, swaps # Swap
        if not swapped_in_pass:
            break # Optimisation: si pas d'échange, la liste est triée
    yield arr, (), (), comparisons, swaps # État final

def insertion_sort(arr):
    """Tri par insertion. Yield l'état pendant le décalage et l'insertion."""
    n = len(arr)
    comparisons = 0
    swaps = 0
    for i in range(1, n):
        key = arr[i]
        j = i - 1
        # Comparaison initiale avant la boucle while
        comparisons += 1 
        yield arr, (i, j), (), comparisons, swaps # Comparaison initiale key vs arr[j]
        
        while j >= 0 and key < arr[j]:
            comparisons += 1 # Compte la comparaison dans la condition while
            arr[j + 1] = arr[j] # Décalage (considéré comme un 'swap' conceptuel pour la visu)
            swaps += 1 
            yield arr, (i, j), (j + 1, j), comparisons, swaps # Décalage
            j -= 1
            # Si j>=0, il y aura une autre comparaison dans le while suivant
            if j >= 0:
                 yield arr, (i, j), (), comparisons, swaps # Comparaison pour le prochain tour de while

        if arr[j + 1] != key: # Vérifie si un décalage a eu lieu
             arr[j + 1] = key
             # Pas un swap au sens strict, mais on peut le visualiser comme la fin du déplacement
             yield arr, (), (j + 1, i), comparisons, swaps # Insertion finale
        
    yield arr, (), (), comparisons, swaps # État final


# --- Tri Fusion (Merge Sort) ---
# Plus complexe à visualiser pas à pas avec yield de manière intuitive.
# Une approche est de yield l'état après chaque fusion partielle.

def merge_sort(arr):
    """Tri fusion (récursif). Yield l'état après chaque fusion."""
    comparisons = 0
    swaps = 0 # Merge sort ne fait pas de 'swaps' directs, mais on compte les écritures dans le tableau auxiliaire

    def merge(arr, left, mid, right):
        nonlocal comparisons, swaps
        n1 = mid - left + 1
        n2 = right - mid

        L = arr[left : mid + 1]
        R = arr[mid + 1 : right + 1]

        i = j = 0
        k = left

        while i < n1 and j < n2:
            comparisons += 1
            yield arr, (left + i, mid + 1 + j), (), comparisons, swaps # Comparaison entre L[i] et R[j]
            if L[i] <= R[j]:
                arr[k] = L[i]
                i += 1
            else:
                arr[k] = R[j]
                j += 1
            swaps += 1 # Compte chaque écriture dans arr
            yield arr, (), (k,), comparisons, swaps # Placement dans arr[k]
            k += 1

        while i < n1:
            arr[k] = L[i]
            swaps += 1
            yield arr, (), (k,), comparisons, swaps # Placement résiduel L
            i += 1
            k += 1

        while j < n2:
            arr[k] = R[j]
            swaps += 1
            yield arr, (), (k,), comparisons, swaps # Placement résiduel R
            j += 1
            k += 1

    def merge_sort_recursive(arr, left, right):
        if left < right:
            mid = left + (right - left) // 2
            yield from merge_sort_recursive(arr, left, mid)
            yield from merge_sort_recursive(arr, mid + 1, right)
            yield from merge(arr, left, mid, right)
            # Yield un état stable après la fusion complète de ce niveau
            yield arr, (), tuple(range(left, right + 1)), comparisons, swaps

    yield from merge_sort_recursive(arr, 0, len(arr) - 1)
    yield arr, (), (), comparisons, swaps # État final

# --- Tri Rapide (Quick Sort) ---
# Similaire à Merge Sort pour la complexité de visualisation.
# Yield avant/après partitionnement et pendant les swaps.

def quick_sort(arr):
    """Tri rapide (récursif). Yield pendant les swaps et après partition."""
    comparisons = 0
    swaps = 0

    def partition(arr, low, high):
        nonlocal comparisons, swaps
        pivot = arr[high]
        i = low - 1
        yield arr, (high,), tuple(range(low, high)), comparisons, swaps # Highlight pivot and range being partitioned

        for j in range(low, high):
            comparisons += 1
            yield arr, (j, high), (), comparisons, swaps # Compare arr[j] with pivot
            if arr[j] < pivot:
                i += 1
                arr[i], arr[j] = arr[j], arr[i]
                swaps += 1
                yield arr, (), (i, j), comparisons, swaps # Swap elements

        arr[i + 1], arr[high] = arr[high], arr[i + 1]
        swaps += 1
        yield arr, (), (i + 1, high), comparisons, swaps # Swap pivot into place
        return i + 1

    def quick_sort_recursive(arr, low, high):
        if low < high:
            pi = yield from partition(arr, low, high)
            yield arr, (), tuple(range(low, high+1)), comparisons, swaps # Show result of partition
            yield from quick_sort_recursive(arr, low, pi - 1)
            yield from quick_sort_recursive(arr, pi + 1, high)

    yield from quick_sort_recursive(arr, 0, len(arr) - 1)
    yield arr, (), (), comparisons, swaps # Final state

# --- Tri par Tas (Heap Sort) ---
def heap_sort(arr):
    """Tri par tas. Yield pendant le heapify et l'extraction."""
    n = len(arr)
    comparisons = 0
    swaps = 0

    def heapify(arr, n, i):
        nonlocal comparisons, swaps
        largest = i
        left = 2 * i + 1
        right = 2 * i + 2
        
        # Compare parent with left child
        if left < n:
            comparisons += 1
            yield arr, (i, left), (), comparisons, swaps
            if arr[left] > arr[largest]:
                largest = left
        
        # Compare current largest with right child
        if right < n:
            comparisons += 1
            yield arr, (largest, right), (), comparisons, swaps
            if arr[right] > arr[largest]:
                largest = right

        if largest != i:
            arr[i], arr[largest] = arr[largest], arr[i]
            swaps += 1
            yield arr, (), (i, largest), comparisons, swaps # Swap happened
            yield from heapify(arr, n, largest) # Recursively heapify the affected sub-tree

    # Construire le tas max (Build max heap)
    for i in range(n // 2 - 1, -1, -1):
        yield from heapify(arr, n, i)
        yield arr, (), tuple(range(n)), comparisons, swaps # Show state after heapifying node i

    # Extraire les éléments un par un (Extract elements one by one)
    for i in range(n - 1, 0, -1):
        arr[i], arr[0] = arr[0], arr[i] # Mettre le max à la fin
        swaps += 1
        yield arr, (), (0, i), comparisons, swaps # Swap root with last element
        yield from heapify(arr, i, 0) # Heapify la racine du tas réduit
        yield arr, (), tuple(range(i)), comparisons, swaps # Show state after heapify root on reduced heap

    yield arr, (), (), comparisons, swaps # Final state


# --- Tri à Peigne (Comb Sort) ---
def comb_sort(arr):
    """Tri à peigne. Yield pendant les comparaisons et swaps."""
    n = len(arr)
    gap = n
    shrink = 1.3
    sorted_flag = False
    comparisons = 0
    swaps = 0

    while not sorted_flag:
        gap = int(gap / shrink)
        if gap <= 1:
            gap = 1
            sorted_flag = True # Potentiellement trié, on vérifie une dernière fois

        i = 0
        while i + gap < n:
            comparisons += 1
            yield arr, (i, i + gap), (), comparisons, swaps # Comparaison
            if arr[i] > arr[i + gap]:
                arr[i], arr[i + gap] = arr[i + gap], arr[i]
                swaps += 1
                sorted_flag = False # Un échange a eu lieu, donc pas encore trié
                yield arr, (), (i, i + gap), comparisons, swaps # Swap
            i += 1
            
    yield arr, (), (), comparisons, swaps # Final state


# --- Dictionnaire des algorithmes pour accès facile ---
# Utilise les versions décorées pour main.py, les versions brutes pour visualizer.py
SORTING_ALGORITHMS = {
    "Selection Sort": selection_sort,
    "Bubble Sort": bubble_sort,
    "Insertion Sort": insertion_sort,
    "Merge Sort": merge_sort,
    "Quick Sort": quick_sort,
    "Heap Sort": heap_sort,
    "Comb Sort": comb_sort,
}

SORTING_ALGORITHMS_TIMED = {
    "Selection Sort": _measure_time(selection_sort),
    "Bubble Sort": _measure_time(bubble_sort),
    "Insertion Sort": _measure_time(insertion_sort),
    "Merge Sort": _measure_time(merge_sort),
    "Quick Sort": _measure_time(quick_sort),
    "Heap Sort": _measure_time(heap_sort),
    "Comb Sort": _measure_time(comb_sort),
}

# --- Fonctions utilitaires ---
def generate_list(size, min_val=0.0, max_val=100.0, disorder_type='random'):
    """Génère une liste de nombres réels avec différents types de désordre."""
    if disorder_type == 'random':
        return [random.uniform(min_val, max_val) for _ in range(size)]
    elif disorder_type == 'sorted':
        return sorted([random.uniform(min_val, max_val) for _ in range(size)])
    elif disorder_type == 'reversed':
        return sorted([random.uniform(min_val, max_val) for _ in range(size)], reverse=True)
    elif disorder_type == 'nearly_sorted':
        arr = sorted([random.uniform(min_val, max_val) for _ in range(size)])
        # Introduire quelques swaps pour le désordre léger
        swaps = max(1, size // 10) 
        for _ in range(swaps):
            i, j = random.sample(range(size), 2)
            arr[i], arr[j] = arr[j], arr[i]
        return arr
    else: # Défaut sur random
        return [random.uniform(min_val, max_val) for _ in range(size)]