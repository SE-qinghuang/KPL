import csv

sta = 0
ty = 0
eve = 0
con = 0
pur = 0
loc = 0
dir = 0
man = 0
ext = 0
tem = 0
goa = 0
res = 0
pre_o = 0
dir_o = 0

with open("/media/dell/DATA/WZY-KG-prompt-QA/data/embedding_train.csv", 'r', encoding='utf-8') as file:
    content = csv.reader(file)
    rows = list(content)
    for row in rows:
        if row[3].lower() == "status":
            sta += 1
        elif row[3].lower() == "type":
            ty += 1
        elif row[3].lower() == "event":
            eve += 1
        elif row[3].lower() == "condition":
            con += 1
        elif row[3].lower() == "purpose":
            pur += 1
        elif row[4].lower() == "location":
            loc += 1
        elif row[4].lower() == "direction":
            dir += 1
        elif row[4].lower() == "manner":
            man += 1
        elif row[4].lower() == "extent":
            ext += 1
        elif row[4].lower() == "temporal":
            tem += 1
        elif row[4].lower() == "goal":
            goa += 1
        elif row[4].lower() == "result":
            res += 1
        elif row[4].lower() == "preposition":
            pre_o += 1
        elif row[4].lower() == "direct":
            dir_o += 1


print('status: ' + str(sta))
print('type: ' + str(ty))
print('event: ' + str(eve))
print('condition: ' + str(con))
print('purpose: ' + str(pur))
print('location: ' + str(loc))
print('direction: ' + str(dir))
print('manner: ' + str(man))
print('extent: ' + str(ext))
print('temporal: ' + str(tem))
print('goal: ' + str(goa))
print('result: ' + str(res))
print('preparation object: ' + str(pre_o))
print('direct object: ' + str(dir_o))

# with open('/media/dell/DATA/WZY-KG-prompt-QA/data/embedding_train.csv', 'r', encoding='utf-8') as file:
#     content = csv.reader(file)
#     rows = list(content)
#
# for row in rows:
#     if row[3].lower() == "constraint":
#         row[3] = "Condition"
#
# with open('/media/dell/DATA/WZY-KG-prompt-QA/data/embedding_train.csv', 'w', encoding='utf-8', newline='') as file:
#     writer = csv.writer(file)
#     writer.writerows(rows)
#
# print('done')