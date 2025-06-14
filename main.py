import pygame
import random
import sys

pygame.init()

# Constantes et paramètres
LARGEUR, HAUTEUR = 1000, 800
TAILLE_BLOC = 20
vitesse_base = 10

# Couleurs
NOIR = (18, 18, 18)
GRIS_FONCE = (30, 30, 30)
ROUGE = (220, 40, 40)
BLANC = (245, 245, 245)
OMBRE = (60, 60, 60)

# Initialisation fenêtre redimensionnable
fenetre = pygame.display.set_mode((LARGEUR, HAUTEUR), pygame.RESIZABLE)
pygame.display.set_caption("Snake Stylé")

# Polices
font_score = pygame.font.SysFont("consolas", 28, bold=True)
font_message = pygame.font.SysFont("consolas", 48, bold=True)

clock = pygame.time.Clock()

def draw_grid():
    """Dessine une grille discrète sur le fond pour effet visuel."""
    for x in range(0, LARGEUR, TAILLE_BLOC):
        pygame.draw.line(fenetre, GRIS_FONCE, (x, 0), (x, HAUTEUR))
    for y in range(0, HAUTEUR, TAILLE_BLOC):
        pygame.draw.line(fenetre, GRIS_FONCE, (0, y), (LARGEUR, y))

def afficher_texte(text, font, couleur, pos, center=False, ombre=False):
    """Affiche un texte avec option d'ombre et centrage."""
    if ombre:
        ombre_surface = font.render(text, True, OMBRE)
        rect = ombre_surface.get_rect()
        if center:
            rect.center = (pos[0]+2, pos[1]+2)
        else:
            rect.topleft = (pos[0]+2, pos[1]+2)
        fenetre.blit(ombre_surface, rect)
    surface = font.render(text, True, couleur)
    rect = surface.get_rect()
    if center:
        rect.center = pos
    else:
        rect.topleft = pos
    fenetre.blit(surface, rect)

def afficher_score(score):
    afficher_texte(f"Score : {score}", font_score, BLANC, (10, 10))

def afficher_niveau(niveau):
    afficher_texte(f"Niveau: {niveau}", font_score, BLANC, (LARGEUR - 140, 10))

def message_fin(msg, couleur):
    afficher_texte(msg, font_message, couleur, (LARGEUR//2, HAUTEUR//2), center=True, ombre=True)

def dessiner_segment(pos):
    """Dessine un segment arrondi du serpent rouge avec ombre."""
    x, y = pos
    radius = TAILLE_BLOC // 2

    # Ombre
    pygame.draw.circle(fenetre, OMBRE, (x + radius + 2, y + radius + 2), radius)
    pygame.draw.rect(fenetre, OMBRE, (x + 2, y + radius//2 + 2, TAILLE_BLOC, radius))
    pygame.draw.rect(fenetre, OMBRE, (x + radius//2 + 2, y + 2, radius, TAILLE_BLOC))

    # Serpent rouge vif
    pygame.draw.circle(fenetre, ROUGE, (x + radius, y + radius), radius)
    pygame.draw.rect(fenetre, ROUGE, (x, y + radius//2, TAILLE_BLOC, radius))
    pygame.draw.rect(fenetre, ROUGE, (x + radius//2, y, radius, TAILLE_BLOC))

def jeu():
    global LARGEUR, HAUTEUR, fenetre

    game_over = False
    game_close = False
    pause = False

    x = LARGEUR // 2
    y = HAUTEUR // 2
    dx = 0
    dy = 0

    snake = []
    longueur = 1

    nourriture_x = random.randrange(0, LARGEUR - TAILLE_BLOC, TAILLE_BLOC)
    nourriture_y = random.randrange(0, HAUTEUR - TAILLE_BLOC, TAILLE_BLOC)

    score = 0

    while not game_over:

        while game_close:
            fenetre.fill(NOIR)
            message_fin("PERDU!", ROUGE)
            afficher_texte(f"Q: Quitter   C: Rejouer", font_score, BLANC, (LARGEUR//2, HAUTEUR//2 + 60), center=True, ombre=True)
            afficher_score(score)
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        game_close = False
                    elif event.key == pygame.K_c:
                        jeu()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True

            elif event.type == pygame.VIDEORESIZE:
                LARGEUR, HAUTEUR = event.w, event.h
                fenetre = pygame.display.set_mode((LARGEUR, HAUTEUR), pygame.RESIZABLE)

                nourriture_x = min(nourriture_x, (LARGEUR - TAILLE_BLOC) // TAILLE_BLOC * TAILLE_BLOC)
                nourriture_y = min(nourriture_y, (HAUTEUR - TAILLE_BLOC) // TAILLE_BLOC * TAILLE_BLOC)
                snake = [(min(px, (LARGEUR - TAILLE_BLOC) // TAILLE_BLOC * TAILLE_BLOC),
                          min(py, (HAUTEUR - TAILLE_BLOC) // TAILLE_BLOC * TAILLE_BLOC))
                         for px, py in snake]

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    pause = not pause
                if not pause:
                    if event.key == pygame.K_LEFT and dx == 0:
                        dx = -TAILLE_BLOC
                        dy = 0
                    elif event.key == pygame.K_RIGHT and dx == 0:
                        dx = TAILLE_BLOC
                        dy = 0
                    elif event.key == pygame.K_UP and dy == 0:
                        dy = -TAILLE_BLOC
                        dx = 0
                    elif event.key == pygame.K_DOWN and dy == 0:
                        dy = TAILLE_BLOC
                        dx = 0

        if pause:
            fenetre.fill(NOIR)
            afficher_texte("PAUSE", font_message, BLANC, (LARGEUR//2, HAUTEUR//2 - 40), center=True, ombre=True)
            afficher_texte("Appuyez sur P pour reprendre", font_score, BLANC, (LARGEUR//2, HAUTEUR//2 + 20), center=True, ombre=True)
            afficher_score(score)
            niveau = score // 50 + 1
            afficher_niveau(niveau)
            pygame.display.update()
            clock.tick(5)
            continue

        if x < 0 or x >= LARGEUR or y < 0 or y >= HAUTEUR:
            game_close = True

        x += dx
        y += dy

        fenetre.fill(NOIR)
        draw_grid()

        pygame.draw.rect(fenetre, BLANC, (nourriture_x, nourriture_y, TAILLE_BLOC, TAILLE_BLOC))

        snake.append((x, y))
        if len(snake) > longueur:
            del snake[0]

        if len(snake) != len(set(snake)):
            game_close = True

        for segment in snake:
            dessiner_segment(segment)

        afficher_score(score)
        niveau = score // 50 + 1
        afficher_niveau(niveau)

        pygame.display.update()

        if x == nourriture_x and y == nourriture_y:
            nourriture_x = random.randrange(0, LARGEUR - TAILLE_BLOC, TAILLE_BLOC)
            nourriture_y = random.randrange(0, HAUTEUR - TAILLE_BLOC, TAILLE_BLOC)
            longueur += 1
            score += 10

        vitesse = vitesse_base + (niveau - 1) * 2
        clock.tick(vitesse)

def draw_grid():
    for x in range(0, LARGEUR, TAILLE_BLOC):
        pygame.draw.line(fenetre, GRIS_FONCE, (x, 0), (x, HAUTEUR))
    for y in range(0, HAUTEUR, TAILLE_BLOC):
        pygame.draw.line(fenetre, GRIS_FONCE, (0, y), (LARGEUR, y))

GRIS_FONCE = (30, 30, 30)

if __name__ == "__main__":
    jeu()
