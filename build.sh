#!/usr/bin/env bash
# скачиваем uv и запускаем команду установки зависимостей

make install && psql -a -d $DATABASE_URL -f database.sql