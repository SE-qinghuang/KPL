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

def setup_logger(name, log_file, level=logging.INFO):
    formatter = logging.Formatter('%(message)s')
    file_handler = logging.FileHandler(log_file)
    file_handler.setFormatter(formatter)

    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.addHandler(file_handler)

    return logger

def generate_query_expansion(query):
    # TODO figure out alternative stopping criterion for generating initial characters?
    answers = []
    questions = []
    log = log
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
            question_prompt = 'A user is interacting with a large language model.They are crafting prompts and giving them to the LLM in order to get the model to complete a task or generate output.\n\n' + \
                              'In Java programming, unclear and ambiguous queries often have multiple APIs that can be implemented, while clear and unambiguous queries can usually be implemented by specific APIs. To get the appropriate API, a series of clarification questions need to be asked for unclear and ambiguous queries.\n\n' + \
                              'As an expert in the Java API domain, you will guide users through their requirements by asking one clarifying question at a time based on the user\'s response.\n\n' + \
                              'Please ask a clarifying question for the query based on known information.'
            question_prompt += '\"\n\nQuery: ' + query.strip()
            question_prompt += '\nClarification question: '
        else:
            question_prompt = 'A user is interacting with a large language model.They are crafting prompts and giving them to the LLM in order to get the model to complete a task or generate output.\n\n' + \
                              'In Java programming, unclear and ambiguous queries often have multiple APIs that can be implemented, while clear and unambiguous queries can usually be implemented by specific APIs. To get the appropriate API, a series of clarification questions need to be asked for unclear and ambiguous queries.\n\n' + \
                              'As an expert in the Java API domain, you will guide users through their requirements by asking one clarifying question at a time based on the user\'s response.\n\n' + \
                              'Please ask a clarifying question for the query based on known information.'
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
        # for n in range(len(filtered_question_candidates)):
        #     print(str(n + 1) + ': ' + filtered_question_candidates[n].strip())
        print("\n\nQuestions:")
        print_logger.info("\n\nQuestions:")
        for n in range(3):
            print(str(n + 1) + ': ' + filtered_question_candidates[n].strip())
        print('please select question:')
        print_logger.info('please select question:')
        sn = input()
        if int(sn) > 3:
            print("Please re-enter your choice(in the numbers given):")
            print_logger.info("Please re-enter your choice(in the numbers given):")
            sn = input()
        elif int(sn) < 1:
            print("Please re-enter your choice(in the numbers given):")
            print_logger.info("Please re-enter your choice(in the numbers given):")
            sn = input()
        selected_question = filtered_question_candidates[int(sn) - 1].strip()
        # selected_name = filtered_name_continuations[0].strip()
        print(selected_question + '\n')
        print_logger.info(selected_question + '\n')
        questions.append(selected_question)

        context_prompt = "Answer the question based on the setting below.\n\nSetting:" + \
                         "The query is " + query.strip() + ".\n\n" + \
                         "The question is a question for the query.\n\n" + \
                         "The answer should give multiple possible answers, and sequence these answers in the order of their relevance to the query.\n\n" + \
                         "Question: " + selected_question + "\nAnswer: "
        context = program_Generate(prompt=context_prompt, temperature=0, num_candidates=1, max_tokens=2048)

        print("Help information:\n" + context[0])
        print_logger.info("Help information:\n" + context[0])

        print('\nplease input answer:')
        print_logger.info('\nplease input answer:')
        answer = input()
        print("Answer: " + answer)
        print_logger.info("Answer: " + answer)

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
                     "Pay attention! You cannot change the semantics of the query.\n\n"

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
            for a in apis[0].strip().split('\n'):
                new_apis.append(a[2:])

            for n in new_apis:
                if n in known_apis:
                    continue
                else:
                    known_apis.append(n)

            view_apis = []
            for api in apis[0].strip().split('\n'):
                if api[2:] in known_apis:
                    view_apis.append(api)
                else:
                    view_apis.append(api + '(new)')

            text_apis['text' + str(i + 1)] = new_apis
            old_apis = new_apis
            print("Recommend APIs:")
            print_logger.info("Recommend APIs:")
            for v in view_apis:
                print(v)
                print_logger.info(v)
        else:
            view_apis = []
            for api in apis[0].strip().split('\n'):
                if api[2:] in known_apis:
                    view_apis.append(api)
                else:
                    view_apis.append(api + ' -- (new)')

            new_apis = []
            for a in apis[0].strip().split('\n'):
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
            print("Recommend APIs:")
            print_logger.info("Recommend APIs:")
            for v in view_apis:
                print(v)
                print_logger.info(v)
        # n = 1
        # for a in apis:
        #     print(str(n) + ". " + a)
        #     n = n + 1

        end = input("\nDo you want to continue the conversation?(y/n): ")
        if end == "n":
            end = False
        else:
            end = True
        if not end:
            break

    expansion_prompt_end = 'Query: ' + query.strip() + '\n\n' + 'Known information:'
    for a in answers:
        expansion_prompt_end += '\n' + a
    expansion_prompt_end += '\n\nPlease revise the query based on the known information, keeping the response to a single sentence.'

    # expansion_prompt = 'Query: ' + query.strip() + '\n\n'
    # for q, a in zip(questions, answers):
    #     expansion_prompt += 'Q: ' + q + '\nA: ' + a + '\n'
    # expansion_prompt += '\nPlease revise the query based on the Q&A information, keeping the response to a single declarative sentence.\n\n'

    expansion_end = program_Generate(prompt=expansion_prompt_end, num_candidates=1, max_tokens=256, temperature=0)

    print("end==================================")
    print_logger.info("end==================================")

    return expansion_end

# query_expansion = ''

def clarify_question(query):
    # global query_expansion
    while True:
        try:
            if query is "":
                query = "save data."
            else:
                query = query

            query_expansion = generate_query_expansion(query=query)
        except Exception as e:
            import traceback
            traceback.print_exc()
        break

    print("end=========")

    return query_expansion