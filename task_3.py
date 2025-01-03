def files_set(files_list):
    files_dict = {}
    for i in files_list:
        with open(i, encoding='UTF-8') as file:
            a = len(file.readlines())
            if a not in files_dict:
                files_dict[a] = [i]
            else:
                files_dict[a].append(i)
    lines_cnt_list = sorted(list(files_dict.keys()), reverse=True)
    return files_dict, lines_cnt_list
    
    
with open('new_file.txt', 'at', encoding='UTF-8') as file_2:
        for i in files_set(['1.txt', '2.txt'])[1]:
            for j in files_set(['1.txt', '2.txt'])[0][i]:
                 with open(j, encoding='UTF-8') as x:
                      file_2.write(f'{j}\n')
                      file_2.write(f'{str(i)}\n')
                      file_2.write(f'{x.read()}\n')
                      


