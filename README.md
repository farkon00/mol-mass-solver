# Molecular Mass Solver

Compute the molecular mass of your favorite compound whether or not it can or will exist.

Requires: Python 3

Setup:
```shell
git clone https://github.com/farkon00/mol-mass-solver
cd mol-mass-solver
python3 main.py
```

Usage:
```shell
$ python3 main.py
H2O
18
Ca(OH)2
97
^C
$ python3 main.py -v
CO2
1 * 12 + 2 * 16 = 44
^C
```

Exit using Ctrl + C

You can use verbose mode using `-v` flag to display the underlying calculations. Consider using [rlwrap](https://github.com/hanslub42/rlwrap) for line history available on both apt (ubuntu/debian) and dnf (fedora). i.e. use arrow keys for history.

```shell
rlwrap python3 main.py
```
