import pygame
import math
import random

# Инициализация Pygame
pygame.init()

# Установки экрана
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Танки")

# Цвета
black = (0, 0, 0)
white = (255, 255, 255)
green = (0, 255, 0)
red = (255, 0, 0)

# Параметры танка
tank_width = 40
tank_height = 20
tank_speed = 5

# Параметры снаряда
bullet_speed = 10
bullets = []

# Параметры астероида
asteroid_speed = 3
asteroids = []

# Счетчик уничтоженных астероидов
score = 0
font = pygame.font.SysFont(None, 36)

# Класс танка
class Tank:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.angle = 0

    def draw(self, screen):
        # Рисуем корпус танка
        pygame.draw.rect(screen, green, [self.x, self.y, tank_width, tank_height])
        # Рисуем пушку танка
        turret_end_x = self.x + tank_width / 2 + (math.cos(self.angle) * tank_width)
        turret_end_y = self.y + tank_height / 2 + (math.sin(self.angle) * tank_width)
        pygame.draw.line(screen, green, (self.x + tank_width / 2, self.y + tank_height / 2), (turret_end_x, turret_end_y), 5)

    def move(self, dx, dy):
        new_x = self.x + dx
        new_y = self.y + dy

        # Проверяем границы экрана
        if 0 <= new_x <= screen_width - tank_width and 0 <= new_y <= screen_height - tank_height:
            self.x = new_x
            self.y = new_y

    def rotate(self, angle):
        self.angle += angle

    def shoot(self):
        turret_end_x = self.x + tank_width / 2 + (math.cos(self.angle) * tank_width)
        turret_end_y = self.y + tank_height / 2 + (math.sin(self.angle) * tank_width)
        bullets.append([turret_end_x, turret_end_y, self.angle])

    def hit_by_asteroid(self, asteroid):
        tank_rect = pygame.Rect(self.x, self.y, tank_width, tank_height)
        asteroid_rect = pygame.Rect(asteroid.x - asteroid.size, asteroid.y - asteroid.size, asteroid.size * 2, asteroid.size * 2)
        return tank_rect.colliderect(asteroid_rect)

# Класс астероида
class Asteroid:
    def __init__(self):
        self.x = screen_width
        self.y = random.randint(0, screen_height)
        self.size = random.randint(20, 50)

    def draw(self, screen):
        pygame.draw.circle(screen, red, (self.x, self.y), self.size)

    def move(self):
        self.x -= asteroid_speed

    def is_off_screen(self):
        return self.x < 0

    def hit_by_bullet(self, bullet):
        bx, by = bullet[0], bullet[1]
        distance = math.sqrt((self.x - bx) ** 2 + (self.y - by) ** 2)
        return distance < self.size

# Создаем танк
tank = Tank(screen_width // 2, screen_height // 2)

# Основной игровой цикл
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Обработка нажатий клавиш
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        tank.move(-tank_speed, 0)
    if keys[pygame.K_RIGHT]:
        tank.move(tank_speed, 0)
    if keys[pygame.K_UP]:
        tank.move(0, -tank_speed)
    if keys[pygame.K_DOWN]:
        tank.move(0, tank_speed)
    if keys[pygame.K_a]:
        tank.rotate(-0.1)
    if keys[pygame.K_d]:
        tank.rotate(0.1)
    if keys[pygame.K_SPACE]:
        tank.shoot()

    # Перемещение снарядов
    for bullet in bullets:
        bullet[0] += bullet_speed * math.cos(bullet[2])
        bullet[1] += bullet_speed * math.sin(bullet[2])

    # Создание астероидов
    if random.randint(1, 50) == 1:
        asteroids.append(Asteroid())

    # Перемещение астероидов и проверка на столкновения
    for asteroid in asteroids[:]:
        asteroid.move()
        if tank.hit_by_asteroid(asteroid):
            running = False  # Игра заканчивается при столкновении
        if asteroid.is_off_screen():
            asteroids.remove(asteroid)
        for bullet in bullets[:]:
            if asteroid.hit_by_bullet(bullet):
                asteroids.remove(asteroid)
                bullets.remove(bullet)
                score += 1
                break

    # Очистка экрана
    screen.fill(black)

    # Рисуем танк
    tank.draw(screen)

    # Рисуем снаряды
    for bullet in bullets:
        pygame.draw.circle(screen, white, (int(bullet[0]), int(bullet[1])), 5)

    # Рисуем астероиды
    for asteroid in asteroids:
        asteroid.draw(screen)

    # Рисуем счетчик
    score_text = font.render(f"Score: {score}", True, white)
    screen.blit(score_text, [10, 10])

    # Обновление экрана
    pygame.display.flip()

    # Ограничение FPS
    pygame.time.Clock().tick(60)

pygame.quit()
