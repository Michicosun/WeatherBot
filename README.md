# WeatherBot
По сути бот показывает погоду и температуру в заданных заранее городах

Интерфейс:
```bash
/list
# показывает список добавленных городов
```


```bash
/add_city
# добавляет город в список отслеживаемых
```


```bash
/delete_city
# удаляет город из списка, если он там был
```

```bash
{{message}}
# любое сообщение триггерит вывод по всем городам
# если добавить много городов, может работать долго
```

Сервис: Amazon

Для автоматического запуска бота на сервере использовал WatchTower:

```dockerfile
version: '3'

services:
  weather:
    image: michicosun/weather
    labels:
      - "com.centurylinklabs.watchtower.scope=myscope"
    environment:
      TELEGRAM_BOT_TOKEN: "key"

  watchtower:
    image: containrrr/watchtower
    volumes:
      - /var/run/docker.sock:/var/run/docker.sock
    command: --interval 10 --scope myscope
    labels:
      - "com.centurylinklabs.watchtower.scope=myscope"
```















