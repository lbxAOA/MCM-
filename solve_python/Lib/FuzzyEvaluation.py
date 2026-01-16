"""
模糊综合评价
作用：对多个评价指标进行综合评价，得出总体评价结果
适用于评价指标较多，且各指标之间存在一定模糊性的情况
步骤：
1.确定评价指标及其权重
2.构建模糊评价矩阵
3.进行模糊综合运算，得出综合评价结果
"""

import math
import numpy as np

class FuzzyEvaluation:
    """模糊综合评价类"""
    
    def __init__(self, data_matrix, thresholds=None, levels=None):
        """
        初始化模糊综合评价
        :param data_matrix: 数据矩阵，每一列代表一个评价指标，每一行代表一个样本
        :param thresholds: 阈值列表，用于划分等级，如[[0.018, 0.028, 0.038], [1, 2, 3]]
        :param levels: 评价等级列表，默认为['优', '良', '中', '差']
        """
        self.data_matrix = np.array(data_matrix)
        self.thresholds = thresholds
        self.levels = levels if levels else ['优', '良', '中', '差']
        self.n_indicators = self.data_matrix.shape[1]  # 指标数量
        self.n_samples = self.data_matrix.shape[0]     # 样本数量
        self.n_levels = len(self.levels)               # 等级数量
        
    def calculate_membership(self):
        """
        计算每个指标在各个等级下的隶属度（频率）
        :return: 隶属度矩阵，形状为(n_indicators, n_levels)
        """
        membership_matrix = []
        
        for i in range(self.n_indicators):
            indicator_data = self.data_matrix[:, i]
            level_counts = [0] * self.n_levels
            
            # 根据阈值划分等级并统计
            if self.thresholds and i < len(self.thresholds):
                threshold = self.thresholds[i]
                for value in indicator_data:
                    assigned = False
                    for j, t in enumerate(threshold):
                        if value <= t:
                            level_counts[j] += 1
                            assigned = True
                            break
                    if not assigned:
                        level_counts[-1] += 1
            else:
                # 默认等分
                min_val, max_val = np.min(indicator_data), np.max(indicator_data)
                interval = (max_val - min_val) / self.n_levels
                for value in indicator_data:
                    level_idx = min(int((value - min_val) / interval), self.n_levels - 1)
                    level_counts[level_idx] += 1
            
            # 转换为频率（隶属度）
            membership = [count / self.n_samples for count in level_counts]
            membership_matrix.append(membership)
        
        return np.array(membership_matrix)
    
    def entropy_weight(self, membership_matrix):
        """
        使用熵权法计算指标权重
        :param membership_matrix: 隶属度矩阵
        :return: 权重列表
        """
        k = -1 / math.log(self.n_levels)
        entropies = []
        
        for i in range(self.n_indicators):
            entropy_sum = 0
            for j in range(self.n_levels):
                if membership_matrix[i][j] > 0:
                    entropy_sum += membership_matrix[i][j] * math.log(membership_matrix[i][j])
            entropy = k * entropy_sum
            entropies.append(entropy)
        
        # 计算权重
        entropy_sum = sum(entropies)
        weights = [(1 - e) / (self.n_indicators - entropy_sum) for e in entropies]
        
        return weights
    
    def frequency_weight(self, p=10):
        """
        频数统计法确定权重
        :param p: 分组数
        :return: 权重向量
        """
        weights = np.zeros(self.n_indicators)
        
        for i in range(self.n_indicators):
            indicator_data = self.data_matrix[:, i]
            maximum = np.max(indicator_data)
            minimum = np.min(indicator_data)
            gap = (maximum - minimum) / p
            
            # 创建分组区间
            groups = []
            item = minimum
            while item < maximum:
                groups.append([item, item + gap])
                item = item + gap
            
            # 统计频数
            freq_dict = {str(k): 0 for k in range(len(groups))}
            for value in indicator_data:
                for k in range(len(groups)):
                    if value >= groups[k][0] and value < groups[k][1]:
                        freq_dict[str(k)] += 1
                        break
            
            # 取最大频数对应的组中值
            max_idx = int(max(freq_dict, key=freq_dict.get))
            mid = (groups[max_idx][0] + groups[max_idx][1]) / 2
            weights[i] = mid
        
        # 归一化
        weights = weights / np.sum(weights)
        return weights
    
    def comprehensive_evaluation(self, weights=None, method='entropy'):
        """
        进行模糊综合评价
        :param weights: 权重列表，如果为None则自动计算
        :param method: 权重计算方法，'entropy'(熵权法) 或 'frequency'(频数统计法)
        :return: 综合评价结果字典
        """
        # 计算隶属度矩阵
        membership_matrix = self.calculate_membership()
        
        # 计算或使用给定的权重
        if weights is None:
            if method == 'entropy':
                weights = self.entropy_weight(membership_matrix)
            elif method == 'frequency':
                weights = self.frequency_weight()
            else:
                weights = [1/self.n_indicators] * self.n_indicators  # 平均权重
        
        # 模糊综合运算
        result = np.zeros(self.n_levels)
        for i in range(self.n_indicators):
            for j in range(self.n_levels):
                result[j] += weights[i] * membership_matrix[i][j]
        
        # 确定最终评价等级
        max_idx = np.argmax(result)
        final_level = self.levels[max_idx]
        
        return {
            'weights': weights,
            'membership_matrix': membership_matrix.tolist(),
            'scores': result.tolist(),
            'final_level': final_level,
            'level_scores': {self.levels[i]: result[i] for i in range(self.n_levels)}
        }


def fuzzy_evaluate_from_excel(file_path, sheet_name, indicator_cols, thresholds=None, method='entropy'):
    """
    从Excel文件读取数据并进行模糊综合评价
    :param file_path: Excel文件路径
    :param sheet_name: 工作表名称
    :param indicator_cols: 指标列索引列表，如[0, 1]表示第1和第2列
    :param thresholds: 阈值列表
    :param method: 权重计算方法
    :return: 评价结果字典
    """
    try:
        import xlrd
    except ImportError:
        raise ImportError("需要安装xlrd库: pip install xlrd")
    
    # 读取数据
    data = xlrd.open_workbook(file_path)
    table = data.sheet_by_name(sheet_name)
    
    # 提取指标数据
    data_matrix = []
    nrows = table.nrows
    
    for row_idx in range(nrows):
        row_data = []
        for col_idx in indicator_cols:
            try:
                value = table.cell_value(row_idx, col_idx)
                if isinstance(value, (int, float)):
                    row_data.append(value)
            except:
                continue
        if len(row_data) == len(indicator_cols):
            data_matrix.append(row_data)
    
    # 创建评价对象并进行评价
    fuzzy_eval = FuzzyEvaluation(data_matrix, thresholds=thresholds)
    result = fuzzy_eval.comprehensive_evaluation(method=method)
    
    return result
