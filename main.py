import pygame
import sys
import time


pygame.init()
pygame.font.init()

screen = pygame.display.set_mode((800, 600), pygame.RESIZABLE)
pygame.display.set_caption("Conway's Game of Life")

clock = pygame.time.Clock()
MIN_BLOCK_SIZE = 10
MAX_BLOCK_SIZE = 50
active_blocks = set(())
block_size = 20
game_started = False
game_desc_show = True

desc = """
Conway's Game of Life is a simulation that shows
how groups of cells on a grid can change over time.
Simple rules determine this, leading to interesting
and complex patterns.

Any live cell with 2 or 3 live neighbors stays alive
Any live cell with fewer than 2 live neighbors dies (underpopulation)
Any live cell with more than 3 live neighbors dies (overpopulation)
Any dead cell with exactly 3 live neighbors becomes alive (reproduction)

Hit any key to continue
After that click cells to activate or deactivate them  
then hit enter to start the game
use enter pause and edit the game
use enter to continue
Use Arrow up too zoom in and Arrow down to zoom out
Use Esc to clear screen
"""

desc_font = pygame.font.SysFont('Arial', 18)


def main():
    global game_desc_show, game_started, active_blocks
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            select_block(event)
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_RETURN and not game_desc_show:
                    game_started = not game_started
                game_desc_show = False

                if event.key == pygame.K_ESCAPE:
                    active_blocks.clear()

                

        screen.fill((0, 0, 0))

        handle_key_events()

        if game_desc_show:
            lines = desc.splitlines()
            for i, line in enumerate(lines):
                pos = len(lines) // 2
                game_desc_text = desc_font.render(
                    line, True, (255, 255, 255), (0, 0, 0))

                text_x = screen.get_width() / 2 - game_desc_text.get_width() / 2
                text_y = (screen.get_height() / 2 +
                          ((-pos + i) * game_desc_text.get_height()))

                mid_point = (text_x, text_y)

                screen.blit(game_desc_text, mid_point)
        else:
            draw_grid()

        if game_started:
            game_logic()

        pygame.display.flip()

        clock.tick(5)

    pygame.quit()
    sys.exit()


def draw_grid():
    WINDOW_WIDTH, WINDOW_HEIGHT = screen.get_size()

    for x in range(0, WINDOW_WIDTH, block_size):
        for y in range(0, WINDOW_HEIGHT, block_size):
            block = pygame.Rect(x, y, block_size, block_size)
            pygame.draw.rect(screen, (200, 200, 200), block, 1)

    for block in active_blocks:
        x, y = block
        x *= block_size
        y *= block_size

        block = pygame.Rect(x, y, block_size, block_size)
        pygame.draw.rect(screen, (200, 200, 200), block, 0)


def handle_key_events():
    global block_size
    keys = pygame.key.get_pressed()

    if keys[pygame.K_UP]:
        if block_size >= MAX_BLOCK_SIZE:
            block_size = MAX_BLOCK_SIZE
        else:
            block_size += 1

    if keys[pygame.K_DOWN]:
        if block_size <= MIN_BLOCK_SIZE:
            block_size = MIN_BLOCK_SIZE
        else:
            block_size -= 1


def select_block(event: pygame.event.Event):
    if game_desc_show:
        return
    if game_started:
        return

    if event.type == pygame.MOUSEBUTTONUP:
        x, y = pygame.mouse.get_pos()
        x //= block_size
        y //= block_size

        if (x, y) in active_blocks:
            active_blocks.discard((x, y))
        else:
            active_blocks.add((x, y))


def game_logic():
    global game_started
    # check if cell will remain alive
    cells_to_remove = set(())
    cells_to_revive = set(())
    cells_to_revive_possibly = set(())
    for cell in active_blocks:
        neigbours = 0
        for x in range(-1, 2):
            for y in range(-1, 2):
                if x == 0 and y == 0:
                    continue
                neigbour_cell = (cell[0] + x, cell[1] + y)

                if neigbour_cell in active_blocks:
                    neigbours += 1
                else:
                    cells_to_revive_possibly.add(neigbour_cell)
        if neigbours != 2 and neigbours != 3:
            cells_to_remove.add(cell)

    # check if dead cell can be brought alive
    for cell in cells_to_revive_possibly:
        living_neigbours = 0
        for x in range(-1, 2):
            for y in range(-1, 2):
                if x == 0 and y == 0:
                    continue
                neigbour_cell = (cell[0] + x, cell[1] + y)

                if neigbour_cell in active_blocks:
                    living_neigbours += 1

        if living_neigbours == 3:
            cells_to_revive.add(cell)

    for cell in cells_to_remove:
        active_blocks.remove(cell)
    
    for cell in cells_to_revive:
        active_blocks.add(cell)

    if len(active_blocks) == 0:
        game_started = False


if __name__ == '__main__':
    main()
