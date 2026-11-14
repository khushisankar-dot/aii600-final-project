# Proposed costs in dollars (team should confirm)
FALSE_ALARM_COST = 100
MISSED_BAD_AIR_COST = 900
PM25_LIMIT = 35.4

def decision_threshold(false_alarm_cost=FALSE_ALARM_COST,
                       missed_cost=MISSED_BAD_AIR_COST):
    """Probability at which moving indoors becomes cheaper."""
    return false_alarm_cost / (false_alarm_cost + missed_cost)


def move_indoors(probability):
    """Decide whether practice should move indoors."""
    if not 0 <= probability <= 1:
        raise ValueError("Probability must be between 0 and 1")

    return probability > decision_threshold()


def evaluate_cost(actions, actual_pm25):
    """Calculate total decision cost on held-out days."""
    if len(actions) != len(actual_pm25):
        raise ValueError("Inputs must have equal lengths")

    total_cost = 0

    for indoors, pollution in zip(actions, actual_pm25):
        unhealthy = pollution > PM25_LIMIT

        if indoors and not unhealthy:
            total_cost += FALSE_ALARM_COST
        elif not indoors and unhealthy:
            total_cost += MISSED_BAD_AIR_COST

    return total_cost


# Small example
print("Threshold:", decision_threshold())
print("5% risk:", move_indoors(0.05))
print("25% risk:", move_indoors(0.25))
