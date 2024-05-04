# Основной файл, предназначенный в основном для взаимодействия с пользователем
from back import Wallet


def main():
    wal = Wallet()
    while True:
        choice = input('[+] Выберите Ваше действие:\n'
                       '1) Вывод баланса и фин. статистики\n'
                       '2) Добавление новой записи\n'
                       '3) Редактирование записи\n'
                       '4) Поиск по записям\n'
                       '5) Выход из программы\n'
                       '>>> ')
        match choice:
            case '1':
                balance, income, spending = wal.balance_out()
                print('\n-- Финансовая статистика:'
                      '\nТекущий баланс: {0}'
                      '\nОбщий доход: {1}'
                      '\nОбщие расходы: {2}\n'
                      .format(balance, income, spending))
            case '2':
                res = wal.note_add()
                print("-- Запись добавлена\n" if res == True else "-- Проверьте, пожалуйста, корректность данных и повторите ввод.\n")
            case '3':
                print("\n-- Выберите какую запись, начиная с конца списка, вы хотите изменить?\n")
                note_number = int(input('Редактируем запись номер...: '))
                edit_res = wal.note_edit(note_number)
                print("-- Запись успешно изменена\n" if edit_res == True else "-- Проверьте, пожалуйста, корректность данных и повторите ввод.\n")

            case '4':
                wal.notes_out()
            case '5':
                print('\n-- Всего доброго!')
                break
            case _:
                print("Ошибка. Выбрана неправильная функция.")


if __name__ == "__main__":
    main()