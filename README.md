# Reconfigurable Antenna — IEEE AP-S Student Design Contest

Research and development work for the 2026 IEEE AP-S Student Design Contest on multifunctional automotive antennas.

## Project status

This repository is currently focused on research, system definition, and early-stage signal-processing planning. Hardware and algorithms are still being developed and experimentally validated.

## Current direction

The project explores an electronically reconfigurable receiving antenna combined with RF/CSI-based sensing. The broader idea is to use existing wireless signals as opportunistic sensing sources and study whether changes in the wireless channel can provide useful information about human-associated activity.

The system is intended to operate as a closed loop:

**RF environment → reconfigurable antenna → receiver → CSI/RF data → signal processing → spatial decision → antenna control → new measurement**

## Work covered so far

- Problem definition and use case
- Opportunistic RF sensing concept
- CSI-based channel variation analysis
- Reconfigurable antenna concept
- Antenna-state scanning and spatial comparison
- Signal preprocessing and feature extraction pipeline
- Signal-quality scoring
- Closed-loop antenna-state selection
- Raspberry Pi as the high-level controller
- False-positive considerations
- Initial experimental plan
- Candidate performance metrics

## Important note

The ability to detect respiration or reliably identify a survivor has **not** been assumed as a proven result. These are research questions that require controlled experiments.

## Repository structure

```text
docs/
├── project-background.md
├── system-concept.md
├── signal-processing.md
├── reconfigurable-antenna.md
├── experiments.md
├── performance-metrics.md
└── research-status.md

research/
└── research-notes.md

meeting-notes/
└── 2026-10-06.md
```

## Contest context

The IEEE AP-S Student Design Contest calls for a compact multifunctional automotive antenna system, at least two automotive applications, real-time visualization, reproducible demonstration instructions, and a total production cost below US$1,500.

This repository is intended to document the technical work as it develops rather than serve as a final contest submission.
