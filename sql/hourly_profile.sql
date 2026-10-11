-- UTC hour profile. Translate to Ontario local time in a later, documented step.
SELECT CAST(strftime('%H', timestamp) AS INTEGER) AS hour_utc,
       COUNT(*) AS observations,
       ROUND(AVG(demand_mw), 2) AS mean_demand_mw,
       ROUND(MAX(demand_mw), 2) AS peak_demand_mw
FROM observations
GROUP BY hour_utc
ORDER BY hour_utc;
