# pulp2localsolver

A PuLP to LocalSolver converter

## Install

```
git clone https://github.com/nariaki3551/pulp2localsolver.git
cd pulp2localsolver
pip install .
```

## Setting

You have to install Python interface of LocalSolver.
Please read this document https://www.localsolver.com/docs/last/installation/pythonsetup.html ,
and install localsolver python package.

## Usage


```python
import pulp

# create pulp LpProblem
prob = pulp.LpProblem("sample")

# define variables
x = pulp.LpVariable("x", lowBound=0, upBound=10)
y = pulp.LpVariable("y", lowBound=0, upBound=10)
z = pulp.LpVariable("z", cat="Binary")

# set objective
prob += x + y + z + 1

# set constraints
prob += 3 * x + 5 * y <= 15
prob += 2 * x + y >= 4
prob += x - y == 1

print(prob)


# solve problem using LocalSolver
#   and decode solution to pulp variable objects
import pulp2localsolver

pulp2localsolver.localsolver_solve(prob)

print("Result")
print("x", x.value())
print("y", y.value())
print("z", z.value())
print("obj", prob.objective.value())
```
