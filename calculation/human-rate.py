# 假设每个方面的得分都在0到5之间，这些方面的权重在0到1之间。
# 假设得分数据保存在一个字典对象scores中，权重保存在一个字典对象weights中。
# 计算总分。
scores = {"Intelligibility": 5,
           "Diversity": 4,
           "Relevance": 5,
           "Trustworthiness": 5,
           "Language fluency": 5,
           "Practicality": 5}
weights = {"Intelligibility": 0.15,
           "Diversity": 0.15,
           "Relevance": 0.2,
           "Trustworthiness": 0.2,
           "Language fluency": 0.15,
           "Practicality": 0.15}

total_score = 0
for key, value in scores.items():
    total_score += value * weights[key]

# 打印总分。
print('Total Score: ' + str(total_score))
