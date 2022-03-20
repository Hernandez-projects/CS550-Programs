from csp_lib.backtrack_util import (first_unassigned_variable,
                                    unordered_domain_values,
                                    no_inference)


def backtracking_search(csp,
                        select_unassigned_variable=first_unassigned_variable,
                        order_domain_values=unordered_domain_values,
                        inference=no_inference):
    """backtracking_search
    Given a constraint satisfaction problem (CSP),
    a function handle for selecting variables, 
    a function handle for selecting elements of a domain,
    and a function handle for making inferences after assignment,
    solve the CSP using backtrack search

    Returns two outputs:
       dictionary of assignments or None if there is no solution
       Number of variable assignments made in backtrack search (not counting
       assignments made by inference)
    """
    def backtrack(assignment, csp):
        if csp.goal_test(csp.infer_assignment()):
            return assignment
        # if the puzzle is solved then all variables are assigned
        var = select_unassigned_variable(assignment, csp)
        for value in order_domain_values(var, assignment, csp):
            if csp.nconflicts(var, value, assignment) == 0:  # using nconflicts to check for consistency
                csp.assign(var, value, assignment)   # since the assignment is consistent it is assigned
                removals = csp.suppose(var, value)
                if inference(csp, var, value, assignment, removals):

                    result = backtrack(assignment, csp)
                    if result is not None:
                        return result, csp.nassigns
                # all of this happens when the result is None meaning we need to backtrack the assignments that lead
                # to an unsolvable puzzle and try again
                csp.restore(removals)
        csp.unassign(var, assignment)
        return None, csp.nassigns

    # See Figure 6.5 of your book for details
    return backtrack({}, csp)  # recursive call to fill an empty dictionary


