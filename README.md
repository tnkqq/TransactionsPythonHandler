Функционал: 
    !MAIN_MENUE
        -добавление транзакции
        -удалениее транзакции по номеру из выводиммого в терминал списка 
        -редактирование транзакции по номеру из выводимого в терминал списка
        -вывод списка тразакций 
        -выход 

    0 - ОЧИСТАК ТЕРМИНАЛА:

    1 - ADD_TRANSACTION:
        -ввод категории(только 'r'/'R' и 'd'/'D' - расход и доход)
        -ввод суммы тразакции 
        -ввод описания транзакции
        Транзакция добавляется в конец файла  
    2 -DELETE_TRANSACTION:
        -выводит список тразакций 
        -ввод номера транзакции для удаления 
        В транзакция определяется по id, файл полностью перезаписывается 

    4 -GET_TRANSACTION_LIST:
        -выводит список тразакций

    4 -EDIT_TRANSACTION: 
        -выводит список тразакций 
        -ввод данных тразакции также как в ADD_TRANSACTION
        Транзакция перезаписывается в конец файла и transactions 
    5 -EXIT:
        Выход из программы

MODELS:
    Transaction:
        -get_transaction_list -> dict{
            date:,
            category:,
            value:,
            description:,
            id:,
        }

        -edit_trasaction(date: str, id: int, *args)

    Wallet:
        !Вывод_баланса
        -change_value(self, action_type: str, value: int) -> None

        !Список транзакций
        -get_transaction_list -> list
        
        !Добавление_транзакции
        Возвращает True если добавлена и False если не добавлена 
        -add_transaction(category: str, value: int, description: str) -> bool

        !Удаление_транзакции
        Удаляет транзакцию по ее индексу 
        Возвращает True если удалена и False если не удалена 
        -delete_transaction(position: int) -> bool

        !Редактирование_транзакции_по_ее_индексу
        Также в функцию передаются новые данные транзакции
        -edit_trasaction(position: int, *args)

