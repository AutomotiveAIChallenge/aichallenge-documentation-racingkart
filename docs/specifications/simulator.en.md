# Simulator

## Overview

This page describes the specifications of the simulator used in the AI Challenge.

The simulator is based on the open-source autonomous driving simulator "[AWSIM](https://github.com/tier4/AWSIM)" developed for Autoware.

## Commandline Options

| Option     | Type   | Default    | Description                                           |
| ---------- | ------ | ---------- | ----------------------------------------------------- |
| --timeout  | float  | 420.0      | Set session timeout seconds.                          |
| --endless  | bool   | false      | Enable/disable session timeout.                       |
| --pit-stop | bool   | true       | Enable/disable features related to pit-stop.          |
| --replay0  | string |            | Load driving logs and replay as a different vehicle.  |

Use `result-details.json` for the driving log for replay. Also, replay supports 10 vehicles from `--replay0` to `--replay9`.

## Keyboard Operation

| Operation          | Key               |
| ------------------ | ----------------- |
| Quit               | Esc               |
| Reset              | Space             |
| Switch camera      | C                 |
| Accel              | Arrow Up          |
| Brake              | Arrow Down        |
| Steering           | Arrow Left, Right |
| Gear (D)           | D                 |
| Gear (R)           | R                 |
| Gear (N)           | N                 |
| Gear (P)           | P                 |

## Topic Operation

| Topic                                | Type                           | Description                           |
| ------------------------------------ | ------------------------------ | ------------------------------------- |
| /aichallenge/awsim/status            | std_msgs.msg.Float32MultiArray | Get status of the simulation.         |
| /aichallenge/awsim/change_time_scale | std_msgs.msg.Float32           | Set the timescale for the simulation. |
| /aichallenge/awsim/reset             | std_msgs.msg.Empty             | Reset the simulation.                 |

The above `/aichallenge/awsim/status` has the following structure.

| Index | Value           |
| ----- | --------------- |
| 0     | session timeout |
| 1     | lap count       |
| 2     | lap time        |
| 3     | section         |
| 4     | timescale       |

## Vehicle (Racing Kart)

The vehicle conforms to the specifications of the [EGO Vehicle]in AWSIM and is designed with specifications close to an actual racing kart.

![vehicle-appearance](./images/vehicle-appearance.png)

### Parameters

The following table summarizes the vehicle parameters.

| **Item**               | **Value** |
| ---------------------- | --------- |
| Vehicle Weight         | 160 kg    |
| Length                 | 200 cm    |
| Width                  | 145 cm    |
| Front Wheel Diameter   | 24 cm     |
| Front Wheel Width      | 13 cm     |
| Front Wheel Tread      | 93 cm     |
| Rear Wheel Diameter    | 24 cm     |
| Rear Wheel Width       | 18 cm     |
| Rear Wheel Tread       | 112 cm    |
| Maximum Steering Angle | 80°       |
| Maximum Acceleration   | 3.2 m/s^2 |

#### Vehicle Component

The following table summarizes the settings of the Vehicle component. For detailed information of the setting.

| **Item**                            | **Value** |
| ----------------------------------- | --------- |
| **Vehicle Settings**                |           |
| Use Inertia                         | Off       |
| **Physics Settings (experimental)** |           |
| Sleep Velocity Threshold            | 0.02      |
| Sleep Time Threshold                | 0         |
| Skidding Cancel Rate                | 0.236     |
| **Input Settings**                  |           |
| Max Steer Angle Input               | 80        |
| Max Acceleration Input              | 3.2       |

#### Rigidbody Component

The following table summarizes the settings of the Rigidbody component. For more information, see.

| **Item**     | **Value** |
| ------------ | --------- |
| Mass         | 160       |
| Drag         | 0         |
| Angular Drag | 0         |

### CoM Position

CoM (Center of Mass) is the mass center of the vehicle Rigidbody. The CoM position is set at the center of the vehicle and at the height of the wheel axles.

![side-view-of-com](./images/side-view-of-com.png)

![top-view-of-com](./images/top-view-of-com.png)

### Vehicle Collider

Vehicle collider is used to detect collision between the vehicle and other objects or checkpoints. The vehicle collider is created based on the mesh of the vehicle object.

![body-collider](./images/body-collider.png)

### Wheel Colliders

The vehicle has a total of four wheel colliders - one for each wheel, simulating the vehicle on a four-wheel model, rather than a kinematic bicycle model.

![wheel-collider](./images/wheel-collider.png)

The Wheel Collider is set as follows. For more details on wheel colliders, please refer to below.

| **Item**              | **Value** |
| --------------------- | --------- |
| Mass                  | 1         |
| Radius                | 0.12      |
| Wheel Damping Rate    | 0.25      |
| Suspension Distance   | 0.001     |
| **Suspension Spring** |           |
| Spring (N/m)          | 35000     |
| Damper (N\*s/m)       | 3500      |
| Target Position       | 0.01      |

### Sensor Configuration

#### GNSS

The GNSS is mounted at the following position relative to the vehicle base link.

| **Item** | **Value** |
| -------- | --------- |
| x        | 0.0 m     |
| y        | 0.0 m     |
| z        | 0.0 m     |
| roll     | 0.0 rad   |
| pitch    | 0.0 rad   |
| yaw      | 0.0 rad   |

#### IMU

The IMU is mounted at the following position relative to the vehicle base link.

| **Item** | **Value** |
| -------- | --------- |
| x        | 0.0 m     |
| y        | 0.0 m     |
| z        | 0.0 m     |
| roll     | 0.0 rad   |
| pitch    | 0.0 rad   |
| yaw      | 0.0 rad   |
