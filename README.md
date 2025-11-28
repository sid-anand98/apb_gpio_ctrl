# APB GPIO Controller with Secret Toggle

APB3-compliant 8-bit GPIO controller with a hidden secret output toggle feature.

## Problem Description

Implement an APB3 GPIO controller with a special "secret_pin" output that toggles when a specific magic sequence is written to the GPIO register with correct timing.

## Directory Structure

```
.
├── sources/                    # Verilog source files
│   └── apb_gpio_with_secret_toggle.sv
├── tests/                      # Cocotb test files
│   └── test_apb_gpio_toggle_hidden.py
├── docs/                       # Documentation
│   └── Specification.md
├── prompt.txt                  # Task description
├── pyproject.toml              # Python dependencies
└── README.md                   # This file
```

## Requirements

- Python 3.10+
- cocotb >= 1.8.0
- pytest >= 7.0.0
- Icarus Verilog (for simulation)

## Installation

```bash
pip install -e .
```

## Running Tests

```bash
pytest tests/ -v
```

## Features

- APB3-compliant GPIO register interface
- 8-bit GPIO register at address 0x00
- Secret pin toggle on magic sequence: 0x55 → 0xAA → 0x5A
- Timing-sensitive: requires ≥3 clock cycles between writes
- Read operations abort the sequence

See `docs/Specification.md` for complete requirements.

