# Participant Operations at the Real-Vehicle Finals

!!! warning "WIP"

    This page is under construction. Confirmed information will be updated as it becomes available.

This page describes how participating teams operate the real vehicle at the Sim to Real SW Division real-vehicle finals (September 20, City Circuit Tokyo Bay). For the competition rules and how rankings are decided, see the [Sim to Real Division rules (Japanese)](https://automotiveaichallenge.github.io/aichallenge-documentation-racingkart/competition/sw-class.html#final-abst); for the schedule on the day and the operations allowed during a run slot, see the [Real-Vehicle Finals Special Page](../competition/kart-finals.en.md).

!!! warning "The code you submitted in advance runs on the vehicle as-is"
    During a run slot you cannot change or rebuild any code on the vehicle PC. On the day, you can only tune parameters and operate the vehicle manually by remote control. Any value you want to adjust while watching the run **must be implemented so that it can be changed at runtime (dynamic reconfigure)**.

## Part 1: Advance Preparation

### 1-1. Submitting Your Code

Submit the code to be used at the real-vehicle finals to the organizers by the specified deadline.

| Item | Details |
| --- | --- |
| Submission deadline | 9/14 |
| Submission | The complete code to run at the real-vehicle finals (same `aichallenge_submit.tar.gz` format as the SIM qualifiers) |

After submission, the organizers build and launch it on the vehicle to check that it works, and will contact you individually if a problem is found. **The code cannot be replaced after the deadline**, so before submitting, make sure that `make autoware-build` succeeds locally and that the stack launches and drives.

### 1-2. Supporting dynamic reconfigure

Make the parameters you want to tune on the day changeable without restarting the node. Declare them as ROS 2 parameters and receive changes with `rclcpp::Node::add_on_set_parameters_callback` (C++) or `Node.add_on_set_parameters_callback` (Python). Typical targets are control gains, limits on target speed and acceleration/deceleration, and decision thresholds for obstacle avoidance and overtaking.

Parameters that do not support this will not take effect, even if you edit the launch file or YAML on the day, unless you restart Autoware. Restarting is possible but is not recommended because it consumes your limited run slot.

### 1-3. Implementing a Tuning TUI (Recommended)

Tuning on the day is done from a TUI (terminal UI) prepared by each participating team.

| Item | Requirement |
| --- | --- |
| Launch | When the organizers run `make tui` on the vehicle PC, the submission's `aichallenge_submit/tui.bash` is executed inside the autoware container. Include this script in your submission |
| Function | It must let you view and change, while driving, the parameters you made dynamic-reconfigure-capable in 1-2 |
| Runtime environment | It must work inside the autoware container (ROS 2 environment, with `ROS_DOMAIN_ID` matching the stack). It is operated over SSH from the PC in the operation booth, so do not assume X forwarding |

The organizers standardize the launch method so that the TUI is already launched and displayed when a team arrives at the operation booth. `make tui` runs the TUI inside tmux, so the TUI survives an SSH disconnection and you can return to the same screen after reconnecting.

### 1-4. Clearing the Safety Gates (Strongly Recommended)

Clearing the [safety gates](../competition/sw-class.en.md#safety-gate) (obstacle stop, NPC overtaking, lane keeping) is not mandatory but is strongly recommended. At the real-vehicle finals, the number of fouls directly affects the ranking, and collisions and stops count as fouls as they are. For how to run them, see [Running the Safety Gate Scenarios (Japanese)](https://automotiveaichallenge.github.io/aichallenge-documentation-racingkart/development/development-guide.html#safety-gate).

### 1-5. Handling Behavior Specific to the Real Vehicle

There are differences between the simulator and the real vehicle, such as V2X communication delay, starting off with the steering turned, and the starting grid order. Check [Notes on Running on the Real Vehicle](../competition/kart-finals.en.md#real-vehicle-notes) and add any necessary handling to your code. In particular, be sure to add handling before submission so that your stuck detection does not trigger while waiting at the start and make the vehicle reverse or start a multi-point turn.

## Part 2: Operations on the Day

### 2-1. State When You Arrive at the Operation Booth

By the time a participating team arrives at the operation booth, the organizers will have completed the following preparation:

1. The submitted code has been built on the vehicle PC
2. Autoware, driver and zenoh have been launched (rosbags are recorded by the organizers and are not provided to participating teams)
3. The booth PC is connected to the vehicle PC over SSH, and in that terminal the tuning TUI has been launched and is displayed via `make tui`

Participating teams take over operation from this state. All operations on the vehicle PC are performed over this SSH connection.

### 2-2. Tuning with the TUI

Change parameters from the displayed TUI. Changes take effect even while driving. You can also watch the run in RViz ([Remote Operation](remote.en.md)).

The time available for tuning depends on how the match progresses. The semifinal has a free run (10–25 minutes), which is the main tuning time. In the final, the standby time is short and there is no room to fine-tune parameters ([Match Schedule](../competition/kart-finals.en.md#match-schedule)).

!!! warning "Notify the organizers before operating"
    Before performing any operation on the vehicle, including parameter changes, you must notify the organizers (re-setting the self-position and issuing gear-switch and turbo commands via `ros2 topic` do not require notification). Operations that affect anything other than your own team's `ROS_DOMAIN_ID` are prohibited ([Sim to Real Division rules (Japanese)](https://automotiveaichallenge.github.io/aichallenge-documentation-racingkart/competition/sw-class.html#final-rule)).

### 2-3. Remote Manual Operation with a Game Controller

Each participating team is given a game controller (Logicool F310). With it you can operate the vehicle manually and remotely. For the button and axis assignments, see [Remote Operation](remote.en.md).

- **You can switch between autonomous driving and manual operation at any time.**
- Participating teams must recover the vehicle themselves if it gets stuck or behaves unexpectedly. The organizers provide no support (remote operation or physical intervention).
- However, **excessive use of manual driving is prohibited**. In addition, if the organizers judge a situation to be dangerous, they may perform an emergency stop or move the vehicle themselves.
