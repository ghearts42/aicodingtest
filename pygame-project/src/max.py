import pygame
import sys
import random
import time

# 화면 크기
WIDTH, HEIGHT = 400, 600

# 색상
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
NOTE_COLOR = (0, 200, 255)
HIT_LINE_COLOR = (255, 0, 0)

# 노트 설정
LANES = 4
LANE_WIDTH = WIDTH // LANES
NOTE_HEIGHT = 20
NOTE_SPEED = 12
SPAWN_INTERVAL = 0.2  # 초

KEYS = [pygame.K_d, pygame.K_f, pygame.K_j, pygame.K_k]

class Note:
    def __init__(self, lane):
        self.lane = lane
        self.x = lane * LANE_WIDTH
        self.y = -NOTE_HEIGHT
        self.hit = False

    def move(self):
        self.y += NOTE_SPEED

    def draw(self, screen):
        if not self.hit:
            pygame.draw.rect(screen, NOTE_COLOR, (self.x + 5, self.y, LANE_WIDTH - 10, NOTE_HEIGHT))

    def is_hittable(self):
        return HEIGHT - 80 <= self.y <= HEIGHT - 40

    def is_miss(self):
        return self.y > HEIGHT

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("리듬게임")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont(None, 36)

    notes = []
    last_spawn_time = time.time()
    score = 0
    combo = 0
    running = True

    while running:
        screen.fill(BLACK)

        # 노트 생성
        now = time.time()
        if now - last_spawn_time > SPAWN_INTERVAL:
            lane = random.randint(0, LANES - 1)
            notes.append(Note(lane))
            last_spawn_time = now

        # 이벤트 처리
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                for i, key in enumerate(KEYS):
                    if event.key == key:
                        for note in notes:
                            if note.lane == i and note.is_hittable() and not note.hit:
                                note.hit = True
                                score += 100
                                combo += 1
                                break
                        else:
                            combo = 0  # 미스

        # 노트 이동 및 미스 처리
        for note in notes:
            note.move()
            if note.is_miss() and not note.hit:
                combo = 0
                note.hit = True  # 미스 처리

        # 노트 그리기
        for note in notes:
            note.draw(screen)

        # 판정선 그리기
        for i in range(LANES):
            pygame.draw.rect(screen, HIT_LINE_COLOR, (i * LANE_WIDTH + 5, HEIGHT - 60, LANE_WIDTH - 10, 5))
        # 라인 구분선
        for i in range(1, LANES):
            pygame.draw.line(screen, WHITE, (i * LANE_WIDTH, 0), (i * LANE_WIDTH, HEIGHT), 1)

        # 점수, 콤보 표시
        score_text = font.render(f"Score: {score}", True, WHITE)
        combo_text = font.render(f"Combo: {combo}", True, WHITE)
        screen.blit(score_text, (10, 10))
        screen.blit(combo_text, (10, 50))

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()