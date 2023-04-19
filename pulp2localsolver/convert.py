import pulp
import localsolver

def convert(pulp_problem: pulp.LpProblem, ls: localsolver.LocalSolver):
    """Converter from pulp to localsolver

    .. code-block:: python

        import pulp

        prob = pulp.LpProblem(sense=pulp.Maximize)

        x = pulp.LpVariable("x", cat="Binary")
        y = pulp.LpVariable("y", cat="Binary")
        prob += x + y
        prob += 2 * x + y <= 1

    We can convert this pulp problem to localsolver model by pulp2localsolver

    .. code-block:: python

        import pulp2localsolver

        with localsolver.LocalSolver() as ls:
            model = pulp_to_localsolver
            ls.solver()

    Parameters
    ----------
    pulp_problem : pulp.LpProblem
    ls : localsolver.LocalSolver

    Returns
    -------
    model : localsolver.LSModel
    ls_variables : dict of localsolver.LSOperator
    """

    #
    # Declare the optimization model
    #
    model = ls.model
    
    ls_variables = dict()
    for var in pulp_problem.variables():
        assert (
            var.getLb() is not None
        ), f"Lower bound of variable must not be None: variable name {var.getName()}"
        assert (
            var.getUb() is not None
        ), f"Upper bound of variable must not be None: variable name {var.getName()}"
        if var.cat == "Continuous":
            ls_variables[var.getName()] = model.float(var.getLb(), var.getUb())
        elif var.cat == "Integer":
            ls_variables[var.getName()] = model.int(var.getLb(), var.getUb())
    
    def lp_exp(const, var_dicts):
        elms = []
        for var_dict in var_dicts:
            name, value = var_dict["name"], var_dict["value"]
            elms.append(value * ls_variables[name])
        return model.sum(elms) + const
    
    # convert objective function
    obj = lp_exp(pulp_problem.objective.constant, pulp_problem.objective.to_dict())
    if pulp_problem.sense == pulp.LpMinimize:
        model.minimize(obj)
    else:
        model.maximize(obj)
    
    for const in pulp_problem.constraints.values():
        if "coefficients" in const.to_dict():
            exp = lp_exp(const.constant, const.to_dict()["coefficients"])
        else:
            exp = lp_exp(const.constant, const.to_dict())
        if const.sense == 0:
            model.constraint(exp == 0)
        elif const.sense == -1:
            model.constraint(exp <= 0)
        elif const.sense == 1:
            model.constraint(exp >= 0)
    
    return model, ls_variables



def localsolver_solve(pulp_problem : pulp.LpProblem):

    # solve
    with localsolver.LocalSolver() as ls:
        model, ls_variables = convert(pulp_problem, ls)
        model.close()
        ls.solve()

        # decode result
        var_dict = {var.name: var for var in pulp_problem.variables()}
        for ls_var_name, ls_var in ls_variables.items():
            var_dict[ls_var_name].varValue = ls_var.value
