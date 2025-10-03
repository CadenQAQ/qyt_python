list1 = ['aaa', 111, (4, 5), 2.01]
list2 = ['bbb', 333, 111, 3.14, (4, 5)]

def find_word(list1, list2):
    list_common = []
    list_1only = []
    list_2only = []
    # 找 list1 里有的
    for word in list1:
        if word in list2:
            list_common.append(word)
        else:
            list_1only.append(word)

    # # 找 list2 独有的
    # for word in list2:
    #     if word not in list1:
    #         list_2only.append(word)

    for item in list_1only:
        print(f"{item} only in List1")
    for item in list_common:
        print(f"{item} in List1 and List2")
    # for item in list_2only:
    #     print(f"{item} only in List2")

find_word(list1, list2)