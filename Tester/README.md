# Tester: Jupyter Notebooks для анализа констант

## Установка (уже сделано)
- Добавлен `jupyterlab` в `pyproject.toml` [dev]
- `pip install -e .[dev]`

## Запуск
```bash
cd Tester
jupyter lab
```
- Откроется [localhost:8888/tree/Tester](http://localhost:8888/lab/tree/Tester)
- Запустите **Tester.ipynb** (Run All)

## Что делает ноутбук
1. Парсит CODATA из `../Universe/Физические_константы.md` → `codata_2022.csv`
2. Парсит LHC частицы из `../Physics/Вибрации/Вселенная_и_вибрации.md` → `lhc_particles.csv`
3. Загружает `formulas_registry.yaml`
4. Вычисляет константы по реестру (CODATA lookup, sympy, linregress LHC)
5. Сохраняет `reports/all_constants.{md,csv}` + `constants_scatter.png`

## Оригинальные скрипты
Сохранены `.py` файлы для справки/сравнения.

**Переход на Jupyter завершён!** 🎉
