# Decisions

This file is the history of the project. Append an entry when a choice changes the work: the quantity, the data, the split, the model, the loss, or the action. Leave old entries in place. A later entry can reverse an earlier one. If a result depends on a random draw, record the seed under Why. The split entry records the cutoff date, or the seed and the fraction. The pull request that merges the code names this entry.

## 2026-10-30: Forecast next-day DC PM2.5 for an outdoor-practice decision

- Decision. We will forecast the next day's 24-hour mean PM2.5 (µg/m³) across the District of Columbia AQS monitors, issued at 8:00 pm the evening before. The forecast supports a high-school athletic director, who moves outdoor practice indoors whenever the predicted probability of exceeding 35.4 µg/m³ (the start of the AQI's "Unhealthy for Sensitive Groups" range) is above a threshold set by the loss.
- Why. EPA AQS offers more than ten years of daily, validated, public-domain data for DC, so we can post the files on the `data` release. The decision comes up every day, and its costs are lopsided, since missing a bad-air day is worse than moving inside for nothing. That makes it a good fit for a loss-based decision rule. We forecast the concentration itself rather than a simple yes or no, so the model still learns from the many ordinary days while giving the director the probability they need.
- Alternative. We considered forecasting the daily maximum 8-hour ozone level, which crosses the unhealthy threshold more often in DC summers and would give us more bad-air days to learn from. We set it aside because ozone matters mainly in the warm months, while PM2.5 covers the whole school year. We also considered forecasting day-ahead electricity demand, but chose a decision that a school can act on directly.
- Revisit. If 2015–2024 has too few days above 35.4 µg/m³ to check whether the predicted probabilities are calibrated, we will lower the action threshold to a more common level that a cautious school could reasonably use, such as the upper end of the Moderate range, or switch to ozone. If the DC monitors have long gaps in coverage, we will add nearby monitors in Maryland and Virginia.


## 2026-11-14: Define costs and decision threshold for indoor practice

- Decision. We propose a false-alarm cost of $100 for unnecessarily moving practice indoors and a missed-event cost of $900 for keeping students outside when PM2.5 exceeds 35.4 µg/m³. These are illustrative planning costs, not measured school expenses. The resulting probability threshold is 100 / (100 + 900) = 0.10. Practice moves indoors when the predicted probability exceeds 10%.

- Why. Missing a dangerous pollution event has greater consequences than unnecessarily moving practice indoors. The higher missed-event cost represents potential health-related disruption and school liability. A cost-based threshold helps minimize expected decision loss rather than simply maximizing prediction accuracy.

- Alternative. We considered using a 50% probability threshold. However, that would treat the two mistakes as equally costly and could result in more missed pollution events. We therefore chose a threshold based on the relative costs.

- Revisit. We will revise the assumed costs if more reliable school-specific estimates become available. We will also compare the model's total decision cost against the baseline using held-out data. The model has not yet been evaluated.
