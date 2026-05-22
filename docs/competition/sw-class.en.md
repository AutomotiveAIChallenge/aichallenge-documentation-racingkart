# SW Division Rules

## SW Division Overview

The SW Division progresses from qualifying to finals as follows:

| Item | Schedule | Content | Participating Teams |
| --- | --- | --- | --- |
| SW Division SIM Qualifying | July 1 – September 1 | Race in online simulation environment | All participating teams |
| SW Division SIM Finals | September 19 | Race in simulation environment at the finals venue | Top 32 teams from SIM Qualifying |
| SW Division Real Vehicle Finals | September 20 | Real vehicle race at City Circuit Tokyo Bay (CCTB) | Top 8–16 teams from SIM Finals |

## Common Rules for SW Division

### Race Format

- In SIM Qualifying and SIM Finals, vehicles race in a simulated CCTB course environment on AWSIM. In the Real Vehicle Finals, vehicles race at the actual CCTB.
- Races are held with 3–4 vehicles simultaneously.
- The race is 6 laps, and finishing order determines the ranking.
- The time limit is 10 minutes. (TBD)
- Starting positions are random or determined by past performance. (TBD)

!!! info "Changes from previous competitions"
    Previously, competition used a time attack format. Starting this year, competition uses a race format where finishing order among multiple simultaneous vehicles determines ranking. Skills in overtaking other vehicles are now required, not just driving fast.

### Speed and Penalties

- Acceleration limit is approximately 1.0 m/s².
- Speed limit follows the physics model used by the simulator. For real vehicles, the speed is limited to 30 km/h.
- Handicaps may be applied to acceleration and speed based on race position.
- If a collision with course walls or other vehicles occurs, or if invalid acceleration is input, the vehicle's speed will be restricted for a certain time as a penalty.
- Boost items that temporarily increase acceleration are available. (SIM environment only, planned)
- When colliding with a wall, automatic attitude correction is performed. However, this does not 100% prevent the vehicle from becoming stuck after a wall collision. (SIM environment only)

### Available Sensors

- IMU
- GNSS
- Steer Angle
- Wheel Odometry
- V2X information (position of other vehicles)

### Safety Gates

From the Finals onwards, all of the following safety gates must be cleared:

- Obstacle stop
- NPC overtaking
- Lane keeping

### Prohibited Actions

The following actions and code are prohibited.
Code checks will be performed from the Finals onwards.

- Intentionally driving in a dangerous manner.
- Hacking the simulation environment itself. (e.g., intercepting communications of other vehicles or injecting false data)

## SW Division SIM Qualifying Rules

- Matchmaking battles are held in an online simulation environment provided by the organizers.
- Participating teams only need to submit their code. After submission, building, racing, and ranking are performed automatically.
- There is a daily limit on the number of code submissions.

### Ranking System (SIM Qualifying)

When code is submitted, an online race is automatically run with the following 3 vehicles simultaneously:

| Vehicle | Description |
| --- | --- |
| Vehicle 1 | Team that submitted the code (Challenger) |
| Vehicle 2 | Another team with a similar rank to the Challenger (Opponent) |
| Vehicle 3 | NPC provided by the organizers |

Ranking changes based on race results are as follows:

- If the Challenger wins, they move up in the ranking.
- If the time limit is reached or the NPC wins, it is a draw and the ranking does not change.
- In addition to when code is submitted, a team may race as an opponent when other teams submit code. Losing in such cases will also lower the ranking.

## SW Division SIM Finals Rules

- Real-time simultaneous battles are held in the simulation environment on PCs provided by the organizers at the finals venue.
- Participants cannot use their own PCs.
- If a vehicle becomes stuck due to a crash, manual recovery is permitted. (TBD)

### Ranking System (SIM Finals)

There are no NPCs; races are run simultaneously with 4 teams' vehicles. Tournament-style competition between groups of 4 teams is planned.

| Vehicle | Description |
| --- | --- |
| Vehicle 1 | Finalist Team 1 |
| Vehicle 2 | Finalist Team 2 |
| Vehicle 3 | Finalist Team 3 |
| Vehicle 4 | Finalist Team 4 |

## SW Division Real Vehicle Finals Rules

- Real-time simultaneous battles are held using real vehicles at City Circuit Tokyo Bay (CCTB).
- Participants' code runs on PCs installed in the karts. Required PCs are provided by the organizers.
- If a vehicle becomes stuck due to a crash, manual recovery is permitted. (TBD)

### Notes

- Participating teams are required to perform integration work on the real vehicle and be present during the race. (Organizers will provide support)
- Participating teams must stop the vehicle at the operator's instruction and perform remote control as necessary.
- Racing will be stopped under the following conditions:
    - If the course walls are significantly displaced.
    - If the vehicle significantly deviates from the course.
    - If staff instructs a stop for safety or other reasons.
