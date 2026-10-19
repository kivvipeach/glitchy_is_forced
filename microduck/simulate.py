"""First-stage Microduck physics sandbox using the upstream MJCF model."""
import argparse
from pathlib import Path
import queue
import time

import mujoco
import numpy as np


ROOT = Path(__file__).resolve().parent
SCENE = ROOT / "upstream/microduck_rl/src/mjlab_microduck/robot/microduck/scene.xml"


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--headless", action="store_true")
    parser.add_argument("--seconds", type=float, default=5)
    args = parser.parse_args()
    if args.seconds <= 0:
        parser.error("--seconds must be positive")
    model = mujoco.MjModel.from_xml_path(str(SCENE))
    data = mujoco.MjData(model)

    def reset(pose="STAND"):
        key = mujoco.mj_name2id(model, mujoco.mjtObj.mjOBJ_KEY, pose)
        if key < 0:
            raise ValueError(f"Missing pose: {pose}")
        mujoco.mj_resetDataKeyframe(model, data, key)
        mujoco.mj_forward(model, data)

    reset()
    if args.headless:
        for step in range(int(args.seconds / model.opt.timestep)):
            mujoco.mj_step(model, data)
            if not np.isfinite(data.qpos).all():
                raise RuntimeError("Non-finite simulation state")
        print(f"PASS: {data.time:.2f}s physics, {model.nu} actuators, "
              f"{data.ncon} contacts, base height {data.qpos[2]:.3f}m")
        return

    from mujoco import viewer as mj_viewer

    events = queue.SimpleQueue()
    paused = False
    print("Space: pause | R: reset stand | 1: stand | 2: sit | 3: fold")
    print("Pose changes reset the state; these are not learned transitions.")
    with mj_viewer.launch_passive(model, data, key_callback=events.put) as viewer:
        viewer.cam.distance = 0.65
        viewer.cam.azimuth = 135
        viewer.cam.elevation = -20
        while viewer.is_running():
            started = time.perf_counter()
            while not events.empty():
                key = events.get()
                if key == 32:
                    paused = not paused
                elif key in (82, 49, 50, 51):
                    reset({50: "SIT", 51: "FOLD"}.get(key, "STAND"))
            if not paused:
                mujoco.mj_step(model, data)
            viewer.cam.lookat[:] = data.qpos[:3]
            viewer.sync()
            time.sleep(max(0, model.opt.timestep - (time.perf_counter() - started)))


if __name__ == "__main__":
    main()
