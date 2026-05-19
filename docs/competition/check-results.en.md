# Checking Results

This page explains the rules and ranking system for the competition. Please note that the content of this page may change during the competition period.

## Ranking System

Scores will be calculated based on the following steps. If multiple runs are made, the higher score will be adopted. If a run is stopped, it will be treated as having completed 0 laps.

1. The number of laps completed at the end of the run.

2. The shortest total lap time up to the final lap.

Special Awards: Preliminary rounds will have a seeding system, and finals will have awards.

- Best Lap Time: Measured using SIM in the preliminaries and TOM’S system in the finals.

- Best Comfortable Ride: Measured using SIM in the preliminaries and by measuring the water in a glass in the finals.
  - Interaction and recognition of engineers from various fields.

***Ranking Example***

| Lap | Time     | Gap         | Rank |
|-----|----------|-------------|------|
| 7   | 04:41.000| ―           | 1    |
| 7   | 04:47.000| +00:06.000  | 2    |
| 7   | 04:54.000| +00:13.000  | 3    |
| 6   | 04:18.000| ―           | 4    |
| 6   | 04:29.000| +00:11.000  | 5    |
| 6   | 04:42.000| +00:24.000  | 6    |
| 6   | 04:56.000| +00:38.000  | 7    |
| 5   | 04:05.000| ―           | 8    |
| 5   | 04:23.000| +00:18.000  | 9    |

## Submission

Participants are required to upload their developed software to the evaluation system via the submission page. For details, please refer to [this link](submission.en.md).

### How to Check Results

The result scores will be sent to `result-summary.json`.

#### Result Log Format

Results will be output in the following format in `./output/result-summary.json`.

```json
{
  "laps": [50.12, 50.34, 50.56, 50.78, 50.90],
  "min_time": 50.12,
  "max_jerk": 32.10
}
```
