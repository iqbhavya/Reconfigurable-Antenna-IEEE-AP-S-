# Research Notes

This file records the technical direction explored so far.

## Opportunistic RF sensing

Instead of requiring a dedicated transmitter on the target, the system can investigate signals already present in the environment, such as Wi-Fi transmissions from a smartphone.

The useful information is not necessarily the absolute received power. Changes in the wireless channel may be more informative.

## Human-induced channel variation

A human body interacts with electromagnetic propagation. Movement can alter multipath paths, amplitude, phase, and CSI.

Respiration involves smaller periodic movement, so detecting it is expected to be more difficult and more sensitive to noise and environmental changes.

## False positives

Potential causes of RF variation include:

- other people
- rescue workers
- vehicles
- rubble movement
- smartphone movement
- changes in wireless traffic
- other wireless devices
- multipath changes
- RF interference
- receiver noise

Because of this, a single CSI change should not be treated as proof of human presence.

A more useful direction is to combine evidence such as temporal behavior, periodicity, spatial consistency, and persistence.

## Signal quality

A possible quality score can combine:

```text
Q = w1(SNR)
  + w2(CSI stability)
  + w3(temporal variation quality)
  + w4(spatial consistency)
```

The weights and exact implementation are intentionally left open until experimental data is available.

## Spatial decision

For each antenna state:

```text
State → measurement → score
```

The software can compare the scores and select the state with the strongest useful evidence.

## Key point

The research is currently about establishing whether these ideas work experimentally. The repository therefore separates proposed methods from measured results.
