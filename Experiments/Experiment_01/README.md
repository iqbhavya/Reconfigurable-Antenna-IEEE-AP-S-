# Bluetooth RF Spatial Characterization

Experimental analysis of Bluetooth RSSI variation with angular position.

## Experiment 01

The objective is to determine whether received Bluetooth RSSI changes
measurably with angular position at a fixed distance.

### Setup

- Technology: Bluetooth
- Target device: TestPhone2
- Distance: 6 units
- Angular positions: 0° to 315° in 45° increments
- Total RSSI samples: 6660

### Main Result

The strongest measured mean RSSI was -58.31 dBm at 315°,
while the weakest was -65.03 dBm at 180°.

Maximum measured difference: 6.71 dB.

One-way ANOVA:
F = 137.6682
p < 0.001

Eta-squared:
η² = 0.1265

## Repository Structure

- `data/` — raw measurement logs
- `src/` — processing and statistical analysis scripts
- `results/` — generated data and figures
- `docs/` — experiment documentation

## Limitations

The experiment demonstrates angular RSSI variation but does not by itself
prove antenna directivity. Multipath, device orientation, environmental
reflections and temporal variation may contribute to the observed results.

Repeated randomized measurements are required for stronger validation.