description: Official documentation for the Autonomous Driving AI Challenge (Racing Kart): Autoware/ROS 2/AWSIM/Docker-based simulation overview, rules, setup, specs, tutorials, and AI guide.

# Japan Automotive AI Challenge 2026

## FY2026 Videos

<div class="video-carousel" data-videos="current">
  <noscript>
    <ul>
      <li><a href="https://www.youtube.com/watch?v=K_ToeWGitbk">Guide 01: Introduction</a></li>
      <li><a href="https://www.youtube.com/watch?v=5BowSyA8hV8">Guide 02: Autoware</a></li>
      <li><a href="https://www.youtube.com/watch?v=MabDMP6f-Ek">Talk 1: Launch of the End-to-End AI Category (TIER IV)</a></li>
      <li><a href="https://www.youtube.com/watch?v=cGJK4Zlm11c">Talk 2: Community-born AI Chatbot (TPAC)</a></li>
      <li><a href="https://www.youtube.com/watch?v=fGzGK3MC1Gw">Talk 3: The Wabi-Sabi of the AI Challenge (SUBARU)</a></li>
      <li><a href="https://www.youtube.com/watch?v=jrDxfqbDJd4">Talk 4: GNSS for Autonomous Driving (Nikon-Trimble)</a></li>
      <li><a href="https://www.youtube.com/watch?v=Sh-8HNGfQaw">Talk 5: Toward Social Implementation (AIST)</a></li>
      <li><a href="https://www.youtube.com/watch?v=4YcWzPdrdbE">Talk 6: Cooperative Driving with V2X (UTokyo Tsukada Lab)</a></li>
      <li><a href="https://www.youtube.com/watch?v=nG4jIycigBo">Talk 7: The World of Autonomous Racing (GMO)</a></li>
    </ul>
  </noscript>
</div>

## Past Competition Videos

<div class="video-carousel" data-videos="past">
  <noscript>
    <ul>
      <li><a href="https://www.youtube.com/watch?v=z3pqjLJnENo">2025 Preliminary Award Ceremony Digest</a></li>
      <li><a href="https://www.youtube.com/watch?v=G07HQNn1_tU">2025 Final Digest</a></li>
      <li><a href="https://www.youtube.com/watch?v=_wvVNh3_Axo">2025 Final (Day 2)</a></li>
      <li><a href="https://www.youtube.com/watch?v=yjgMUAnJHKw">2025 AI vs Racer Digest</a></li>
      <li><a href="https://www.youtube.com/watch?v=Mynxk4GBAzA">2025 Simulation Footage</a></li>
      <li><a href="https://www.youtube.com/watch?v=COZDHMm4E_8">2024 EV Kart Test Run</a></li>
      <li><a href="https://www.youtube.com/watch?v=FGGTUcfV7nU">2024 Documentary</a></li>
    </ul>
  </noscript>
</div>

## Concept

!!! info

    This competition is a new initiative aimed at discovering and nurturing engineers who will lead the future automotive industry in the new technological domains known as CASE and MaaS.

    The competition involves not only developing programs for autonomous driving mobility but also competing in driving competitions with these developed programs. It aims to provide a platform for engineers, researchers, and students involved in computer science, AI, software, and information processing to challenge themselves, learn, and create organic connections.

## Objectives

### The Role of the Competition from a Technical Perspective

- Learn SDV (Software Defined Vehicle) development through software integration while understanding hardware
- Learn Continuous Integration / Continuous Deployment (CI/CD)
- Conduct development using Open Source Software (OSS) as a platform for innovation towards social implementation

### The Role of the Competition in Human Resource Development

- Promote participation of engineers from various fields
- Accelerate skill development through the provision of educational content
- Learn how to develop SDVs by reconciling real machines and simulators
- Innovate through digital twin simulations
- Create "aspirations" and "passion and excitement" by combining technical competition with entertainment, using motorsport as a theme

## Overview

### Preliminary Round

The preliminary round will be conducted through online simulations. The competition aims to achieve faster lap times on the course using AWSIM, which is oriented towards digital twin simulations. Participants will not only learn the structure of Autoware but also adjust parameters for behavior and decision-making parts and develop new algorithms as needed.

### Final Round

The final competition will be conducted using an EV racing kart as the competition vehicle. Participants will apply the knowledge gained from simulations to real vehicles and tackle challenges unique to real vehicles that cannot be replicated in AWSIM.

For example, participants will be challenged to adjust parameters for application to real vehicles and develop algorithms for noise handling and delay countermeasures that cannot be replicated in simulations.

## Awards

<!-- The total prize money is over 1 million yen. For details, please refer to the [racingkart Autonomous Driving AI Challenge Overview](https://www.jsae.or.jp/jaaic/racingkartver/summary/). -->

## Vehicle

![TOM'S Racing Kart](./assets/racing-kart.jpeg)

## Challenges

The racing kart will drive around a circuit course and compete for the time it takes to complete a set number of laps. Although the karts will be driving alone this time, in the future they will be driving together with others. Therefore, there is a challenge to avoid virtual objects placed on the course.
