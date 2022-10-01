import numpy as np
from random import randrange
import datetime
from  multiprocessing import Pool, Process, Manager

rows, columns = 400, 400


def create_matrix(rows, columns):
    matrix = np.empty((rows,columns))
    for i in range(rows):
        for j in range(columns):
            matrix[i][j] = randrange(10)
    return matrix

a_matrix = create_matrix(rows, columns)
b_matrix = create_matrix(rows, columns)


c = []


def comp_matrix_mult_str_x_col(first_matrix, second_matrix):
    length = len(first_matrix)
    result_matrix = [[0 for i in range(length)] for i in range(length)]
    for i in range(length):
        for j in range(length):
            for k in range(length):
                result_matrix[i][j] += first_matrix[i][k] * second_matrix[k][j]
    return result_matrix

def comp_matrix_mult_col_x_str(first_matrix, second_matrix):
    length = len(first_matrix)
    result_matrix = [[0 for i in range(length)] for i in range(length)]
    for i in range(length):
        for j in range(length):
            for k in range(length):
                result_matrix[j][i] += first_matrix[i][k] * second_matrix[k][j]
    return result_matrix


def dividing(matrix):
    return [matrix[: rows // 2, : rows // 2 ],
            matrix[: rows // 2,rows // 2  : ],
            matrix[rows // 2 : , : rows // 2],
            matrix[rows // 2 :, rows // 2 : ]]

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
    print(row_end - row_start)

    # For columns
    start = datetime.datetime.now()
    res2 = comp_matrix_mult_col_x_str(a_matrix, b_matrix)
    end = datetime.datetime.now()
    print(end - start)

    # For 4 processes
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
    print(e - s)





