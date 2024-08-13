import pygame
import sys
import ctypes

# Initialiser Pygame
pygame.init()

# Configurer la fenêtre
SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Nono's Normal Adventure")

# Couleurs
WHITE = (255, 255, 255)
GRAY = (200, 200, 200)
BLACK = (0, 0, 0)
DIALOGUE_BOX_COLOR = (0, 0, 0, 180)  # Couleur de la boîte de dialogue avec transparence

# Charger les images
def load_image(filename, size=None):
    try:
        image = pygame.image.load(filename)
        if size:
            image = pygame.transform.scale(image, size)
        return image
    except pygame.error as e:
        print(f"Erreur lors du chargement de l'image {filename} : {e}")
        return None

background_game = load_image("background_game.png")
npc_image = load_image("Kira.png", (50, 100))
arrow_image = load_image("arrow.png", (30, 30))
killerqueen_image = load_image("killerqueen.png", (50, 100))

# Charger le son
def load_sound(filename):
    try:
        pygame.mixer.music.load(filename)
        return True
    except pygame.error as e:
        print(f"Erreur lors du chargement du son {filename} : {e}")
        return False

sound_loaded = load_sound("killerqueen.mp3")

# Police de caractères
font = pygame.font.Font(None, 74)
small_font = pygame.font.Font(None, 36)
dialogue_font = pygame.font.Font(None, 20)  # Police réduite pour le dialogue

# Fonction pour dessiner le texte
def draw_text(text, font, color, surface, x, y):
    textobj = font.render(text, True, color)
    textrect = textobj.get_rect()
    textrect.center = (x, y)
    surface.blit(textobj, textrect)

# Fonction pour dessiner un bouton
def draw_button(text, rect, color, hover_color):
    mouse_pos = pygame.mouse.get_pos()
    is_hovered = rect.collidepoint(mouse_pos)
    pygame.draw.rect(screen, hover_color if is_hovered else color, rect)
    draw_text(text, small_font, BLACK, screen, rect.centerx, rect.centery)

# Fonction pour mettre l'ordinateur en veille
def put_computer_to_sleep():
    ctypes.windll.kernel32.SetThreadExecutionState(0x80000002)  # Met l'ordinateur en veille (Windows uniquement)

# Fonction pour dessiner un personnage
def draw_human(x, y):
    pygame.draw.circle(screen, WHITE, (x, y), 20)  # Tête
    pygame.draw.line(screen, WHITE, (x, y + 20), (x, y + 80), 3)  # Corps
    pygame.draw.line(screen, WHITE, (x - 30, y + 40), (x + 30, y + 40), 3)  # Bras
    pygame.draw.line(screen, WHITE, (x, y + 80), (x - 20, y + 140), 3)  # Jambe gauche
    pygame.draw.line(screen, WHITE, (x, y + 80), (x + 20, y + 140), 3)  # Jambe droite

# Fonction pour dessiner un PNJ avec dialogue
def draw_npc(x, y):
    screen.blit(npc_image, (x - 25, y - 50))
    if pygame.mouse.get_pos()[0] in range(x - 25, x + 25) and pygame.mouse.get_pos()[1] in range(y - 50, y + 50):
        dialogue = (
            "Je m'appelle Yoshikage Kira. J'ai 33 ans. Ma maison se trouve dans la partie nord-est de Morioh, "
            "où se trouvent toutes les villas, et je ne suis pas mariée. Je travaille comme employé dans les grands "
            "magasins de Kame Yu, et je rentre chez moi tous les jours au plus tard à 20 heures. Je ne fume pas, mais je "
            "bois de temps en temps. Je suis au lit à 23 h et je dois dormir huit heures, quoi qu'il arrive. Après avoir "
            "bu un verre de lait chaud et fait une vingtaine de minutes d'étirements avant d'aller au lit, je n'ai généralement "
            "aucun problème à dormir jusqu'au matin. Comme un bébé, je me réveille sans fatigue ni stress le matin. On m'a "
            "dit qu'il n'y avait aucun problème lors de mon dernier contrôle. J'essaie d'expliquer que je suis une personne "
            "qui souhaite vivre une vie très tranquille. Je prends soin de ne pas me préoccuper d'ennemis, comme gagner ou "
            "perdre, qui me feraient perdre le sommeil la nuit. C'est ainsi que je traite la société, et je sais que c'est ce "
            "qui m'apporte le bonheur. Mais si je me battais, je ne perdrais face à personne."
        )
        # Créer une boîte de dialogue
        dialogue_box_rect = pygame.Rect(x - 200, SCREEN_HEIGHT - 100, 400, 80)
        pygame.draw.rect(screen, DIALOGUE_BOX_COLOR, dialogue_box_rect)
        
        # Afficher le texte de dialogue dans la boîte
        lines = [dialogue[i:i+40] for i in range(0, len(dialogue), 40)]  # Découper le texte en lignes de 40 caractères
        y_offset = SCREEN_HEIGHT - 95
        for line in lines:
            draw_text(line, dialogue_font, WHITE, screen, dialogue_box_rect.centerx, y_offset)
            y_offset += 20

# Fonction pour dessiner le PNJ Killer Queen
def draw_killer_queen(x, y):
    screen.blit(killerqueen_image, (x - 25, y - 50))

# Fonction pour afficher le jeu
def game_loop():
    player_pos = [SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2]
    player_speed = 5
    npc_pos = [SCREEN_WIDTH // 4, SCREEN_HEIGHT // 2]
    arrow_pos = [SCREEN_WIDTH // 3, SCREEN_HEIGHT // 3]
    killer_queen_pos = None  # Position de Killer Queen
    killer_queen_active = False
    killer_queen_started = False
    clock = pygame.time.Clock()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            player_pos[0] -= player_speed
        if keys[pygame.K_RIGHT]:
            player_pos[0] += player_speed
        if keys[pygame.K_UP]:
            player_pos[1] -= player_speed
        if keys[pygame.K_DOWN]:
            player_pos[1] += player_speed

        # Limiter les mouvements du personnage pour qu'il reste dans les limites de l'écran
        player_pos[0] = max(20, min(SCREEN_WIDTH - 20, player_pos[0]))
        player_pos[1] = max(20, min(SCREEN_HEIGHT - 20, player_pos[1]))

        # Vérifier la collision avec l'arrow
        player_rect = pygame.Rect(player_pos[0] - 20, player_pos[1] - 20, 40, 40)
        arrow_rect = pygame.Rect(arrow_pos[0] - 15, arrow_pos[1] - 15, 30, 30)
        if player_rect.colliderect(arrow_rect):
            if not killer_queen_active:
                killer_queen_active = True
                if not killer_queen_started and sound_loaded:
                    pygame.mixer.music.play()
                    killer_queen_started = True

        if killer_queen_active:
            killer_queen_pos = player_pos  # La Killer Queen suit le personnage

        # Dessiner l'image de fond du jeu
        screen.blit(background_game, (0, 0))

        # Dessiner les éléments du jeu
        draw_human(player_pos[0], player_pos[1])
        draw_npc(npc_pos[0], npc_pos[1])
        if killer_queen_active:
            draw_killer_queen(killer_queen_pos[0], killer_queen_pos[1])
        screen.blit(arrow_image, arrow_pos)

        pygame.display.flip()
        clock.tick(30)

# Fonction pour l'écran titre
def title_screen():
    play_button = pygame.Rect(200, 150, 240, 60)
    options_button = pygame.Rect(200, 230, 240, 60)
    sleep_button = pygame.Rect(200, 310, 240, 60)
    clock = pygame.time.Clock()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if play_button.collidepoint(event.pos):
                    return  # Quitter l'écran titre pour commencer le jeu
                elif options_button.collidepoint(event.pos):
                    print("Options clicked")  # Remplace par l'appel de la fonction d'options
                elif sleep_button.collidepoint(event.pos):
                    put_computer_to_sleep()

        screen.fill(WHITE)  # Remplir l'écran avec la couleur blanche
        draw_text("Nono's Normal Adventure", font, BLACK, screen, SCREEN_WIDTH // 2, 80)
        draw_button("Play", play_button, GRAY, BLACK)
        draw_button("Options", options_button, GRAY, BLACK)
        draw_button("You can't exit", sleep_button, GRAY, BLACK)
        
        pygame.display.flip()
        clock.tick(30)

# Boucle principale
def main():
    title_screen()  # Afficher l'écran titre
    game_loop()     # Commencer le jeu après avoir quitté l'écran titre

# Appel de la fonction principale
if __name__ == "__main__":
    main()
