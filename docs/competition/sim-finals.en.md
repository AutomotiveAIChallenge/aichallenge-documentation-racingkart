# SIM Finals Special Page (2026/9/19)

This page summarizes the venue, schedule, and day-of proceedings for the SIM Finals held on September 19. The SIM Finals are held in two divisions: the Sim to Real division and the End to End division.

## Who this page is for

Teams that have advanced to the SIM Finals, and reserve teams

## Venue

- Tokyo International Exchange Center, Plaza Heisei 3F, [International Exchange Conference Hall](https://www.jasso.go.jp/ryugaku/kyoten/tiec/plazaheisei/facility/hall.html)
- [Access](https://www.jasso.go.jp/ryugaku/kyoten/tiec/access.html)

## Schedule

### Overall schedule

| Date | Venue | Event |
| --- | --- | --- |
| 9/18 (Fri) | International Exchange Center | Pre-event practice |
| **9/19 (Sat)** | **International Exchange Center** | **SIM Finals** |
| 9/20 (Sun) | CCTB | Sim to Real division, Real Vehicle Finals |

### 9/18 Pre-event practice

- On September 18, you can join a pre-event practice session where you can do test runs in the same environment as the actual competition. Participation is optional, but strongly recommended.
- At this event, each team sets up its PC at its own responsibility, and matches start forcibly when the scheduled start time arrives. Being familiar with the operations is therefore extremely important. Teams bringing their own PC in particular can avoid trouble on the SIM Finals day by checking connections and operation in advance.
- Teams in the E2E division can also check the projection of their presentation slides.
- Details and attendance will be announced later.

| Time | Event |
| --- | --- |
| 13:00–17:00 | Practice runs (Sim to Real division) |
| 15:00–17:00 | Practice runs (End to End division) |

### 9/19 SIM Finals overall schedule

| Time | Event |
| --- | --- |
| 9:30–10:30 | Practice runs (Sim to Real division) |
| 10:30–10:40 | Opening and announcement of the match table |
| 10:40–12:00 | Sim to Real division, General class, SIM Finals |
| 12:00–13:00 | Lunch break. Practice runs (End to End division) |
| 13:00–14:20 | Sim to Real division, Student class, SIM Finals |
| 14:30–17:10 | End to End division, SIM Selection Rounds |
| 17:10–17:40 | End to End division, SIM Final Match |
| 18:00– | Networking reception |

- Note: Please complete check-in by 10:00 at the latest.
- Note: In addition to the matches, the day features poster exhibits, sponsor booths, free-play match tables, and a networking reception. At the free-play match tables you can freely enjoy head-to-head runs!

### 9/19 Match schedule (Sim to Real division)

| Start | End | Event |
| ----- | ----- | ------------------------------------- |
| 10:40 | 11:00 | Sim to Real division, General class, Match 1 |
| 11:00 | 11:20 | Sim to Real division, General class, Match 2 |
| 11:20 | 11:40 | Sim to Real division, General class, Match 3 |
| 11:40 | 12:00 | Sim to Real division, General class, Match 4 |
| 13:00 | 13:20 | Sim to Real division, Student class, Match 1 |
| 13:20 | 13:40 | Sim to Real division, Student class, Match 2 |
| 13:40 | 14:00 | Sim to Real division, Student class, Match 3 |
| 14:00 | 14:20 | Sim to Real division, Student class, Match 4 |

- Note: Please gather at the rehearsal table set up at the venue 40 minutes before your match starts. Then, 20 minutes before the match starts, staff will guide you to the waiting area. If you are late, you may be treated as withdrawn / lose by forfeit.
- Note: A 10-minute review of the run is held after each match. Therefore General class Match 4 ends at 12:10, and Student class Match 4 ends at 14:30.

### 9/19 Match schedule (End to End division)

| Start | End | Event |
| ----- | ----- | ------------------------------- |
| 14:30 | 15:10 | End to End division, Selection Round, Match 1 |
| 15:10 | 15:50 | End to End division, Selection Round, Match 2 |
| 15:50 | 16:30 | End to End division, Selection Round, Match 3 |
| 16:30 | 17:10 | End to End division, Selection Round, Match 4 |
| 17:10 | 17:40 | End to End division, Final Match |

- Note: Please gather at the waiting area set up at the venue 40 minutes before your match starts. If you are late, you may be treated as withdrawn / lose by forfeit.
- Note: For the Final Match, please gather at the waiting area at 16:30. This applies to all teams except those taking part in Selection Round Match 4. The teams advancing to the Final Match are announced as soon as Match 4 ends. If you are not at the waiting area, you may be treated as withdrawn / lose by forfeit.
- Note: Please use the pre-event practice day and the practice-run time slots to bring in your PC.

## Sim to Real division proceedings

Please check the rules [here](./sw-class.en.md#sw-division-sim-finals-rules).

!!! info "About the overtaking lane"

    The SIM Finals are run in `s2r-final` mode (overtaking lane on). For the rules, see [Overtaking lane](https://automotiveaichallenge.github.io/aichallenge-documentation-racingkart/competition/sw-class.html#overtake-lane) (Japanese).

### Roles { #s2r-role }

- Operator: sets up and operates the Autoware PC
    - Make sure you remember your login ID and password, which are needed to download your source code
- Presenter: answers questions from the MC during the race run, and conducts the review after the race run (may be the same person as the operator)

!!! info "Request: status visualization"

    We are preparing an app that shows spectators what each team is currently doing (running, fixing a bug, etc.). You should be able to update it just by tapping your current status. We want to reflect it to spectators as close to real time as possible, so please update it whenever your status changes.

### Match flow { #s2r-flow }

| Time (relative to start time) | Activity |
| --- | --- |
| ① 40 min before | Gather at the rehearsal table. Check connections and operation |
| ② 20 min before | Move to the waiting area |
| ③ Start time | Move onto the stage |
| ④ 0–10 min | Setup |
| ⑤ 10–18 min | Race run |
| ⑥ 18–20 min | Clean-up (deleting source code, etc.) |
| ⑦ 20–30 min | Review of the run |

![s2r_sim_flow](./images/s2r_sim_flow.png)

- Each match proceeds according to the timetable above.
- Please gather at the rehearsal table at the back of the main hall by 40 minutes before the start time.
    - The rehearsal table has PCs with the same configuration as in the match.
    - You can do a final check of your operations at the rehearsal table.
- 20 minutes before the start time, move to the waiting area at the front of the main hall.
- At the start time, go up on stage and begin setup.
- Setup consists of (downloading the source code), building, and launching Autoware. If you use a PC you brought, you also need to configure the network.
    - The organizers plan to download in advance the latest source code as of 18:00 on the previous day (9/18). To save time and avoid unexpected network trouble, please use the pre-downloaded files whenever possible.
- Setup time is 10 minutes. When 10 minutes have passed, the run starts even if some team has not finished setting up.
    - The organizers provide minimal support, but in principle setup is your own responsibility.
    - Please make use of the preparation day, the practice runs, and the rehearsal table.
- You may delete the downloaded source code after the run (leaving it is also fine).
- In the 10 minutes after the match, a review of the run is held. Please answer the commentator's questions.
    - Example question: "You lost speed in the first corner. What was the cause?"
    - The presenter who does the review and the operator may be different members, or one person may do both.

### PC configuration { #s2r-pc }

- Each match uses the following five PCs.
    - PC for AWSIM
    - PC for Autoware (for Team A)
    - PC for Autoware (for Team B)
    - PC for Autoware (for Team C)
    - PC for Autoware (for Team D)
- Each team's seat has an Autoware PC, a monitor, a keyboard, a mouse, and a LAN cable.
- Each PC is connected to the AWSIM PC through a switching hub. Internet access is also provided.
- Teams may use a PC they bring, but the organizing staff provide only basic support.
    - A setup guide will be provided separately.

## End to End division proceedings

Please check the rules [here](./ai-class.en.md#ai-division-sim-finals-rules).

### Roles { #e2e-role }

- Operator: sets up and operates the Autoware PC
- Presenter: gives a 5-minute presentation before the race run, and answers questions from the MC during the race run

### Match flow (Selection Rounds) { #e2e-flow }

| Time (relative to start time) | Activity |
| --- | --- |
| ① 40 min before | Move to the waiting area |
| ② Start time | Move onto the stage |
| ③ 0–25 min | - Setup<br>- Presentations (5 min × 4 teams) |
| ④ 25–35 min | Race run |
| ⑤ 35–40 min | Clean-up (moving PCs, etc.) |

![e2e_sim_flow](./images/e2e_sim_flow.png)

- Each match proceeds according to the timetable above.
- Please gather at the waiting area at the front of the main hall by 40 minutes before the start time.
- At the start time, go up on stage and begin setup.
- Setup consists of booting the PC you brought, configuring the network, and launching Autoware.
- Setup time is 25 minutes. When 25 minutes have passed, the run starts even if some team has not finished setting up.
    - The organizers provide minimal support, but in principle setup is your own responsibility.
    - Please make use of the preparation day, the practice runs, and the rehearsal table.
- In parallel with setup, each team gives a 5-minute presentation.
    - Please assign a presenter for the presentation, separate from the operator doing the setup work.
    - Please send your presentation slides in advance.

### Match flow (Final Match) { #e2e-flow-final }

| Time (relative to start time) | Activity |
| --- | --- |
| ① 40 min before | Move to the waiting area |
| ② 5 min before | Announcement of the teams advancing to the Final Match |
| ③ Start time | Move onto the stage |
| ④ 0–20 min | Setup |
| ⑤ 20–30 min | Race run |

- Please gather at the waiting area at the front of the main hall by 40 minutes before the start time.
    - This applies to all teams except those taking part in Selection Round Match 4
- The Final Match proceeds according to the timetable above. The basic flow is the same as the Selection Rounds, but there is no presentation.

### PC configuration { #e2e-pc }

- Each match uses the following five PCs.
    - PC for AWSIM
    - PC brought by a participating team (Team A)
    - PC brought by a participating team (Team B)
    - PC brought by a participating team (Team C)
    - PC brought by a participating team (Team D)
- Each team's seat has an AC power strip, a monitor, a keyboard, a mouse, and a LAN cable. Participants must bring all other equipment they need, including a way to connect to wired LAN (a LAN port or a USB-LAN adapter).
- The LAN cable is connected to the AWSIM PC through a switching hub. Internet access is provided over the same cable.
- Connect the PC you brought to the LAN cable and configure the network.
    - A setup guide will be provided separately, but the organizing staff provide only basic support.
