# Sampling Experiment Plan (draft)

## Target task

Primary MVP: binary acoustic event detection (`mosquito` vs `background`) using labelled HumBugDB examples. A separate species-level experiment may be added only if class metadata and sample counts support it.

## Candidate conditions

- 8 kHz: literature-grounded low-cost reference; HumBug records are described as 8 kHz mono PCM for the low-cost smartphone pipeline.
- 4 kHz: 2x downsampling from the same source clips.
- 2 kHz: 4x downsampling from the same source clips.

Optional 16 kHz can be tested only on a common source subset originally recorded at 16 kHz or higher. Do not upsample 8 kHz material and call it a 16 kHz measurement.

## Fair-comparison rules

1. Use the same source recordings for all conditions being compared.
2. Split by original recording / session / source before making overlapping windows, so windows from one recording cannot leak across train and test.
3. Use identical labels, windows, model architecture, training budget, and test examples for each condition.
4. Report accuracy, precision, recall, F1, confusion matrix, and class balance.
5. Report model size and ESP32 memory/latency estimates separately from simulation measurements.
6. Quantization (e.g. int8) is a separate compression axis from sample-rate reduction; test it separately before combining them.

## Success criterion

The research target is test accuracy >90% for a reduced-data condition. Report the actual result even if no tested condition reaches the target.
