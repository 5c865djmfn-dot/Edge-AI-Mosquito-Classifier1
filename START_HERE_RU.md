# Начни отсюда (Windows)

## 1. Создай аккаунты и установи инструменты

1. Создай бесплатный аккаунт на https://github.com/ .
2. Установи Python 3.11 (64-bit): https://www.python.org/downloads/ . Во время установки отметь **Add Python to PATH**.
3. Установи Git for Windows: https://git-scm.com/download/win .
4. (Необязательно) Установи Visual Studio Code: https://code.visualstudio.com/ .

## 2. Скачай аудиоданные

Открой https://zenodo.org/records/4904800 . Скачай четыре ZIP-архива `humbugdb_neurips_2021_1.zip` ... `_4.zip` и CSV `neurips_2021_zenodo_0_0_1.csv`. На странице указано около 4.1 GB данных в ZIP-архивах.

Создай папку `data/raw/audio/`. Распакуй содержимое всех четырёх ZIP-архивов в одну общую папку `data/raw/audio/` (не создавай отдельные папки на каждый архив, если архивы уже содержат собственную внутреннюю структуру). Скопируй CSV в `data/raw/metadata/`.

Не загружай WAV-файлы и ZIP-архивы в GitHub: они большие. В репозитории храним код, инструкции, небольшие отчёты и ссылки на источник данных.

## 3. Установи Python-библиотеки и проверь WAV-файлы

Открой PowerShell в папке проекта и выполни:

```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
python src/inspect_audio.py --audio-dir data/raw/audio --output results/audio_inventory.csv
```

В конце скопируй сюда первые строки вывода и содержимое `results/audio_inventory_summary.txt` (если создан). По фактической структуре аудио и CSV мы настроим разметку классов и сделаем честный эксперимент с частотами дискретизации.

## Важно

HumBugDB содержит около 20 часов записей комаров и 15 часов фоновых записей; в публикации описаны 36 видов/видовых комплексов в метаданных. Это подходит для первого бинарного эксперимента **mosquito / background**. Наличие звука комара не доказывает вид или способность переносить конкретное заболевание; для видовой классификации нужна отдельная корректная разметка по видам.
