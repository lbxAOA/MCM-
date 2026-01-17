import numpy as np
import sys
import os

# 添加父目录到路径以导入Lib模块
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if parent_dir not in sys.path:
    sys.path.append(parent_dir)

from Lib.PSO import PSO
from Lib.FuzzyEvaluation import FuzzyEvaluation

# 主程序
if __name__ == '__main__':
    # 示例数据
    data_matrix = [
        [0.8, 0.6, 0.9],
        [0.7, 0.8, 0.6],
        [0.9, 0.7, 0.8]
    ]
    
    # 创建模糊综合评价对象
    fuzzy_eval = FuzzyEvaluation(data_matrix)
    
    # 进行评价
    result = fuzzy_eval.evaluate(method='entropy')
    
    # 输出结果
    print("评价结果：")
    print(result)