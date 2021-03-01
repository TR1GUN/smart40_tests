# Расположим тут список всяких типов запроса к прибору учёта , которых нет в archtypes

# Текущее показание времени прибора учета

GetTime_list = \
    [
        'GetTime',
        'PlsGetTime',
        'ElGetTime',
        'DigGetTime'
    ]

# Установка времени прибора учета

SetTime_list = \
    [
        'SetTime',
        'PlsSetTime',
        'ElSetTime',
        'DigSetTime'
    ]

# Синхрв онизация времени прибора учета

SyncTime_list = \
    [
        'SyncTime',
        'PlsSyncTime',
        'ElSyncTime',
        'DigSyncTime'
    ]

# Запрос состояний реле прибора учета

GetRelay_list = \
    [
        'GetRelay',
        'PlsGetRelay',
        'ElGetRelay',
        'DigGetRelay',
    ]

# Установка состояний реле прибора учета

SetRelay_list = \
    [
        'SetRelay',
        'PlsSetRelay',
        'ElSetRelay',
        'DigSetRelay'
    ]

# Запрос серийного номера

GetSerial_list = \
    [
        'GetSerial',
        'PlsSerial',
        'ElSerial',
        'DigSerial'
    ]

Journal_dict = \
    {
        'ElJrnlPwr': 1,
        'ElJrnlTimeCorr': 2,
        'ElJrnlReset': 3,
        'ElJrnlTrfCorr': 6,
        'ElJrnlOpen': 7,
        'ElJrnlUnAyth': 8,
        'ElJrnlPwrA': 9,
        'ElJrnlPwrB': 10,
        'ElJrnlPwrC': 11,
        'ElJrnlLimUAMax': 20,
        'ElJrnlLimUAMin': 21,
        'ElJrnlLimUBMax': 22,
        'ElJrnlLimUBMin': 23,
        'ElJrnlLimUCMax': 24,
        'ElJrnlLimUCMin': 25
    }


JournalValues_list = \
    [
    'ElJrnlPwr',
    'ElJrnlTimeCorr',
    'ElJrnlReset',
    'ElJrnlTrfCorr',
    # 'ElJrnlOpen',
    'ElJrnlUnAyth',
    'ElJrnlPwrA',
    'ElJrnlPwrB',
    'ElJrnlPwrC',
    'ElJrnlLimUAMax',
    'ElJrnlLimUAMin',
    'ElJrnlLimUBMax',
    'ElJrnlLimUBMin',
    'ElJrnlLimUCMax',
    'ElJrnlLimUCMin'
        ]