import openai
import sys
from CQ.clarify_ai_aspect_people import *

if __name__=='__main__':
    # query = "return stream from generator in Java."
    print("Please input your query: ")
    query = input()

    log = 'log/log_ai_aspect_people/ai_aspect_people_log.txt'
    # log_out = 'log_ai_aspect_people/ai_aspect_people_log_out_29.txt'
    log_out = 'log/log_ai_aspect_people/test.txt'

    query_expansion = clarify_question(query, log)

    with open(log, 'r') as input_file, open(log_out, 'w') as output_file:
        for line in input_file:
            # 去除每一行开头的 "message=" 字符串
            if line.startswith('message='):
                line = ''
            if line.startswith('Retrying'):
                line = ''
            # 写入处理后的行到输出文件
            output_file.write(line)