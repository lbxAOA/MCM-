def frequency(matrix,p):
    '''
    频数统计法确定权重
    :param matrix: 因素矩阵
    :param p: 分组数
    :return: 权重向量
    '''
    A = np.zeros((matrix.shape[0]))
    for i in range(0, matrix.shape[0]):
        ## 根据频率确定频数区间列表
        row = list(matrix[i, :])
        maximum = max(row)
        minimum = min(row)
        gap = (maximum - minimum) / p
        row.sort()
        group = []
        item = minimum
        while(item < maximum):
            group.append([item, item + gap])
            item = item + gap
        print(group)
        ## 初始化一个数据字典，便于记录频数
        dataDict = {}
        for k in range(0, len(group)):
            dataDict[str(k)] = 0
        ## 判断本行的每个元素在哪个区间内，并记录频数
        for j in range(0, matrix.shape[1]):
            for k in range(0, len(group)):
             if(matrix[k, j] >= group[k][0]):
                 dataDict[str(k)] = dataDict[str(k)] + 1
             break
        print(dataDict)
        ## 取出最大频数对应的key，并以此为索引求组中值
        index = int(max(dataDict,key=dataDict.get))
        mid = (group[index][0] + group[index][1]) / 2
        print(mid)
        A[i] = mid
    A = A / sum(A[:]) ## 归一化
    return A
