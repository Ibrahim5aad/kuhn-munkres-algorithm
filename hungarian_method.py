import sys
from typing import NewType, Sequence, Tuple
Matrix = NewType('Matrix', Sequence[Sequence[int]])

class Hungarian:
    
    def __init__(self):
        self.mat = None
        self.row_covered = []
        self.col_covered = []
        self.starred = None
        self.n = 0
        self.Z0_r = 0
        self.Z0_c = 0
        self.series = None
    
    def solve(self, cost_matrix: Matrix):
        self.mat = cost_matrix
        self.n = len(self.mat)
        self.row_covered = [False for i in range(self.n)]
        self.col_covered = [False for i in range(self.n)]
        self.Z0_r = 0
        self.Z0_c = 0
        self.series = [[0 for j in range(2)] for j in range(self.n*2)]
        self.starred = [[0 for j in range(self.n)] for j in range(self.n)]

        done = False
        step = 1

        steps = { 1 : self.step1,
                  2 : self.step2,
                  3 : self.step3,
                  4 : self.step4,
                  5 : self.step5,
                  6 : self.step6
                  }

        while not done:
            try:
                func = steps[step]
                step = func()
            except:
                done = True
                
        results = []
        for i in range(self.n):
            for j in range(self.n):
                if self.starred[i][j] == 1:
                    results += [(i, j)]

        return results

    def step1(self):
        """
        For each row of the matrix, find the smallest element and
        subtract it from every element in its row. Go to Step 2.
        """
        n = self.n
        for i in range(n):
            vals = [x for x in self.mat[i]]
            minval = min(vals)
            for j in range(n):
                self.mat[i][j] -= minval
        return 2

    def step2(self):
        """
        Find a zero (Z) in the resulting matrix. If there is no starred
        zero in its row or column, star Z. Repeat for each element in the
        matrix. Go to Step 3.
        """
        for i in range(self.n):
            for j in range(self.n):
                if (self.mat[i][j] == 0) and \
                        (not self.col_covered[j]) and \
                        (not self.row_covered[i]):
                    self.starred[i][j] = 1
                    self.col_covered[j] = True
                    self.row_covered[i] = True
                    break

        self.__clear_covers()
        return 3

    def step3(self):
        """
        Cover each column containing a starred zero. If K columns are
        covered, the starred zeros describe a complete set of unique
        assignments. In this case, Go to DONE, otherwise, Go to Step 4.
        """
        n = self.n
        count = 0
        for i in range(n):
            for j in range(n):
                if self.starred[i][j] == 1 and not self.col_covered[j]:
                    self.col_covered[j] = True
                    count += 1

        if count >= n:
            step = 7 # done
        else:
            step = 4

        return step

    def step4(self):
        """
        Find a noncovered zero and prime it. If there is no starred zero
        in the row containing this primed zero, Go to Step 5. Otherwise,
        cover this row and uncover the column containing the starred
        zero. Continue in this manner until there are no uncovered zeros
        left. Save the smallest uncovered value and Go to Step 6.
        """
        step = 0
        done = False
        row = 0
        col = 0
        star_col = -1
        while not done:
            (row, col) = self.__find_a_zero(row, col)
            if row < 0:
                done = True
                step = 6
            else:
                self.starred[row][col] = 2
                star_col = self.__find_star_in_row(row)
                if star_col >= 0:
                    col = star_col
                    self.row_covered[row] = True
                    self.col_covered[col] = False
                else:
                    done = True
                    self.Z0_r = row
                    self.Z0_c = col
                    step = 5

        return step

    def step5(self):
        """
        Construct a series of alternating primed and starred zeros as
        follows. Let Z0 represent the uncovered primed zero found in Step 4.
        Let Z1 denote the starred zero in the column of Z0 (if any).
        Let Z2 denote the primed zero in the row of Z1 (there will always
        be one). Continue until the series terminates at a primed zero
        that has no starred zero in its column. Unstar each starred zero
        of the series, star each primed zero of the series, erase all
        primes and uncover every line in the matrix. Return to Step 3
        """
        count = 0
        series = self.series
        series[count][0] = self.Z0_r
        series[count][1] = self.Z0_c
        done = False
        while not done:
            row = self.__find_star_in_col(series[count][1])
            if row >= 0:
                count += 1
                series[count][0] = row
                series[count][1] = series[count-1][1]
            else:
                done = True

            if not done:
                col = self.__find_prime_in_row(series[count][0])
                count += 1
                series[count][0] = series[count-1][0]
                series[count][1] = col

        self.__convert_series(series, count)
        self.__clear_covers()
        self.__erase_primes()
        return 3

    def step6(self):
        """
        Add the value found in Step 4 to every element of each covered
        row, and subtract it from every element of each uncovered column.
        Return to Step 4 without altering any stars, primes, or covered
        lines.
        """
        minval = self.__find_smallest()
        for i in range(self.n):
            for j in range(self.n):
                if self.row_covered[i]:
                    self.mat[i][j] += minval
                if not self.col_covered[j]:
                    self.mat[i][j] -= minval
        return 4

    def __find_smallest(self):
        """Find the smallest uncovered value in the matrix."""
        minval = sys.maxsize
        for i in range(self.n):
            for j in range(self.n):
                if (not self.row_covered[i]) and (not self.col_covered[j]):
                    if minval > self.mat[i][j]:
                        minval = self.mat[i][j]
        return minval

    def __find_a_zero(self, i0: int = 0, j0: int = 0):
        """Find the first uncovered element with value 0"""
        row = -1
        col = -1
        i = i0
        n = self.n
        done = False

        while not done:
            j = j0
            while True:
                if (self.mat[i][j] == 0) and \
                        (not self.row_covered[i]) and \
                        (not self.col_covered[j]):
                    row = i
                    col = j
                    done = True
                j = (j + 1) % n
                if j == j0:
                    break
            i = (i + 1) % n
            if i == i0:
                done = True

        return (row, col)

    def __find_star_in_row(self, row: Sequence[int]):
        """
        Find the first starred element in the specified row. Returns
        the column index, or -1 if no starred element was found.
        """
        col = -1
        for j in range(self.n):
            if self.starred[row][j] == 1:
                col = j
                break

        return col

    def __find_star_in_col(self, col: Sequence[int]):
        """
        Find the first starred element in the specified col. Returns
        the row index, or -1 if no starred element was found.
        """
        row = -1
        for i in range(self.n):
            if self.starred[i][col] == 1:
                row = i
                break

        return row

    def __find_prime_in_row(self, row):
        """
        Find the first prime element in the specified row. Returns
        the column index, or -1 if no starred element was found.
        """
        col = -1
        for j in range(self.n):
            if self.starred[row][j] == 2:
                col = j
                break

        return col


    def __convert_series(self,
                       series: Matrix,
                       count: int):
        """
        Unstar each starred zero
        of the series, star each primed zero of the series
        """
        for i in range(count+1):
            if self.starred[series[i][0]][series[i][1]] == 1:
                self.starred[series[i][0]][series[i][1]] = 0
            else:
                self.starred[series[i][0]][series[i][1]] = 1


    def __clear_covers(self):
        for i in range(self.n):
            self.row_covered[i] = False
            self.col_covered[i] = False


    def __erase_primes(self):
        for i in range(self.n):
            for j in range(self.n):
                if self.starred[i][j] == 2:
                    self.starred[i][j] = 0
