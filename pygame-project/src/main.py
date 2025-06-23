import pygame
import sys

# 색상 정의
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 102, 204)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# 게임 설정
SCREEN_WIDTH = 480
SCREEN_HEIGHT = 640
PADDLE_WIDTH = 80
PADDLE_HEIGHT = 15
BALL_SIZE = 15
BRICK_ROWS = 6
BRICK_COLS = 8
BRICK_WIDTH = 55
BRICK_HEIGHT = 25

class Paddle:
    def __init__(self):
        self.rect = pygame.Rect(
            (SCREEN_WIDTH - PADDLE_WIDTH) // 2,
            SCREEN_HEIGHT - 40,
            PADDLE_WIDTH,
            PADDLE_HEIGHT
        )
        self.speed = 8

    def move(self, dx):
        self.rect.x += dx * self.speed
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH

    def draw(self, screen):
        pygame.draw.rect(screen, BLUE, self.rect)

class Ball:
    def __init__(self):
        self.rect = pygame.Rect(
            SCREEN_WIDTH // 2 - BALL_SIZE // 2,
            SCREEN_HEIGHT // 2,
            BALL_SIZE,
            BALL_SIZE
        )
        self.dx = 5
        self.dy = -5

    def move(self):
        self.rect.x += self.dx
        self.rect.y += self.dy

        if self.rect.left <= 0 or self.rect.right >= SCREEN_WIDTH:
            self.dx *= -1
        if self.rect.top <= 0:
            self.dy *= -1

    def draw(self, screen):
        pygame.draw.ellipse(screen, RED, self.rect)

class Brick:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, BRICK_WIDTH, BRICK_HEIGHT)
        self.alive = True

    def draw(self, screen):
        if self.alive:
            pygame.draw.rect(screen, GREEN, self.rect)
            pygame.draw.rect(screen, WHITE, self.rect, 2)

def create_bricks():
    bricks = []
    for row in range(BRICK_ROWS):
        for col in range(BRICK_COLS):
            x = col * (BRICK_WIDTH + 5) + 20
            y = row * (BRICK_HEIGHT + 5) + 40
            bricks.append(Brick(x, y))
    return bricks

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("벽돌깨기")
    clock = pygame.time.Clock()

    paddle = Paddle()
    ball = Ball()
    bricks = create_bricks()
    score = 0
    font = pygame.font.SysFont(None, 36)
    game_over = False

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            paddle.move(-1)
        if keys[pygame.K_RIGHT]:
            paddle.move(1)

        if not game_over:
            ball.move()

            # 패들 충돌
            if ball.rect.colliderect(paddle.rect):
                ball.dy *= -1
                ball.rect.bottom = paddle.rect.top

            # 벽돌 충돌
            for brick in bricks:
                if brick.alive and ball.rect.colliderect(brick.rect):
                    ball.dy *= -1
                    brick.alive = False
                    score += 10
                    break

            # 바닥에 닿으면 게임 오버
            if ball.rect.top > SCREEN_HEIGHT:
                game_over = True

            # 모든 벽돌 제거 시 클리어
            if all(not brick.alive for brick in bricks):
                game_over = True

        # 화면 그리기
        screen.fill(BLACK)
        paddle.draw(screen)
        ball.draw(screen)
        for brick in bricks:
            brick.draw(screen)
        score_text = font.render(f"Score: {score}", True, WHITE)
        screen.blit(score_text, (10, 10))

        if game_over:
            msg = "Game Over" if any(brick.alive for brick in bricks) else "Clear!"
            over_text = font.render(msg, True, WHITE)
            screen.blit(over_text, (SCREEN_WIDTH // 2 - over_text.get_width() // 2, SCREEN_HEIGHT // 2))

        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main()