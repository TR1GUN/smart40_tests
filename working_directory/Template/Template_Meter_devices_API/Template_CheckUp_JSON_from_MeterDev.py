# Здесь Расположим наш Файл проверки - Это вааажно

class CheckUp:
    """
    Итак - это наш класс для сравнения , здесь сравниваем JSON ответа, с предполагаемым ответом
    """

    JSON_Normal = []
    JSON_answer = []
    Error_collector = None

    def __init__(self, JSON_Normal, JSON_answer):

        # Пункт первый - Переопределяем наши поля

        self.JSON_Normal = JSON_Normal
        self.JSON_answer = JSON_answer
        self.Error_collector = self.__checkup(JSON_Normal=self.JSON_Normal, JSON_answer=self.JSON_answer)

    def __checkup(self, JSON_Normal, JSON_answer):

        # ПУНКТ Первый - Сравниваем их по длине
        error = []

        error = self.__checkup_element_ts(JSON_Normal=JSON_Normal, JSON_answer=JSON_answer)
        # if len(JSON_Normal) == len(JSON_answer):
        #
        #     error = self.__checkup_element_ts(JSON_Normal=JSON_Normal, JSON_answer=JSON_answer)
        #
        # else:
        #     error.append({
        #         'Error': 'У JSON Разная длина: Длина ожилаеммого ответа : ' + str(len(JSON_Normal)) +
        #                  " . Длина полученного ответа : " + str(len(JSON_answer))})

        return error

    def __checkup_element_ts(self, JSON_Normal, JSON_answer):

        """
        Здесь проходимся по каждому элементу списка - где каждый элемент списка должен быть равен

        :param JSON_Normal:
        :param JSON_answer:
        :return:
        """

        error = []
        error_key = []

        # from datetime import datetime
        # for ts in  JSON_answer:
        #     print("JSON_answer",datetime.fromtimestamp(ts['time']),  ts['time'])
        #
        # print('---------------')
        # for ts in  JSON_Normal:
        #     print("JSON_Normal" ,datetime.fromtimestamp(ts['time']),  ts['time'])
        # print("JSON_answer", JSON_answer)
        # print("JSON_Normal", JSON_Normal)

        # Производим проверку на наличие таймштампа
        if (JSON_Normal[0].get('time') is not None) and (JSON_answer[0].get('time') is not None):
            # сначала сортируем все по таймштампам
            JSON_Normal = sorted(JSON_Normal, key=lambda x: x['time'])
            JSON_answer = sorted(JSON_answer, key=lambda x: x['time'])

            # Теперь опускаем в ставнимавтель
            error = self.__check_up_element()

        # иначе - У нас один элемент
        else:

            # print("JSON_answer" , JSON_answer)
            # print("JSON_Normal", JSON_Normal)
            error = self.__check_up_element_keys(answer_element=JSON_answer[0], normal_element=JSON_Normal[0])

        # for i in range(len(JSON_answer)):
        #     for keys in JSON_answer[i]:
        #
        #         # Итак - тут очень важно - славниваем все ключи
        #
        #         if JSON_answer[i].get(keys) != JSON_Normal[i].get(keys):
        #
        #             # Если это тэг 'diff' - то игнорируем его
        #             if keys != 'diff':
        #                 error_string = 'Элемент - ' + str(i) + \
        #                                ' ,\n Ключ - ' + str(keys) + \
        #                                ' ,\n Значение ключа в  JSON ответа - ' + str(JSON_answer[i].get(keys)) + \
        #                                ' ,\n Значение ключа в предполагаеммый JSON - ' + str(JSON_Normal[i].get(keys))
        #                 error.append(
        #                     {'Значения данных Ключей не равно': error_string})
        #             else:
        #                 if (JSON_answer[i].get('diff') is None) or (type(JSON_answer[i].get('diff')) != int):
        #                     error_string = 'Элемент - ' + str(i) + \
        #                                    ' ,\n Ключ - ' + str(keys) + \
        #                                    ' ,\n Значение ключа в  JSON ответа - ' + str(JSON_answer[i].get(keys)) + \
        #                                    ' ,\n Значение ключа в предполагаеммый JSON - ' + str(
        #                         JSON_Normal[i].get(keys))
        #                     error.append(
        #                         {'Значения тэга diff не корректно ': error_string})
        #
        #             # Добавляем проблемный ключ - для того чтоб не повторяться
        #             error_key.append(keys)
        #
        #     # Теперь проходимя по значениям котоыре есть в нормальном  JSON
        #     for keys in JSON_Normal[i]:
        #         if JSON_Normal[i].get(keys) != JSON_answer[i].get(keys):
        #             print('error_key', error_key)
        #             # проверяем на дубликаты - Если данный ключ не входит или это diff , то добавляем его
        #             if (str(keys) not in error_key) or (keys not in ['diff']):
        #                 error_string = 'Элемент - ' + str(i) + \
        #                                ' ,\n Ключ - ' + str(keys) + \
        #                                ' ,\n Значение ключа в  JSON ответа - ' + str(JSON_answer[i].get(keys)) + \
        #                                ' ,\n Значение ключа в предполагаеммый JSON - ' + str(JSON_Normal[i].get(keys))
        #
        #                 error.append(
        #                     {'Значения данных Ключей не равно': error_string})
        #
        # # Если у нас есть проблемы с валидацией
        # if len(error) > 0:
        #     error.append({' Ответ JSON от API ': str(JSON_answer),
        #                   ' Наш предполагаеммый JSON': str(JSON_Normal)})
        return error

    def __check_up_element(self):
        '''
        Вырываем по таймштампу , и отправляем на валидацию элемент
        :return:
        '''

        error = []
        # Сначала берем и переоопределяем наши значения в отдельные списки , которые будем удалять.
        JSON_answer_list = []
        JSON_Normal_list = []
        for i in range(len(self.JSON_answer)):
            JSON_answer_list.append(self.JSON_answer[i])

        for i in range(len(self.JSON_Normal)):
            JSON_Normal_list.append(self.JSON_Normal[i])


        # print("self.JSON_answer" , self.JSON_answer)
        # print("self.JSON_Normal", self.JSON_Normal)
        if len(self.JSON_answer) != len(self.JSON_Normal) :
            error.append({'ERROR':' ожидаемый ответ и полученный разной длины' ,
                          'Длина ожидаемого ответа': len(self.JSON_Normal),
                          'Длина полученного ответа' :len(self.JSON_answer)})

        # Теперь берем , проходимся по списку JSON ответа , и ищем в JSON ПРЕДПОЛАГАЕМОГО ОТВЕТА такой же тайм штамп
        for i in range(len(self.JSON_answer)):
            ts = self.JSON_answer[i]["time"]


            for x in range(len(self.JSON_Normal)):
                if self.JSON_Normal[x]["time"] == ts:
                    # Теперь мы нашли нужный нам таймтамп, и теперь оупскаем эти элеметы в сравниватель значений
                    result = self.__check_up_element_keys(answer_element=self.JSON_answer[i],
                                                          normal_element=self.JSON_Normal[x])

                    # Если нашли ошибки , добавляем таймштамп:
                    if len(result) > 0:
                        result = {'ERROR': 'ОШИБКА ПРИ СРАВНИВАНИИ КЛЮЧЕЙ', 'ЗНАЧЕНИЕ TIME': ts, 'ТЭГИ': result}
                        error.append(result)

            # # Теперь ищем наши значения в списке что создали, и удаляем их
            # index_list = []
            # for x in range(len(JSON_answer_list)):
            #     if JSON_answer_list[x]["time"] == ts:
            #         # Удаляем этот элемент
            #         index_list.append(x)
            # for x in range(len(index_list)):
            #     JSON_answer_list.pop(index_list[x])
            #
            # index_list = []
            # for x in range(len(JSON_Normal_list)):
            #     if JSON_Normal_list[x]["time"] == ts:
            #         # Удаляем этот элемент
            #         index_list.append(x)
            # for x in range(len(index_list)):
            #     JSON_Normal_list.pop(index_list[x])

        set_JSON_answer = set()
        for i in JSON_answer_list:
            set_JSON_answer.add(i['time'])

        set_JSON_Normal = set()
        for i in JSON_Normal_list:
            set_JSON_Normal.add(i['time'])

        # print(sorted(set_JSON_Normal))
        # print((sorted(set_JSON_answer)))
        JSON_answer_divestment_set = (set_JSON_answer - set_JSON_Normal)
        JSON_Normal_divestment_set = (set_JSON_Normal - set_JSON_answer)

        # Теперь самое главное - смотрим что за таймштампы остались
        if len(JSON_Normal_divestment_set) > 0:
            error.append({'ЕСТЬ ОТСУТСВУЮЩИЕ ЭЛМЕНТЫ В JSON ОТВЕТА': JSON_Normal_divestment_set})

        if len(JSON_answer_divestment_set) > 0:
            error.append({'ЕСТЬ ЛИШНИЕ ЭЛМЕНТЫ В JSON ОТВЕТА': JSON_answer_divestment_set})

        return error

    def __check_up_element_keys(self, answer_element: dict, normal_element: dict):
        """Сравнивание поэлементно """
        error = []
        error_keys = []
        # Сначала проверяем значения ответа
        for keys in answer_element:
            # отбрасываем ключ diff
            if keys != 'diff':
                # Теперь сравниваем значения
                answer_value = answer_element.get(keys)
                normal_value = normal_element.get(keys)

                # Теперь проверяем их равнество

                if (type(normal_value) == float) and (type(answer_value) == float):
                    epsilon = 5.96e-08
                    if abs(normal_value / answer_value - 1) > epsilon:
                        error_string = {
                                        'Неравенство значений Ключа': str(keys),
                                        'Значение ключа в  JSON ответа': answer_value,
                                        'Значение ключа в предполагаеммый JSON': normal_value
                                        }

                        # Добавляем это в ошибку , и добавляем наш ключ
                        error.append(error_string)
                        error_keys.append(keys)
                else:
                    if answer_value != normal_value:
                        error_string = {
                                        'Неравенство значений Ключа': str(keys),
                                        'Значение ключа в  JSON ответа': answer_value,
                                        'Значение ключа в предполагаеммый JSON': normal_value
                                        }
                        # Добавляем это в ошибку , и добавляем наш ключ
                        error.append(error_string)
                        error_keys.append(keys)

        for keys in normal_element:
            # отбрасываем ключ diff
            if keys != 'diff':
                if keys not in error_keys:
                    # Теперь сравниваем значения
                    answer_value = answer_element.get(keys)
                    normal_value = normal_element.get(keys)

                    # Теперь проверяем их равнество

                    if (type(normal_value) == float) or (type(answer_value) == float):
                        epsilon = 5.96e-08
                        if abs(normal_value / answer_value - 1) > epsilon:
                            error_string = {
                                            'Неравенство значений Ключа': str(keys),
                                            'Значение ключа в  JSON ответа': answer_value,
                                            'Значение ключа в предполагаеммый JSON': normal_value
                                            }

                            # Добавляем это в ошибку , и добавляем наш ключ
                            error.append(error_string)

                    else:
                        if answer_value != normal_value:
                            error_string = {
                                            'Неравенство значений Ключа': str(keys),
                                            'Значение ключа в  JSON ответа': answer_value,
                                            'Значение ключа в предполагаеммый JSON': normal_value
                                            }

                        # Добавляем это в ошибку , и добавляем наш ключ
                            error.append(error_string)
        return error
