# visualizer.py
import pygame
import sys
import random
import math
import time
from sorting import SORTING_ALGORITHMS, generate_list # Utilise les générateurs bruts ici

# --- Initialisation Pygame ---
pygame.init()
pygame.mixer.init() # Initialisation du module son

# --- Constantes (Mettre dans config.py serait mieux) ---
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 700
FPS = 60

# Couleurs de base (Thème par défaut - peut-être "Antique")
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (128, 128, 128)
LIGHT_GRAY = (211, 211, 211)
SAND = (244, 164, 96) # Thème antique
DARK_SAND = (210, 140, 65)
HIGHLIGHT_COLOR = (0, 255, 0, 150) # Vert semi-transparent pour comparaison
SWAP_COLOR = (255, 0, 0, 150)     # Rouge semi-transparent pour échange
BAR_COLOR = SAND
BACKGROUND_COLOR = DARK_SAND

# Polices
try:
    TITLE_FONT = pygame.font.Font(None, 74) # Ou charger depuis assets/fonts/
    UI_FONT = pygame.font.Font(None, 36)
    STATS_FONT = pygame.font.Font(None, 28)
except pygame.error:
    print("Erreur chargement police par défaut. Utilisation fallback.")
    TITLE_FONT = pygame.font.SysFont('arial', 74)
    UI_FONT = pygame.font.SysFont('arial', 36)
    STATS_FONT = pygame.font.SysFont('arial', 28)

# Sons (Charger depuis assets/sounds/)
try:
    # Remplace None par les objets Sound chargés si les fichiers existent
    sound_compare = pygame.mixer.Sound("assets/sounds/compare.wav") if "assets/sounds/compare.wav" else None 
    sound_swap = pygame.mixer.Sound("assets/sounds/swap.wav") if "assets/sounds/swap.wav" else None
    sound_done = pygame.mixer.Sound("assets/sounds/done.mp3") if "assets/sounds/done.mp3" else None
    sound_click = pygame.mixer.Sound("assets/sounds/click.wav") if "assets/sounds/click.wav" else None
    if sound_compare: sound_compare.set_volume(0.3)
    if sound_swap: sound_swap.set_volume(0.5)
    if sound_click: sound_click.set_volume(0.7)
except pygame.error as e:
    print(f"Erreur chargement sons : {e}. Les sons seront désactivés.")
    sound_compare, sound_swap, sound_done, sound_click = None, None, None, None

# --- Classe principale de la visualisation ---
class Visualizer:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Les Papyrus de Héron - Visualisation de Tri")
        self.clock = pygame.time.Clock()

        self.algorithms = SORTING_ALGORITHMS
        self.selected_algorithm_name = list(self.algorithms.keys())[0]
        self.list_data = []
        self.list_size = 50 # Taille par défaut
        self.min_val = 0.0
        self.max_val = 100.0
        self.disorder_type = 'random'
        self.theme = 'egyptian' # egyptian, futuristic, natural
        self.visualization_type = 'bars' # bars, circle, spiral, grid

        self.sorting_generator = None
        self.is_sorting = False
        self.is_paused = False
        self.step_by_step = False
        self.sort_speed = 1.0 # Facteur de vitesse (1.0 = normal)

        self.comparisons = 0
        self.swaps = 0
        self.start_time = 0
        self.time_elapsed = 0

        self.current_compared = ()
        self.current_swapped = ()
        
        self.state = 'menu' # 'menu', 'sorting', 'finished'

        self._setup_ui()
        self.apply_theme() # Appliquer le thème initial

    def _setup_ui(self):
        # Définir les zones cliquables (Rect) pour les boutons, etc.
        self.buttons = {} 
        # Exemple: self.buttons['start_button'] = pygame.Rect(x, y, w, h)
        # Créer des boutons pour chaque algo, taille, désordre, thème, etc.
        # ... (Implémentation détaillée nécessaire)

    def apply_theme(self):
        # Change les couleurs, potentiellement les images de fond
        global BACKGROUND_COLOR, BAR_COLOR, HIGHLIGHT_COLOR, SWAP_COLOR 
        if self.theme == 'egyptian':
            BACKGROUND_COLOR = DARK_SAND
            BAR_COLOR = SAND
            # Charger image de fond ?
        elif self.theme == 'futuristic':
            BACKGROUND_COLOR = (10, 10, 40) # Bleu foncé
            BAR_COLOR = (0, 200, 255) # Cyan
            HIGHLIGHT_COLOR = (0, 255, 0, 150)
            SWAP_COLOR = (255, 0, 255, 150) # Magenta
        elif self.theme == 'natural':
            BACKGROUND_COLOR = (34, 139, 34) # Vert forêt
            BAR_COLOR = (160, 82, 45) # Sienna (bois)
            HIGHLIGHT_COLOR = (255, 255, 0, 150) # Jaune
            SWAP_COLOR = (255, 69, 0, 150) # Orange-Rouge
        # Ajouter d'autres thèmes
        print(f"Thème appliqué: {self.theme}")


    def run(self):
        running = True
        while running:
            self.handle_input()
            if self.state == 'sorting' and not self.is_paused:
                self.update_sorting()
            
            self.draw()
            self.clock.tick(FPS)

        pygame.quit()
        sys.exit()

    def handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            if event.type == pygame.KEYDOWN:
                 if event.key == pygame.K_ESCAPE: # Quitter le tri en cours vers le menu
                     self.reset_sorting()
                     self.state = 'menu'
                 if event.key == pygame.K_SPACE and self.is_sorting: # Pause/Reprendre
                     self.is_paused = not self.is_paused
                     if not self.is_paused:
                         self.start_time = time.perf_counter() - self.time_elapsed # Reprend le chrono
                 if event.key == pygame.K_RIGHT and self.is_paused and self.step_by_step: # Pas-à-pas
                     self.update_sorting(force_step=True)
                 if event.key == pygame.K_UP: # Augmenter vitesse
                     self.sort_speed = min(10.0, self.sort_speed * 1.2)
                 if event.key == pygame.K_DOWN: # Diminuer vitesse
                     self.sort_speed = max(0.1, self.sort_speed / 1.2)
                 if event.key == pygame.K_r: # Reset la visualisation avec les mêmes paramètres
                     self.start_sorting()


            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1: # Clic gauche
                    if self.state == 'menu':
                        self.handle_menu_clicks(event.pos)
                    elif self.state == 'sorting' or self.state == 'finished':
                        self.handle_sorting_clicks(event.pos) # Pour boutons pause/reset etc.


    def handle_menu_clicks(self, mouse_pos):
        # Vérifier si un bouton du menu a été cliqué
        # Exemple simplifié :
        # if self.buttons['algo_bubble'].collidepoint(mouse_pos):
        #     self.selected_algorithm_name = "Bubble Sort"
        #     if sound_click: sound_click.play()
        # elif self.buttons['size_medium'].collidepoint(mouse_pos):
        #     self.list_size = 50
        #     if sound_click: sound_click.play()
        # ... etc pour tous les boutons (algos, tailles, désordres, thèmes, type de visu) ...
        
        # Bouton pour démarrer le tri (exemple)
        start_button_rect = pygame.Rect(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT - 100, 200, 50) # À définir précisément
        if start_button_rect.collidepoint(mouse_pos):
             if sound_click: sound_click.play()
             self.start_sorting()

    def handle_sorting_clicks(self, mouse_pos):
         # Gérer clics sur boutons pendant le tri (ex: Pause, Reset, Menu)
         reset_button_rect = pygame.Rect(10, SCREEN_HEIGHT - 60, 100, 40) # À définir
         menu_button_rect = pygame.Rect(120, SCREEN_HEIGHT - 60, 100, 40) # À définir
         
         if reset_button_rect.collidepoint(mouse_pos):
             if sound_click: sound_click.play()
             self.start_sorting() # Relance avec les mêmes params
         elif menu_button_rect.collidepoint(mouse_pos):
             if sound_click: sound_click.play()
             self.reset_sorting()
             self.state = 'menu'


    def generate_new_list(self):
        self.list_data = generate_list(self.list_size, self.min_val, self.max_val, self.disorder_type)
        # Normaliser si nécessaire pour certaines visualisations (ex: couleurs)
        self.max_list_val = max(self.list_data) if self.list_data else 1 # Éviter division par zéro


    def start_sorting(self):
        self.generate_new_list()
        if not self.list_data:
            print("Impossible de trier une liste vide.")
            return

        sort_function = self.algorithms[self.selected_algorithm_name]
        self.sorting_generator = sort_function(self.list_data[:]) # Travaille sur une copie
        
        self.is_sorting = True
        self.is_paused = False
        self.step_by_step = False # Mettre à True si un mode pas-à-pas est activé via UI
        self.comparisons = 0
        self.swaps = 0
        self.start_time = time.perf_counter()
        self.time_elapsed = 0
        self.current_compared = ()
        self.current_swapped = ()
        self.state = 'sorting'
        print(f"Démarrage du tri: {self.selected_algorithm_name} ({self.list_size} éléments, type: {self.disorder_type})")

    def reset_sorting(self):
        self.is_sorting = False
        self.sorting_generator = None
        self.list_data = [] # Ou garder la dernière liste générée?
        self.comparisons = 0
        self.swaps = 0
        self.time_elapsed = 0
        self.current_compared = ()
        self.current_swapped = ()


    def update_sorting(self, force_step=False):
        if not self.is_sorting or (self.is_paused and not force_step):
            return

        if self.sorting_generator:
            try:
                # Ajuster le nombre d'étapes par frame basé sur la vitesse
                steps_to_take = max(1, int(self.sort_speed)) if not force_step else 1
                
                final_step_data = None
                for _ in range(steps_to_take):
                     if self.sorting_generator is None: break # Peut être arrêté entre temps
                     
                     step_data = next(self.sorting_generator)
                     # step_data = (list_state, compared_indices, swapped_indices, comps, swaps)
                     self.list_data = step_data[0]
                     self.current_compared = step_data[1]
                     self.current_swapped = step_data[2]
                     self.comparisons = step_data[3]
                     self.swaps = step_data[4]
                     final_step_data = step_data # Garder le dernier état de cette frame

                     # Jouer les sons (seulement pour le dernier état de la frame pour éviter cacophonie)
                     if _ == steps_to_take - 1:
                         if self.current_compared and sound_compare:
                             sound_compare.play()
                         elif self.current_swapped and sound_swap:
                             sound_swap.play()
                
                # Mettre à jour le temps écoulé si pas en pause
                if not self.is_paused:
                     self.time_elapsed = time.perf_counter() - self.start_time
                
                # Si en mode pas-à-pas et forcé, on repasse en pause après l'étape
                if force_step:
                    self.is_paused = True

            except StopIteration:
                print("Tri terminé!")
                self.is_sorting = False
                self.state = 'finished'
                self.current_compared = ()
                self.current_swapped = ()
                self.sorting_generator = None # Important
                if sound_done: sound_done.play()
            except Exception as e:
                print(f"Erreur pendant le tri: {e}")
                self.reset_sorting()
                self.state = 'menu' # Retour au menu en cas d'erreur

    def draw(self):
        self.screen.fill(BACKGROUND_COLOR) # Applique la couleur de fond du thème

        if self.state == 'menu':
            self.draw_menu()
        elif self.state == 'sorting' or self.state == 'finished':
            self.draw_sorting_interface()
            self.draw_stats()
            self.draw_controls() # Dessine les boutons Pause, Reset, etc.
            if self.state == 'finished':
                 # Afficher message "Terminé"
                 finish_text = TITLE_FONT.render("Tri Terminé!", True, WHITE)
                 finish_rect = finish_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
                 self.screen.blit(finish_text, finish_rect)


        pygame.display.flip()

    def draw_menu(self):
         # Dessiner le titre, les options (algos, taille, désordre, thème, visu), le bouton Start
         title_surf = TITLE_FONT.render("Les Papyrus de Héron", True, WHITE)
         title_rect = title_surf.get_rect(center=(SCREEN_WIDTH // 2, 50))
         self.screen.blit(title_surf, title_rect)
         
         # --- Dessiner les boutons --- (Exemple simplifié)
         y_offset = 150
         # Algorithmes
         algo_label = UI_FONT.render("Algorithme:", True, WHITE)
         self.screen.blit(algo_label, (50, y_offset))
         col_width = 200
         row_height = 40
         for i, name in enumerate(self.algorithms.keys()):
              btn_rect = pygame.Rect(250 + (i % 3) * col_width, y_offset + (i // 3) * row_height, col_width - 10, row_height - 5)
              is_selected = (name == self.selected_algorithm_name)
              btn_color = LIGHT_GRAY if is_selected else GRAY
              pygame.draw.rect(self.screen, btn_color, btn_rect)
              btn_text = STATS_FONT.render(name, True, BLACK)
              btn_text_rect = btn_text.get_rect(center=btn_rect.center)
              self.screen.blit(btn_text, btn_text_rect)
              # Stocker le rect pour la détection de clic
              self.buttons[f'algo_{name}'] = btn_rect

         # Ajouter les autres options (Taille, Désordre, Thème, Visualisation) de manière similaire...
         # ...
         
         # Bouton Démarrer
         start_btn_rect = pygame.Rect(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT - 100, 200, 50)
         pygame.draw.rect(self.screen, (0, 180, 0), start_btn_rect) # Vert
         start_text = UI_FONT.render("Commencer le Tri", True, WHITE)
         start_text_rect = start_text.get_rect(center=start_btn_rect.center)
         self.screen.blit(start_text, start_text_rect)
         self.buttons['start_button'] = start_btn_rect # Stocker pour clic


    def draw_sorting_interface(self):
        if not self.list_data:
            return

        if self.visualization_type == 'bars':
            self.draw_bars()
        elif self.visualization_type == 'circle':
            self.draw_circle()
        # Ajouter elif pour 'spiral', 'grid'...

    def draw_bars(self):
        num_bars = len(self.list_data)
        # Ajuster la zone de dessin pour laisser de la place aux stats/contrôles
        drawing_area_height = SCREEN_HEIGHT - 150 
        drawing_area_y_start = 50
        
        # Calculer largeur et espacement des barres
        total_width = SCREEN_WIDTH * 0.9 # Utiliser 90% de la largeur
        bar_spacing = 2 
        bar_width = (total_width - (num_bars - 1) * bar_spacing) / num_bars
        start_x = (SCREEN_WIDTH - total_width) // 2

        # Valeur max pour normaliser la hauteur
        max_val = self.max_list_val 
        if max_val == 0: max_val = 1 # Éviter division par zéro

        for i, val in enumerate(self.list_data):
            bar_height = (val / max_val) * (drawing_area_height * 0.95) # Hauteur proportionnelle
            bar_x = start_x + i * (bar_width + bar_spacing)
            bar_y = drawing_area_y_start + drawing_area_height - bar_height
            
            rect = pygame.Rect(bar_x, bar_y, bar_width, bar_height)
            
            # Couleur de base
            color = BAR_COLOR
            
            # Dessiner la barre
            pygame.draw.rect(self.screen, color, rect)

            # --- Ajout des effets visuels ---
            # Créer une surface pour le highlighting (avec alpha)
            highlight_surface = pygame.Surface((bar_width, bar_height), pygame.SRCALPHA)

            # Appliquer surbrillance/couleur spéciale
            if i in self.current_compared:
                 highlight_surface.fill(HIGHLIGHT_COLOR)
                 self.screen.blit(highlight_surface, (bar_x, bar_y))
            if i in self.current_swapped:
                 highlight_surface.fill(SWAP_COLOR)
                 self.screen.blit(highlight_surface, (bar_x, bar_y))
                 
            # Ajouter ombres (optionnel, coûteux en perf)
            # shadow_offset = 2
            # shadow_rect = pygame.Rect(bar_x + shadow_offset, bar_y + shadow_offset, bar_width, bar_height)
            # pygame.draw.rect(self.screen, (0,0,0,50), shadow_rect) # Ombre noire semi-transparente


    def draw_circle(self):
         # Implémentation pour la visualisation en cercle
         # Mapper les valeurs en couleurs (ex: teinte HSV) et les positions en angles
         center_x, center_y = SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50 # Ajuster le centre
         max_radius = min(SCREEN_WIDTH, SCREEN_HEIGHT) * 0.35
         num_items = len(self.list_data)
         angle_step = 360 / num_items if num_items > 0 else 0
         
         max_val = self.max_list_val if self.max_list_val > 0 else 1

         for i, val in enumerate(self.list_data):
             angle_rad = math.radians(i * angle_step - 90) # -90 pour commencer en haut
             
             # Mapper valeur en couleur (Teinte varie de 0 à 360)
             hue = (val / max_val) * 360
             color = pygame.Color(0)
             color.hsva = (hue % 360, 100, 100, 100) # Saturation, Value, Alpha = 100%
             
             # Position
             x = center_x + math.cos(angle_rad) * max_radius
             y = center_y + math.sin(angle_rad) * max_radius
             
             # Dessiner un point ou un petit cercle
             point_radius = 5
             pygame.draw.circle(self.screen, color, (int(x), int(y)), point_radius)

             # Highlight (plus simple : dessiner un cercle plus grand autour)
             highlight_radius = 8
             if i in self.current_compared:
                 pygame.draw.circle(self.screen, HIGHLIGHT_COLOR, (int(x), int(y)), highlight_radius, 2) # Largeur 2
             if i in self.current_swapped:
                 pygame.draw.circle(self.screen, SWAP_COLOR, (int(x), int(y)), highlight_radius, 2)


    # Ajouter draw_spiral(), draw_grid() ...

    def draw_stats(self):
        # Afficher les infos : algo, comparaisons, échanges, temps
        algo_text = f"Algorithme: {self.selected_algorithm_name}"
        comp_text = f"Comparaisons: {self.comparisons}"
        swap_text = f"Échanges: {self.swaps}"
        time_text = f"Temps écoulé: {self.time_elapsed:.3f} s"
        speed_text = f"Vitesse: x{self.sort_speed:.1f}"

        texts = [algo_text, comp_text, swap_text, time_text, speed_text]
        y_pos = SCREEN_HEIGHT - 100 # Positionnement en bas

        for i, text in enumerate(texts):
            surf = STATS_FONT.render(text, True, WHITE)
            rect = surf.get_rect(left=10, top=y_pos + i * 25)
            self.screen.blit(surf, rect)
            
    def draw_controls(self):
         # Dessiner les boutons interactifs (Pause/Play, Reset, Menu, Step?)
         # Exemple simplifié pour Reset et Menu
         reset_btn_rect = pygame.Rect(SCREEN_WIDTH - 230, SCREEN_HEIGHT - 60, 100, 40) 
         menu_btn_rect = pygame.Rect(SCREEN_WIDTH - 120, SCREEN_HEIGHT - 60, 100, 40)
         
         pygame.draw.rect(self.screen, GRAY, reset_btn_rect)
         reset_text = STATS_FONT.render("Reset (R)", True, BLACK)
         self.screen.blit(reset_text, reset_text.get_rect(center=reset_btn_rect.center))
         self.buttons['reset_button'] = reset_btn_rect

         pygame.draw.rect(self.screen, GRAY, menu_btn_rect)
         menu_text = STATS_FONT.render("Menu (Esc)", True, BLACK)
         self.screen.blit(menu_text, menu_text.get_rect(center=menu_btn_rect.center))
         self.buttons['menu_button'] = menu_btn_rect

         # Bouton Pause/Play (change de texte)
         pause_btn_rect = pygame.Rect(SCREEN_WIDTH - 340, SCREEN_HEIGHT - 60, 100, 40)
         pause_text_str = "Pause (Spc)" if not self.is_paused else "Play (Spc)"
         pygame.draw.rect(self.screen, GRAY, pause_btn_rect)
         pause_text = STATS_FONT.render(pause_text_str, True, BLACK)
         self.screen.blit(pause_text, pause_text.get_rect(center=pause_btn_rect.center))
         self.buttons['pause_button'] = pause_btn_rect 
         # Note: La logique de clic pour Pause est gérée au clavier pour l'instant


# --- Point d'entrée ---
if __name__ == '__main__':
    visualizer = Visualizer()
    visualizer.run()