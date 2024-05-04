# Файл с основным функционалом
import datetime
import re


class Wallet:
    def __init__(self, path='journal.txt'):
        self.file_path = path

    def load_journal(self):  # Загрузка данных их журнала
        with open(self.file_path, 'r', encoding="UTF-8") as journal_file:
            return journal_file.readlines()

    def data_to_dictionaries(self):  # Перевод данных в список словарей для более удобной работы с ними
        journal = self.load_journal()
        j = []
        for i in range(0, len(journal), 5):
            j.append(
                {
                    'Дата': journal[i].split(': ')[1].strip('\n'),
                    'Категория': journal[i+1].split(': ')[1].strip('\n'),
                    'Сумма': journal[i + 2].split(': ')[1].strip('\n'),
                    'Описание': journal[i + 3].split(': ')[1].strip('\n')
                }
            )
        return j

    def save_data(self, data):  # Сохранение данных в журнал
        with open(self.file_path, 'a', encoding="UTF-8") as journal_file:
            journal_file.writelines(data)

    def update_data(self, data):  # Обновление данных в журнале
        with open(self.file_path, 'w', encoding="UTF-8") as journal_file:
            journal_file.writelines(data)

    def balance_out(self):  # Вывод текущего баланса кошелька
        journal = self.load_journal()
        income = 0
        spending = 0
        index = 0
        for line in journal:
            if "Доход" in line:
                income += int(journal[index + 1].split(": ")[1])  # Считаем весь доход
            elif "Расход" in line:
                spending += int(journal[index + 1].split(": ")[1])  # Считаем все расходы
            index += 1
        return income - spending, income, spending  # Возвращаем разницу - баланс, а также доход и расходы

    def note_add(self):  # Добавление записи в журнал
        print('\n-- Введите корректные данные для добавления новой записи:\n')
        date = datetime.date.today()
        category = input("Введите категорию (Доход/Расход): ")
        amount = input("Введите сумму без пробелов: ")
        description = input("Введите описание: ")

        if category in ("Доход", "Расход") and amount.isdigit():  # Проверка корректности данных
            new_note = ["\n\n",
                        "Дата: " + str(date) + "\n",
                        "Категория: " + category + "\n",
                        "Сумма: " + amount + "\n",
                        "Описание: " + description
                        ]
            self.save_data(new_note)
            return True  # Успешное добавление записи
        else:
            return False  # Неуспешное добавление записи

    def note_edit(self, note_number):  # Редактирование записи в журнале
        all_notes = self.data_to_dictionaries()

        if note_number > len(all_notes):  # Проверяем есть ли номер записи в журнале
            return False

        da = input("Введите дату в формате YYYY-MM-DD: ")
        cat = input("Введите категорию Доход/Расход: ")
        am = input("Введите сумму без пробелов: ")
        des = input("Введите описание: ")

        if ((re.match(r'\d{4}-\d{2}-\d{2}', da) or da == '+')
                and cat in ("Доход", "Расход", "+")
                and (am.isdigit() or am == "+")):  # Проверка введенных данных на корректность
            all_notes[note_number + 1]['Дата'] = da
            all_notes[note_number + 1]['Категория'] = cat
            all_notes[note_number + 1]['Сумма'] = am
            all_notes[note_number + 1]['Описание'] = des

            data = []  # Обновление данных в файле
            for i in all_notes:
                for k, v in i.items():
                    data.append(str(k) + ': ' + str(v) + '\n')
                data.append('\n')
            self.update_data(data)

            return True  # Редактирование прошло успешно
        else:
            return False  # Редактирование прошло неуспешно

    def notes_out(self):  # Вывод записей по фильтрам
        print('\n-- Введите критерии, по которым будут фильтроваться записи')
        print('   Если критерия нет, введите "+" в поле\n')
        da = input("Введите дату в формате YYYY-MM-DD: ")
        cat = input("Введите категорию Доход/Расход: ")
        am = input("Введите сумму без пробелов: ")
        des = input("Введите описание: ")

        if re.match(r'\d{4}-\d{2}-\d{2}', da) or da == '+' and cat in ("Доход", "Расход", "+") and am.isdigit() or am == "+":  # Проверка введенных данных на корректность
            print('\n-- Записи, подходящие по фильтрам --'
                  '\n-----------------------------------+')
            all_notes = self.data_to_dictionaries()  # Загружаем все существующие записи
            for i in all_notes:  # И выводим нежные пользователю
                if ((i['Дата'] == da or da == "+")
                        and (i['Категория'] == cat or cat == "+")
                        and (i['Сумма'] == am or am == "+")
                        and (i['Описание'] == des or des == "+")):
                    for k, v in i.items():
                        print(k, v)
                    print('-----------------------------------+')
            return True  # Данные выведены успешно
        else:
            print("Проверьте, пожалуйста, корректность данных и повторите ввод.")
            return False  # Данные выведены неуспешно
