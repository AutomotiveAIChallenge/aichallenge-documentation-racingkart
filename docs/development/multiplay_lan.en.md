# Multiplay (Multiple PCs on a LAN)

Using the `make dev4` command launches AWSIM and four instances of Autoware on a single PC to enable multi-vehicle driving. However, this approach has limitations: it places a very heavy load on the PC, and all vehicles must run the exact same Autoware source code.

By connecting multiple PCs to the same network and running Autoware individually on each PC, you can overcome these limitations. This enables competitive multi-team racing using different source codes. Additionally, distributing the processing load eliminates the need to run AWSIM on the Autoware PCs, allowing participation even with lower-spec PCs.

Note that the system configuration for the Simulation Finals follows the method described on this page.

## Requirements

- 1 to 5 PCs capable of network connection (via LAN cable or Wi-Fi)
- 1 router or network switch (switching hub)

## Configuration

AWSIM can be run on a dedicated PC, or together on one of the PCs running Autoware. Two configuration examples are shown below.

- Although 4 Autoware PCs are listed below, you can operate with any number of PCs from 1 to 4.
- IP address configuration is required only when using a network switch. It is unnecessary when using a router (with DHCP enabled).
- The IP addresses listed are examples; you do not necessarily need to use the exact same values. If they conflict with settings on other network interfaces, please configure different addresses.

### Configuration Pattern 1: Running AWSIM on a Dedicated PC

| PC Name | Description | IP Address (When Using a Network Switch) | `ROS_DOMAIN_ID` |
| :--- | :--- | :--- | :--- |
| AWSIM PC | PC for running AWSIM | 192.168.10.1 | - |
| Autoware PC 1 | PC for running Autoware | 192.168.10.11 | 1 |
| Autoware PC 2 | PC for running Autoware | 192.168.10.12 | 2 |
| Autoware PC 3 | PC for running Autoware | 192.168.10.13 | 3 |
| Autoware PC 4 | PC for running Autoware | 192.168.10.14 | 4 |

### Configuration Pattern 2: Running AWSIM and Autoware on the Same PC

| PC Name | Description | IP Address (When Using a Network Switch) | `ROS_DOMAIN_ID` |
| :--- | :--- | :--- | :--- |
| Autoware PC 1 | PC for running Autoware + AWSIM | 192.168.10.11 | 1 |
| Autoware PC 2 | PC for running Autoware | 192.168.10.12 | 2 |
| Autoware PC 3 | PC for running Autoware | 192.168.10.13 | 3 |
| Autoware PC 4 | PC for running Autoware | 192.168.10.14 | 4 |

## Procedure

### 1. Disable ROS 2 Settings on the Host PC

When running Autoware and AWSIM, the ROS 2 and CycloneDDS instances inside the Docker container are used. Because active ROS 2 or CycloneDDS settings on the host PC may interfere with communication, disable them first.

- If any ROS 2-related environment variables are configured in `~/.bashrc` or similar files on the host PC, disable them by commenting out the corresponding lines with a `#` at the beginning:
  - `ROS_DOMAIN_ID`
  - `ROS_LOCALHOST_ONLY`
  - `RMW_IMPLEMENTATION`
  - `CYCLONEDDS_URI`
- Restart your terminal to apply the changes, then run the following command and verify that **nothing is output**:

```bash
echo $ROS_DOMAIN_ID
```

### 2. Connect All PCs to the Same Network

#### When Connected to a Router (Ubuntu)

Enable DHCP using the following steps:

1. Open **Settings** → **Network**.
2. Click the gear icon next to `<Network Connected Name Router to>` and select the **IPv4** tab.
3. Configure and apply the settings as follows:
   - **IPv4 Method**: `Automatic (DHCP)`
   - **DNS**: `Automatic`
   - **Routes**: `Automatic`

#### When Connected to a Network Switch (Ubuntu)

Configure a static IP address using the following steps:

1. Open **Settings** → **Network**.
2. Click the gear icon next to `<Network Connected Name Network Switch to>` and select the **IPv4** tab.
3. Configure and apply the settings as follows (refer to the "Configuration" table above and set a unique last octet for each PC):
   - **IPv4 Method**: `Manual`
   - **Address**: `192.168.10.ooo` (e.g., `192.168.10.1`, `192.168.10.11`, etc.)
   - **Netmask**: `255.255.255.0`
   - **Gateway**: Leave blank

*Note: In either case, once configuration is complete, it is recommended to unplug and replug the LAN cable so the settings take effect immediately (unplug the cable → wait 5 seconds → plug the cable back in).*

### 3. Verify IP Connectivity

Verify that network communication between the PCs is working properly.

- First, identify the IP addresses of the other PCs you want to communicate with:
  - **When using a network switch**: Use the static IP addresses configured in the previous step (e.g., `192.168.10.1`, `192.168.10.11` to `192.168.10.14`).
  - **When using a router**: Since IP addresses are assigned automatically, run the `ip a` command in the terminal on each PC to check its assigned IP address.

- Once you have confirmed the target IP address, run the following command to test connectivity (replace `192.168.10.ooo` with the target PC's IP address):

```bash
ping 192.168.10.ooo
```

If the connection is successful, response messages (such as round-trip times) will be displayed continuously (press `Ctrl + C` to stop).

### 4. Configure CycloneDDS

Autoware uses CycloneDDS as its communication middleware. Configure CycloneDDS inside the Docker container so that it properly uses the network interface connected to the router (or network switch).

- First, run the `ip a` command to identify the network interface name connected to the router (or network switch). If your PC has multiple LAN ports, unplugging and replugging the Ethernet cable makes it easier to identify which interface changes to `UP`.
- In the example output below, `enx607` is the target interface:

```console
1: lo: ...
    ...
2: docker0: ...
    ...
3: enx607: <BROADCAST,MULTICAST,UP,LOWER_UP> ...
    ...
```

- Next, run the following commands to configure CycloneDDS (replace `enx607` with the interface name you identified above):

```bash
IF_LOCAL=enx607    # Change this to your identified network interface name
cd ~/aichallenge-racingkart/
./setup.bash network if $IF_LOCAL
```

### 5. Set the ROS 2 Domain ID

Open the configuration file (`.env`) with the following command and set `ROS_DOMAIN_ID` to a value from `1` to `4` according to your starting position. Refer to the "Configuration" table above for the mapping between starting positions and `ROS_DOMAIN_ID`.

```bash
code ~/aichallenge-racingkart/.env
```

```bash
# Set according to your starting position (uncomment only the ID to use)
ROS_DOMAIN_ID=1
#ROS_DOMAIN_ID=2
#ROS_DOMAIN_ID=3
#ROS_DOMAIN_ID=4
```

### 6. Verify ROS 2 Connectivity

Verify that ROS 2 communication works properly across the PCs and that traffic is properly isolated by `ROS_DOMAIN_ID`.

- First, publish test topics from any one PC (sender). Open four terminals, enter the container in each, and publish topics with `ROS_DOMAIN_ID` set from `1` to `4`:

```bash
# Terminal 1 (Publish topic for ROS_DOMAIN_ID=1)
cd ~/aichallenge-racingkart/
make autoware-bash
ROS_DOMAIN_ID=1 ros2 topic pub -r 1 /chatter1 std_msgs/msg/String "data: 'Hello World 1'"

# In Terminals 2 to 4, also run `make autoware-bash` first, then run each of the following:
ROS_DOMAIN_ID=2 ros2 topic pub -r 1 /chatter2 std_msgs/msg/String "data: 'Hello World 2'"
ROS_DOMAIN_ID=3 ros2 topic pub -r 1 /chatter3 std_msgs/msg/String "data: 'Hello World 3'"
ROS_DOMAIN_ID=4 ros2 topic pub -r 1 /chatter4 std_msgs/msg/String "data: 'Hello World 4'"
```

- Next, on each PC being verified (receiver), confirm that `ROS_DOMAIN_ID` is set correctly and that the corresponding topic is received:

```bash
cd ~/aichallenge-racingkart/
make autoware-bash
echo $ROS_DOMAIN_ID
ros2 topic list
```

### 7. Launch AWSIM (On One PC Only)

Launch AWSIM on any single PC connected to the network. Run one of the following commands depending on the number of vehicles (Autoware PCs) running simultaneously:

```bash
cd ~/aichallenge-racingkart

# Run one of the following according to the number of vehicles
make simulator-dev     # For 1 vehicle
make simulator-dev2    # For 2 vehicles
make simulator-dev3    # For 3 vehicles
make simulator-dev4    # For 4 vehicles
```

### 8. Launch Autoware (On Each PC)

Launch Autoware on each Autoware PC connected to the network. Note that this command does not launch AWSIM.

```bash
cd ~/aichallenge-racingkart
make autoware-simulator
```
