# borg_parser
A simple tool for parsing results from the [Borg MOEA](http://borgmoea.org/) and doing basic runtime analysis.

# Installation
1. In a cloned version of this repository run `$ pip install .` to install `borg_parser` and its dependencies.


# Example usage
This is also in `example.py`

```
import borg_parser

# Setup
path_to_runtime = borg_parser.datasets.water_energy()
decision_names = ['w_with', 'w_con', 'w_emit']
objective_names = [
    'f_gen',
    'f_with_tot',
    'f_con_tot',
    'f_disvi_tot',
    'f_emit',
    'f_ENS',
    'f_w_with',
    'f_w_con',
    'f_w_emit',
]
metric_names = [
    'coal_output',
    'ng_output',
    'nuclear_output',
    'wind_output',
    'RI_output',
    'OC_output',
    'RC_output',
    'No Cooling System_output',
]

# Create runtime object
runtime = borg_parser.BorgRuntimeDiagnostic(
    path_to_runtime,
    n_decisions=len(decision_names),
    n_objectives=len(objective_names),
    n_metrics=len(metric_names),
)
runtime.set_decision_names(decision_names)
runtime.set_objective_names(objective_names)
runtime.set_metric_names(metric_names)

# Interactive parallel
exp = runtime.plot_interactive_front()
exp.to_html('my_front.html')

# Improvements
fig = runtime.plot_improvements()
fig.savefig('my_improvements.jpg')
```

# TODOs
* Update example to not use "metrics" version of Borg.
* This backend was done in a rather rushed fashion, should be be made more efficient with better error handling.
* There are commented implementations for hypervolume packages that rely on the [pygmo package](https://esa.github.io/pygmo/install.html) which currently has lacking support for windows machinges.