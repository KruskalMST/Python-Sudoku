import pygame

class SudokuPuzzleLogic:
    ''' class contains the logic puzzle game mechanics'''
    def __init__(self, rows, cols, initial = None):
        ''' create a blank board with r rows and c columns '''
        self.rows = rows
        self.cols = cols

        if initial is not None:
            if len(initial) != rows:
                raise ValueError("Initial board has wrong number of rows.")
            for r in range(rows):
                if len(initial[r]) != cols:
                    raise ValueError("Initial board has wrong number of columns.")
                for c in range(cols):
                    self.board[r][c] = initial[r][c]
                
        # create a blank board
        self.board = [[' ' for _ in range(cols)] for _ in range(rows)]

    def add_initial_values(self, r: int, c: int, value: int):
        ''' add the initial vales to board '''
        self.board[r][c] = value

    def check_if_valid_move(self, r: int, c: int, val: int) -> bool:
        ''' value check for empty, rows, columns, 3 by 3 sections '''
        board = self.board

        # 1) Check if the cell is empty
        if board[r][c] != ' ':
            return False

        # 2) Check row
        for x in range(self.cols):
            if board[r][x] == val:
                return False

        # 3) Check column
        for y in range(self.rows):
            if board[y][c] == val:
                return False

        # 4) Check 3×3 subgrid
        box_row = (r // 3) * 3
        box_col = (c // 3) * 3

        for i in range(box_row, box_row + 3):
            for j in range(box_col, box_col + 3):
                if board[i][j] == val:
                    return False

        return True

    def check_win(self):
        ''' check for finished game '''
        for r in range(self.rows):
            for c in range(self.cols):
                val = self.board[r][c]
                if val == ' ':
                    return False
                # Temporarily remove the value to check validity
                self.board[r][c] = ' '
                if not self.check_if_valid_move(r, c, val):
                    self.board[r][c] = val
                    return False
                self.board[r][c] = val
        return True
