import os
print('方案二')
print('文件中包含"qytang"关键字的文件为')
for root,dirs,files in os.walk(os.getcwd(),topdown=False):
    for filename in files:
        filepath = os.path.join(root, filename)

        try:
            # 尝试读取文件内容
            with open(filepath, 'r', encoding='utf-8') as f:

                if 'qytang' in f.read():
                    print(f'{filename} ')
        except:
            # 跳过无法读取的文件
            pass