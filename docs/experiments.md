# Experimental Plan

The current plan is to validate the system progressively rather than assuming the final sensing capability from the beginning.

## Experiment 1 — RF source detection

Place a wireless device at known positions and verify that the receiver can obtain a usable RF/CSI signal.

**Question:** Can a stable measurement be obtained from the selected source?

## Experiment 2 — Directional scanning

Place the source at different angles and compare measurements from different antenna states.

**Question:** Do the antenna states produce distinguishable spatial responses?

## Experiment 3 — Human movement

Keep the RF source controlled and introduce controlled human movement.

**Question:** Does the channel contain measurable variation correlated with the movement?

## Experiment 4 — Respiration-related variation

Use a stationary person and controlled breathing conditions.

**Question:** Is there a measurable periodic component that remains distinguishable from noise?

This is an experiment, not an assumed capability.

## Experiment 5 — Obstruction

Introduce controlled obstacles between the source/person and receiving antenna.

**Question:** How does obstruction affect the extracted features and detection performance?

## Experiment 6 — Closed-loop scanning

Allow the software to scan antenna states, calculate scores, select a promising state, and reconfigure the antenna.

**Question:** Can the complete measure → decide → reconfigure loop work reliably?

## Experimental discipline

Each experiment should record:

- setup
- distance
- antenna state
- RF source
- acquisition settings
- environmental conditions
- processing method
- raw/processed data
- plots
- observations
- limitations

Results should be added only after measurement.
