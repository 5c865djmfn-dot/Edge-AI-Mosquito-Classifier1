"""Inventory WAV files before choosing sampling-rate experiment settings.

The script intentionally does not infer class labels. HumBugDB labels are supplied
through metadata, so the metadata mapping will be added after inspecting the real
folder and CSV structure.
"""

from __future__ import annotations

import argparse
import csv
import sys
from collections import Counter
from pathlib import Path

try:
    import soundfile as sf
except ImportError as exc:  # pragma: no cover - clear setup message
    raise SystemExit(
        "Missing dependency 'soundfile'. Activate .venv and run: pip install -r requirements.txt"
    ) from exc


def inspect_audio(audio_dir: Path) -> list[dict[str, object]]:
    if not audio_dir.exists():
        raise FileNotFoundError(
            f"Audio folder not found: {audio_dir.resolve()}\n"
            "Download and extract the dataset into data/raw/audio first."
        )

    wav_files = sorted(p for p in audio_dir.rglob("*") if p.is_file() and p.suffix.lower() == ".wav")
    if not wav_files:
        raise FileNotFoundError(
            f"No .wav files found under: {audio_dir.resolve()}\n"
            "Check that all dataset ZIP archives were extracted into this folder."
        )

    rows: list[dict[str, object]] = []
    failed: list[tuple[str, str]] = []

    for path in wav_files:
        try:
            info = sf.info(str(path))
            rows.append(
                {
                    "relative_path": path.relative_to(audio_dir).as_posix(),
                    "sample_rate_hz": int(info.samplerate),
                    "channels": int(info.channels),
                    "frames": int(info.frames),
                    "duration_seconds": round(float(info.duration), 6),
                    "subtype": info.subtype,
                }
            )
        except Exception as exc:  # keep inventory running if one file is corrupt
            failed.append((str(path), str(exc)))

    if failed:
        print(f"Warning: {len(failed)} WAV file(s) could not be read:", file=sys.stderr)
        for name, error in failed[:10]:
            print(f"  {name}: {error}", file=sys.stderr)

    return rows


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--audio-dir", type=Path, required=True, help="Folder containing extracted WAV files")
    parser.add_argument("--output", type=Path, default=Path("results/audio_inventory.csv"))
    args = parser.parse_args()

    try:
        rows = inspect_audio(args.audio_dir)
    except (FileNotFoundError, OSError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1

    args.output.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = ["relative_path", "sample_rate_hz", "channels", "frames", "duration_seconds", "subtype"]
    with args.output.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    rates = Counter(int(row["sample_rate_hz"]) for row in rows)
    channels = Counter(int(row["channels"]) for row in rows)
    total_seconds = sum(float(row["duration_seconds"]) for row in rows)

    summary = [
        "AUDIO INVENTORY SUMMARY",
        f"Readable WAV files: {len(rows)}",
        f"Total duration: {total_seconds / 3600:.2f} hours",
        "Sample-rate counts:",
    ]
    summary.extend(f"  {rate} Hz: {count}" for rate, count in sorted(rates.items()))
    summary.append("Channel counts:")
    summary.extend(f"  {channel}: {count}" for channel, count in sorted(channels.items()))
    summary.append(f"CSV report: {args.output.as_posix()}")

    summary_text = "\n".join(summary)
    summary_path = args.output.with_name("audio_inventory_summary.txt")
    summary_path.write_text(summary_text + "\n", encoding="utf-8")
    print(summary_text)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
