# Experiment 01 — Bluetooth RSSI Spatial Characterization

## Objective

To determine whether received Bluetooth RSSI exhibits measurable variation with angular position at a fixed source-receiver distance.

## Experimental Setup

- RF technology: Bluetooth
- Target device: TestPhone2
- Distance: 6 units
- Angular positions: 0°, 45°, 90°, 135°, 180°, 225°, 270°, 315°
- Measurement: Received Signal Strength Indicator (RSSI)
- Number of angular positions: 8
- Total RSSI samples: 6660

## Method

RSSI measurements were collected independently for each angular position. 
The recorded data were parsed and filtered for the target Bluetooth device.
For each angle, the mean, median, standard deviation, and confidence interval
were calculated.

A one-way ANOVA was then performed to determine whether the observed RSSI
means differed across angular positions. Eta-squared was calculated as an
estimate of effect size.

## Results

| Angle | Samples | Mean RSSI (dBm) | Median | Std. Dev. |
|------:|--------:|----------------:|-------:|----------:|
| 0° | 841 | -60.90 | -60 | 6.61 |
| 45° | 877 | -60.02 | -60 | 4.72 |
| 90° | 907 | -59.50 | -58 | 4.83 |
| 135° | 801 | -63.73 | -63 | 5.60 |
| 180° | 792 | -65.03 | -64 | 4.93 |
| 225° | 854 | -60.69 | -60 | 5.71 |
| 270° | 802 | -62.02 | -62 | 4.69 |
| 315° | 786 | -58.31 | -57 | 5.76 |

### Spatial Difference

- Strongest measured direction: **315°**
- Mean RSSI: **−58.31 dBm**
- Weakest measured direction: **180°**
- Mean RSSI: **−65.03 dBm**
- Maximum measured difference: **6.71 dB**

### Statistical Analysis

- One-way ANOVA F-statistic: **137.6682**
- p-value: **< 0.001**
- Eta-squared (η²): **0.1265**

The ANOVA indicates statistically significant differences among at least some
of the measured angular groups. The calculated eta-squared indicates a
moderate effect in this dataset.

## Interpretation

The experiment demonstrates measurable angular variation in received
Bluetooth RSSI at a fixed distance. The measured difference between the
strongest and weakest angular positions was 6.71 dB.

This provides initial evidence that RSSI measurements can contain useful
spatial information and supports further investigation of RF-based spatial
characterization.

## Limitations

This experiment does not by itself establish antenna directivity or prove
that the observed RSSI variation is caused exclusively by angular position.

Possible contributing factors include:

- Multipath propagation
- Environmental reflections
- Bluetooth device orientation
- Temporal variation
- Changes in the RF environment

Furthermore, the angular measurements were collected sequentially rather
than through repeated randomized trials. Therefore, temporal and
environmental effects cannot be completely separated from the angular effect.

## Next Experiment

A stronger experiment will repeat measurements under controlled conditions
and investigate whether RF measurements change systematically when a human
target is introduced into the propagation environment.

The next stage will move toward human-associated RF variation and eventually
CSI-based signal processing.