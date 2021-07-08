# ACTIVE
from typing import List


# Sudoko Solver
class Solution37:
    def __init__(self):
        self.valid_char_list = ['1', '2', '3', '4', '5', '6', '7', '8', '9']
        self.n_valid_char = len(self.valid_char_list)
        self.allRows = []
        self.allRowsB = []  # backup
        for r in range(9):
            self.allRows.append([9, []])
            self.allRowsB.append([9, []])
        self.allCols = []
        self.allColsB = []
        for c in range(9):
            self.allCols.append([9, []])
            self.allColsB.append([9, []])
        self.allGroups = []
        self.allGroupsB = []
        for gr in range(3):
            self.allGroups.append([])
            self.allGroupsB.append([])
            for gc in range(3):
                self.allGroups[gr].append([9, []])
                self.allGroupsB[gr].append([9, []])
        self.row_char_count = []
        for r in range(9):
            self.row_char_count.append([])
            for i in range(len(self.valid_char_list)):
                self.row_char_count[r].append([0, []])

        self.col_char_count = []
        for c in range(9):
            self.col_char_count.append([])
            for i in range(len(self.valid_char_list)):
                self.col_char_count[c].append([0, []])

        self.group_char_count = []
        for gr in range(3):
            self.group_char_count.append([])
            for gc in range(3):
                self.group_char_count[gr].append([])
                for i in range(len(self.valid_char_list)):
                    self.group_char_count[gr][gc].append([0, []])

    def solveSudoku(self, board: List[List[str]]) -> None:
        """
        Do not return anything, modify board in-place instead.
        """
        char_list = self.valid_char_list
        rows = self.allRows
        cols = self.allCols
        groups = self.allGroups
        self.board1 = board
        self.boardB = []

        for r in range(9):
            self.boardB.append([])
            for c in range(9):
                self.boardB[r].append(self.board1[r][c])
        r_ref = 0
        gr_ref = 0
        r_sub_count = 0
        dot_count = 0
        for r in range(9):
            c_ref = 0
            c_sub_count = 0
            gc_ref = 0
            for c in range(9):
                val = board[r][c]
                if not val == '.':
                    self.note_down(rows[r_ref], val)
                    self.note_down(cols[c_ref], val)
                    self.note_down(groups[gr_ref][gc_ref], val)
                else:
                    dot_count = dot_count + 1
                c_ref = c_ref + 1
                c_sub_count = c_sub_count + 1
                if c_sub_count >= 3:
                    gc_ref = gc_ref + 1
                    c_sub_count = 0
            r_ref = r_ref + 1
            r_sub_count = r_sub_count + 1
            if r_sub_count >= 3:
                gr_ref = gr_ref + 1
                r_sub_count = 0

        rounds = 0
        self.filled = 0
        self.filledB = 0
        last_filled = -1
        self.look_at_2 = False
        choice_stat = []
        self.choice_char = []
        self.choice_charB = []
        for r in range(9):
            choice_stat.append([0, 0, 0, 0, 0, 0, 0, 0, 0])
            self.choice_char.append([])
            self.choice_charB.append([])
            for c in range(9):
                self.choice_char[r].append([])
                self.choice_charB[r].append([])

        self.choice2cells = []
        self.gamble_cell = []
        self.gamble_char = []
        gamble_cell_pos = 0
        self.n_trial = 0
        self.trials_on = False
        choice2cell_filled_chars1 = []
        choice2cell_filled_chars2 = []
        self.fresh_filled = [[], []]
        for r in range(9):
            self.fresh_filled[0].append([])
            self.fresh_filled[1].append([])
            for c in range(9):
                self.fresh_filled[0][r].append('.')
                self.fresh_filled[1][r].append('.')

        self.backedup = False
        while self.filled < dot_count and rounds <= 81:
#            if self.look_at_2 and self.filled <= last_filled:
#                self.collectChoice2Cells()
#                break

            if self.look_at_2:
                if self.trials_on:
                    if self.n_trial == 0:
                        print('n_trial = ', self.n_trial)
                        self.n_trial = self.n_trial + 1
#                        choice2cell_filled_chars1.clear()
#                        for cell in self.choice2cells:
#                            choice2cell_filled_chars1.append(board[cell[0]][cell[1]])
                        # try next
                        if self.restore():
                            r, c = self.gamble_cell[0]
                            self.update_done_char(r, c, *self.gamble_char[self.n_trial])
                        else:
                            break

                    elif self.n_trial == 1:
                        print('n_trial = ', self.n_trial)
#                           choice2cell_filled_chars2.clear()
#                           for cell in self.choice2cells:
#                            choice2cell_filled_chars2.append(board[cell[0]][cell[1]])
#                        print('trying ', self.choice2cells[gamble_cell_pos], self.choice2cells)
                        repeat_found = False
                        self.restore()
                        for r_found in range(9):
                            for c_found in range(9):
                                s1 = self.fresh_filled[0][r_found][c_found]
                                if not s1 == '.':
                                    if self.fresh_filled[1][r_found][c_found] == s1:
                                        self.update_done_char(r_found, c_found, s1)
                                        repeat_found = True
                        if not repeat_found:
                            if gamble_cell_pos < len(self.choice2cells) - 1:
                                gamble_cell_pos = gamble_cell_pos + 1
                                self.n_trial = 0
                                self.gamble_cell.clear()
                                self.gamble_cell.append(self.choice2cells[gamble_cell_pos])
                                r, c = self.gamble_cell[0]
                                self.gamble_char.clear()
                                for s in self.choice_char[r][c]:
                                    self.gamble_char.append(s)
                                self.update_done_char(r, c, *self.gamble_char[self.n_trial])
                                self.clear_fresh_filled()
                                continue
                            else:
                                self.trials_on = False
                                break

                elif self.filled <= last_filled:
                    self.backup()
                    self.collect_choice2cells()
                    if len(self.choice2cells):
                        self.gamble_cell.clear()
                        self.gamble_cell.append(self.choice2cells[gamble_cell_pos])
                        r, c = self.gamble_cell[0]
                        self.gamble_char.clear()
                        for s in self.choice_char[r][c]:
                            self.gamble_char.append(s)
                        self.update_done_char(r, c, *self.gamble_char[self.n_trial])
                        self.trials_on = True
                        self.clear_fresh_filled()

            if self.filled <= last_filled:
                self.look_at_2 = True
                #                break
            last_filled = self.filled
            # print(count, filled, look_at_2)
            rounds = rounds + 1
#            missed = 0
            r_sub_count = 0
            self.clear_char_counts()

            for r in range(9):
                row = rows[r][1]
                gr_ref = r // 3
                c_sub_count = 0
                for c in range(9):
                    gc_ref = c // 3
                    missed = 0
                    val = '.'
                    col = cols[c][1]
                    if board[r][c] == '.':
                        for char_pos in range(self.n_valid_char):
                            s = char_list[char_pos]
                            if not ((s in row) or (s in col) or (s in groups[gr_ref][gc_ref][1])):
                                missed = missed + 1
                                # print(count, 'count',r, c, s, row)
                                if missed > 1 and not self.look_at_2:
                                    break
                                val = s
                                if self.look_at_2:
                                    self.update_missed_char(r, c, val)

                        if missed == 1:
                            self.update_done_char(r, c, val)
                        elif self.look_at_2:
                            choice_stat[r][c] = missed

            if self.look_at_2:
                self.check_single_miss_and_update()
                if self.filled <= last_filled:
                    self.gamble_pos = -1

                #                    print('No Change')
                else:
                    print("Changed")

        print('rounds ', rounds, 'dot_count', dot_count, 'filled ', self.filled)
        print('ROW choice_char')
        for r in range(9):
            s = []
            for i in range(9): s.append(self.row_char_count[r][i][0])
            print('     ch_count', s)

        print('COL choice_char')
        for c in range(9):
            s = []
            for i in range(9): s.append(self.col_char_count[c][i][0])
            print('     ch_count', s)

        print('GROUP choice_char')
        for g1 in range(3):
            for g2 in range(3):
                s = []
                for i in range(9): s.append(self.group_char_count[g1][g2][i][0])
                print('     ch_count', s)

        for r in self.choice_char:
            print(r)

        print('choice2Cells')
        print(self.choice2cells)
        print(self.gamble_cell)
        print('gamble_char', self.gamble_char)
        print('choice2cell_filled_chars1', choice2cell_filled_chars1)
        print('choice2cell_filled_chars2', choice2cell_filled_chars2)

    def clear_fresh_filled(self):
        for r in range(9):
            for c in range(9):
                self.fresh_filled[0][r][c] = '.'
                self.fresh_filled[1][r][c] = '.'

    def collect_choice2cells(self):
        self.choice2cells.clear()
        for r in range(9):
            char_r = self.choice_char[r]
            for c in range (9):
                if len(char_r[c]) == 2:
                    self.choice2cells.append([r, c])

    def clear_char_counts(self):
        for i in range(9):
            for char_num in range(self.n_valid_char):
                self.row_char_count[i][char_num][0] = 0
                self.row_char_count[i][char_num][1].clear()
                self.col_char_count[i][char_num][0] = 0
                self.col_char_count[i][char_num][1].clear()
        for g1 in range(3):
            for g2 in range(3):
                for char_num in range(self.n_valid_char):
                    self.group_char_count[g1][g2][char_num][0] = 0
                    self.group_char_count[g1][g2][char_num][1].clear()
        for r in self.choice_char:
            for c in r:
                c.clear()

    def check_single_miss_and_update(self):
        # rows
        for r in range(9):
            self.update_one_single_miss_cell(self.row_char_count[r])
        # cols
        for c in range(9):
            self.update_one_single_miss_cell(self.col_char_count[c])
        # group
        for g1 in range(3):
            for g2 in range(3):
                self.update_one_single_miss_cell(self.group_char_count[g1][g2])

    def update_one_single_miss_cell(self, miss_list: List):
        for s in range(self.n_valid_char):
            if miss_list[s][0] == 1:
                self.update_done_char(*miss_list[s][1][0], *self.valid_char_list[s])

    def update_done_char(self, r: int, c: int, val: str):
        if self.board1[r][c] == '.':
            self.board1[r][c] = val
            self.note_down(self.allRows[r], val)
            self.note_down(self.allCols[c], val)
            self.note_down(self.allGroups[r // 3][c // 3], val)
            self.filled = self.filled + 1
            if self.trials_on:
                self.fresh_filled[self.n_trial][r][c] = val

    def update_missed_char(self, r: int, c: int, val: str):
        if self.look_at_2:
            char_num = self.valid_char_list.index(val)
            self.row_char_count[r][char_num][0] = self.row_char_count[r][char_num][0] + 1
            self.row_char_count[r][char_num][1].append([r, c])
            self.col_char_count[c][char_num][0] = self.col_char_count[c][char_num][0] + 1
            self.col_char_count[c][char_num][1].append([r, c])
            gr_ref = r // 3
            gc_ref = c // 3
            self.group_char_count[gr_ref][gc_ref][char_num][0] = self.group_char_count[gr_ref][gc_ref][char_num][0] + 1
            self.group_char_count[gr_ref][gc_ref][char_num][1].append([r, c])
            self.choice_char[r][c].append(val)

    def note_down(self, note: List, val: str):
        if val not in note[1]:
            note[1].append(val)
            note[0] = note[0] - 1

    def backup(self):
        self.filledB = self.filled
        for r in range(9):
            for c in range(9):
                self.boardB[r][c] = self.board1[r][c]

        for i in range(9):
            self.allRowsB[i][0] = self.allRows[i][0]
            self.allRowsB[i][1].clear()
            for j in range(len(self.allRows[i][1])):
                s = self.allRows[i][1][j]
                self.allRowsB[i][1].append(s)
        for i in range(9):
            self.allColsB[i][0] = self.allCols[i][0]
            self.allColsB[i][1].clear()
            for j in range(len(self.allCols[i][1])):
                s = self.allCols[i][1][j]
                self.allColsB[i][1].append(s)
        for g1 in range(3):
            for g2 in range(3):
                self.allGroupsB[g1][g2][0] = self.allGroups[g1][g2][0]
                self.allGroupsB[g1][g2][1].clear()
                for j in range(len(self.allGroups[g1][g2][1])):
                    s = self.allGroups[g1][g2][1][j]
                    self.allGroupsB[g1][g2][1].append(s)
        for r in range(9):
            for c in range(9):
                self.choice_charB[r][c].clear()
                for i in range(len(self.choice_char[r][c])):
                    self.choice_charB[r][c].append(self.choice_char[r][c][i])
        self.backedup = True

    def restore(self):
        ret_val = False
        if self.backedup:
            self.filled = self.filledB
            for r in range(9):
                for c in range(9):
                    self.board1[r][c] = self.boardB[r][c]

            for i in range(9):
                self.allRows[i][0] = self.allRowsB[i][0]
                self.allRows[i][1].clear()
                for j in range(len(self.allRowsB[i][1])):
                    s = self.allRowsB[i][1][j]
                    self.allRows[i][1].append(s)
            for i in range(9):
                self.allCols[i][0] = self.allColsB[i][0]
                self.allCols[i][1].clear()
                for j in range(len(self.allColsB[i][1])):
                    s = self.allColsB[i][1][j]
                    self.allCols[i][1].append(s)
            for g1 in range(3):
                for g2 in range(3):
                    self.allGroups[g1][g2][0] = self.allGroupsB[g1][g2][0]
                    self.allGroups[g1][g2][1].clear()
                    for j in range(len(self.allGroups[g1][g2][1])):
                        s = self.allGroupsB[g1][g2][1][j]
                        self.allGroups[g1][g2][1].append(s)
            for r in range(9):
                for c in range(9):
                    self.choice_char[r][c].clear()
                    for i in range(len(self.choice_charB[r][c])):
                        self.choice_char[r][c].append(self.choice_charB[r][c][i])
        ret_val = True
#        else:
#            print('No backed up data!')
        return ret_val

S = Solution37()
# board2 = [["5","3",".",".","7",".",".",".","."],["6",".",".","1","9","5",".",".","."],[".","9","8",".",".",".",".","6","."],["8",".",".",".","6",".",".",".","3"],["4",".",".","8",".","3",".",".","1"],["7",".",".",".","2",".",".",".","6"],[".","6",".",".",".",".","2","8","."],[".",".",".","4","1","9",".",".","5"],[".",".",".",".","8",".",".","7","9"]]
# original unsolved input
board2 = [[".", ".", "9", "7", "4", "8", ".", ".", "."], ["7", ".", ".", ".", ".", ".", ".", ".", "."],
         [".", "2", ".", "1", ".", "9", ".", ".", "."], [".", ".", "7", ".", ".", ".", "2", "4", "."],
         [".", "6", "4", ".", "1", ".", "5", "9", "."], [".", "9", "8", ".", ".", ".", "3", ".", "."],
         [".", ".", ".", "8", ".", "3", ".", "2", "."], [".", ".", ".", ".", ".", ".", ".", ".", "6"],
         [".", ".", ".", "2", "7", "5", "9", ".", "."]]
# part updated
#board2 = [[".",".","9","7","4","8",".",".","2"],["7",".",".",".",".",".",".",".","9"],[".","2",".","1",".","9",".",".","."],[".",".","7",".",".",".","2","4","."],[".","6","4",".","1",".","5","9","."],[".","9","8",".",".",".","3",".","."],["9",".",".","8",".","3",".","2","."],[".",".","2",".",".",".",".",".","6"],[".",".",".","2","7","5","9",".","."]]
# part updated from filled dotCount 54 filled 24
# board2 = [[".","1","9","7","4","8",".",".","2"],["7",".",".","6",".","2",".",".","9"],[".","2",".","1",".","9",".",".","."],[".",".","7","9","8","6","2","4","1"],["2","6","4","3","1","7","5","9","8"],["1","9","8","5","2","4","3","6","7"],["9",".",".","8","6","3",".","2","."],[".",".","2","4","9","1",".",".","6"],[".",".",".","2","7","5","9",".","."]]
# solved input
board2 = [["5","3",".",".","7",".",".",".","."],["6",".",".","1","9","5",".",".","."],[".","9","8",".",".",".",".","6","."],["8",".",".",".","6",".",".",".","3"],["4",".",".","8",".","3",".",".","1"],["7",".",".",".","2",".",".",".","6"],[".","6",".",".",".",".","2","8","."],[".",".",".","4","1","9",".",".","5"],[".",".",".",".","8",".",".","7","9"]]
S.solveSudoku(board2)
print('Result')
for r1 in board2:
    print(r1)
