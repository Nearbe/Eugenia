#!/bin/bash
# scripts/junie_local.sh
# Удобная обертка для запуска Junie с локальной моделью

# Директория проекта
PROJECT_ROOT="$( cd "$( dirname "${BASH_SOURCE[0]}" )/.." && pwd )"

# Загрузка переменных окружения из .env если он есть
if [ -f "$PROJECT_ROOT/.env" ]; then
    # Читаем файл построчно, экспортируя переменные
    while IFS= read -r line || [[ -n "$line" ]]; do
        # Игнорируем комментарии и пустые строки
        if [[ ! "$line" =~ ^# && "$line" =~ = ]]; then
            export "$line"
        fi
    done < "$PROJECT_ROOT/.env"
fi

# Модель по умолчанию (из .env или custom:gemma-local)
# Мы используем имя файла конфигурации без .json как идентификатор в Junie CLI
MODEL_ID="custom:gemma-local"

# Обработка аргументов
while [[ "$#" -gt 0 ]]; do
    case $1 in
        --model) MODEL_ID="$2"; shift ;;
        *) break ;;
    esac
    shift
done

# Проверка наличия junie
JUNIE_BIN=""
if command -v junie &> /dev/null; then
    JUNIE_BIN=$(which junie)
elif [ -f "$HOME/.local/bin/junie" ]; then
    JUNIE_BIN="$HOME/.local/bin/junie"
else
    echo "Error: junie CLI not found. Please install it or add ~/.local/bin to PATH."
    exit 1
fi

# Если аргументов нет, показываем помощь
if [ $# -eq 0 ]; then
    echo "Использование: ./scripts/junie_local.sh \"Ваша задача\""
    echo "Или: make junie task=\"Ваша задача\""
    exit 0
fi

# Запуск Junie
"$JUNIE_BIN" --model "$MODEL_ID" "$@"
