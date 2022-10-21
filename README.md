# ITMO EVENTS

_____
На данный момент в docker-compose поднимется только бд. Для тестирования функционала должно хватить.
Когда запустишь бд выполни команды описанные ниже в том же порядке.

### "Make" options
Для запуска docker-compose (создастся локальная бд):
```
make run
```
Для проверки подключения к базе данных (креды в .env):
```
make db
```
Выполни миграцию:
```
make migrate head
```

Теперь рекомендую проверить содержимое бд:
```
1) make db
2) \dt; #эта команда непосредственно после подключения в бд вводится
```
Должны быть выведены все таблицы. Если все так - супер.

---

