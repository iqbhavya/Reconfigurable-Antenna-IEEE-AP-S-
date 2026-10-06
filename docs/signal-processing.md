# Signal Processing

## Objective

The software side is intended to convert raw RF/CSI measurements into features that can be compared across time and antenna configurations.

## Channel model

A wireless channel can be represented conceptually as:

```text
H(f,t) = |H(f,t)| exp(jφ(f,t))
```

where amplitude and phase vary with frequency and time.

The processing work will investigate:

- CSI amplitude
- CSI phase
- amplitude variation
- phase variation
- subcarrier behavior
- temporal characteristics
- periodic components
- noise
- channel stability

## Initial processing pipeline

```text
Raw RF/CSI data
      ↓
Data acquisition
      ↓
Preprocessing
      ↓
Noise reduction
      ↓
Amplitude/phase processing
      ↓
Filtering
      ↓
Feature extraction
      ↓
Temporal analysis
      ↓
Activity score
      ↓
Spatial estimation
      ↓
Antenna-state selection
```

## Preprocessing candidates

- corrupted-sample removal
- normalization
- outlier removal
- phase correction/unwrapping where appropriate

## Filtering candidates

- moving average
- low-pass filtering
- band-pass filtering
- other filters selected after inspecting the measured data

## Candidate features

- mean
- variance
- standard deviation
- peak-to-peak variation
- temporal correlation
- spectral energy
- dominant frequency
- periodicity
- subcarrier correlation

No particular algorithm is being treated as final yet. The choice should follow the data collected during experiments.
