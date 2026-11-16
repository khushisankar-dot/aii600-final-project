import numpy as np

# Illustrative planning costs in dollars (decisions.md, 2026-11-14)
FALSE_ALARM_COST = 100
MISSED_BAD_AIR_COST = 900
PM25_LIMIT = 35.4  # µg/m³; above this is Unhealthy for Sensitive Groups


def decision_threshold(false_alarm_cost=FALSE_ALARM_COST,
                       missed_cost=MISSED_BAD_AIR_COST):
    """Probability above which moving indoors has the lower expected cost."""
    return false_alarm_cost / (false_alarm_cost + missed_cost)


def move_indoors(probability, false_alarm_cost=FALSE_ALARM_COST,
                 missed_cost=MISSED_BAD_AIR_COST):
    """True where practice should move indoors. Accepts a number or an array."""
    p = np.asarray(probability, dtype=float)
    if np.any(np.isnan(p)) or np.any((p < 0) | (p > 1)):
        raise ValueError("Probabilities must be between 0 and 1")
    return p > decision_threshold(false_alarm_cost, missed_cost)


def evaluate_cost(actions, actual_pm25, false_alarm_cost=FALSE_ALARM_COST,
                  missed_cost=MISSED_BAD_AIR_COST, limit=PM25_LIMIT):
    """Total decision cost in dollars on held-out days."""
    indoors = np.asarray(actions, dtype=bool)
    pm = np.asarray(actual_pm25, dtype=float)
    if indoors.shape != pm.shape:
        raise ValueError("Inputs must have equal lengths")
    if np.any(np.isnan(pm)):
        raise ValueError("Drop days with missing PM2.5 before scoring")
    unhealthy = pm > limit
    false_alarms = indoors & ~unhealthy
    misses = ~indoors & unhealthy
    return float(false_alarm_cost * false_alarms.sum()
                 + missed_cost * misses.sum())


if __name__ == "__main__":
    print("Threshold:", decision_threshold())
    print("5% risk:", move_indoors(0.05))
    print("25% risk:", move_indoors(0.25))
