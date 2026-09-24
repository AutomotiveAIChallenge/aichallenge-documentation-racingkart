# Hardware

## Sensor Configuration

| Sensor | Model / Spec | Role |
| --- | --- | --- |
| GNSS | u-blox ZED-F9R | Obtains the vehicle's latitude, longitude and altitude by satellite positioning |
| IMU | ICM-20948 | Measures acceleration and angular velocity (detects the vehicle's attitude and rotation) |

In the preliminaries these are reproduced as virtual sensors in AWSIM.

## PC Configuration (On-Vehicle PC)

| Item | Spec |
| --- | --- |
| OS | Ubuntu 22.04 |
| CPU | Intel Core i9-11900H |
| Mem | 32 GB |
| Notes | The vehicle control software also runs on the same ECU |

## PC Configuration (SIM Preliminary Environment)

| Item | Spec |
| --- | --- |
| OS | Ubuntu 22.04 |
| CPU | 16 vCPU Intel Xeon Scalable (Cascade Lake) |
| Mem | 64 GB |
| Notes | 3 vCPUs and 12 GiB are allocated to each Autoware |

In the SIM preliminaries, AWSIM and three teams' Autoware instances are launched simultaneously on one instance of the online environment. Because one instance is shared by several teams, ROS_DOMAIN_ID separation and resource allocation are used to prevent interference from other teams' programs.

## PC Configuration (SIM Finals Environment)

| Item | Spec |
| --- | --- |
| OS | Ubuntu 22.04 |
| CPU | Intel Core i7-8700 |
| Mem | 16 GB |
| Notes | Lower spec than the recommended environment (for the reason below) |

In the SIM finals, Autoware runs on its own and AWSIM runs on a separate PC, so PCs with the spec above are used. Specifically, the plan is to connect four Autoware PCs to one AWSIM PC for each race.
