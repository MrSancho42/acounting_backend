#!/bin/bash

# Перевірка, чи задано порт у вхідних параметрах
if [[ $# -ne 1 ]]; then
  echo 'Введіть порт який необхідно перевірити'
  exit 1
fi

port=$1

# Перевірка, чи є процес, що слухає порт
if sudo lsof -Pi :$port -sTCP:LISTEN -t >/dev/null ; then
  echo 'Процес, що слухає порт $port, було знайдено і зупинено'
  sudo kill $(sudo lsof -t -i:$port)
fi

# Очікування повного завершення процесу, який слухає порт
echo 'Очікування повного завершення процесу, який слухає порт $port'
while sudo lsof -Pi :$port -sTCP:LISTEN -t >/dev/null ; do
  sleep 1
done

# Запуск uvicorn
echo 'Запуск uvicorn на порті $port'
uvicorn main:app --port $port --reload
