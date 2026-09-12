# End to End Division Rules

!!! warning "WIP"
    Some rules are not yet finalized and may be updated.

## End to End Division Overview

The End to End AI Division progresses from qualifying to the finals as follows.

| Item | Schedule | Content | Participating Teams |
| --- | --- | --- | --- |
| End to End Division Qualifying | July 1 – September 1 | Submit presentation documents and a driving video. ([Submission form](https://forms.office.com/pages/responsepage.aspx?id=NVLCok7DvEuOMQxVDG-yrJTP427xWZBKkcBQTu6n-vxUMTU5SkpIRFQ3UDRWUk9WNTBLVjUwR0lUNy4u&route=shorturl)) | Applicants |
| SIM Finals Preparation | September 18 | Operation check and practice runs in the same environment as on the SIM Finals day | Finalist teams that wish to take part |
| End to End Division SIM Finals | September 19 | Race in the simulation environment at the finals venue | Top 16 teams from E2E AI Qualifying |

!!! warning
    - Teams participating in the End to End Division must also participate in the Sim to Real Division.
    - There is no real vehicle race in the End to End Division.

## Common Rules for the End to End Division

### Race Format

- Vehicles race on AWSIM in an environment that replicates the City Circuit Tokyo Bay (CCTB) course.

### Speed and Penalties

Same as the [Sim to Real Division](./sw-class.en.md).

### Available Sensors

- Camera
- LiDAR
- Steer Angle
- Wheel Odometry
- Gear Status

!!! warning "About available sensors"
    Because End to End AI approaches are emphasized, sensors used in the Sim to Real Division that are not listed above, such as GNSS, cannot be used.

### Safety Gates

Same as the [Sim to Real Division](./sw-class.en.md).

### Prohibited Actions

Same as the [Sim to Real Division](./sw-class.en.md).

## End to End Division SIM Qualifying

- In the End to End Division qualifying, the teams' approaches are reviewed.
- Teams submit presentation documents and a driving video, which are scored by judges.
- [Submission form](https://forms.office.com/pages/responsepage.aspx?id=NVLCok7DvEuOMQxVDG-yrJTP427xWZBKkcBQTu6n-vxUMTU5SkpIRFQ3UDRWUk9WNTBLVjUwR0lUNy4u&route=shorturl)

![e2e_submit](./images/e2e_submit.png)

## End to End Division SIM Finals { #semifinal }

### Ranking System

- Races are held with 4 vehicles simultaneously. The race is 6 laps.
- Selection round
    - 4 races are held, with general and student teams mixed.
    - Starting positions are determined by the qualifying review results.
    - The 4 teams that advance to the final race are selected by a combined score of the document review, presentation and race results.
        - Because this division emphasizes the approach, the document review and presentation account for 70% and the race results for 30%. Therefore, a team with a top race result does not necessarily advance to the final.
        - The breakdown of the scores is not disclosed, and inquiries about it cannot be answered.
- Final race
    - A race is held with the 4 teams that advanced from the selection round.
    - Starting positions are determined by the selection round ranking.
    - The final ranking is determined solely by the finishing order of the race.

![e2e_tournament](./images/e2e_sim_tournament.png)

### Rules

- The basic rules follow the common rules above.
- Races start forcibly at the scheduled start time. A team whose setup is not complete either continues working and aims to join mid-race, or retires.
- If a vehicle gets stuck because of a crash or behaves unexpectedly, the organizers will not help it recover.
- Participants may perform any operation from their own terminal and RViz (but cannot operate the AWSIM screen). The expected operations are:
    - Restarting Autoware
    - Re-setting the self-position (localization)
    - Moving the vehicle by manual driving when it is stuck
    - Switching gear and issuing turbo commands with the `ros2 topic` command
- However, you must report to the organizers before operating. Frequent use of manual driving is prohibited. Operations that affect anything other than your own ROS_DOMAIN_ID are also prohibited.
