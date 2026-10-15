# Sim to Real Division Rules

!!! warning "WIP"
    Some rules are not yet finalized and may be updated.

## Sim to Real Division Overview

The Sim to Real SW Division progresses from qualifying to the finals as follows.

| Item | Schedule | Content | Participating Teams |
| --- | --- | --- | --- |
| Sim to Real Division SIM Qualifying | July 1 – September 1 | Race in the online simulation environment | All participating teams |
| SIM Finals Preparation | September 18 | Operation check and practice runs in the same environment as on the SIM Finals day | Teams among the top 32 of SIM Qualifying that wish to take part |
| Sim to Real Division SIM Finals | September 19 | Race in the simulation environment at the finals venue | Top 32 teams from SIM Qualifying |
| Sim to Real Division Real Vehicle Finals | September 20 | Real vehicle race at City Circuit Tokyo Bay (CCTB) | Top 16 teams from the SIM Finals |

## Common Rules for the Sim to Real Division

### Race Format

- In SIM Qualifying and the SIM Finals, vehicles race on AWSIM in an environment that replicates the City Circuit Tokyo Bay (CCTB) course. In the Real Vehicle Finals, real karts race on site at CCTB.
- Races are held with 3–4 vehicles running simultaneously.
- Starting positions are determined by past results.

!!! info "Changes from previous competitions"
    Previous competitions used a time attack format. From this year, the competition uses a race format with multiple vehicles running simultaneously. Driving fast is not enough; the ability to overtake other vehicles is also required. In addition, in the Real Vehicle Finals, not only speed but also having few collisions is evaluated.

### Speed and Penalties

- The acceleration limit is approximately 1.0 m/s². (Breakdown: acceleration limit 1.37, rolling resistance 0.37)
- The speed limit follows the physics model used by the simulator. On the real vehicle, speed is limited to about 25 km/h.
- Depending on the in-race position, a handicap may be applied to acceleration and speed. (SIM environment only)
- When one of the following penalties is incurred, speed is limited to **5 km/h** for a fixed period. The type is the name shown on the HUD and in the race result. (SIM environment only)
    - Penalties exist to prevent driving that falls under the [Prohibited Actions](#prohibited).
    - The length of the speed limit is proportional to the danger. Driving that obstructs other vehicles is penalized the longest, and over-acceleration, which only affects your own vehicle, the shortest.

| Type | Condition | Speed limit |
| --- | --- | --- |
| `CRASH` | Your front bumper touches another vehicle's rear bumper. While reversing, contact between your rear bumper and another vehicle's front bumper also triggers it | 10 seconds |
| `WALL` | Contact with a wall. Contact between vehicles is treated as `CRASH` and is not counted as `WALL` | 5 seconds |
| `OVER` | Over-acceleration. The acceleration input before clamping exceeds **3 m/s²**, or the input rate is **250 Hz** or higher | 2 seconds |
| `BLOCK` | Overtaking lane violation (see below) | 20 seconds |

In a rear-end collision, the vehicle that hits is penalized; the vehicle that is hit is not exempt. While contact continues, the `CRASH` limit time keeps being renewed.

If a vehicle that is reversing collides with a vehicle behind it, **the reversing vehicle (the one in front) also receives `CRASH`**. Because contact between your rear bumper and another vehicle's front bumper triggers it, both the reversing vehicle and the vehicle behind that it hit are penalized. When reversing, for example to return to the course, wait until the vehicles behind have passed before moving.

When a penalty is triggered, its type is shown in red next to the speed display on the HUD, and speed drops to 5 km/h.

??? example "HUD display examples"
    ![penalty_crash](../assets/penalty_crash.png)

    `CRASH` triggered after rear-ending the vehicle ahead.

    ![penalty_wall](../assets/penalty_wall.png)

    `WALL` triggered after touching a wall.

- A boost item that temporarily increases acceleration is available. (SIM environment only)

#### Overtaking Lane { #overtake-lane }

In the SIM Finals, to discourage driving that blocks the path of vehicles behind, designated sections of the course are defined as an **overtaking lane**. AWSIM judges this automatically. (SIM Finals only. Not applied to the End to End Division.)

??? info "Detailed rules and appearance"
    - The overtaking lane is drawn on the road surface as a **light-blue rectangle**.
    - A vehicle whose entire body is inside the overtaking lane and that is running at **27 km/h or faster** is an **attacker**. While an attacker is present, the overtaking lane pulses orange.
    - While an attacker is present, any other vehicle touching the overtaking lane at **27 km/h or slower** commits a violation unless it has fully left the lane within **3 seconds**. Accelerating does not remove the obligation to leave.
    - While an attacker is present, a vehicle outside the overtaking lane that touches it at **less than 27 km/h** also commits a violation.
    - A vehicle that commits a violation receives a `BLOCK` penalty (**speed limited to 5 km/h for 20 seconds**). The HUD shows `BLOCK` and the remaining seconds.

    ![overtake_lane_normal](../assets/overtake_lane_normal.png)

    The normal state. The light-blue area of the road surface is the overtaking lane.

    ![overtake_lane_active](../assets/overtake_lane_active.png)

    While a vehicle at 27 km/h or faster is inside the overtaking lane, the lane turns orange.

There are no restrictions if you do not enter the overtaking lane. To practice under the same conditions, start AWSIM with `make simulator-s2r-final` and run `make autoware-simulator` in another terminal (see also the [Simulator specifications](../specifications/simulator.en.md)). Frequently asked questions are collected in the [FAQ (Japanese)](https://automotiveaichallenge.github.io/aichallenge-documentation-racingkart/faq.html#overtake-lane).

### Available Sensors

- IMU
- GNSS
- Steer Angle
- Wheel Odometry
- Gear Status
- V2X information (positions of other vehicles)

### Safety Gates { #safety-gate }

Clearing all of the following safety gates is strongly recommended. It is not mandatory, but to win races with multiple vehicles it is important that your vehicle can drive while clearing these safety gates. They can be run locally with `make gate1` (obstacle stop), `make gate2` (overtaking) and `make gate3` (lane keeping); see the [Development Guide](../development/development-guide.en.md).

- Obstacle stop
- NPC overtaking
- Lane keeping

### Prohibited Actions { #prohibited }

The following actions and code are prohibited.
Code checks will be performed from the Finals onwards.

- Intentionally driving in a dangerous manner.
- Intentionally weaving or driving in a way that obstructs other vehicles.
- Using information about vehicles behind you obtained via V2X to obstruct their path. This includes squeezing, weaving and unnecessary deceleration. Referring to information about vehicles behind for safety checks, for example when returning to the course in reverse, is not prohibited.
- Hacking the environment itself. (For example, eavesdropping on other vehicles' communication or injecting fake data.)

## Sim to Real Division SIM Qualifying

### Overview { #preliminaries-abst }

- Matchmaking battles are held in the online simulation environment provided by the organizers.
- Participating teams only submit code. After submission, building, racing and ranking are performed automatically.
- For details, see the [Submission Procedure](./submission.en.md).

### Ranking System { #preliminaries-race }

- Races are held with 3 vehicles simultaneously. The race is 6 laps, and the position in each race is determined by finishing order.
- When code is submitted, a race with the following 3 vehicles is run online automatically. The rating goes up or down depending on the race result. The higher the rating, the higher the rank.

| Vehicle | Description |
| --- | --- |
| Vehicle 1 | The team that submitted the code (challenger) |
| Vehicle 2 | Another team close to the challenger's rank band (opponent) |
| Vehicle 3 | NPC provided by the organizers |

### Rules { #preliminaries-rule }

- The basic rules follow the common rules above.
- There is a daily limit on the number of code submissions.

## Sim to Real Division SIM Finals { #semifinal }

### Overview { #semifinal-abst }

- Real-time simultaneous battles are held in the simulation environment on PCs provided by the organizers at the SIM Finals venue.
- For details of the SIM Finals, see the [SIM Finals special page](./sim-finals.en.md).

### Ranking System { #semifinal-race }

Ranking within each race

- Races are held with 4 vehicles simultaneously. The race is 6 laps, and the position in each race is determined by finishing order.
    - However, if the time runs out before a vehicle finishes, the more laps + sections completed, the higher the position.
    - If still tied, the fewer penalties, the higher the position.
    - If still tied, the SIM Qualifying position decides.
- Starting positions are determined by the SIM Qualifying ranking.

Ranking for the SIM Finals as a whole

- Each class runs 4 races, and the top 2 teams of each race advance to the Real Vehicle Finals on September 20.
- Due to time constraints, no races between the top teams are held in the SIM Finals to decide the overall order.
- The SIM Finals ranking is decided by grouping teams by finishing position in their race. The 4 teams that finished 1st in their race are ranked 1–4, the 4 teams that finished 2nd are ranked 5–8, the 4 teams that finished 3rd are ranked 9–12, and the 4 teams that finished 4th are ranked 13–16. Within each group, the order is decided as follows.
    1. The fewer penalties, the higher the position (penalties are rear-end collisions, wall collisions and input anomalies detected automatically by AWSIM)
    2. If the number of penalties is equal, the SIM Qualifying rank

    *This follows the same idea as the Real Vehicle Finals on September 20: driving that takes safety into account is prioritized.<br>
    *This ranking is used to decide the starting positions in the Real Vehicle Finals. There is no award based on the SIM Finals ranking, so the SIM Finals are positioned as a selection round rather than a final.

![s2r_sim_tournament](./images/s2r_sim_tournament.png)

### Rules { #semifinal-rule }

- The basic rules follow the common rules above.
- Races start forcibly at the scheduled start time. A team whose setup is not complete either continues working and aims to join mid-race, or retires.
- If a vehicle gets stuck because of a crash or behaves unexpectedly, the organizers will not help it recover.
- Participants may perform any operation from their own terminal and RViz (but cannot operate the AWSIM screen). The expected operations are:
    - Restarting Autoware
    - Re-setting the self-position (localization)
    - Moving the vehicle by manual driving when it is stuck
    - Switching gear and issuing turbo commands with the `ros2 topic` command
- However, you must report to the organizers before operating. Frequent use of manual driving is prohibited. Operations that affect anything other than your own ROS_DOMAIN_ID are also prohibited.

## Sim to Real Division Real Vehicle Finals

### Overview { #final-abst }

- Real-time simultaneous battles are held with real vehicles at City Circuit Tokyo Bay (CCTB).
- Each team's code runs on the PC mounted on the kart. The PCs needed for the work are provided by the organizers.
- Because real vehicles are used, the match structure and rules take safety into account.
- Details will be announced later.

### Ranking System { #final-race }

- Races are free-running within a time limit, with 4 vehicles simultaneously.
- Vehicles keep running for the specified time (7 minutes). There is no upper limit on the number of laps.
- The ranking is decided in the following order.
    1. The fewer fouls, the higher the position
    2. If the number of fouls is equal, the more laps + sections completed, the higher the position
        - For example, between a team that completed 2 laps and reached the 2nd section of lap 3 and a team that completed 2 laps and reached the 3rd section of lap 3, the latter ranks higher
    3. If still tied, the SIM Finals ranking
- Starting positions are determined by the SIM Finals ranking. However, for safety, the spacing between vehicles is larger than in the SIM.
- After the tournament within each class, a mixed-class race among the top teams of each class is held.

![s2r_kart_tournament](./images/s2r_kart_tournament.png)

### Definition of Fouls { #final-foul }

The following driving counts as a foul (regardless of whether it is intentional, accidental, or caused by a malfunction).

- Driving extremely slowly, or stopping partway without reason
    - This is to prevent passive driving intended to avoid fouls
- Driving while obstructing the path of other vehicles
- Obstructing other vehicles when returning to the course
- Stopping anywhere other than the edge of the course (if you need to stop, pull over to the edge of the course)
- Collisions **other than** the following cases
    - Grazing another vehicle while trying to overtake it (when it is not path obstruction)
    - A collision from behind when the vehicle ahead decelerates suddenly
    - A collision from behind when the vehicle ahead is returning to the course
    - A collision from behind when the vehicle ahead is driving dangerously
- Prohibited actions listed in the rules

### Rules { #final-rule }

- The basic rules follow the common rules above.
- If a vehicle gets stuck because of a crash or behaves unexpectedly, the organizers will not help it recover (neither by remote operation nor by physical intervention).
    - However, the organizers may perform an emergency stop or move the vehicle if they judge the situation to be dangerous.
- Participants may perform any operation from their own terminal and RViz.
- However, you must report to the organizers before operating. Frequent use of manual driving is prohibited. Operations that affect anything other than your own ROS_DOMAIN_ID are also prohibited.

### Notes

- Participating teams must carry out the integration work on the real vehicle and be present during the run. (The organizers support the work.)
- Participating teams must stop the vehicle on the operator's instruction and, if necessary, operate it remotely.
- The run is stopped in the following cases.
    - The course walls have moved significantly.
    - The vehicle has deviated significantly from the course.
    - Staff instruct a stop for safety or other reasons.
