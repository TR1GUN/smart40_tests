def parametrize_by_element(Adding_Tags: list, ArchType_name_list: list):
    parametrize_list = []
    # Если у нас гет запрос
    template_parametrize = [
        [1, 1],
        [2, 3],
        [3, 1],
        [1, 1],
        [2, 3],
        [3, 1]
    ]
    for i in range(len(ArchType_name_list)):
        ArchType_name = [ArchType_name_list[i]]
        for x in range(len(template_parametrize)):
            for y in range(len(Adding_Tags)):
                element = [ArchType_name] + template_parametrize[x] + [Adding_Tags[y]]
                element = tuple(element)
                parametrize_list.append(element)

    return parametrize_list


adding_tag = [{
        'A-0': None, 'R+0': None, 'R-0': None, 'A+0': None,
        'A-1': None, 'R+1': None, 'A+1': None, 'R-1': None,
        'A+2': None, 'A-2': None, 'R+2': None, 'R-2': None,
        'A+3': None, 'A-3': None, 'R+3': None, 'R-3': None,
        'A+4': None, 'A-4': None, 'R+4': None, 'R-4': None,
    }, {
        'A-0': None, 'R+0': None, 'R-0': None, 'A+0': None,
        'A-1': None, 'R+1': None, 'A+1': None, 'R-1': None,
        'A+2': None, 'A-2': None, 'R+2': None, 'R-2': None,
        'A+3': None, 'A-3': None, 'R+3': None, 'R-3': None,
    }, {
        'A-0': None, 'R+0': None, 'R-0': None, 'A+0': None,
        'A-1': None, 'R+1': None, 'A+1': None, 'R-1': None,
        'A+2': None, 'A-2': None, 'R+2': None, 'R-2': None,
    }, {
        'A-0': None, 'R+0': None, 'R-0': None, 'A+0': None,
        'A-1': None, 'R+1': None, 'A+1': None, 'R-1': None,
    }, {
        'A-0': None, 'R+0': None, 'R-0': None, 'A+0': None,
    },

    ]

ArchType_name_list = ['ElMomentEnergy', 'ElDayEnergy', 'ElMonthEnergy', 'ElDayConsEnergy', 'ElMonthConsEnergy']
tag  = parametrize_by_element(Adding_Tags = adding_tag, ArchType_name_list=ArchType_name_list)

print(tag)