# ACTIVE
from typing import List


# Sudoku Solver
class Solution37:
    def __init__(self):
        self.look_at_2 = False
        self.trials_on = True
        self.gamble_char = []
        self.gamble_cell = []
        self.choice2cells = []
        self.choice_charB = []
        self.choice_char = []
        self.fresh_filled = []
        for i in range(9):
            self.fresh_filled.append([])
#        self.trial_filled = [0, 0, 0]
        self.filledB = 0
        self.filled = 0
        self.n_trial = 0
        self.board1 = []
        self.boardB = []
        self.backed_up = False
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

        for r in range(9):
            self.boardB.append([])
            for c in range(9):
                self.boardB[r].append(self.board1[r][c])
        r_ref = 0
        dot_count = 0
        for r in range(9):
            c_ref = 0
            for c in range(9):
                val = board[r][c]
                if not val == '.':
                    self.note_down(rows[r_ref], val)
                    self.note_down(cols[c_ref], val)
                    self.note_down(groups[r // 3][c // 3], val)
                else:
                    dot_count = dot_count + 1
                c_ref = c_ref + 1
            r_ref = r_ref + 1
        eff_rounds = 0
        last_filled = -1
#        self.look_at_2 = True
        choice_stat = []
        for r in range(9):
            choice_stat.append([0, 0, 0, 0, 0, 0, 0, 0, 0])
            self.choice_char.append([])
            self.choice_charB.append([])
            for c in range(9):
                self.choice_char[r].append([])
                self.choice_charB[r].append([])

        gamble_cell_pos = 0
        self.n_trial = 0
        self.trials_on = False
        for i in range(9):
            for r in range(9):
                self.fresh_filled[i].append([])
                for c in range(9):
                    self.fresh_filled[i][r].append('.')

        self.unique_count = [0, 0]
        self.sole_count = [0, 0]
        self.forced_count = [0, 0]
        self.forced_trial = 0
        # all above [now, backup]
        rounds = 0
        self.eff_rounds = 0
        self.eff_rounsB = 0
        while self.filled < dot_count:
            # if self.look_at_2 and self.filled <= last_filled:
            #     self.collectChoice2Cells()
            #     break
            rounds = rounds + 1
            if rounds > 1000:
                print('too many rounds, exiting')
                break
            if self.eff_rounds > 120:
                print('too many self.eff_rounds, exiting')
                break
            if self.look_at_2:
                if self.trials_on:
                    if self.n_trial < len(self.gamble_char) - 1:
                        self.n_trial = self.n_trial + 1
                        # try next
                        if self.restore():
                            self.forced_trial = self.forced_trial - 1
                            r, c = self.gamble_cell[0]
                            self.update_done_char(r, c, *self.gamble_char[self.n_trial])  # force chain
                            self.forced_trial = self.forced_trial + 1
                        else:
                            break

                    elif self.n_trial >= len(self.gamble_char) - 1:
                        repeat_found = False
                        self.restore()
                        # look for force chain effect
                        for r_found in range(9):
#                            if repeat_found:
#                                break
                            for c_found in range(9):
#                                if repeat_found:
#                                    break
                                s0 = self.fresh_filled[0][r_found][c_found]
                                if s0 == '.':
                                    continue
                                local_repeat_found = False
                                for i in range(1, len(self.gamble_char)):
                                    s = self.fresh_filled[i][r_found][c_found]
                                    local_repeat_found = (s == s0)
                                    if not local_repeat_found:
                                        break
                                if local_repeat_found:
                                    repeat_found = True
                                    self.update_done_char(r_found, c_found, s0)
                                    self.forced_count[0] = self.forced_count[0] + 1
#                                    self.trials_on = False
                                    print('repeat_found in cell ', [r_found, c_found], s0, 'filled', self.filled,
                                          'self.eff_rounds', self.eff_rounds)

                        if not repeat_found:
                            if gamble_cell_pos < len(self.choice2cells) - 1:
                                self.forced_trial = self.forced_trial - 1
                                gamble_cell_pos = gamble_cell_pos + 1
                                self.n_trial = 0
                                self.gamble_cell.clear()
                                self.gamble_cell.append(self.choice2cells[gamble_cell_pos])
                                r, c = self.gamble_cell[0]
                                self.gamble_char.clear()
                                for s in self.choice_char[r][c]:
                                    self.gamble_char.append(s)
                                self.update_done_char(r, c, *self.gamble_char[self.n_trial])  # force chain
                                self.forced_trial = self.forced_trial + 1
                                self.clear_fresh_filled()
                                print('trying ', *self.gamble_char[self.n_trial], 'at ', self.gamble_cell[0],
                                      gamble_cell_pos, 'of', len(self.choice2cells))
#                                continue
                            else:
                                self.trials_on = False
                                self.restore()
                                self.forced_trial = self.forced_trial - 1
                                gamble_cell_pos = 0
#                                self.look_at_2 = False
                                print('all trials exhausted at round', self.eff_rounds, 'filled', self.filled)

                elif self.filled <= last_filled:
                    self.n_trial = 0
                    self.backup()
                    self.collect_choice2cells()
                    if len(self.choice2cells):
                        self.gamble_cell.clear()
                        self.gamble_cell.append(self.choice2cells[gamble_cell_pos])
                        r, c = self.gamble_cell[0]
                        self.gamble_char.clear()
                        for s in self.choice_char[r][c]:
                            self.gamble_char.append(s)
                        print('Start trying ', *self.gamble_char[self.n_trial], 'at ', self.gamble_cell[0],
                              'self.eff_rounds', self.eff_rounds, 'filled', self.filled)
                        self.update_done_char(r, c, *self.gamble_char[self.n_trial])  # force chain
                        self.forced_trial = self.forced_trial + 1
                        self.trials_on = True
                        self.clear_fresh_filled()

            if self.filled <= last_filled:
                self.look_at_2 = True

            last_filled = self.filled
            self.eff_rounds = self.eff_rounds + 1

            self.clear_char_counts()
            try_once_more = True
            while try_once_more:
                try_once_more = False
                for r in range(9):
                    row = rows[r][1]
                    gr_ref = r // 3
                    for c in range(9):
                        gc_ref = c // 3
                        missed = 0
                        val = '.'
                        col = cols[c][1]
                        if board[r][c] == '.':
                            for char_pos in range(self.n_valid_char):
                                s = char_list[char_pos]
                                if not ((s in row) or (s in col) or (s in groups[gr_ref][gc_ref][1])):
                                    val = s
                                    missed = missed + 1
                                    if missed > 1 and not self.look_at_2:
                                        break
                                    if self.look_at_2:
                                        self.update_missed_char(r, c, val)

                            if missed == 1:  # sole candidate
                                self.update_done_char(r, c, val)
                                self.sole_count[0] = self.sole_count[0] + 1
                                try_once_more = try_once_more or True
                            elif self.look_at_2:
                                choice_stat[r][c] = missed

            if self.look_at_2 and not self.trials_on:
                self.check_single_miss_and_update() # unique candidate
        print('self.eff_rounds', self.eff_rounds)
        print('filled', self.filled, ' / ', dot_count)
        print('sole = ', self.sole_count)
        print('unique = ', self.unique_count)
        print('forced = ', self.forced_count)
        print('forced_trial = ', self.forced_trial)

    def clear_fresh_filled(self):
        for r in range(9):
            for c in range(9):
                for i in range(9):
                    self.fresh_filled[i][r][c] = '.'

    def collect_choice2cells(self):
        self.choice2cells.clear()
        for r in range(9):
            char_r = self.choice_char[r]
            for c in range(9):
                if 1 < len(char_r[c]) < 3:
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
        done = False
        for row in self.row_char_count:
            if done:
                break
            for char_pos in range(9):
                if done:
                    break
                elem = row[char_pos]
                if elem[0] == 1:
                    r, c = elem[1][0]
                    # check with col_char_count
                    elem_c = self.col_char_count[c][char_pos]
                    if elem_c[0] == 1:
                        cr, cc = elem_c[1][0]
                        if cr == r and cc == c:
                            g1 = r // 3
                            g2 = c // 3
                            # check with group
                            elem_g = self.group_char_count[g1][g2][char_pos]
                            if elem_g[0] == 1:
                                gr, gc = elem_g[1][0]
                                if gr == r and gc == c:
                                    self.update_done_char(r, c, self.valid_char_list[char_pos])
                                    self.unique_count[0] = self.unique_count[0] + 1
                                    done = True

    def update_one_single_miss_cell(self, miss_list: List):
        found = False
        for s in range(self.n_valid_char):
            if miss_list[s][0] == 1:
                self.update_done_char(*miss_list[s][1][0], *self.valid_char_list[s])
                found = found or True
        return found

    def update_done_char(self, r: int, c: int, val: str):
        if self.board1[r][c] == '.':
            self.board1[r][c] = val
            self.note_down(self.allRows[r], val)
            self.note_down(self.allCols[c], val)
            self.note_down(self.allGroups[r // 3][c // 3], val)
            self.filled = self.filled + 1
            if self.trials_on:
                self.fresh_filled[self.n_trial][r][c] = val
#                self.trial_filled[self.n_trial] = self.filled

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
        self.eff_rounsB = self.eff_rounds
        self.filledB = self.filled
        self.unique_count[1] = self.unique_count[0]
        self.sole_count[1] =  self.sole_count[0]
        self.forced_count[1] = self.forced_count[0]

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
        self.backed_up = True

    def restore(self):
        ret_val = False
        self.eff_rounds = self.eff_rounsB
        self.unique_count[0] = self.unique_count[1]
        self.sole_count[0] = self.sole_count[1]
        self.forced_count[0] = self.forced_count[1]
        if self.backed_up:
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
        return ret_val


S = Solution37()
# board2 = [["5","3",".",".","7",".",".",".","."],["6",".",".","1","9","5",".",".","."],[".","9","8",".",".",".",".","6","."],["8",".",".",".","6",".",".",".","3"],["4",".",".","8",".","3",".",".","1"],["7",".",".",".","2",".",".",".","6"],[".","6",".",".",".",".","2","8","."],[".",".",".","4","1","9",".",".","5"],[".",".",".",".","8",".",".","7","9"]]
# original unsolved input
#board2 = [[".", ".", "9", "7", "4", "8", ".", ".", "."], ["7", ".", ".", ".", ".", ".", ".", ".", "."],
#    [".", "2", ".", "1", ".", "9", ".", ".", "."], [".", ".", "7", ".", ".", ".", "2", "4", "."],
#    [".", "6", "4", ".", "1", ".", "5", "9", "."], [".", "9", "8", ".", ".", ".", "3", ".", "."],
#    [".", ".", ".", "8", ".", "3", ".", "2", "."], [".", ".", ".", ".", ".", ".", ".", ".", "6"],
#    [".", ".", ".", "2", "7", "5", "9", ".", "."]]
# part updated
# board2 = [[".",".","9","7","4","8",".",".","2"],["7",".",".",".",".",".",".",".","9"],[".","2",".","1",".","9",".",".","."],[".",".","7",".",".",".","2","4","."],[".","6","4",".","1",".","5","9","."],[".","9","8",".",".",".","3",".","."],["9",".",".","8",".","3",".","2","."],[".",".","2",".",".",".",".",".","6"],[".",".",".","2","7","5","9",".","."]]
# part updated from filled dotCount 54 filled 24
# board2 = [[".","1","9","7","4","8",".",".","2"],["7",".",".","6",".","2",".",".","9"],[".","2",".","1",".","9",".",".","."],[".",".","7","9","8","6","2","4","1"],["2","6","4","3","1","7","5","9","8"],["1","9","8","5","2","4","3","6","7"],["9",".",".","8","6","3",".","2","."],[".",".","2","4","9","1",".",".","6"],[".",".",".","2","7","5","9",".","."]]
# solved input
# board2 = [["5","3",".",".","7",".",".",".","."],["6",".",".","1","9","5",".",".","."],[".","9","8",".",".",".",".","6","."],["8",".",".",".","6",".",".",".","3"],["4",".",".","8",".","3",".",".","1"],["7",".",".",".","2",".",".",".","6"],[".","6",".",".",".",".","2","8","."],[".",".",".","4","1","9",".",".","5"],[".",".",".",".","8",".",".","7","9"]]
# test sample 6
board2 = [[".",".",".","2",".",".",".","6","3"],["3",".",".",".",".","5","4",".","1"],[".",".","1",".",".","3","9","8","."],[".",".",".",".",".",".",".","9","."],[".",".",".","5","3","8",".",".","."],[".","3",".",".",".",".",".",".","."],[".","2","6","3",".",".","5",".","."],["5",".","3","7",".",".",".",".","8"],["4","7",".",".",".","1",".",".","."]]
# test sample 4 requiring force chain code
# board2 = [[".",".","9","7","4","8",".",".","."],["7",".",".",".",".",".",".",".","."],[".","2",".","1",".","9",".",".","."],[".",".","7",".",".",".","2","4","."],[".","6","4",".","1",".","5","9","."],[".","9","8",".",".",".","3",".","."],[".",".",".","8",".","3",".","2","."],[".",".",".",".",".",".",".",".","6"],[".",".",".","2","7","5","9",".","."]]
S.solveSudoku(board2)
print('Result')
for r1 in board2:
    print(r1)
