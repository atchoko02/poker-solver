# Poker Game Tree Solver

A Python-based poker solver that implements Counterfactual Regret Minimization (CFR) to find Nash equilibrium strategies for heads-up poker situations. The solver includes a graphical interface for exploring game trees and analyzing optimal strategies.

## Features

- **Game Tree Generation**
  - Models multi-street betting sequences
  - Configurable bet sizing and raise limits
  - Support for turn and river card runouts

- **Strategy Computation**
  - Implements CFR algorithm for Nash equilibrium approximation
  - Handles complex range vs range equity calculations
  - Computes optimal frequencies for betting, calling, and folding

- **Interactive Visualization**
  - Tree-based GUI for exploring decision points
  - Real-time strategy and regret inspection
  - Dynamic range and frequency visualization

## Usage

Launch the GUI:
```bash
python -m ui.gui
```

### Summary
The application launches with a default configuration:
- Pre-flop ranges: Pocket pairs 99+ for both players
- Board cards: 3♦ J♥ A♠ 7♦ 8♥
- Standard bet sizing for both positions

The interface provides:
- Left panel: Interactive game tree visualization
- Right panel: Node properties and analysis
- Analysis buttons for each node:
  - Range viewer
  - Strategy frequencies
  - Regret values

> Note: Future updates will allow direct configuration of ranges, board cards, and bet sizing through the GUI interface. Currently these must be modified in the source code.

## Requirements

```
Python 3.8+
PyQt5
treys
```

## Authors

- Alex Tchokokam
- Sebastian Baxa