import pygame
import random
import time

SIZE = 40
background = (11, 184, 31)

class Apple:
    def __init__(self, screen):
        self.screen = screen
        self.apple = pygame.image.load("apple.jpg")
        self.x = 120
        self.y = 120
    
    def draw(self):
        self.screen.blit(self.apple, (self.x, self.y))

    def move(self):
        self.x = random.randint(1, 19)*SIZE
        self.y = random.randint(1, 14)*SIZE

class Snake:
    def __init__(self, screen, length):
        self.screen = screen
        self.snake = pygame.image.load("block.jpg")
        self.direction = 'right'
        self.length = length
        self.x = [SIZE]*length
        self.y = [SIZE]*length
        
    def draw(self):
        for i in range(self.length):
            self.screen.blit(self.snake, (self.x[i], self.y[i]))

    def moveup(self):
        self.direction = 'up'

    def movedown(self):
        self.direction = 'down'

    def moveleft(self):
        self.direction = 'left'

    def moveright(self):
        self.direction = 'right'

    def walk(self):
        for i in range(self.length-1, 0, -1):
            self.x[i] = self.x[i-1]
            self.y[i] = self.y[i-1]
        
        if self.direction == 'up':
            self.y[0] -= SIZE
        if self.direction == 'down':
            self.y[0] += SIZE
        if self.direction == 'left':
            self.x[0] -= SIZE
        if self.direction == 'right':
            self.x[0] += SIZE
        
        self.draw()

    def inc_length(self):
        self.length += 1
        self.x.append(-1)
        self.y.append(-1)

class Game:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        self.screen = pygame.display.set_mode((800, 600))
        img = pygame.image.load("snake.png")
        pygame.display.set_icon(img)
        pygame.display.set_caption("Snake Game")
        self.snake = Snake(self.screen, 1)
        self.apple = Apple(self.screen)
        self.snake.draw()
        self.play_background_music()

    def background_image(self):
        bg = pygame.image.load("background.jpg")
        self.screen.blit(bg, (0, 0))
    
    def isCollision(self, x1, y1, x2, y2):
        if x1 >= x2 and x1 < x2 + SIZE:
            if y1 >= y2 and y1 < y2 + SIZE:
                return True
        return False

    def display_score(self):
        font = pygame.font.SysFont('arial', 30)
        score = font.render(f"Score: {self.snake.length}", True, (255, 255, 255))
        self.screen.blit(score, (670, 10))

    def play_background_music(self):
        pygame.mixer.music.load("bg_music_1.mp3")
        pygame.mixer.music.play(-1)

    def play(self):
        self.background_image()
        self.snake.walk()
        self.apple.draw()
        self.display_score()

        if self.isCollision(self.snake.x[0], self.snake.y[0], self.apple.x, self.apple.y):
            s = pygame.mixer.Sound("ding.mp3")
            pygame.mixer.Sound.play(s)
            self.apple.move()
            self.snake.inc_length()

        for i in range(2, self.snake.length):
            if self.isCollision(self.snake.x[0], self.snake.y[0], self.snake.x[i], self.snake.y[i]):
                s = pygame.mixer.Sound("crash.mp3")
                pygame.mixer.Sound.play(s)
                raise Exception("Game Over")

    def game_over(self):
        self.background_image()
        font = pygame.font.SysFont("arial", 30)
        over = font.render(f"Game Over.. Your score is {self.snake.length}.", True, ((255, 255, 255)))
        self.screen.blit(over, (250, 250))
        playagain = font.render(f"To play again.. Press Enter...", True, ((255, 255, 255)))
        self.screen.blit(playagain, (250, 300))
        pygame.mixer.music.pause()

    def reset(self):
        self.snake = Snake(self.screen, 1)
        self.apple = Apple(self.screen)

    def boundary_case(self):
        if self.snake.x[0] < 0 or self.snake.x[0] >= 800 or self.snake.y[0] < 0 or self.snake.y[0] >= 600:
            s = pygame.mixer.Sound("crash.mp3")
            pygame.mixer.Sound.play(s)
            raise Exception("GAME OVER")

    def time(self):
        if self.snake.length >= 1 and self.snake.length < 10:
            time.sleep(0.2)
        elif self.snake.length >= 10 and self.snake.length < 20:
            time.sleep(0.1)
        elif self.snake.length >= 20 and self.snake.length < 30:
            time.sleep(0.05)
        elif self.snake.length >= 30 and self.snake.length < 40:
            time.sleep(0.02)
        elif self.snake.length >= 10:
            time.sleep(0.01)

    def run(self):
        running = True
        pause = False
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
                    if event.key == pygame.K_RETURN:
                        pause = False
                        pygame.mixer.music.play()
                        self.reset()
                    if not pause: 
                        if event.key == pygame.K_UP:
                            self.snake.moveup()
                        if event.key == pygame.K_DOWN:
                            self.snake.movedown()
                        if event.key == pygame.K_LEFT:
                            self.snake.moveleft()
                        if event.key == pygame.K_RIGHT:
                            self.snake.moveright()

            try: 
                if not pause:  
                    self.play()
                    self.boundary_case()
            except Exception as e:
                self.game_over()
                pause = True

            self.time()
            pygame.display.update()

if __name__ == "__main__":
    game = Game()
    game.run()