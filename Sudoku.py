import pygame

ROWS, COLS = 9, 9 # constant values
SIZE = (600, 600)
WHITE = (255, 255, 255)
DARK_PURPLE = (180, 130, 220)
LIGHT_PURPLE = (220, 180, 255)
HIGHLIGHT = (200, 200, 255)   # for selected cell
BLACK = (0, 0, 0)             # grid lines and numbers

from SudokuPuzzleGameMechanics import SudokuPuzzleLogic

class SudokuUI:
    ''' implements the view (interaction with the user through handling input and outputting the updated board) '''
    def __init__(self):
        ''' initialize a board with values '''
        pygame.init() # Initialize Pygame
        pygame.font.init()

        self._surface = pygame.display.set_mode(SIZE)
        self._game = SudokuPuzzleLogic(ROWS, COLS)
        pygame.display.set_caption("Sudoku")

        # Example pre-filled numbers
        initial_numbers = [
            (0, 0, 5),
            (0, 1, 3),
            (1, 0, 6),
            (4, 4, 7),
            (8, 8, 9)
        ]
        for r, c, val in initial_numbers:
            self._game.add_initial_values(r, c, val)

        self._running = True
        self.selected_cell = None  # (row, col)
        self.font = pygame.font.SysFont(None, 48)

    def run(self):
        '''  run the game '''
        clock = pygame.time.Clock()
        while self._running:
            clock.tick(60)
            self._running = self.handle_input()
            self._surface.fill(WHITE)
            self.display_board()
            pygame.display.flip()

        pygame.quit()

    def handle_input(self):
        ''' handle clicked cell '''
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                self.handle_mouse_click(event.pos)
            elif event.type == pygame.KEYDOWN and self.selected_cell:
                self.handle_key_input(event.key)
        return True

    def handle_mouse_click(self, pos):
        ''' output which selected cell '''
        x, y = pos
        cell_width = self._surface.get_width() // COLS
        cell_height = self._surface.get_height() // ROWS

        col = x // cell_width
        row = y // cell_height

        if 0 <= row < ROWS and 0 <= col < COLS:
            self.selected_cell = (row, col)
            print(f"Selected cell: {self.selected_cell}")

    def handle_key_input(self, key):
        ''' check if valid number in cell '''
        row, col = self.selected_cell

        # Only allow numbers 1-9
        if pygame.K_1 <= key <= pygame.K_9:
            value = key - pygame.K_0

            # Check validity
            if self._game.check_if_valid_move(row, col, value):
                self._game.board[row][col] = value
                if self._game.check_win():
                    print("You win!")
                    self._running = False
            else:
                print(f"Invalid move: {value} at ({row},{col})")

        # Backspace to clear
        elif key == pygame.K_BACKSPACE:
            self._game.board[row][col] = ' '
            print(f"Cleared cell {row},{col}")

    def display_board(self):
        ''' display the colored board with highlighted selected cell '''
        width = self._surface.get_width()
        height = self._surface.get_height()
        cell_width = width // COLS
        cell_height = height // ROWS

        for r in range(ROWS):
            for c in range(COLS):
                # Choose color based on row+col parity
                if (r + c) % 2 == 0:
                    color = LIGHT_PURPLE
                else:
                    color = DARK_PURPLE

                rect = pygame.Rect(c*cell_width, r*cell_height, cell_width, cell_height)
                pygame.draw.rect(self._surface, color, rect)

        # Draw numbers
        for r in range(ROWS):
            for c in range(COLS):
                val = self._game.board[r][c]
                if val != ' ':
                    text = self.font.render(str(val), True, BLACK)
                    rect = text.get_rect(center=(c*cell_width + cell_width//2, r*cell_height + cell_height//2))
                    self._surface.blit(text, rect)

        # Draw grid
        for i in range(ROWS + 1):
            thickness = 3 if i % 3 == 0 else 1
            # Horizontal lines
            pygame.draw.line(self._surface, BLACK, (0, i*cell_height), (width, i*cell_height), thickness)
            # Vertical lines
            pygame.draw.line(self._surface, BLACK, (i*cell_width, 0), (i*cell_width, height), thickness)

        # Highlight selected cell
        if self.selected_cell:
            r, c = self.selected_cell
            rect = pygame.Rect(c*cell_width, r*cell_height, cell_width, cell_height)
            pygame.draw.rect(self._surface, HIGHLIGHT, rect, 3)

# main function to run the game
if __name__ == '__main__':
    ui = SudokuUI()
    ui.run()
