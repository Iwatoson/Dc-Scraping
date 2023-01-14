import json

# バイト配列を作成する
bytes_data = b''

# 文字列に変換する
hex_string = bytes_data.decode('utf-8')

print(hex_string)

a = dict()
a["collor"] = "red"
with open('log.json', mode='w',encoding='utf-8') as f:
    json.dump(a,f,indent=2)

# d = dict()
# r = []
# def test():
#     for i in range(10):
#         d = dict()
#         print(d)
#         d["number"] = i
#         alpha
#         r.append(d)

# for i in test():
#     print(f"test id:{i}")

# def alpha():
#     for i in range(3):
#         d["name"] = i


# print(r)
# with open('log.json', mode='w',encoding='utf-8') as f:
#     json.dump(r,f,indent=2)