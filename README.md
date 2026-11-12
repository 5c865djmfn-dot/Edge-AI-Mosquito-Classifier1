# Edge-AI Mosquito Call Classifier

A low-cost edge-AI prototype for detecting mosquito flight-tone events from short audio windows. The initial implementation uses the public HumBugDB audio dataset, then evaluates how resampling affects classification performance before preparing an ESP32/TFLite Micro deployment.

> **Current status:** project scaffold only. No model accuracy, latency, RAM, or flash results have been measured yet. The target of >90% accuracy is an experimental goal, not a claimed result.

## Research question

**What audio sampling rate / compression setting can maintain more than 90% classification accuracy while remaining feasible for an ESP32-class device?**

For a fair experiment, all sampling-rate variants must be generated from the same source clips and evaluated with the same train/validation/test split. The test split must not be used during training or model selection.

## Planned pipeline

1. Audio data: HumBugDB mosquito recordings and matched background recordings.
2. Preprocessing: mono PCM audio, fixed-length windows, resampling variants (initial targets: 8 kHz, 4 kHz, 2 kHz; revise only after inspecting the original audio sample rates).
3. Model: compact CNN / audio impulse in Edge Impulse.
4. Deployment: export an embedded C++ library or TensorFlow Lite Micro model, then assess feasibility for ESP32.
5. Demonstration: Wokwi software-in-the-loop simulation if physical ESP32 + INMP441 hardware is unavailable.

## Dataset

The primary candidate is **HumBugDB** (Kiskin et al.). It contains about 20 hours of labelled mosquito audio and 15 hours of corresponding background noise; species metadata is available for many mosquito recordings. The published dataset archive is split across four ZIP files (about 4.1 GB total) plus a metadata CSV. The dataset is licensed CC BY 4.0; provide attribution when reusing it.

- Dataset: https://zenodo.org/records/4904800
- Companion research/code repository: https://github.com/HumBug-Mosquito/HumBugDB
- Supplementary material (licensing and methodology): https://openreview.net/attachment?id=vhjsBtq9OxO&name=supplementary_material

Do not commit the raw dataset to this GitHub repository. Store it locally under `data/raw/` and cite the dataset in your documentation.

## Repository structure

```text
Edge-AI-Mosquito-Classifier/
├── README.md
├── START_HERE_RU.md
├── requirements.txt
├── .gitignore
├── src/
│   └── inspect_audio.py
├── data/
│   └── raw/
│       ├── audio/       # extracted WAV files (not committed)
│       └── metadata/    # CSV metadata (not committed)
├── results/             # generated reports and plots
├── firmware/            # ESP32 / TFLite Micro code
├── simulation/          # Wokwi project files
└── docs/                # proposal, experiment notes, final analysis
```

## Setup (Windows PowerShell)

Install Python 3.11 (64-bit), Git for Windows, and optionally Visual Studio Code.

```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
```

If PowerShell blocks virtual-environment activation, run this once in the current terminal:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1
```

## Inspect the downloaded audio

After extracting the dataset WAV files into `data/raw/audio/` and placing the metadata CSV in `data/raw/metadata/`, run:

```powershell
python src/inspect_audio.py --audio-dir data/raw/audio --output results/audio_inventory.csv
```

The script reports the WAV file count, sample-rate distribution, channels, duration, and relative paths. This inspection is required before choosing valid downsampling rates.

## Hardware and simulation note

The intended physical sensor is an INMP441 I2S microphone connected to an ESP32. If hardware is unavailable, Wokwi can be used for a **software-in-the-loop demonstration** of the ESP32 application. Do not describe a simulated or mocked microphone input as a physical INMP441 measurement. Wokwi's current ESP32 peripheral support lists I2S as partial for the original ESP32 and not supported for several ESP32 variants; verify the selected board before claiming live I2S microphone simulation.

## Evidence to collect

- Dataset citation and licence attribution.
- WAV inventory and class counts.
- Identical test-set accuracy, precision, recall, F1, and confusion matrix for each sampling condition.
- Model file size and estimated/observed RAM, flash, and inference latency for the chosen ESP32 target.
- Video showing the software demonstration and clearly stating whether hardware is physical or simulated.

## Dataset citation

Kiskin, I. et al. (2021). *HumBugDB: a large-scale acoustic mosquito dataset*. Zenodo. https://doi.org/10.5281/zenodo.4904800. Dataset licence: CC BY 4.0.
