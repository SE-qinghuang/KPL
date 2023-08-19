import pandas as pd
from  transformers import RobertaTokenizer, RobertaModel
import torch
import os
from tqdm import tqdm
import torch.nn.functional as F
import bisect
import csv
from datapath import *
# tokenizer = RobertaTokenizer.from_pretrained('roberta-large')
# model = RobertaModel.from_pretrained('roberta-large')
# text = "do you love me?"
# encoded_input = tokenizer(text, padding="max_length", truncation=True, return_tensors='pt')
# output = model(**encoded_input)
# embedding =  output.pooler_output.detach().numpy().tolist()[0]
# tensor_embedding = torch.tensor([embedding])

def get_kg_tasks(trainingFileName, testPrompt):
    Tag = os.path.exists(general_DIR + "embedding_train.csv")
    if not Tag:
        EmbeddingFileName = embedding(trainingFileName)

    else:
        EmbeddingFileName = os.path.join(general_DIR, "embedding_train.csv")

    #获得testPrompt的向量表示
    tokenizer = RobertaTokenizer.from_pretrained("roberta-large")
    model = RobertaModel.from_pretrained('roberta-large')
    encoded_input = tokenizer(testPrompt, padding="max_length", truncation=True, return_tensors='pt')
    output = model(**encoded_input)
    embedding_testPrompt = output.pooler_output.detach().numpy().tolist()[0]

    #开始计算testPrompt与训练集中各个向量的距离，这里采用余弦相似度，最终生成一个文件，其中包含了top-64 and testPrompt
    # ids = []
    tasks = []
    answers = []
    questions = []
    aspects = []
    embeddings_task = []
    embeddings_answer = []
    distances = []
    # ids.append(["0"])
    # tasks.append(testPrompt)
    # questions.append(["no"])
    # answers.append(["no"])
    # aspects.append(["no"])
    # embeddings_task.append(embedding_testPrompt)
    # embeddings_answer.append(["no"])
    # distances.append(1)
    answers_embedding = pd.read_csv(EmbeddingFileName)
    content = answers_embedding.values.tolist()
    testPrompt_tensor = torch.FloatTensor(embedding_testPrompt)
    for items in content:
        task_embedding = items[4].strip("[")
        task_embedding = task_embedding.strip("]")
        task_embedding = task_embedding.split(",")
        answer_embedding = items[5].strip("[")
        answer_embedding = answer_embedding.strip("]")
        answer_embedding = answer_embedding.split(",")
        for i in range(0,len(task_embedding)):
            task_embedding[i] = float(task_embedding[i])
            answer_embedding[i] = float(answer_embedding[i])
        task_tensor = torch.FloatTensor(task_embedding)
        cosin_similarity = F.cosine_similarity(testPrompt_tensor, task_tensor,dim=0)
        cosin_similarity = cosin_similarity.item()
        index = bisect.bisect(distances,cosin_similarity)
        # ids.insert(index, items[0])
        tasks.insert(index, items[0])
        questions.insert(index, items[1])
        answers.insert(index, items[2])
        aspects.insert(index, items[3])
        embeddings_task.insert(index, task_embedding)
        embeddings_answer.insert(index, answer_embedding)
        distances.insert(index, cosin_similarity)
    length = len(questions)
    # ids = ids[length-1000:length+1]
    tasks = tasks[length-1000:length+1]
    questions = questions[length-1000:length+1]
    answers = answers[length-1000:length+1]
    aspects = aspects[length-1000:length+1]
    embeddings_task = embeddings_task[length-1000:length+1]
    embeddings_answer = embeddings_answer[length-1000:length+1]
    distances = distances[length-1000:length+1]
    dataFrame = pd.DataFrame({"tasks": tasks, "questions": questions, "answers": answers, "aspects": aspects , "embeddings_task": embeddings_task, "embeddings_answer": embeddings_answer, "distances": distances})
    dataFrame.to_csv(general_DIR + "filter_tasks.csv", mode="w", index=False, header=False)
    all_aspects = ['event', 'status', 'type', 'purpose', 'condition']
    # with open(general_DIR + "filter_tasks.csv", 'r', encoding='utf-8') as file:
    #     content = csv.reader(file)
    #     rows = list(content)
    #     rows.reverse()
    #     filter_tasks = []
    #     filter_questions = []
    #     filter_answers = []
    #     filter_aspects = []
    #     for row in rows:
    #         if row[3].lower() in all_aspects:
    #             all_aspects.remove(row[3].lower())
    #             filter_tasks.append(row[0])
    #             filter_questions.append(row[1])
    #             filter_answers.append(row[2])
    #             filter_aspects.append(row[3])
    #         if all_aspects is None:
    #             break
    #
    # return filter_tasks, filter_questions, filter_answers, filter_aspects

    # with open("/media/dell/DATA/WZY-KG-prompt-QA/data/testPrompt_results.csv", 'r', encoding='utf-8') as file:
    #     content = csv.reader(file)
    #     rows = list(content)
    #     filter_tasks = [row[0] for row in rows[-4:-1]]
    #     filter_questions = [row[1] for row in rows[-4:-1]]
    #     filter_answers = [row[2] for row in rows[-4:-1]]
    #     filter_aspects = [row[3] for row in rows[-4:-1]]
    #
    # return filter_tasks, filter_questions, filter_answers, filter_aspects

def get_kg_questions(trainingFileName, testPrompt):
    Tag = os.path.exists(general_DIR + "filter_tasks.csv")
    if not Tag:
        EmbeddingFileName = embedding(trainingFileName)

    else:
        EmbeddingFileName = os.path.join(general_DIR, "filter_tasks.csv")

    #获得testPrompt的向量表示
    tokenizer = RobertaTokenizer.from_pretrained("roberta-large")
    model = RobertaModel.from_pretrained('roberta-large')
    encoded_input = tokenizer(testPrompt, padding="max_length", truncation=True, return_tensors='pt')
    output = model(**encoded_input)
    embedding_testPrompt = output.pooler_output.detach().numpy().tolist()[0]

    #开始计算testPrompt与训练集中各个向量的距离，这里采用余弦相似度，最终生成一个文件，其中包含了top-64 and testPrompt
    # ids = []
    tasks = []
    answers = []
    questions = []
    aspects = []
    embeddings_task = []
    embeddings_answer = []
    distances = []
    # ids.append(["0"])
    tasks.append(["no"])
    questions.append(["no"])
    answers.append(testPrompt)
    aspects.append(["no"])
    embeddings_task.append(["no"])
    embeddings_answer.append(embedding_testPrompt)
    distances.append(1)
    answers_embedding = pd.read_csv(EmbeddingFileName)
    content = answers_embedding.values.tolist()
    testPrompt_tensor = torch.FloatTensor(embedding_testPrompt)
    for items in content:
        task_embedding = items[4].strip("[")
        task_embedding = task_embedding.strip("]")
        task_embedding = task_embedding.split(",")
        answer_embedding = items[5].strip("[")
        answer_embedding = answer_embedding.strip("]")
        answer_embedding = answer_embedding.split(",")
        for i in range(0, len(task_embedding)):
            task_embedding[i] = float(task_embedding[i])
            answer_embedding[i] = float(answer_embedding[i])
        answer_tensor = torch.FloatTensor(answer_embedding)
        cosin_similarity = F.cosine_similarity(testPrompt_tensor, answer_tensor, dim=0)
        cosin_similarity = cosin_similarity.item()
        index = bisect.bisect(distances, cosin_similarity)
        # ids.insert(index, items[0])
        tasks.insert(index, items[0])
        questions.insert(index, items[1])
        answers.insert(index, items[2])
        aspects.insert(index, items[3])
        embeddings_task.insert(index, task_embedding)
        embeddings_answer.insert(index, answer_embedding)
        distances.insert(index, cosin_similarity)
    length = len(questions)
    # ids = ids[length-1000:length+1]
    tasks = tasks[length - 1000:length + 1]
    questions = questions[length - 1000:length + 1]
    answers = answers[length - 1000:length + 1]
    aspects = aspects[length - 1000:length + 1]
    embeddings_task = embeddings_task[length - 1000:length + 1]
    embeddings_answer = embeddings_answer[length - 1000:length + 1]
    distances = distances[length - 1000:length + 1]
    dataFrame = pd.DataFrame({"tasks": tasks, "questions": questions, "answers": answers, "aspects": aspects,
                              "embeddings_task": embeddings_task, "embeddings_answer": embeddings_answer,
                              "distances": distances})
    dataFrame.to_csv(general_DIR + "filter_answer.csv", mode="w", index=False, header=False)
    all_aspects = ['event', 'status', 'type', 'purpose', 'condition']
    with open(general_DIR + "filter_answer.csv", 'r', encoding='utf-8') as file:
        content = csv.reader(file)
        rows = list(content)
        rows.reverse()
        filter_tasks = []
        filter_questions = []
        filter_answers = []
        filter_aspects = []
        for row in rows:
            if row[3].lower() in all_aspects:
                all_aspects.remove(row[3].lower())
                filter_tasks.append(row[0])
                filter_questions.append(row[1])
                filter_answers.append(row[2])
                filter_aspects.append(row[3])
            if all_aspects is None:
                break

    return filter_tasks, filter_questions, filter_answers, filter_aspects

def embedding(trainingFileName):
    train_questions = pd.read_csv(trainingFileName)
    content = train_questions.values.tolist()

    #将训练中的所有问题都变成向量并加以存储
    tokenizer = RobertaTokenizer.from_pretrained('roberta-large')
    model = RobertaModel.from_pretrained('roberta-large')
    tasks = []
    answers = []
    questions = []
    aspects = []
    embeddings_task = []
    embeddings_answer = []
    all_aspect = ['event', 'status', 'type', 'constraint', 'purpose']
    for items in tqdm(content):
        if items[4].lower() not in all_aspect:
            continue
        tasks.append(items[1])
        questions.append(items[2])
        answers.append(items[3])
        aspects.append(items[4])
        encoded_input1 = tokenizer(items[1], padding="max_length", truncation=True, return_tensors='pt')
        output1 = model(**encoded_input1)
        vec1 = output1.pooler_output.detach().numpy().tolist()[0]
        embeddings_task.append(vec1)
        encoded_input2 = tokenizer(items[3], padding="max_length", truncation=True, return_tensors='pt')
        output2 = model(**encoded_input2)
        vec2 = output2.pooler_output.detach().numpy().tolist()[0]
        embeddings_answer.append(vec2)
    dataframe = pd.DataFrame({"tasks": tasks, "questions": questions, "answers": answers, "aspects": aspects, "embedding_task": embeddings_task, "embedding_answer": embeddings_answer})
    dataframe.to_csv(general_DIR + "embedding_train.csv", mode="a", index=False, header=False)
    EmbeddingFileName = os.path.join(general_DIR, "embedding_train.csv")
    return EmbeddingFileName



if __name__ == '__main__':
    testPrompt = "store data"
    get_kg_tasks(general_DIR + 'task_data.csv', testPrompt)
    get_kg_questions(general_DIR + 'filter_tasks.csv', testPrompt)