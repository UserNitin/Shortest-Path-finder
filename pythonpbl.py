import pygame
import heapq

# Initialize Pygame
pygame.init()

# Grid settings
TILE_SIZE = 5
MIN_TILE_SIZE = 2
MAX_TILE_SIZE = 40
tile_size = TILE_SIZE  # Use variable tile size for zoom
GRID_COLS, GRID_ROWS = 300, 390
GRID_WIDTH, GRID_HEIGHT = GRID_COLS * TILE_SIZE, GRID_ROWS * TILE_SIZE

# Window settings
WINDOW_WIDTH, WINDOW_HEIGHT = 800, 600
SCROLLBAR_WIDTH = 15

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 150, 255)
GREEN = (0, 200, 0)
YELLOW = (255, 255, 0)
PURPLE = (150, 50, 150)
RED = (255, 0, 0)

# Assign colors to labeled regions
labeled_regions = [
    (0, 0, 50, 70, "library", BLUE),
    (10, 70, 40, 40, "Class 9", GREEN),
    (10, 120, 40, 40, "class 10", GREEN),
    (10, 160, 40, 40, "class 11", GREEN),
    (10, 200, 40, 40, "class 12", GREEN),
    (10, 240, 40, 30, "washroom", PURPLE),
    (10, 280, 40, 40, "class 13", GREEN),
    (0, 320, 50, 70, "Auditorium hall", GREEN),

    (50, 0, 40, 40, "class 8", GREEN),
    (90, 0, 40, 50, "class 7", GREEN),
    (130, 0, 50, 40, "class 6", GREEN),
    
    (140, 40, 40, 40, "Lab II", GREEN),
    (140, 80, 40, 40, "Class 5", GREEN),
    (140, 120, 40, 40, "Lab I", GREEN),

    (130, 170, 50, 80, "Washroom", GREEN),

    (70, 160, 50, 60, "Physics Lab", GREEN),
    (70, 220, 50, 50, "Chemistry Lab", GREEN),

    (140, 260, 40, 40, "class 1", GREEN),
    (140, 300, 40, 40, "class 2", GREEN),
    (140, 340, 40, 50, "class 3", GREEN),

    (50, 360, 50, 30, "unknown", GREEN),
    (100, 350, 40, 40, "class 4", GREEN),

    (240,100,30,20, "unknown 1", GREEN),
    (270, 100, 30, 40, "Principal office", GREEN),

    (240, 120, 20, 20, "Instument room", GREEN),
    (240, 140, 20, 20, "V.Principla office", GREEN),

    (250, 180, 50, 60, "Office", GREEN),
    (250, 240, 50, 40, "class 14", GREEN),

    (240, 290, 30, 30, "Exam office", GREEN),
    (270, 280, 30, 40, "Document room", GREEN),
]

# Create Pygame window (make resizable)
screen = pygame.display.set_mode((WINDOW_WIDTH + SCROLLBAR_WIDTH, WINDOW_HEIGHT + SCROLLBAR_WIDTH), pygame.RESIZABLE)
pygame.display.set_caption("Scrollable Grid with Colored Labeled Regions and Walls")

# Font
font = pygame.font.SysFont("Arial", 18, bold=True)

# Initial scroll position
scroll_x, scroll_y = 0, 0
scroll_speed = 20

# Build a grid to mark walkable and blocked tiles
def build_grid():
    grid = [[1 for _ in range(GRID_COLS)] for _ in range(GRID_ROWS)]
    for x, y, w, h, _, _ in labeled_regions:
        for i in range(y, y + h):
            for j in range(x, x + w):
                if 0 <= i < GRID_ROWS and 0 <= j < GRID_COLS:
                    grid[i][j] = 0  # Blocked (region)
    return grid

grid = build_grid()

start_point = None
end_point = None
path = []

def grid_pos_from_mouse(mx, my):
    gx = (mx + scroll_x) // tile_size
    gy = (my + scroll_y) // tile_size
    return int(gx), int(gy)

def mouse_in_grid(mx, my):
    win_w, win_h = screen.get_width() - SCROLLBAR_WIDTH, screen.get_height() - SCROLLBAR_WIDTH
    return 0 <= mx < win_w and 0 <= my < win_h

def heuristic(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def neighbors(node):
    x, y = node
    for dx, dy in [(-1,0),(1,0),(0,-1),(0,1)]:
        nx, ny = x + dx, y + dy
        if 0 <= nx < GRID_COLS and 0 <= ny < GRID_ROWS and grid[ny][nx]:
            yield (nx, ny)

def astar(start, goal):
    heap = []
    heapq.heappush(heap, (0 + heuristic(start, goal), 0, start, [start]))
    visited = set()
    while heap:
        est, cost, node, path = heapq.heappop(heap)
        if node == goal:
            return path
        if node in visited:
            continue
        visited.add(node)
        for n in neighbors(node):
            if n not in visited:
                heapq.heappush(heap, (cost + 1 + heuristic(n, goal), cost + 1, n, path + [n]))
    return []

def draw_path(path):
    for (x, y) in path:
        rx = x * tile_size - scroll_x
        ry = y * tile_size - scroll_y
        pygame.draw.rect(screen, RED, (rx, ry, tile_size, tile_size))

# Function to draw labeled regions with black walls
def draw_labeled_regions():
    for x, y, w, h, label, color in labeled_regions:
        rect_x = x * tile_size - scroll_x
        rect_y = y * tile_size - scroll_y
        rect_w = w * tile_size
        rect_h = h * tile_size

        # Draw filled rectangle (region)
        pygame.draw.rect(screen, color, (rect_x, rect_y, rect_w, rect_h))

        # Draw black border (walls)
        pygame.draw.rect(screen, BLACK, (rect_x, rect_y, rect_w, rect_h), 3)

        # Draw label text inside region (always draw label)
        text_surface = font.render(label, True, BLACK)
        screen.blit(text_surface, (rect_x + 5, rect_y + 5))

# Function to draw scrollbars
def draw_scrollbars():
    # Use current window size
    win_w, win_h = screen.get_width() - SCROLLBAR_WIDTH, screen.get_height() - SCROLLBAR_WIDTH
    grid_width = GRID_COLS * tile_size
    grid_height = GRID_ROWS * tile_size
    scrollbar_x_length = win_w * (win_w / grid_width) if grid_width > 0 else win_w
    scrollbar_x_pos = (scroll_x / (grid_width - win_w)) * (win_w - scrollbar_x_length) if grid_width > win_w else 0
    pygame.draw.rect(screen, (150, 150, 150), (scrollbar_x_pos, win_h, scrollbar_x_length, SCROLLBAR_WIDTH))

    scrollbar_y_length = win_h * (win_h / grid_height) if grid_height > 0 else win_h
    scrollbar_y_pos = (scroll_y / (grid_height - win_h)) * (win_h - scrollbar_y_length) if grid_height > win_h else 0
    pygame.draw.rect(screen, (150, 150, 150), (win_w, scrollbar_y_pos, SCROLLBAR_WIDTH, scrollbar_y_length))

# Main loop
running = True
dragging_x = dragging_y = False
while running:
    # Get current window size
    win_w, win_h = screen.get_width() - SCROLLBAR_WIDTH, screen.get_height() - SCROLLBAR_WIDTH
    grid_width = GRID_COLS * tile_size
    grid_height = GRID_ROWS * tile_size
    screen.fill(WHITE)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.VIDEORESIZE:
            # Resize window and keep scrollbars
            new_w = max(event.w, 200)
            new_h = max(event.h, 200)
            screen = pygame.display.set_mode((new_w, new_h), pygame.RESIZABLE)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mx, my = pygame.mouse.get_pos()
            if event.button == 1 and mouse_in_grid(mx, my):
                gx, gy = grid_pos_from_mouse(mx, my)
                if not start_point:
                    start_point = (gx, gy)
                elif not end_point:
                    end_point = (gx, gy)
                    if grid[start_point[1]][start_point[0]] and grid[end_point[1]][end_point[0]]:
                        path = astar(start_point, end_point)
                else:
                    # Reset if both points already set
                    start_point = end_point = None
                    path = []
            elif event.button == 3:
                # Right click resets
                start_point = end_point = None
                path = []
            elif my >= win_h:
                dragging_x = True
            elif mx >= win_w:
                dragging_y = True
            elif event.button == 4:  # Mouse wheel up (zoom in)
                old_tile_size = tile_size
                tile_size = min(tile_size + 2, MAX_TILE_SIZE)
                # Adjust scroll to keep center
                mx, my = pygame.mouse.get_pos()
                cx = scroll_x + mx
                cy = scroll_y + my
                scroll_x = int((cx / old_tile_size) * tile_size - mx)
                scroll_y = int((cy / old_tile_size) * tile_size - my)
            elif event.button == 5:  # Mouse wheel down (zoom out)
                old_tile_size = tile_size
                tile_size = max(tile_size - 2, MIN_TILE_SIZE)
                mx, my = pygame.mouse.get_pos()
                cx = scroll_x + mx
                cy = scroll_y + my
                scroll_x = int((cx / old_tile_size) * tile_size - mx)
                scroll_y = int((cy / old_tile_size) * tile_size - my)
        elif event.type == pygame.MOUSEBUTTONUP:
            dragging_x = dragging_y = False
        elif event.type == pygame.MOUSEMOTION:
            if dragging_x:
                mx, _ = pygame.mouse.get_pos()
                scrollbar_x_length = win_w * (win_w / grid_width) if grid_width > 0 else win_w
                max_scroll_x = win_w - scrollbar_x_length
                if max_scroll_x > 0:
                    scroll_x = (mx / max_scroll_x) * (grid_width - win_w)
                    scroll_x = max(0, min(scroll_x, grid_width - win_w))
            if dragging_y:
                _, my = pygame.mouse.get_pos()
                scrollbar_y_length = win_h * (win_h / grid_height) if grid_height > 0 else win_h
                max_scroll_y = win_h - scrollbar_y_length
                if max_scroll_y > 0:
                    scroll_y = (my / max_scroll_y) * (grid_height - win_h)
                    scroll_y = max(0, min(scroll_y, grid_height - win_h))
        elif event.type == pygame.MOUSEWHEEL:
            mods = pygame.key.get_mods()
            mx, my = pygame.mouse.get_pos()
            if mods & pygame.KMOD_CTRL:
                # Zoom in/out
                old_tile_size = tile_size
                if event.y > 0:
                    tile_size = min(tile_size + 2, MAX_TILE_SIZE)
                elif event.y < 0:
                    tile_size = max(tile_size - 2, MIN_TILE_SIZE)
                cx = scroll_x + mx
                cy = scroll_y + my
                scroll_x = int((cx / old_tile_size) * tile_size - mx)
                scroll_y = int((cy / old_tile_size) * tile_size - my)
            elif mods & pygame.KMOD_SHIFT:
                # Horizontal scroll
                scroll_x += -event.y * tile_size * 5
            else:
                # Vertical scroll
                scroll_y += -event.y * tile_size * 5

    # Clamp scroll to grid bounds
    scroll_x = max(0, min(scroll_x, max(0, grid_width - win_w)))
    scroll_y = max(0, min(scroll_y, max(0, grid_height - win_h)))

    # Draw elements
    draw_labeled_regions()  # Draw colored regions with black walls
    if path:
        draw_path(path)
    # Draw start/end points
    for pt, color in [(start_point, (0,0,255)), (end_point, (255,165,0))]:
        if pt:
            rx = pt[0] * tile_size - scroll_x
            ry = pt[1] * tile_size - scroll_y
            pygame.draw.rect(screen, color, (rx, ry, tile_size, tile_size))
    draw_scrollbars()  # Draw scrollbars

    pygame.display.flip()

pygame.quit()
