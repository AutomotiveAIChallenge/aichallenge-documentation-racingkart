# Real-Vehicle Finals Special Page (2026/9/20)

!!! warning "WIP"

    This page is under construction. Confirmed information will be published on this page as it becomes available.

## Schedule

The real-vehicle finals are held for the Sim to Real SW Division only. For how rankings are decided and how fouls are defined, see [Sim to Real Division Real-Vehicle Finals (Japanese)](https://automotiveaichallenge.github.io/aichallenge-documentation-racingkart/competition/sw-class.html#final-abst).

### Overall Schedule of the 9/20 Real-Vehicle Finals

| Start | End | Item |
| --- | --- | --- |
| 08:50 | 09:00 | Opening |
| 09:00 | 10:00 | Semifinal, General Class, Match 1 |
| 10:00 | 11:00 | Semifinal, General Class, Match 2 |
| 11:00 | 12:00 | Semifinal, Student Class, Match 1 |
| 12:00 | 13:00 | Semifinal, Student Class, Match 2 |
| 13:00 | 14:30 | Lunch break, 90 min (semifinal buffer slot) |
| 14:30 | 15:15 | Final, General Class |
| 15:15 | 16:00 | Final, Student Class |
| 16:00 | 16:45 | Break, 45 min (final buffer slot) |
| 16:45 | 17:30 | Final, Mixed Classes |
| 17:30 | 18:00 | Closing (announcement of results) |

- Each semifinal match is 60 minutes; each final match is 45 minutes.
- The detailed match table will be decided on September 19 (the day of the SIM finals).
- The lunch break and the break also serve as buffer slots for the semifinals and finals.
- The team driving next must move to the operation booth (VIP room on the 2nd floor of the building) as soon as the previous match's run has finished.

### Match Schedule { #match-schedule }

#### Semifinal (60 minutes per match) { #semifinal-flow }

| Duration | Item |
| --- | --- |
| 5 min | Changeover and setup |
| 10–25 min | Free run (parameter tuning, etc.) |
| 10 min | Practice match |
| 7–15 min | Match run slot (driving time is 7 minutes) |
| 5 min | Cleanup + score tallying (including penalty deliberation), announcement of the final ranking for this match |

#### Final (45 minutes per match) { #final-flow }

| Duration | Item |
| --- | --- |
| 5 min | Changeover and setup |
| 0–15 min | Standby (remote manual driving practice is possible if time allows) |
| 5 min | Practice match (2 laps only) |
| 7–15 min | Match run slot (driving time is 7 minutes) |
| 5 min | Cleanup + score tallying (including penalty deliberation) |

## Operations Allowed During a Run Slot { #operations }

| Operation | Allowed? |
| --- | --- |
| Starting Autoware | Yes |
| Stopping / restarting Autoware | Yes (not recommended) |
| Parameter tuning via dynamic reconfigure | Yes |
| Manual driving by remote control | Yes |
| Driving with only the steering automated | Yes |
| Re-setting the self-position (localization) | Yes (no need to notify) |
| Gear switching and turbo commands via `ros2 topic` | Yes (no need to notify) |
| Recording rosbags | No |
| Editing launch files / YAML | Not recommended (changes require an Autoware restart to take effect) |
| Changing code / rebuilding | No |
| Replacing the submission | No |

For advance preparation (dynamic reconfigure support, a tuning TUI) and the operating procedure on the day, see [Participant Operations at the Real-Vehicle Finals](https://automotiveaichallenge.github.io/aichallenge-documentation-racingkart/vehicle/operation.html) (Japanese).

## Notes on Running on the Real Vehicle { #real-vehicle-notes }

### V2X Communication Delay { #v2x-delay }

The real vehicles share position information over a wireless network, so delays and packet loss occur. Measurements show an average delay of about 90 ms.
Handling the delay is the responsibility of the algorithm. We recommend extrapolating received positions, discarding stale data, and keeping safety margins that assume the delay.

### Main Cases in Which the Vehicle Stops { #vehicle-stop-cases }

The vehicle may stop during a run in cases such as the following.

- The organizers may perform an emergency stop of the vehicle to ensure safety.
- If the internet connection is lost for a certain period, a safety function stops the vehicle automatically.
- If the vehicle keeps receiving an accelerator command while it is pressed against a wall or otherwise unable to move, the drive motor may stall and the vehicle may stop. Do not keep driving into a wall: when a collision or a stuck state is detected, release the accelerator command promptly. Once the motor has stalled, the vehicle cannot return to the race.

### Traction and Speed { #traction }

- Starting off with the steering turned requires a large torque from the throttle motor. It is known that the vehicle cannot start with the steering at full lock, so we recommend not starting off with the steering turned.
- The top speed of the real vehicle is about 25 km/h.

### Localization and Communication { #localization }

- RTK-GNSS localization depends on an internet connection, so its accuracy may degrade or it may drop out.

### IMU Bias and accel/brake map { #imu-bias-and-accel-brake-map }

- The vehicle-specific IMU bias and accel/brake map settings are configured by the organizers.

### Behavior at the Start { #start-behavior }

- At the start, the vehicles line up in single file, which differs from the simulator.
- No topic announcing the race start is published; the vehicle is only switched from manual mode to autonomous mode. Each team must make sure that its stuck detection does not trigger while waiting at the start position and cause the vehicle to suddenly reverse or start a multi-point turn.

## Information to Be Published Later { #tbd }

- Venue and access, reception time, and division of roles on the day
