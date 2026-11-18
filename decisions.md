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

## 2026-11-17: Build one daily DC series from the AQS monitor files

- Decision. We download `daily_88101_YYYY.zip` for 2015–2024 with `build_data.py` and keep the District of Columbia monitors (state code 11). Monitor-days with less than 75% of the hours reported are dropped. We average the instruments at each site, then the sites, into one value per day in `data/dc_pm25_daily.csv`. On days AQS flags as exceptional events, such as wildfire smoke or fireworks, we keep the readings with the event included and drop the copies with it excluded.
- Why. The decision is about the air the athletes breathe, so smoke days are the days that matter most, even though EPA can set them aside for regulatory purposes. Averaging sites first keeps a site with two instruments from counting twice.
- Alternative. We considered using a single monitor near a school. We set it aside because any one monitor has gaps, and the director needs one number for the city.
- Revisit. If a single site is missing for long stretches, the daily mean shifts with which sites reported. We will check that `n_sites` does not change the level and, if it does, model the sites separately.

## 2026-11-17: Hold out 2022–2024 by date

- Decision. The cutoff date is 1 January 2022. The model is fitted on days from 2015 to 2021 and scored on every day from 2022 to 2024. There is no random draw, so there is no seed. The baseline and the model are scored on the same held-out days, in dollars with `evaluate_cost` from `decision_rule.py`.
- Why. The decision is about tomorrow, so the test has to be on days later than anything the model saw. Three held-out years include the June 2023 Canadian wildfire smoke, which is exactly the kind of day the director needs to catch.
- Alternative. We considered a random 20% of days. We rejected it because neighboring days are strongly correlated, so a random split would let the model see the day before and the day after each test day and would overstate its skill.
- Revisit. Days above 35.4 µg/m³ are rare, so the held-out dollar cost rests on a handful of days. If the held-out set has fewer than five such days, we will also report a rolling-origin evaluation by year so that the comparison does not hinge on one or two days.
- Data. Both the model and its score use the validated AQS daily mean, midnight to midnight. A forecast run live at 8:00 pm would only have preliminary AirNow readings for that day, and only through 8:00 pm, so our held-out score is somewhat optimistic about how well the forecast would do in practice.

## 2026-11-17: Forecast with a log-linear regression and a lognormal predictive distribution

- Decision. The model is a least-squares regression of log PM2.5 on day $d$ on the log of the reading on day $d-1$, the log of the seven-day mean ending on day $d-1$, and the sine and cosine of the day of the year. The residuals are treated as normal with a constant standard deviation, so tomorrow's PM2.5 is lognormal, and the probability that it exceeds 35.4 µg/m³ feeds the rule from the 2026-11-14 loss entry. The baseline is persistence: tomorrow equals today, and practice moves inside when today was above 35.4 µg/m³.
- Why. Persistence and season are the two effects the proposal named, and the log scale makes them multiplicative and keeps forecasts positive. The model gives a probability rather than a single number, which the cost-based threshold needs. It is small enough for every member to explain each coefficient.
- Alternative. We considered gradient-boosted trees with weather inputs. We set them aside for now because the probability of a rare day is what matters, and a tree model would need a separate calibration step that our few bad-air days cannot support.
- Revisit. If the probabilities are badly calibrated on the held-out days, or the model misses the first day of smoke events, we will add a forecast input, such as NOAA smoke or the AirNow next-day forecast, or use heavier-tailed residuals.
