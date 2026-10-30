# Proposal

## Hypothesis

Using today's reading and the time of year, we can forecast tomorrow's fine-particle pollution in Washington, DC more accurately than simply assuming tomorrow will look like today, and accurately enough to guide whether outdoor athletic practice should move inside. The quantity we forecast is the next calendar day's 24-hour mean PM2.5 concentration across the District of Columbia monitors, in micrograms per cubic meter (µg/m³), issued at 8:00 pm the evening before.

## Data

Our data come from the U.S. EPA Air Quality System (AQS), which publishes daily PM2.5 readings from regulatory monitors (parameter 88101, in the files `daily_88101_YYYY.zip`). Each record is one monitor's reading for one day. We average the DC monitors (state code 11) into a single value per day, which gives roughly 3,650 days from 2015 through 2024. The monitors use 24-hour filter samples and continuous instruments, and state agencies validate the readings before they are posted to AQS.

What we measure is close to, but not the same as, what the decision needs. The athletic director cares about the air on a school field during afternoon practice, while our data are midnight-to-midnight averages from a handful of fixed monitors that may be miles away. Afternoon levels can run higher or lower than the daily mean, and smoke plumes are patchy, so the gap is partly noise from location and partly bias from time of day. There is also a timing gap: AQS data are validated months after the fact, so a forecast used in practice would have to rely on preliminary AirNow readings, which are noisier.

Because AQS data are produced by a federal agency, they are in the public domain and can be republished. We will post the files on this repository's `data` release.

## Decision affected by the model

Each evening, a high-school athletic director decides whether the next day's outdoor practice should move indoors. Using our forecast, they would move practice inside whenever the predicted probability that PM2.5 exceeds 35.4 µg/m³ is above a set threshold. At that level the AQI enters the "Unhealthy for Sensitive Groups" category, and EPA advises active children and teens to limit heavy outdoor exertion. A false alarm costs a lost field session and a scramble for gym space. A missed bad-air day costs more: athletes doing hard exercise in unhealthy air, with the risk of asthma attacks and liability for the school. Because a miss is the costlier mistake, the director should move practice inside even when the chance of a bad-air day is well below 50%.
