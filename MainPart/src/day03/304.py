from typing import List 

class NumMatrix:

    def __init__(self, matrix: List[List[int]]):
        self.matrix = matrix
        column = len(matrix[0])
        row = len(matrix)
        self.f_matrix = [[0 for _ in range(column + 1)] for _ in range(row + 1)]
        
        for i in range(row):
            for j in range(column):
                self.f_matrix[i+1][j+1] = (
                    self.f_matrix[i][j+1] + 
                    self.f_matrix[i+1][j] - 
                    self.f_matrix[i][j] + 
                    matrix[i][j]
                )


    def sumRegion(self, row1: int, col1: int, row2: int, col2: int) -> int:
        f = self.f_matrix
        return (
            f[row2+1][col2+1]
            - f[row1][col2+1]
            - f[row2+1][col1]
            + f[row1][col1]
        )
        


# Your NumMatrix object will be instantiated and called as such:
# obj = NumMatrix(matrix)
# param_1 = obj.sumRegion(row1,col1,row2,col2)