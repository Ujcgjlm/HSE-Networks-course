# Проверка минимального MTU до хоста

## Сборка
```
docker build -t mtu_checker .
```

## Запуск
Минимальный:
```
docker run --rm mtu_checker --address ya.ru
```

Максимальный:
```
docker run --rm mtu_checker --min_mtu 68 --max_mtu 3000 --address ya.ru --interval 0
```

Помощь:
```
docker run --rm mtu_checker --help
```
