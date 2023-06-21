import pygame
import random

# Inicialización de Pygame
pygame.init()

# Dimensiones de la pantalla
WIDTH = 800
HEIGHT = 600

# Colores
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)

# Creación de la pantalla
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Mi Juego")

# Carga de las imágenes
player_img = pygame.image.load("player.png")  # Reemplaza "player.png" con la ruta de tu imagen de jugador
enemy_img = pygame.image.load("enemy.png")  # Reemplaza "enemy.png" con la ruta de tu imagen de enemigo
background_img = pygame.image.load("background.jpg")  # Reemplaza "background.png" con la ruta de tu imagen de fondo

# Escalado de las imágenes
player_img = pygame.transform.scale(player_img, (50, 50))  # Ajusta el tamaño según tus necesidades
enemy_img = pygame.transform.scale(enemy_img, (50, 50))  # Ajusta el tamaño según tus necesidades
background_img = pygame.transform.scale(background_img, (WIDTH, HEIGHT))

# Variables del jugador
player_x = WIDTH // 2
player_y = HEIGHT - 100
player_speed = 5
player_lives = 3

# Variables de movimiento del jugador
move_left = False
move_right = False

# Variables de los disparos
bullet_speed = 10
bullets = []

# Variables de los enemigos
enemy_speed = 1
enemies = []
enemy_spawn_counter = 0

# Puntuación
score = 0

# Fuente de texto
font = pygame.font.Font(None, 36)

# Función para dibujar elementos en la pantalla
def draw():
    screen.blit(background_img, (0, 0))
    screen.blit(player_img, (player_x, player_y))
    
    for bullet in bullets:
        pygame.draw.rect(screen, YELLOW, bullet)
    
    for enemy in enemies:
        screen.blit(enemy_img, (enemy[0], enemy[1]))
    
    # Mostrar vidas del jugador
    lives_text = font.render("Vidas: " + str(player_lives), True, WHITE)
    screen.blit(lives_text, (10, 10))
    
    # Mostrar puntaje
    score_text = font.render("Puntaje: " + str(score), True, WHITE)
    screen.blit(score_text, (WIDTH - score_text.get_width() - 10, 10))
    
    pygame.display.update()

# Función para manejar eventos
def handle_events():
    global move_left, move_right  # Agrega estas líneas para poder modificar las variables globales
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                move_left = True
            elif event.key == pygame.K_RIGHT:
                move_right = True
            elif event.key == pygame.K_SPACE:
                bullets.append(pygame.Rect(player_x + 22, player_y, 6, 10))
        
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                move_left = False
            elif event.key == pygame.K_RIGHT:
                move_right = False

# Función para actualizar el estado del juego
def update_game():
    global enemy_spawn_counter, score, player_lives, player_x  # Agrega player_x a las variables globales
    
    if move_left:
        player_x -= player_speed
    elif move_right:
        player_x += player_speed
    
    for bullet in bullets:
        bullet.y -= bullet_speed
    
    for enemy in enemies:
        enemy[1] += enemy_speed
        
        if enemy.colliderect(pygame.Rect(player_x, player_y, 50, 50)):
            player_lives -= 1
            enemies.remove(enemy)
            if player_lives == 0:
                show_loss_message()  # Mostrar mensaje "PERDISTE"
        
        for bullet in bullets:
            if enemy.colliderect(bullet):
                bullets.remove(bullet)
                enemies.remove(enemy)
                score += 1
    
    enemy_spawn_counter += 1
    if enemy_spawn_counter == 60:  # Ajusta este valor para controlar la velocidad de aparición de enemigos
        enemies.append(pygame.Rect(random.randint(0, WIDTH - 50), 0, 50, 50))
        enemy_spawn_counter = 0
    
    if score >= 20:
        show_win_message()  # Mostrar mensaje "GANASTE"

# Función para mostrar el mensaje de "PERDISTE"
def show_loss_message():
    draw()  # Volver a dibujar la pantalla antes de mostrar el mensaje
    text = font.render("PERDISTE", True, WHITE)
    text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    screen.blit(text, text_rect)
    pygame.display.update()
    pygame.time.delay(2000)  # Pausar el juego durante 2 segundos
    main_menu()

# Función para mostrar el mensaje de "GANASTE"
def show_win_message():
    draw()  # Volver a dibujar la pantalla antes de mostrar el mensaje
    text = font.render("¡GANASTE!", True, WHITE)
    text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    screen.blit(text, text_rect)
    pygame.display.update()
    pygame.time.delay(2000)  # Pausar el juego durante 2 segundos
    main_menu()

# Bucle principal del juego
def game_loop():
    clock = pygame.time.Clock()
    
    while True:
        handle_events()
        update_game()
        draw()
        clock.tick(60)  # Ajusta este valor para controlar la velocidad del juego

# Menú principal
def main_menu():
    global player_lives, score  # Agrega player_lives y score a las variables globales
    
    while True:
        screen.fill(WHITE)
        
        # Dibujar el menú
        text_start = font.render("Iniciar partida", True, YELLOW)
        text_start_rect = text_start.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        screen.blit(text_start, text_start_rect)
        
        pygame.display.update()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                
                # Comprobar si se hizo clic en "Iniciar partida"
                if text_start_rect.collidepoint(mouse_pos):
                    player_lives = 3  # Reiniciar las vidas del jugador
                    score = 0  # Reiniciar el puntaje del jugador
                    game_loop()

# Ejecutar el juego
main_menu()
