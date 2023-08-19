import openai
import logging
from tool.question_from_kg import *

openai.api_key = "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"

# def program_Generate(prompt, num_candidates=10, max_tokens=128, stop="",temperature=1):
#     response = None
#     while response is None:
#         try:
#             response = openai.Completion.create(
#                 prompt=prompt,
#                 model="text-davinci-003",
#                 max_tokens=max_tokens,
#                 stop=stop,
#                 temperature=temperature,
#                 n=num_candidates
#             )
#         except Exception as e:
#             print(type(e), e)
#             if str(type(e)) == "<class 'openai.error.InvalidRequestError'>":
#                 response = "null"
#     results = []
#     for choice in response.choices:
#         text = choice.text.strip()
#         results.append(text)
#
#     return results

def program_Generate(prompt, num_candidates=10, max_tokens=128, stop="",temperature=1):
    response = None
    while response is None:
        try:
            response = openai.ChatCompletion.create(
              model="gpt-3.5-turbo",
              messages=[
                {"role": "user", "content": prompt}
              ],
              max_tokens=max_tokens,
              stop=stop,
              temperature=temperature,
              n=num_candidates
            )
        except Exception as e:
            print(type(e), e)
            if str(type(e)) == "<class 'openai.error.InvalidRequestError'>":
                response = "null"
    results = []
    for choice in response.choices:
        text = choice.text.strip()
        results.append(text)

    return results

def get_aspect_l(task, answer, answers, aspects):
    # all_aspects = ['event', 'status', 'type', 'location', 'direction', 'manner', 'extent', 'temporal', 'goal', 'purpose', 'result', 'condition', 'preposition object', 'direct object']
    all_aspects = ['event', 'status', 'type', 'purpose', 'condition']
    # get_kg_tasks('/media/dell/DATA/WZY-KG-prompt-QA/data/task_data.csv', task)
    kg_tasks, kg_questions, kg_answers, kg_aspects = get_kg_questions('/media/dell/DATA/WZY-KG-prompt-QA/data/filter_tasks.csv', answer)
    aspect_prompt = 'The meanings of each query aspect are shown below.\n' \
                    '1. event: The action that the query requires.\n' \
                    '2. status: The status of the object that the query requires. The modifier include adjectives, verbs, quantifiers, and adverbs.\n' \
                    '3. type: The type of the object that the query requires. The noun or proper noun is the modifier.' \
                    'The modifier is java built-in data type, such as "byte", "float", "char", "boolean", "double, etc"\n' \
                    '4. purpose: Purpose contains purpose clauses, which are employed to highlight the driving forces behind specific actions. ' \
                    'The words "to," "in order to," and "so that" are used to start canonical purpose clauses.\n' \
                    '5. condition: The condition of the query.The conditional adverbial sentences that alter the query are included in condition.\n\n' \
                    '===============================================================================\n\n'
    for i in range(len(kg_aspects)):
        if i > 0:
            aspect_prompt += '\n\n'
        aspect_prompt += 'Query: ' + kg_tasks[i] + '\n' + 'Known information: <' + kg_answers[i] + '>' + \
                         '\nUpon obtaining the query and known information, what <aspect> of the query can be subject to questioning?\n' \
                         'Please choose one <aspect> from the following options.\n' \
                         'The five <aspect>: 1. event; 2. status; 3. type; 4. purpose; 5. condition.\nThe <aspect> is ' + kg_aspects[i].lower() + \
                         '\n\n==============================================================================='

    aspect_prompt += '\n\nQuery: ' + task + '\n' + 'Known information: '
    for a in answers:
        aspect_prompt += ' <' + a + '>'
    aspect_prompt += '\nUpon obtaining the query and known information, what <aspect> of the query can be subject to questioning?\n' \
                     'Please choose one <aspect> from the following options.\n' \
                     'The five <aspect>: 1. event; 2. status; 3. type; 4. purpose; 5. condition.\n' \
                       'However, please refrain from choosing ' + ' and '.join(asp for asp in aspects) + '.\nThe <aspect> is '
    aspect = program_Generate(prompt=aspect_prompt, temperature=0, max_tokens=8, num_candidates=1)
    for i in all_aspects:
        if i in aspect[0].lower():
            aspect = i
            break

    return aspect

def get_aspect_firstl(task, answer):
    # all_aspects = ['event', 'status', 'type', 'location', 'direction', 'manner', 'extent', 'temporal', 'goal', 'purpose', 'result', 'condition', 'preposition object', 'direct object']
    all_aspects = ['event', 'status', 'type', 'purpose', 'condition']
    get_kg_tasks('/media/dell/DATA/WZY-KG-prompt-QA/data/task_data.csv', task)
    kg_tasks, kg_questions, kg_answers, kg_aspects = get_kg_questions('/media/dell/DATA/WZY-KG-prompt-QA/data/filter_tasks.csv', answer)
    aspect_prompt = 'Below are the meanings of <aspect> for the query.\n' \
                    '1. event: The action that the query requires.\n' \
                    '2. status: The status of the object that the query requires. The modifier include adjectives, verbs, quantifiers, and adverbs.\n' \
                    '3. type: The type of the object that the query requires. The noun or proper noun is the modifier.' \
                    'The modifier is java built-in data type, such as "byte", "float", "char", "boolean", "double, etc"\n' \
                    '4. purpose: Purpose contains purpose clauses, which are employed to highlight the driving forces behind specific actions. ' \
                    'The words "to," "in order to," and "so that" are used to start canonical purpose clauses.\n' \
                    '5. condition: The condition of the query.The conditional adverbial sentences that alter the query are included in condition.\n\n' \
                    '===============================================================================\n\n'
    for i in range(len(kg_aspects)):
        if i > 0:
            aspect_prompt += '\n\n'
        aspect_prompt += 'Query: ' + kg_tasks[i] + '\n' + 'Known information: None' + \
                         '\nUpon obtaining the query and known information, what <aspect> of the query can be subject to questioning?\n' \
                         'Please choose one <aspect> from the following options.\n' \
                         'The five <aspect>: 1. event; 2. status; 3. type; 4. purpose; 5. condition.\nThe <aspect> is ' + kg_aspects[i].lower() + \
                         '\n\n==============================================================================='

    aspect_prompt += '\n\nQuery: ' + task + '\n' + 'Known information: None' + \
                     '\nUpon obtaining the query and known information, what <aspect> of the query can be subject to questioning?\n' \
                     'Please choose one <aspect> from the following options.\n' \
                     'The five <aspect>: 1. event; 2. status; 3. type; 4. purpose; 5. condition.\nThe <aspect> is '
    aspect = program_Generate(prompt=aspect_prompt, num_candidates=1, max_tokens=8, temperature=0)
    for i in all_aspects:
        if i in aspect[0].lower():
            aspect = i
            break

    return aspect

def setup_logger(name, log_file, level=logging.INFO):
    formatter = logging.Formatter('%(message)s')
    file_handler = logging.FileHandler(log_file)
    file_handler.setFormatter(formatter)

    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.addHandler(file_handler)

    return logger

def generate_query_expansion(query, log):
    # TODO figure out alternative stopping criterion for generating initial characters?
    aspect_definition = {'event': 'The action that the query requires.',
                         'status': 'The status of the object that the query requires. The modifier include adjectives, verbs, quantifiers, and adverbs.',
                         'type': 'The type of the object that the query requires. The noun or proper noun is the modifier. The modifier is java built-in data type, such as "byte", "float", "char", "boolean", "double, etc"',
                         'purpose': 'Purpose contains purpose clauses, which are employed to highlight the driving forces behind specific actions. The words "to," "in order to," and "so that" are used to start canonical purpose clauses.',
                         'condition': 'The condition of the query.The conditional adverbial sentences that alter the query are included in condition.'}
    answers = []
    questions = []
    log = log
    aspects = []
    known_apis = []
    old_apis = []
    new_apis = []
    text_apis = {}
    print_logger = setup_logger('print_logger', log)

    logging.basicConfig(filename=log, filemode='w', level=logging.INFO, format='%(message)s')

    print("Query: " + query)
    print_logger.info("Query: " + query)


    for i in range(5):
        if i == 0:
            aspect = get_aspect_firstl(task=query, answer='No')
            aspects.append(aspect.lower())
            # question_prompt = 'The meaning of <' + aspect + "> is " + aspect_definition[aspect] + '\n' + \
            #                   '===============================================================================\n'
            # question_prompt += 'Query: ' + query.strip()
            # aspects.append(aspect.lower())
            # question_prompt += '\nPlease ask a clarifying question for the query from <' + aspect + '> aspect.\n\n'
            question_prompt = 'In Java programming, unclear and unambiguous queries often have multiple APIs that can be implemented, ' \
                              'while clear and unambiguous queries can only be implemented by certain specific APIs. ' \
                              'So in order to be able to get specific API, clarification questions need to be asked for unclear and unambiguous queries.\n\n' + \
                              'Please ask a clarifying question for the query from <' + aspect + '> aspect.\n\n' + \
                              'The meaning of <' + aspect + "> aspect is \"" + aspect_definition[aspect]
            question_prompt += '\"\n\nQuery: ' + query.strip()
            question_prompt += '\nClarification question: '
        else:
            aspect = get_aspect_l(task=query, answer=answer, answers=answers, aspects=aspects)
            aspects.append(aspect.lower())
            # question_prompt = 'The meaning of <' + aspect + "> is " + aspect_definition[aspect] + '\n' + \
            #                   '===============================================================================\n'
            # question_prompt += 'Query: ' + query.strip()
            # question_prompt += '\nKnown information: ' + ''.join([c.strip() for c in answers])
            # aspects.append(aspect.lower())
            # question_prompt += '\nPlease ask a clarifying question for the query from <' + aspect + '> aspect based on known information.\n\n'
            question_prompt = 'In Java programming, unclear and unambiguous queries often have multiple APIs that can be implemented, ' \
                              'while clear and unambiguous queries can only be implemented by certain specific APIs. ' \
                              'So in order to be able to get specific API, clarification questions need to be asked for unclear and unambiguous queries.\n\n' + \
                              'Please ask a clarifying question for the query from <' + aspect + '> aspect based on known information.\n\n' + \
                              'The meaning of <' + aspect + "> aspect is \"" + aspect_definition[aspect]
            question_prompt += '\"\n\nQuery: ' + query.strip()
            question_prompt += '\nKnown information: ' + ''.join([c.strip() for c in answers])
            question_prompt += '\nClarification question: '

        for _ in range(2):
            question_candidates = program_Generate(prompt=question_prompt, temperature=1, max_tokens=48, num_candidates=10)

            question_candidates_prefix = []
            for q in question_candidates:
                q_list = q.split('\n')
                q_list_without_null = [n for n in q_list if n != '']
                question_candidates_prefix.append(q_list_without_null[0].strip())

            filtered_question_candidates = []

            for c in question_candidates_prefix:
                c_is_good = True
                if '?' not in c:
                    c_is_good = False
                if '1' in c:
                    c_is_good = False
                if c.lower() in [i.lower() for i in filtered_question_candidates]:
                    c_is_good = False
                if not c_is_good:
                    continue
                filtered_question_candidates.append(c)
            if len(filtered_question_candidates) > 0:
                break
        print("\n\nQuestions:")
        print_logger.info("\n\nQuestions:")
        for n in range(3):
            print(str(n + 1) + ': ' + filtered_question_candidates[n].strip())
            print_logger.info(str(n + 1) + ': ' + filtered_question_candidates[n].strip())
        print('please select question:')
        print_logger.info('please select question:')
        sn = 1
        selected_question = filtered_question_candidates[int(sn) - 1].strip()
        # selected_name = filtered_name_continuations[0].strip()
        print(selected_question + '\n')
        print_logger.info(selected_question + '\n')
        questions.append(selected_question)

        context_prompt = "Answer the question based on the setting below.\n\nSetting:" + \
                         "The query is " + query.strip() + ".\n\n" + \
                         "The meaning of <" + aspect + "> is " + aspect_definition[aspect] + ".\n\n" + \
                         "The question is a question for the query from the <" + aspect + "> aspect.\n\n" + \
                         "The answer only give one answers from the <" + aspect + "> aspect.\n\n" + \
                         "Question: " + selected_question + "\nAnswer: "
        context = program_Generate(prompt=context_prompt, temperature=0, num_candidates=1, max_tokens=2048)

        print("Answer:\n" + context[0])
        print_logger.info("Answer:\n" + context[0])
        answer = context[0]

        answers.append(answer)

        expansion_prompt = 'Query: ' + query.strip() + '\n\nThe following is Q&A information about the query:\n\n============================================\n\n'
        for q, a in zip(questions, answers):
            expansion_prompt += 'Question: ' + q + '\nAnswer: ' + a + '\n'
        # expansion_prompt += '\nPlease revise the query based on the Q&A information, keeping the response to a single declarative sentence. Do not give me interrogative question!\n\n'
        expansion_prompt += '\n============================================\n\nBased on the above Q&A information, expand the query and keep the query body semantics unchanged.\n' + \
                            ' Keeping the response to a single declarative sentence. Do not give me interrogative question!\n\n'

        expansion = program_Generate(prompt=expansion_prompt, num_candidates=1, max_tokens=256, temperature=0)
        print("\nRevised Query: " + expansion[0])
        print_logger.info("\nRevised Query: " + expansion[0])

        api_prompt = "Query: " + expansion[0] + "\nPlease recommend some API methods in Java API document based on the query, and sequence these api in the order of their relevaance to the query.\n\n" + \
                     "Pay attention!\nYou cannot change the semantics of the query.\nYou only need to give the full name of the API method, such as java.util.List.add.\n\n"

        apis1 = program_Generate(prompt=api_prompt, temperature=1, num_candidates=1, max_tokens=512, stop='')
        apis2 = apis1[0].splitlines()
        apis = []
        for api in apis2:
            if ":" in api:
                content = api.split(":")[0]
            elif "-" in api:
                content = api.split("-")[0]
            else:
                content = api
            apis.append(content)

        if i == 0:
            for a in apis:
                new_apis.append(a[2:])

            for n in new_apis:
                if n in known_apis:
                    continue
                else:
                    known_apis.append(n)

            view_apis = []
            for api in apis:
                if api[2:] in known_apis:
                    view_apis.append(api)
                else:
                    view_apis.append(api + '(new)')

            text_apis['text' + str(i + 1)] = new_apis
            old_apis = new_apis
            print("\nRecommend APIs:")
            print_logger.info("\nRecommend APIs:")
            for v in view_apis:
                print(v)
                print_logger.info(v)
        else:
            view_apis = []
            for api in apis:
                if api[2:] in known_apis:
                    view_apis.append(api)
                else:
                    view_apis.append(api + ' -- (new)')

            new_apis = []
            for a in apis:
                new_apis.append(a[2:])

            for n in new_apis:
                if n in known_apis:
                    continue
                else:
                    known_apis.append(n)

            for api in new_apis:
                if api in old_apis and api in view_apis:
                    index1 = old_apis.index(api)
                    index2 = view_apis.index(api)
                    if index1 < index2:
                        view_apis[index2] += ' -- (down)'
                    elif index2 < index1:
                        view_apis[index2] += ' -- (up)'
                    else:
                        continue
            text_apis['text' + str(i + 1)] = new_apis
            old_apis = new_apis
            print("\nRecommend APIs:")
            print_logger.info("\nRecommend APIs:")
            for v in view_apis:
                print(v)
                print_logger.info(v)

    # expansion_prompt = 'Query: ' + query.strip() + '\n\n' + 'Known information:'
    # for a in answers:
    #     expansion_prompt += '\n' + a
    # expansion_prompt += '\n\nPlease revise the query based on the known information, keeping the response to a single sentence.'

    expansion_prompt = 'Query: ' + query.strip() + '\n\nThe following is Q&A information about the query:\n\n'
    for q, a in zip(questions, answers):
        expansion_prompt += 'Question: ' + q + '\nAnswer: ' + a + '\n'
    expansion_prompt += '\nBased on the above Q&A information, expand the query and keep the query body semantics unchanged.\n\n' + \
                        ' Keeping the response to a single declarative sentence. Do not give me interrogative question!\n\n'

    expansion = program_Generate(prompt=expansion_prompt, num_candidates=1, max_tokens=256, temperature=0)

    print("end==================================")
    print_logger.info("end==================================")

    return expansion

def clarify_question(query, log):
    while True:
        try:
            if query is "":
                query = "save data."
            else:
                query = query

            query_expansion = generate_query_expansion(query=query, log=log)
        except Exception as e:
            import traceback
            traceback.print_exc()
        break

    print("end=========")

    return query_expansion