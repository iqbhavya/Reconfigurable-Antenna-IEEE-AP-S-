# Reconfigurable Antenna

## Purpose

The antenna is intended to provide electronically selectable spatial sensitivity.

Instead of physically rotating the receiver, different RF states can be selected electronically.

## Possible implementation

Candidate technologies include:

- PIN diodes
- Varactors
- RF switches

The final implementation depends on the antenna topology, available hardware, operating frequency, bias requirements, and measured radiation patterns.

## Antenna states

A conceptual state table is:

| State | Control condition | Sensing direction |
|---|---|---|
| S1 | V1 / control 1 | Direction 1 |
| S2 | V2 / control 2 | Direction 2 |
| S3 | V3 / control 3 | Direction 3 |
| S4 | V4 / control 4 | Direction 4 |

The actual control values and directions will be filled in after antenna characterization.

## Interface with software

The software should not assume that the Raspberry Pi directly generates arbitrary RF bias voltages.

The intended architecture is:

**Pi decision → DAC/control circuit → bias voltage/control signal → antenna switching network**

The mapping between software state and physical antenna state will come from hardware measurements.
