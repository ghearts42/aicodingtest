import pygame
import sys

# 화면 크기
WIDTH, HEIGHT = 800, 600

# 색상
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
COLORS = [
    (0, 0, 0),      # 검정
    (255, 0, 0),    # 빨강
    (0, 255, 0),    # 초록
    (0, 0, 255),    # 파랑
    (255, 255, 0),  # 노랑
    (255, 165, 0),  # 주황
    (128, 0, 128),  # 보라
]
ERASER_COLOR = WHITE

def draw_palette(screen, selected_color, eraser_mode):
    for i, color in enumerate(COLORS):
        rect = pygame.Rect(10 + i * 40, 10, 30, 30)
        pygame.draw.rect(screen, color, rect)
        if color == selected_color and not eraser_mode:
            pygame.draw.rect(screen, (128, 128, 128), rect, 3)
    # 지우개 버튼
    eraser_rect = pygame.Rect(10 + len(COLORS) * 40, 10, 30, 30)
    pygame.draw.rect(screen, (200, 200, 200), eraser_rect)
    font = pygame.font.SysFont(None, 24)
    text = font.render("E", True, BLACK)
    screen.blit(text, (eraser_rect.x + 7, eraser_rect.y + 3))
    if eraser_mode:
        pygame.draw.rect(screen, (128, 128, 128), eraser_rect, 3)
    return eraser_rect

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("그림판")
    clock = pygame.time.Clock()

    screen.fill(WHITE)
    drawing = False
    last_pos = None
    brush_size = 5
    color = BLACK
    eraser_mode = False

    while True:
        eraser_rect = draw_palette(screen, color, eraser_mode)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = event.pos
                # 팔레트 클릭 시 색상 변경 또는 지우개 선택
                if my < 50:
                    if eraser_rect.collidepoint(mx, my):
                        eraser_mode = True
                    else:
                        for i, c in enumerate(COLORS):
                            rect = pygame.Rect(10 + i * 40, 10, 30, 30)
                            if rect.collidepoint(mx, my):
                                color = c
                                eraser_mode = False
                                break
                else:
                    drawing = True
                    last_pos = event.pos
            elif event.type == pygame.MOUSEBUTTONUP:
                drawing = False
                last_pos = None
            elif event.type == pygame.MOUSEMOTION and drawing:
                if last_pos:
                    draw_color = ERASER_COLOR if eraser_mode else color
                    pygame.draw.line(screen, draw_color, last_pos, event.pos, brush_size)
                last_pos = event.pos
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    brush_size = min(brush_size + 1, 20)
                elif event.key == pygame.K_DOWN:
                    brush_size = max(brush_size - 1, 1)
                elif event.key == pygame.K_c:
                    screen.fill(WHITE)
                elif event.key == pygame.K_e:
                    eraser_mode = not eraser_mode

        pygame.display.flip()
        clock.tick(120)

if __name__ == "__main__":
    main()