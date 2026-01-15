def AHP(matrix):
    if isConsist(matrix):
        lam, x = np.linalg.eig(matrix)
        return x[0] / sum(x[0][:])
    else:
        print("一致性检验未通过")
        return None

def isConsist(matrix):
    '''
    :param matrix: 成对比较矩阵
    :return:    通过一致性检验则返回true，否则返回false
    '''
    n = np.shape(matrix)[0]
    a, b = np.linalg.eig(matrix)
    maxlam = a[0].real
    CI = (maxlam - n) / (n - 1)
    RI = [0, 0, 0.58, 0.9, 1.12, 1.24, 1.32, 1.41, 1.45]
    CR = CI / RI[n-1]
    if CR < 0.1:
        return True, CI, RI[n-1]
    else:
        return False, None, None
