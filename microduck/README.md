# My Microduck — simulation first

First milestone: load the official robot in CPU MuJoCo, inspect contacts and
joint motion, and reset between the upstream stand/sit/fold poses.

## Run on Windows

Install Python 3.13 and Git first. Download or clone this repository, open
PowerShell in its `microduck` folder, and run the one-time setup:

```powershell
python setup.py
```

Setup downloads the official source at the pinned revision, creates `.venv`,
installs dependencies and runs a 10-second headless physics check. Internet
access is required. Existing modified upstream files are preserved: setup
stops if it finds them. The downloaded model retains its upstream licenses.

Double-click `start-simulation.cmd`, or run:

```powershell
.\.venv\Scripts\python.exe simulate.py
```

Space pauses; R resets; 1/2/3 reset to stand/sit/fold. Mouse controls the
MuJoCo camera. Pose selection teleports the initial state; it does not execute
a sit/stand controller. The stock position actuators hold the target angles,
but this is not an active balance controller and the robot can fall.

Headless physics check:

```powershell
.\.venv\Scripts\python.exe simulate.py --headless --seconds 10
```

## Scope and next milestones

1. Inspect the official model and physics locally (this sandbox).
2. Add a compatible pretrained walking policy, its observation contract and
   BAM actuator model; verify forward motion, turns, stopping and recovery.
3. Measure behavior on slopes, low friction and disturbances.
4. Choose a mechanical build and calibrate its mass, joints and actuators.
5. Only then select hardware and plan controlled sim-to-real trials.

No hardware or DIY variant has been selected. This sandbox uses the official
14-actuator simulation, not a validated model of a particular DIY build.
GPU training is separate; this first stage needs only CPU simulation.

## Sources and reproduction

Model: https://github.com/pollen-robotics/microduck_rl
Initial checkout: `b02fdea4902c2b93b7d34a83a6f05da4ececb7d3` (develop).
The upstream checkout lives in `upstream/microduck_rl`; its licenses remain
there (including separate model licensing). We do not modify upstream files.

To recreate the environment: clone that repository into the same path,
create `.venv` with Python, and install the versions in `requirements.txt`.

GitHub stores the source; it does not run the interactive simulator. The
viewer runs on your computer. Headless execution is also possible on a cloud
machine using `python setup.py` and `.venv/bin/python simulate.py --headless`.
