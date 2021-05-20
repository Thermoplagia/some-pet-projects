## В РАЗРАБОТКЕ!
yr_st_in = int(input('Введите год начала отсчёта (любое целое число): '))
ae_in = int(input('Введите максимальный возраст иссл-я популяции, аналогично: '))
capita_in = int(input('Введите стартовое население на год начала отсчёта: '))
gdp_per_in = int(input('Введите ВВП на душу населения: '))
gdp_gr_in = float(input('Введите ежегодный рост ВВП. Для примера, 1% = 0.01: '))
mil_pr_in = float(input('Введите долю военных расходов в ВВП. Для примера, 1% = 0.01: '))
act_add_in = input('Активировать дополнительную настройку? Y/N: ')
if act_add_in == 'N':
    pass
elif act_add_in == 'Y':
    print('Извините, данная функция пока недоступна. Ожидайте новых обновлений!')
print('')
print('')
print('Идёт расчёт, ожидайте...')
print('--------------------------------------------------------------')
print('')
# -------------------------------------------------------------------------
# Опции:

# Год начала отсчёта, принимаются любые целые числа:
YEAR_START = yr_st_in
# До какого возраста исследовать популяцию:
AGE_END = ae_in

# Переменные геометрической прогрессии роста населения:
# Численность населения в год начала отсчёта:
POPULATION = capita_in
# Уровень рождаемости (например: 0.03 значит 3%
# или 30 новорожденных на 1000 населения в год):
FERTILITY_RATE = 0.03
# Уровень смертности, аналогично:
MORTALITY_RATE = 0.011

# Переменные для расчёта военной экономики:
# ВВП на душу населения:
gdp_RATE = gdp_per_in
# Годовой рост ВВП (без инфляции):
gdp_GROWTH = gdp_gr_in
# Доля военного бюджета в ВВП страны.
gdp_ARMY = mil_pr_in

# Коэффициент a:
COMPONENT_A = 0.003
# Коэффициент b:
COEFFICIENT_B = 0.000350
# Коэффициент c:
COEFFICIENT_C = 1.08

# Распределение полов.
MALE_NAME = 'Мужчины'
MALE_perc = 0.5
FEMALE_NAME = 'Женщины'
FEMALE_perc = 0.5

# Армия (или профессия):
# Процент рекрутов: 0.25 — отборные; 0.25-0.5 — середнячки;
prof_perc = 0.15
# Профессиональный риск, изменение компонента Мейкхама:
# (0.01 = 1% риск смерти каждый год)
prof_hazard = 0.01
# Призывники обоих полов? 0 - нет; 1 - да
prof_male_switch = 1
prof_female_switch = 0
# Возраст призыва:
prof_age_new = 18
# Возраст перехода в резервисты:
prof_age_mid_age = 20
# Возраст отставки:
prof_age_retiree = 35
prof_name_new = 'Призывники'
prof_name_mid_age = 'Резервисты'
prof_name_retiree = 'Отставники'

# -------------------------------------------------------------------------
# Список видов войск. Используется базой данных военной техники,
# Смотри параметр 'mil_trps_type'.

dict_trps_types = {
    # Формат:
    # 'Вид_войск':процент,
    # Военно-промышленный комплекс (боеприпасы):
    'ВПК': 0,
    # Сухопутные войска:
    'СВ': 0.5,
    # Ракетные войска и дальняя ПВО:
    'РВ': 0.1,
    # Военно-воздушные войска:
    'ВВС': 0.15,
    # Военно-морской флот:
    'ВМФ': 0.1,
    # Инженерные войска:
    'ИВ': 0.15,
}

# -------------------------------------------------------------------------
# База данных оружия. Двумерный массив.

# Дополняется блоками, без ограничений и очень легко. Пользуйтесь этим.
# Пожалуйста, пишите в строке 'mil_name_comment' краткое описание оружия,
# а в строке 'mil_cost_currency' точно указывайте валюту и год.

# Создаётся объединённый словарь — строки массива.
meta_dict_mil = {}

# Выбирается первый из ключей — номер столбца.
dict_mil_key = 0
dict_mil = {
    # Заполняйте!
}
# Данные записываются в общий словарь, как столбец двумерного массива.
meta_dict_mil[dict_mil_key] = dict_mil

# Пример - для более удобного заполнения.
dict_mil = {
    'mil_name': '',
    'mil_name_comment': '',
    # Принадлежность к виду войск:
    'mil_trps_type': '',
    # Стоимость в валюте
    'mil_cost': 0,
    'mil_cost_currency': '',
    # Стоимость технического обслуживания в год, доля от стоимости машины:
    'mil_maint': 0.01,
    # Доля затрат на данный вид оружия в военном бюджете:
    'mil_budget': 0.006,
    'mil_name_new': ' новая',
    'mil_name_mid': ' устаревш.',
    'mil_name_old': ' под списание',
    # Возраст потрёпанности:
    'mil_age_mid': 10,
    # Возраст старости:
    'mil_age_old': 20,
    # Строка 'mil_a': 0.03 значит 3% вероятность потери в год.
    'mil_a': 0.03,
    'mil_b': 0.0002,
    'mil_c': 1.4,
    # Вооружение техники №1:
    'mil_ammo_1_name': '',
    # Один боекомплект:
    'mil_ammo_1_capacity': 0,
    # Максимум расхода боеприпасов в год:
    'mil_ammo_1_expense': 0,
    # Топливо/источник энергии:
    'mil_fuel_name': '',
    # Разовый запас топлива/энергии:
    'mil_fuel_capacity': 0,
    # Расход топлива на км:
    'mil_fuel_consumption': 0,
    # Годовой расход топлива:
    'mil_fuel_expense': 0,
}

# -------------------------------------------------------------------------
# Внутренние переменные.

# Создаём рабочие переменные на основе данных из опций:
year_real = YEAR_START
age_real = AGE_END
pop = POPULATION
fert = FERTILITY_RATE
mort = MORTALITY_RATE
a = COMPONENT_A
b = COEFFICIENT_B
c = COEFFICIENT_C


# -------------------------------------------------------------------------
# Функции, подпрограммы. Последующие вызывают предыдущие.

def population_size(year):
    """Вычисляем численность популяции.
    Рост популяции, это геометрическая прогрессия, например:
    100000*1.002^(100-1)=121872
    Начальная численность, годовой прирост, период в сто лет.
    Функция вычисляет исходную численность, зная конечную:
    121872*1.002^(1-100)=100000
    """
    population = POPULATION * ((FERTILITY_RATE - MORTALITY_RATE + 1) ** (-year))
    # Округляем число
    population = round(population)
    return population


def gen_size(year, perc):
    """Определяем численность поколения.
    Поколение, это процент от популяции, например, если рождаемость 0.02:
    121872*1.002^(1-100)*0.02=2000 (2% новорожденных в популяции)
    Точно так же можно определить число умерших, прирост населения, состав:
    121872*1.002^(1-100)*0.02*0.5=1000 (50% новорожденных мужского пола)
    """
    gen = round(population_size(year) * perc)
    return gen


def gdp_size(year):
    """ВВП страны в определённый год.
    Рост благосостояния, это та же геометрическая прогрессия:
    10000*1.03^(1-100)=536
    В данном случае от 536$ за столетие ВВП вырос до 10 000$
    """
    gdp_in_year = gdp_RATE * ((gdp_GROWTH + 1) ** (-year)) * population_size(year)
    gdp_in_year = round(gdp_in_year)
    return gdp_in_year


def gompertz_distribution(a, b, c, age):
    """Распределение Гомпертца. Риск смерти в зависимости от возраста.
    Распределение Гомпертца-Мейкхама неплохо работает в
    демографических расчётах для самых разных популяций.
    Единственный недостаток — оно склонно занижать
    смертность в начале и завышать в конце (экспонента, что поделать).
    Для популяции людей даёт хорошие результаты в диапазоне — 30-70 лет.
    Формула: p=a+b*(c^x)
    Где:
    p — вероятность смерти в процентах
    a — независимый от возраста риск (0.002%)
    b — коэффициент 2 (0.000350)
    c — коэффициент 3 (1.08)
    x — возраст в годах
    Коэффициенты подобраны с учётом исследования:
    "Parametric models for life insurance mortality data: gompertz's law over time".
    """
    chance_of_dying = a + b * (c ** age)
    # Проверка. Если получилось больше 1, значит 100% смерть.
    if (chance_of_dying > 1):
        chance_of_dying = 1
    return chance_of_dying


def gen_alive(gen, a, b, c, age_real):
    """Число живых в поколении.
    Каждый год умирает некий процент из поколения.
    Этот цикл вычисляет точное число живых в определённый год.
    """
    # Задаём рабочую переменную для цикла:
    age = 0
    # Из численности поколения вычитаем число погибших в первый год:
    gen_survivors = gen - \
                           gen * \
                           gompertz_distribution(a, b, c, age)
    # Далее это вычитание продолжается циклично.
    while age <= age_real:
        age = age + 1
        gen_survivors = gen_survivors - \
                               gen_survivors * \
                               gompertz_distribution(a, b, c, age)
        # Проверка. Если число выживших уходит в минус, значит все мертвы.
        if (gen_survivors <= 0):
            gen_survivors = 0
            break
    # Округляем число
    gen_survivors = round(gen_survivors)
    return gen_survivors


def gen_profession(prof_perc, prof_hazard):
    """Число представителей определённой профессии, с учётом риска."""
    prof_number = 0
    if prof_male_switch != 0:
        # Берём из словаря численность живых в нужном поколении
        # и пропускаем через ещё один цикл, чтобы учесть риск профессии.
        prof_number = prof_number + \
                      gen_alive(dict_population['gen_alive'] * MALE_perc * prof_perc,
                                       # Отчёт начинается с возраста профессии.
                                       prof_hazard, b, c, age_real - prof_age_new)
    if prof_female_switch != 0:
        prof_number = prof_number + \
                      gen_alive(dict_population['gen_alive'] * FEMALE_perc * prof_perc,
                                       prof_hazard, b, c, age_real - prof_age_new)
    return prof_number


# -------------------------------------------------------------------------
# Главный цикл скрипта.

# Эта база данных станет индексом для словарей.
meta_dict = {}

# Рабочие переменные:
progression_year = 0
year = 0

# Цикл перебирает годы, уходя в прошлое,
# пока возраст популяции не сравняется с возрастом конца исследования.
while (progression_year <= AGE_END):
    # Определяем текущий год (для прогрессии роста населения).
    year = AGE_END - progression_year
    year_real = YEAR_START - year

    # Создаём основной словарь (базу данных) для этого возраста:
    dict_population = {
        'age_real': age_real,
        'year_real': year_real,
        'population_size': population_size(year),
        'gen_size': gen_size(year, fert),
        'gen_alive': gen_alive(gen_size(year, fert), a, b, c, age_real),
        'gdp_size': gdp_size(year)
    }

    # Определяем численность призывников:
    prof_number_new = 0
    if (prof_age_new <= age_real < prof_age_mid_age):
        prof_number_new = prof_number_new + \
                                 gen_profession(prof_perc, prof_hazard)
    # Определяем численность резервистов:
    prof_number_mid_age = 0
    if (prof_age_mid_age <= age_real < prof_age_retiree):
        prof_number_mid_age = prof_number_mid_age + \
                             gen_profession(prof_perc, prof_hazard)
    # И, наконец, пенсионеры:
    prof_number_retiree = 0
    if (prof_age_retiree <= age_real):
        prof_number_retiree = prof_number_retiree + \
                              gen_profession(prof_perc, prof_hazard)

    # Создаём временный словарь гендеров и профессий:
    dict_demography = {
        MALE_NAME: gen_alive(gen_size(year, fert * MALE_perc), a, b, c, age_real),
        FEMALE_NAME: gen_alive(gen_size(year, fert * FEMALE_perc), a, b, c, age_real),
        prof_name_new: prof_number_new,
        prof_name_mid_age: prof_number_mid_age,
        prof_name_retiree: prof_number_retiree,
    }

    # Дополняем первый словарь вторым
    dict_population.update(dict_demography)
    # Создаём объединённый словарь,
    # он будет пополняться при каждом проходе цикла:
    meta_dict[age_real] = dict_population

    # Завершение главного цикла:
    progression_year = progression_year + 1
    age_real = age_real - 1

# -------------------------------------------------------------------------
# Модуль. Вычисляет производство и количество оружия в войсках.

# Произведённое оружие:
meta_dict_equipment_create = {}
# Уцелевшее оружие:
meta_dict_equipment_alive = {}

# Исследование объединённого словаря. Создание баз данных оружия.
# Перебираем вложенные словари начиная с последнего:
for meta_key in sorted(meta_dict.keys(), reverse=True):
    # Временный словарь вооружений (за один год):
    dict_equipment_create = {}
    dict_equipment_alive = {}
    # Перебираем опции из базы данных вооружений:
    for mil_key in sorted(meta_dict_mil.keys()):
        # Количество созданных машин, это бюджет на них, делённый на стоимость.
        mil_create = round(meta_dict[meta_key]['gdp_size'] * gdp_ARMY * \
                           meta_dict_mil[mil_key]['mil_budget'] / meta_dict_mil[mil_key]['mil_cost'])
        mil_alive = gen_alive(mil_create,
                                     meta_dict_mil[mil_key]['mil_a'],
                                     meta_dict_mil[mil_key]['mil_b'],
                                     meta_dict_mil[mil_key]['mil_c'],
                                     meta_dict[meta_key]['age_real'])
        # Создаём временный словарь:
        dict_equipment_create[meta_dict_mil[mil_key]['mil_name']] = mil_create
        dict_equipment_alive[meta_dict_mil[mil_key]['mil_name']] = mil_alive
    # Объединяем временные словари в базу данных:
    meta_dict_equipment_create[meta_key] = dict_equipment_create
    meta_dict_equipment_alive[meta_key] = dict_equipment_alive

# Далее, вычисляем общее число вооружений на складах:
dict_equipment_all = {}
for mil_key in sorted(meta_dict_mil.keys()):
    equipment_all = 0
    for meta_key in sorted(meta_dict_equipment_alive.keys()):
        equipment_all = equipment_all + meta_dict_equipment_alive[meta_key][meta_dict_mil[mil_key]['mil_name']]
    dict_equipment_all[meta_dict_mil[mil_key]['mil_name']] = equipment_all

# -------------------------------------------------------------------------
# Вывод результатов.

# Вывод по годам:
for meta_key in sorted(meta_dict.keys(), reverse=True):
    # Вывод данных о населении:
    print('Год:', meta_dict[meta_key]['year_real'],
          'Возраст:', meta_dict[meta_key]['age_real'],
          'Родившиеся:', meta_dict[meta_key]['gen_size'],
          'Живые:', meta_dict[meta_key]['gen_alive'])
    print(MALE_NAME, meta_dict[meta_key][MALE_NAME],
          FEMALE_NAME, meta_dict[meta_key][FEMALE_NAME])
    # Вывод данных о солдатах:
    if (prof_age_new <= meta_dict[meta_key]['age_real'] < prof_age_mid_age):
        print(prof_name_new, meta_dict[meta_key][prof_name_new])
    if (prof_age_mid_age <= meta_dict[meta_key]['age_real'] < prof_age_retiree):
        print(prof_name_mid_age, meta_dict[meta_key][prof_name_mid_age])
    if (prof_age_retiree <= meta_dict[meta_key]['age_real']):
        print(prof_name_retiree, meta_dict[meta_key][prof_name_retiree])
    # Вывод данных о вооружении:
    for mil_key in sorted(meta_dict_mil.keys()):
        # Отмена вывода, если число машинок по нулям.
        if (meta_dict_equipment_alive[meta_key][meta_dict_mil[mil_key]['mil_name']] != 0):
            if (meta_dict[meta_key]['age_real'] < meta_dict_mil[mil_key]['mil_age_mid']):
                print(meta_dict_mil[mil_key]['mil_name_new'],
                      ' (Создано: ',
                      # Обращение аж к двум словарям, одно вложено в другое.
                      meta_dict_equipment_create[meta_key][meta_dict_mil[mil_key]['mil_name']], ')',
                      ' Уцелело: ',
                      meta_dict_equipment_alive[meta_key][meta_dict_mil[mil_key]['mil_name']], sep='')
            if (meta_dict_mil[mil_key]['mil_age_mid'] <= meta_dict[meta_key]['age_real'] <
                    meta_dict_mil[mil_key]['mil_age_old']):
                print(meta_dict_mil[mil_key]['mil_name_mid'],
                      ' (Создано: ',
                      meta_dict_equipment_create[meta_key][meta_dict_mil[mil_key]['mil_name']], ')',
                      ' Уцелело: ',
                      meta_dict_equipment_alive[meta_key][meta_dict_mil[mil_key]['mil_name']], sep='')
            if (meta_dict_mil[mil_key]['mil_age_old'] <= meta_dict[meta_key]['age_real']):
                print(meta_dict_mil[mil_key]['mil_name_old'],
                      ' (Создано: ',
                      meta_dict_equipment_create[meta_key][meta_dict_mil[mil_key]['mil_name']], ')',
                      ' Уцелело: ',
                      meta_dict_equipment_alive[meta_key][meta_dict_mil[mil_key]['mil_name']], sep='')
    print('------------------------------------------------------------')

# Подведение итогов:
print('Ожидаемая численность:', POPULATION)
population_alive = 0
army_soldiers = 0
army_reservists = 0
for meta_key in sorted(meta_dict.keys()):
    population_alive = population_alive + meta_dict[meta_key]['gen_alive']
    army_soldiers = army_soldiers + meta_dict[meta_key][prof_name_new]
    army_reservists = army_reservists + meta_dict[meta_key][prof_name_mid_age]
print('Численность популяции:', population_alive)
print(prof_name_new, 'и', prof_name_mid_age, 'по видам войск:')
for troop_key in sorted(dict_trps_types.keys()):
    print('    ', troop_key, ' (', round(dict_trps_types[troop_key] * 100), '%) ',
          round(army_soldiers * dict_trps_types[troop_key]),
          ' — ', round((army_soldiers + army_reservists) * dict_trps_types[troop_key]), sep='')
print('Несчастные случаи (в год):', round(POPULATION * COMPONENT_A))
print('Военные потери: ', round(army_soldiers * prof_hazard),
      ' (', round(army_soldiers * prof_hazard / (POPULATION * COMPONENT_A) * 100),
      '% от несчастных случаев)', sep='')
print('------------------------------------------------------------')

# -------------------------------------------------------------------------
# И наконец, суммируем всё вооружение, вычисляем отношение единиц оружия к числу солдат,
# потребность армии в боеприпасаха, а также суммарный бюджет на вооружения и бюджеты по видам войск:

budget_perc = 0
budget_trps_perc = 0
# База данных потребностей в боеприпасах:
ammunition_needs = {}
# Названия боеприпасов превращаем в ключи базы данных:
for mil_key in sorted(meta_dict_mil.keys()):
    if meta_dict_mil[mil_key].get('mil_ammo_1_name'):
        ammunition_needs[meta_dict_mil[mil_key]['mil_ammo_1_name']] = 0
    if meta_dict_mil[mil_key].get('mil_ammo_2_name'):
        ammunition_needs[meta_dict_mil[mil_key]['mil_ammo_2_name']] = 0
    if meta_dict_mil[mil_key].get('mil_ammo_3_name'):
        ammunition_needs[meta_dict_mil[mil_key]['mil_ammo_3_name']] = 0
    if meta_dict_mil[mil_key].get('mil_ammo_4_name'):
        ammunition_needs[meta_dict_mil[mil_key]['mil_ammo_4_name']] = 0
    if meta_dict_mil[mil_key].get('mil_ammo_5_name'):
        ammunition_needs[meta_dict_mil[mil_key]['mil_ammo_5_name']] = 0
    if meta_dict_mil[mil_key].get('mil_ammo_6_name'):
        ammunition_needs[meta_dict_mil[mil_key]['mil_ammo_6_name']] = 0
    if meta_dict_mil[mil_key].get('mil_ammo_7_name'):
        ammunition_needs[meta_dict_mil[mil_key]['mil_ammo_7_name']] = 0
    if meta_dict_mil[mil_key].get('mil_ammo_8_name'):
        ammunition_needs[meta_dict_mil[mil_key]['mil_ammo_8_name']] = 0
    if meta_dict_mil[mil_key].get('mil_ammo_9_name'):
        ammunition_needs[meta_dict_mil[mil_key]['mil_ammo_9_name']] = 0
    if meta_dict_mil[mil_key].get('mil_fuel_name'):
        ammunition_needs[meta_dict_mil[mil_key]['mil_fuel_name']] = 0
# База данных бюджета по видам войск:
# Создаётся рабочий словарь, обнуляются значения:
budget_trps_types = {}
budget_trps_types.update(dict_trps_types)
for troop_key in budget_trps_types:
    budget_trps_types[troop_key] = 0
# База данных стоимости обслуживания по видам войск:
# Создаётся рабочий словарь, обнуляются значения:
maint_trps_types = {}
maint_trps_types.update(dict_trps_types)
for troop_key in budget_trps_types:
    maint_trps_types[troop_key] = 0

# Перебор столбцов в базе данных оружия:
for mil_key in sorted(meta_dict_mil.keys()):
    equipment_all = 0
    # Затем перебор по годам:
    for meta_key in sorted(meta_dict_equipment_alive.keys()):
        equipment_all = equipment_all + meta_dict_equipment_alive[meta_key][meta_dict_mil[mil_key]['mil_name']]
    # Если есть проект, значит есть оружие, хотя бы один экземпляр:
    if equipment_all < 1:
        equipment_all = 1
        print('Не хватает бюджета на', meta_dict_mil[mil_key]['mil_name'])
    # Вывод суммы оружия, сохранившегося за все годы:
    print("[" + meta_dict_mil[mil_key]['mil_trps_type'] + "]", meta_dict_mil[mil_key]['mil_name'], '—', equipment_all, end=' ')
    # Вывод отношения числа вооружений к числу солдат определённых видов войск:
    army_type_perc = dict_trps_types[meta_dict_mil[mil_key]['mil_trps_type']]
    print('на', round(army_soldiers * army_type_perc),
          prof_name_new, meta_dict_mil[mil_key]['mil_trps_type'],
          'или на', round((army_reservists + army_soldiers) * army_type_perc),
          prof_name_new, '+',
          prof_name_mid_age, meta_dict_mil[mil_key]['mil_trps_type'])
    # Вывод описания вооружения:
    print('    ', meta_dict_mil[mil_key]['mil_name_comment'])
    # Подсчитываем, сколько оружия создано за год:
    mil_create = round(gdp_size(0) * gdp_ARMY * \
                       meta_dict_mil[mil_key]['mil_budget'] / meta_dict_mil[mil_key]['mil_cost'])
    # Расходы на проект:
    print('        Расходы: ',
          round(meta_dict_mil[mil_key]['mil_budget'] * 100, 3), '% бюджета ',
          '(', round(meta_dict_mil[mil_key]['mil_cost'] * mil_create / (10 ** 6), 3),
          ' млн ', meta_dict_mil[mil_key]['mil_cost_currency'], ') ', sep='')
    # Подсчитываем потери (без учёта старения оружия):
    print('        Создано:', mil_create)
    print('        Потери:', round(mil_create * meta_dict_mil[mil_key]['mil_a'] + \
                                   equipment_all * meta_dict_mil[mil_key]['mil_a']))
    print('        ---')
    # Считаем потребность в боеприпасах (максимум 9 видов оружия) и топливо:
    if meta_dict_mil[mil_key].get('mil_ammo_1_name'):
        ammunition_needs[meta_dict_mil[mil_key]['mil_ammo_1_name']] = \
            ammunition_needs[meta_dict_mil[mil_key]['mil_ammo_1_name']] + \
            meta_dict_mil[mil_key]['mil_ammo_1_expense'] * equipment_all
    if meta_dict_mil[mil_key].get('mil_ammo_2_name'):
        ammunition_needs[meta_dict_mil[mil_key]['mil_ammo_2_name']] = \
            ammunition_needs[meta_dict_mil[mil_key]['mil_ammo_2_name']] + \
            meta_dict_mil[mil_key]['mil_ammo_2_expense'] * equipment_all
    if meta_dict_mil[mil_key].get('mil_ammo_3_name'):
        ammunition_needs[meta_dict_mil[mil_key]['mil_ammo_3_name']] = \
            ammunition_needs[meta_dict_mil[mil_key]['mil_ammo_3_name']] + \
            meta_dict_mil[mil_key]['mil_ammo_3_expense'] * equipment_all
    if meta_dict_mil[mil_key].get('mil_ammo_4_name'):
        ammunition_needs[meta_dict_mil[mil_key]['mil_ammo_4_name']] = \
            ammunition_needs[meta_dict_mil[mil_key]['mil_ammo_4_name']] + \
            meta_dict_mil[mil_key]['mil_ammo_4_expense'] * equipment_all
    if meta_dict_mil[mil_key].get('mil_ammo_5_name'):
        ammunition_needs[meta_dict_mil[mil_key]['mil_ammo_5_name']] = \
            ammunition_needs[meta_dict_mil[mil_key]['mil_ammo_5_name']] + \
            meta_dict_mil[mil_key]['mil_ammo_5_expense'] * equipment_all
    if meta_dict_mil[mil_key].get('mil_ammo_6_name'):
        ammunition_needs[meta_dict_mil[mil_key]['mil_ammo_6_name']] = \
            ammunition_needs[meta_dict_mil[mil_key]['mil_ammo_6_name']] + \
            meta_dict_mil[mil_key]['mil_ammo_6_expense'] * equipment_all
    if meta_dict_mil[mil_key].get('mil_ammo_7_name'):
        ammunition_needs[meta_dict_mil[mil_key]['mil_ammo_7_name']] = \
            ammunition_needs[meta_dict_mil[mil_key]['mil_ammo_7_name']] + \
            meta_dict_mil[mil_key]['mil_ammo_7_expense'] * equipment_all
    if meta_dict_mil[mil_key].get('mil_ammo_8_name'):
        ammunition_needs[meta_dict_mil[mil_key]['mil_ammo_8_name']] = \
            ammunition_needs[meta_dict_mil[mil_key]['mil_ammo_8_name']] + \
            meta_dict_mil[mil_key]['mil_ammo_8_expense'] * equipment_all
    if meta_dict_mil[mil_key].get('mil_ammo_9_name'):
        ammunition_needs[meta_dict_mil[mil_key]['mil_ammo_9_name']] = \
            ammunition_needs[meta_dict_mil[mil_key]['mil_ammo_9_name']] + \
            meta_dict_mil[mil_key]['mil_ammo_9_expense'] * equipment_all
    if meta_dict_mil[mil_key].get('mil_fuel_name'):
        ammunition_needs[meta_dict_mil[mil_key]['mil_fuel_name']] = \
            ammunition_needs[meta_dict_mil[mil_key]['mil_fuel_name']] + \
            meta_dict_mil[mil_key]['mil_fuel_expense'] * equipment_all
    # Считаем общий бюджет и бюджет по родам войск:
    budget_perc = budget_perc + meta_dict_mil[mil_key]['mil_budget']
    for troop_key in budget_trps_types:
        if troop_key == meta_dict_mil[mil_key]['mil_trps_type']:
            budget_trps_types[troop_key] = budget_trps_types[troop_key] + \
                                             meta_dict_mil[mil_key]['mil_budget'] * 100
    # Считаем расходы на обслуживание данного вида оружия:
    # Стоимость оружия * процент обслуживания * штук на складах
    # Если строка 'mil_maint' не указана, тогда обслуживание бесплатно
    mil_maint_all = meta_dict_mil[mil_key]['mil_cost'] * \
                          meta_dict_mil.get(mil_key, 0).get('mil_maint', 0) * \
                          dict_equipment_all.get(meta_dict_mil[mil_key]['mil_name'])
    # Теперь распределяем расходы на обслуживание по родам войск:
    for troop_key in maint_trps_types:
        if troop_key == meta_dict_mil[mil_key]['mil_trps_type']:
            maint_trps_types[troop_key] = maint_trps_types[troop_key] + \
                                                  mil_maint_all

# Сумма бюджета всех проектов из базы данных оружия:
print('Расходы военного бюджета на закупки и производство:')
for troop_key in sorted(budget_trps_types.keys()):
    print('    ', troop_key, ' (', round(dict_trps_types[troop_key] * 100), '%)',
          ' — ', round(budget_trps_types[troop_key], 2), '%', sep='')
print('Использовано ', round(budget_perc * 100, 2), '% бюджета армии',
      ' (или ', round(gdp_ARMY * budget_perc * 100, 2), '% ВВП страны)',
      sep='')
print('        ---')

# Расходы на обслуживание оружия по видам войск:
maint_perc_sum = 0
print('Расходы военного бюджета на техническое обслуживание:')
for troop_key in sorted(maint_trps_types.keys()):
    maint_perc = maint_trps_types[troop_key] / (gdp_size(0) * gdp_ARMY)
    maint_perc_sum = maint_perc_sum + maint_perc
    print('    ', troop_key, ' (', round(dict_trps_types[troop_key] * 100), '%)',
          ' — ', round(maint_perc * 100, 2), '%', sep='')
print('Использовано ', round(maint_perc_sum * 100, 2), '% бюджета армии',
      ' (или ', round(maint_perc_sum * gdp_ARMY * 100, 2), '% ВВП страны)',
      sep='')
print('        ---')

# Соотношение производства боеприпасов и потребности в них:
print('Боеприпасы на складах (потребность на год войны - 100%):')
for ammo_key in sorted(ammunition_needs.keys()):
    # (ammo_key, 0) — значит, если нет ключа, брать ноль.
    print('   ', ammo_key, ' — ', dict_equipment_all.get(ammo_key, 0), ' (',
          round(dict_equipment_all.get(ammo_key, ammunition_needs[ammo_key]) / \
                ammunition_needs[ammo_key] * 100), '%)', sep='')