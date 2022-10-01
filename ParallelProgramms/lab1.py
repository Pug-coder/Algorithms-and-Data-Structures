import numpy as np
from random import randrange
import datetime
from  multiprocessing import Pool, Process, Manager

rows, columns = 400, 400

# Empty matrix creation
def create_matrix(rows, columns):
    matrix = np.empty((rows,columns))
    for i in range(rows):
        for j in range(columns):
            matrix[i][j] = randrange(10)
    return matrix

a_matrix = create_matrix(rows, columns)
b_matrix = create_matrix(rows, columns)

c = []

# Calculation matrix multiplicaion (row to col)
def comp_matrix_mult_str_x_col(first_matrix, second_matrix):
    length = len(first_matrix)
    result_matrix = [[0 for i in range(length)] for i in range(length)]
    for i in range(length):
        for j in range(length):
            for k in range(length):
                result_matrix[i][j] += first_matrix[i][k] * second_matrix[k][j]
    return result_matrix

# Dividing matrix for mor processes usage
def dividing(matrix):
    return [matrix[: len(matrix[0]) // 2, : len(matrix[0]) // 2 ],
            matrix[: len(matrix[0]) // 2,len(matrix[0]) // 2  : ],
            matrix[len(matrix[0]) // 2 : , : len(matrix[0]) // 2],
            matrix[len(matrix[0]) // 2 :, len(matrix[0]) // 2 : ]]

# Func for calculation multiplication with n processes
def mp_multiplication(r,first_matrix, second_matrix):
    length = len(first_matrix)
    result_matrix = [[0 for i in range(length)] for i in range(length)]
    for i in range(length):
        for j in range(length):
            for k in range(length):
                result_matrix[i][j] += first_matrix[i][k] * second_matrix[k][j]
    r.append(result_matrix)
    return result_matrix



if __name__ == '__main__':

    # For rows
    row_start = datetime.datetime.now()
    res1 = comp_matrix_mult_str_x_col(a_matrix, b_matrix)
    row_end = datetime.datetime.now()
    print('Single multiplication', row_end - row_start)

    # 4-part dividing
    s = datetime.datetime.now()
    manager = Manager()
    r = manager.list()
    m1 = dividing(a_matrix)
    m2 = dividing(b_matrix)
    jobs = []

    for i in range(len(m1)):
        p = Process(target=mp_multiplication, args=(r, m1[i], m2[i]))
        jobs.append(p)
        p.start()

    for proc in jobs:
        proc.join()

    for elem in r:
        c.append(elem)

    e = datetime.datetime.now()
    print("Calculation with 4-part dividing", e - s)


    a_matrix_div = []
    b_matrix_div = []

    #16-part dividing
    s = datetime.datetime.now()
    manager = Manager()
    r = manager.list()

    for i in range(len(m1)):
        a_matrix_div.append(dividing(m1[i]))
        b_matrix_div.append(dividing(m2[i]))

    jobs = []


    for i in range(len(a_matrix_div)):
        for j in range(len(a_matrix_div[i])):
            p = Process(target=mp_multiplication, args=(r, a_matrix_div[i][j], b_matrix_div[i][j]))
        jobs.append(p)
        p.start()

    for proc in jobs:
        proc.join()

    for elem in r:
        c.append(elem)

    e = datetime.datetime.now()
    print("Calculation with 16-part dividing",e - s)