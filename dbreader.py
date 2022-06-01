import csv
from main import NeuroNet
import numpy as np

words = set()
keys = 'не да конечно ага абсолютно определенно но пока'.split(' ')
vals = {'не': -1, 'да': 1, 'конечно': 1, 'абсолютно': 0.5, 'определенно': 0.5, 'ага': 1, 'но': -0.5, 'пока': -0.5}

data = np.array([
    [1, -1, 0],  # да нет
    [0, 1, 0],  # наверно да
    [1, -1, 0],  # конечно нет
    [0.5, -1, 0],  # точно нет
    [1, 0.5, 0],  # да определенно
    [0, 1, 0],  # ну да
    [0, -1, 0],  # ну нет
    [1, 0.5, 0],  # да определенно
    [1, -1, 0.5],  # да нет наверно
    [1, 0.5, -1],  # да точно нет
    [0.5, 0.5, -1],  # наверно точно нет
    [0, 0, 0], #
    [-1, 0, 0],  # отрицательный 1
    [-1, 0.5, 0], # полуопределенный отрицательный
    [0, -1, 0], # оттрицательны 2
    [0, 0, -1],  # оттрицательны 3
    [-1, 1, 0], # не да ...
    [0, 0, 0], # полностью неопределенный ответ
    [1, 0, 0], # да .. ..
    [-1, 0.5, 1],  # нет абсолютно да
    [1, 1, -1], # ага да не (надо)
    [0.5, -1, 1],
    [-0.5, -1, 0], # пока/но нет
    [-1, 1, 1], # спутанные ответ с да/нет, но не обращаясь к телефону
    [1, -1, 1], # ага да не (надо)
])

all_y_trues = np.array([
    0,  # да нет
    1,  # наверно да
    0,  # конечно нет
    0,  # точно нет
    1,  # да определенно
    1,  # ну да
    0,  # ну нет
    1,  # да определенно
    0,  # да нет наверно
    0,  # да точно нет
    0,  # наверно точно нет
    0.5, # неопределенный ответ
    0, # отрицательный 1
    0, # полуопределенный отрицательный
    0,  # оттрицательны2
    0, # оттрицательны 3
    0, # не да ...
    0.5, # полностью неопределенный ответ,
    1,
    0, # нет абсолютно да
    0,
    0,
    0, # пока/но нет
    0,
    0
])

network = NeuroNet()
network.train(data, all_y_trues)

res = set()

with open('ans.csv', 'r', encoding='UTF-8') as file:
    thelines = csv.reader(file, delimiter=' ', quotechar='|')
    for i in thelines:
        orig = i[:]
        line1 = (set(filter(lambda x: x in keys, map(lambda x: x.lower().replace('"', '').replace("'", '').replace('у', '').replace('нет', 'не'), i))))
        line = list(map(lambda x: vals[x], line1))
        line += [0 for _ in range(3 - len(line))]
        if len(line) > 3 and -2 in line:
            line = [-0.5, -1, 0]
        my_val = network.feedforward(line)

        if my_val > 0.1 and line != [-1, 0, 0] or line == [-2, -1, 0]:
            print(f'{my_val}: {line}, {line1}, {i}, {orig}')
            res.add(my_val)


print(res)