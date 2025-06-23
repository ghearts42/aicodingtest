import pygame
import sys
import os

# 화면 크기
WIDTH, HEIGHT = 800, 600
GRID_SIZE = 20  # 한 칸 크기

# 색상
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PLAYER_COLOR = (255, 0, 0)
TRAIL_COLOR = (0, 255, 0)
FILLED_COLOR = (0, 0, 255, 100)

def load_background_image(path):
    if path and os.path.exists(path):
        img = pygame.image.load(path)
        return pygame.transform.scale(img, (WIDTH, HEIGHT))
    return None

def fill_area(grid, x, y):
    # 간단한 flood fill (4방향)
    stack = [(x, y)]
    while stack:
        cx, cy = stack.pop()
        if 0 <= cx < WIDTH // GRID_SIZE and 0 <= cy < HEIGHT // GRID_SIZE:
            if grid[cy][cx] == 0:
                grid[cy][cx] = 2
                stack.extend([(cx+1, cy), (cx-1, cy), (cx, cy+1), (cx, cy-1)])

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("땅따먹기 (사진 배경 가능)")

    # 배경 이미지 경로 입력
    img_path = input("/home/hjpubuntu22045/Downloads/icon_14(1).png").strip()
    bg_img = load_background_image(img_path)

    clock = pygame.time.Clock()

    cols = WIDTH // GRID_SIZE
    rows = HEIGHT // GRID_SIZE
    grid = [[0 for _ in range(cols)] for _ in range(rows)]  # 0: 빈칸, 1: 지나간 길, 2: 채운 땅

    # 플레이어 시작 위치
    px, py = cols // 2, rows // 2
    grid[py][px] = 1
    trail = []

    running = True
    filling = False

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()
        dx, dy = 0, 0
        if keys[pygame.K_LEFT]:
            dx = -1
        elif keys[pygame.K_RIGHT]:
            dx = 1
        elif keys[pygame.K_UP]:
            dy = -1
        elif keys[pygame.K_DOWN]:
            dy = 1

        if dx != 0 or dy != 0:
            nx, ny = px + dx, py + dy
            if 0 <= nx < cols and 0 <= ny < rows:
                px, py = nx, ny
                if grid[py][px] == 0:
                    grid[py][px] = 1
                    trail.append((px, py))
                elif grid[py][px] == 2 and trail:
                    # 닫힌 경로가 만들어졌을 때 영역 채우기
                    for tx, ty in trail:
                        grid[ty][tx] = 2
                    # 내부 영역 채우기 (가장 안쪽 한 칸만 예시로)
                    if len(trail) > 2:
                        mx = sum(x for x, y in trail) // len(trail)
                        my = sum(y for x, y in trail) // len(trail)
                        fill_area(grid, mx, my)
                    trail.clear()

        # 그리기
        if bg_img:
            screen.blit(bg_img, (0, 0))
        else:
            screen.fill(WHITE)

        # 채워진 땅
        for y in range(rows):
            for x in range(cols):
                if grid[y][x] == 2:
                    rect = pygame.Rect(x * GRID_SIZE, y * GRID_SIZE, GRID_SIZE, GRID_SIZE)
                    pygame.draw.rect(screen, FILLED_COLOR, rect)

        # 지나간 길
        for y in range(rows):
            for x in range(cols):
                if grid[y][x] == 1:
                    rect = pygame.Rect(x * GRID_SIZE, y * GRID_SIZE, GRID_SIZE, GRID_SIZE)
                    pygame.draw.rect(screen, TRAIL_COLOR, rect)

        # 플레이어
        pygame.draw.rect(
            screen, PLAYER_COLOR,
            (px * GRID_SIZE, py * GRID_SIZE, GRID_SIZE, GRID_SIZE)
        )

        pygame.display.flip()
        clock.tick(15)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()