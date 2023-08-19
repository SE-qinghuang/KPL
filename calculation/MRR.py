def calculate_mrr(results):
    """
    计算MRR指标。

    :param results: 包含每个查询的结果的列表，每个查询的结果是一个列表，其中包含若干文档及其相关性。
    :return: MRR指标的值。
    """
    mrr_sum = 0
    num_queries = len(results)
    for i in range(num_queries):
        relevant_docs = [j for j in range(len(results[i])) if results[i][j][1] == 1]  # 获取所有相关文档的索引
        if len(relevant_docs) > 0:
            reciprocal_rank = 1 / (relevant_docs[0] + 1)  # 计算第一个相关文档的倒数
            mrr_sum += reciprocal_rank
    mrr = mrr_sum / num_queries  # 计算MRR指标的值
    return mrr

def calculate_map(results):
    """
    计算MAP指标。

    :param results: 包含每个查询的结果的列表，每个查询的结果是一个列表，其中包含若干文档及其相关性。
    :return: MAP指标的值。
    """
    map_sum = 0
    num_queries = len(results)
    for i in range(num_queries):
        relevant_docs = [j for j in range(len(results[i])) if results[i][j][1] == 1]  # 获取所有相关文档的索引
        precision_sum = 0
        num_relevant_docs = len(relevant_docs)
        if num_relevant_docs > 0:
            for j in range(num_relevant_docs):
                precision_sum += (j + 1) / (relevant_docs[j] + 1)  # 计算前j个相关文档的精度和
            map_sum += precision_sum / num_relevant_docs  # 计算平均精度并加入总和中
    map = map_sum / num_queries  # 计算MAP指标的值
    return map

def calculate_precision(round_list):
    precision = 0
    for i in round_list:
        coun = 0
        for j in i:
            if j[1] == 1:
                coun += 1
        precision += (coun / len(i))
    precision = precision / len(round_list)
    return precision


def calculate_recall(round_list, ground_truth):
    recall = 0
    for num, i in enumerate(round_list):
        coun = 0
        for j in i:
            if j[1] == 1:
                coun += 1
        if coun > ground_truth[num]:
            recall += 1
        else:
            recall += (coun / ground_truth[num])
    recall = recall / len(ground_truth)
    return recall

if __name__ == '__main__':
    list = []

    ground_truth = [5, 6, 6, 5, 4, 3,
                    6, 4, 3, 5, 3, 7,
                    7, 4, 5, 3, 4, 3,
                    4, 3, 4, 5, 3, 5,
                    7, 8, 4, 3, 5, 5,
                    3, 4, 5, 3, 3, 3,
                    3, 4, 3, 3, 5, 3,
                    6, 6, 3, 4, 9, 10,
                    4, 5, 3, 3, 3, 4,
                    8, 3, 3, 3, 5, 5]

    mrr = calculate_mrr(list)

    map = calculate_map(list)

    precision = calculate_precision(list)

    recall = calculate_recall(list, ground_truth)

    print("MRR: " + str(mrr))
    print("MAP: " + str(map))
    print("Precision: " + str(precision))
    print("Recall: " + str(recall))