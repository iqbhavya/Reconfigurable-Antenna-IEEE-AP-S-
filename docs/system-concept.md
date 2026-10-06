# System Concept

## High-level architecture

```text
Wireless/RF source
        |
        v
Reconfigurable receiving antenna
        |
        v
RF receiver / CSI acquisition
        |
        v
Preprocessing
        |
        v
Filtering and feature extraction
        |
        v
Signal-quality / activity score
        |
        v
Spatial comparison
        |
        v
Select antenna state
        |
        v
Control circuit
        |
        v
Reconfigure antenna
        |
        +-------------------> new measurement
```

## Reconfigurable antenna

The antenna is expected to change its RF behavior electronically rather than through mechanical rotation.

Possible reconfiguration elements include:

- PIN diodes
- Varactors
- RF switches

The actual topology and control conditions are still to be determined from the antenna-design work.

A simple abstraction is:

**control state → RF component state → radiation/reception pattern → spatial sensitivity**

## Beam scanning

The receiver can collect measurements for several antenna states.

For example:

```text
State 1 → measurement
State 2 → measurement
State 3 → measurement
State 4 → measurement
...
```

The measurements can then be compared to identify the state producing the most useful sensing signature.

The current conceptual decision is:

```text
best_state = argmax(score_1, score_2, ..., score_n)
```

The corresponding direction becomes the current candidate direction.

## Closed-loop operation

The intended system is adaptive:

**measure → evaluate → select → reconfigure → measure again**

This is different from simply measuring RF power with a fixed antenna.
