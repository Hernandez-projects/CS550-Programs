'''
Constraint propagation
'''
from csp_lib import sudoku


def AC3(csp, queue=None, removals=None):
    """AC3 constraint propagation

    csp - constraint satisfaction problem
    queue - list of constraints (might be None in which case they are
        populated from csp's variable list (len m) and neighbors (len k1...km):
        [(v1, n1), (v1, n2), ..., (v1, nk1), (v2, n1), (v2, n3), ... (v2, nk2),
         (vm, n1), (vk, n2), ..., (vk, nkm) ]
    removals - List of variables and values that have been pruned.  This is only
        useful for backtracking search which will enable us to restore things
        to a former point

    returns
        True - All constraints have been propagated and hold
        False - A variables domain has been reduced to the empty set through
            constraint propagation.  The problem cannot be solved from the
            current configuration of the csp.
    """

    # Hints:
    # Remember that:
    #    csp.variables is a list of variables
    #    csp.neighbors[x] is the neighbors of variable x
    # I used a simple list to hold tuples for each variable constraint with its neighbors
    if queue is None:
        q = []
        # no given queue so I create with a list of tuples containing all variable neighbor pairs
        for variable in csp.variables:
            for neighbor in csp.neighbors[variable]:
                test = (variable, neighbor)
                q.append(test)
    else:
        q = queue  # when given an initial queue this is all I need
    while q:
        (xi, xj) = q.pop()
        if revise(csp, xi, xj, removals):  # this bit is important for modifying domains
            if not csp.curr_domains[xi]:
                # if the domain of the current variable is empty then the problem cant be solved
                return False
            else:
                for xk in csp.neighbors[xi]:  # adding new tuples to be able to create arc consistency
                    if xk != xj:
                        q.append((xk, xi))
    return True


def revise(csp, Xi, Xj, removals):
    """Return true if we remove a value.
    Given a pair of variables Xi, Xj, check for each value i in Xi's domain
    if there is some value j in Xj's domain that does not violate the
    constraints.

    csp - constraint satisfaction problem
    Xi, Xj - Variable pair to check
    removals - list of removed (variable, value) pairs.  When value i is
        pruned from Xi, the constraint satisfaction problem needs to know
        about it and possibly updated the removed list (if we are maintaining
        one)
    """
    revised = False
    value = csp.curr_domains[Xj]
    # something will only be revised if the variable we are checking against only has one possible value
    # that value will be removed after ensuring it exists in the other variables domain
    if len(value) != 1:
        return revised
    for valueI in csp.curr_domains[Xi]:
        if value[0] == valueI:  # value[0] being the only value present in the domain of Xj
            csp.prune(Xi, valueI, removals)
            revised = True
    return revised
