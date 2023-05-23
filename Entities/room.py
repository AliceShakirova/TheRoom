import random

"""
0 - пустая клетка
1 - вход
2 - барельеф
"""
level_room = {1: 10, 2: 11, 3: 12, 4: 13, 5: 14, 6: 16, 7: 18, 8: 20, 9: 22, 10: 24, 11: 26, 12: 28, 13: 30, 14: 33,
              15: 36, 16: 39, 17: 42, 18: 45, 19: 48, 20: 50, 21: 50, 22: 50, 23: 50, 24: 50, 25: 50}


# Функция создает квадратную комнату
def maker_room(level):
    list_room = []
    side = list(range(level_room[level]))
    for x in side:
        list_room.append([])
        for y in side:
            list_room[x].append(0)

    return list_room


# print (maker_room (4))

# Функция заполняет комнату объектами
def fill_room(lvl):
    # Определяем, что приехало, только уровень или уже готовая комната
    if type(lvl) is int:
        list_room = maker_room(lvl)
    elif type(lvl) is list:
        list_room = lvl
    else:
        print('Что-то пошло не так')

    # Выделяем периметр, меняем 0 на 4
    side_len = (level_room[lvl])
    for x in range(side_len):
        for y in range(side_len):
            if (x in [0, 1, (side_len - 2), (side_len - 1)]
            or y in [0, 1, (side_len - 2), (side_len - 1)]):
                    list_room[x][y] = 4

    # Определяем вход, меняем 4 на 1
    room_angles = [(0, 0), (0, -1), (-1, 0), (-1, -1)]
    angle_indices = [0, 1, 2, 3]
    angle_index = random.choice(angle_indices)
    enter_point = room_angles[angle_index]
    list_room[enter_point[0]][enter_point[1]] = 1

    # return list_room
    # Создаем список кортежей
    pointlist = []
    for x in range(side_len):
        for y in range(side_len):
            pointlist.append((x, y))
    # print (pointlist)

    # Создаем вес
    weight = []
    for x in range(side_len):
        for y in range(side_len):
            if list_room[x][y] > 2:
                weight.append(85)
            elif list_room[x][y] == 1:
                weight.append(0)
            else:
                weight.append(15)
    # print (weight)

    # Выбираем три точки
    points = random.choices(pointlist, weights=weight, k=3)
    point1 = points[0]
    point2 = points[1]
    point3 = points[2]
    list_room[point1[0]][point1[1]], list_room[point2[0]][point2[1]], list_room[point3[0]][point3[1]] = 2, 2, 2

    #Подчищаем периметр
    for x in range(side_len):
        for y in range(side_len):
            if list_room[x][y] == 4:
                list_room [x][y] = 0
    return list_room


'''def get_room (room):
    n = 0
    for x in room:
        print('%002d' % n, end='')
        num = 0
        for y in x:
            print('%s' % y, end='')
            n += 1
            if num == len(x):
                print('\n')
            num += 1


'''
# Самотестирование в случае запуска напрямую
if __name__ == '__main__':
    lvl = 4
    room = fill_room(lvl)
    '''get_room(room)'''
    for x in room:
        print (x)
"""    
    n = 0
    for x in room:
        print('%002d' % n, end='')
        print(x)
        n += 1
"""