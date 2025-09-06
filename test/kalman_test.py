import unittest
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.pyplot import step
from requests import delete
from kalmanfilter.kalman_filter import KalmanFilter, Radar, Fighter
from utils.util import plot_three_lines



class MyTestCase(unittest.TestCase):

    def test_kalman_filter(self):
        np.random.seed(42)  # For reproducible results

        # Parameters
        dt = 0.1  # Time step
        total_time = 10.0  # Total simulation time
        steps = int(total_time / dt)
        u_x, u_y = 0.1, 0.05  # Constant accelerations
        std_acc = 0.2  # Process noise magnitude
        x_std_meas = 0.5  # X measurement noise std
        y_std_meas = 0.5  # Y measurement noise std

        # Initialize Kalman Filter
        kf = KalmanFilter(dt=0.1, u_x=0.1, u_y=0.05, std_acc=0.2, x_std_meas=0.5, y_std_meas=0.5)
        # kf = kalmanFilter(dt=0.2, u_x=2, u_y=1, std_acc=0.2, x_std_meas=2, y_std_meas=2)

        # Simulation Data Storage
        true_states = []
        measurements = []
        estimates = []

        # Generate true trajectory and measurements
        true_state = np.array([0, 0, 0, 0]).astype(np.float64)  # [x, y, vx, vy]
        for t in range(steps):
            # Update true state (constant acceleration motion)
            true_state[0] += true_state[2] * dt + (0.5 * u_x * pow(dt, 2))  # 1/2 ax t^2 + vx dt
            true_state[1] += true_state[3] * dt + (0.5 * u_y * pow(dt, 2))  # 1/2 ay t^2 + vy dt
            true_state[2] += u_x * dt  # vx = ax dt
            true_state[3] += u_y * dt  # vy = ay dt
            true_states.append(true_state.copy())

            # Generate noisy measurement
            z_x = true_state[0] + np.random.randn() * x_std_meas  # x + random * error x
            z_y = true_state[1] + np.random.randn() * y_std_meas  # y + random * error y
            z = np.array([[z_x], [z_y]]).astype(np.float64)
            measurements.append(z)

            # Kalman Filter steps
            kf.predict()
            kf.updata(z)  # Update with measurement
            estimates.append(kf.x.copy())  # Store full state estimate

        # Convert lists to arrays for plotting
        true_states = np.array(true_states).astype(np.float64)
        measurements = np.array(measurements).squeeze().astype(np.float64)
        estimates = np.array(estimates).squeeze().astype(np.float64)
        time = np.arange(0, total_time, dt)

        # Plotting
        plt.figure(figsize=(15, 10))

        # 1. Trajectory Plot (XY Path)
        plt.subplot(2, 2, 1)
        plt.plot(true_states[:, 0], true_states[:, 1], 'g-', lw=2, label='True Trajectory')
        plt.plot(measurements[:, 0], measurements[:, 1], 'r.', alpha=0.5, label='Measurements')
        plt.plot(estimates[:, 0], estimates[:, 1], 'b--', lw=1.5, label='Kalman Estimate')
        plt.title('Object Trajectory')
        plt.xlabel('X Position')
        plt.ylabel('Y Position')
        plt.legend()
        plt.grid(True)
        plt.axis('equal')

        # 2. X Position over Time
        plt.subplot(2, 2, 2)
        plt.plot(time, true_states[:, 0], 'g-', label='True X')
        plt.plot(time, measurements[:, 0], 'r.', alpha=0.4, label='Measured X')
        plt.plot(time, estimates[:, 0], 'b-', label='Estimated X')
        plt.title('X Position Estimation')
        plt.xlabel('Time (s)')
        plt.ylabel('X Position')
        plt.legend()
        plt.grid(True)

        # 3. Y Position over Time
        plt.subplot(2, 2, 3)
        plt.plot(time, true_states[:, 1], 'g-', label='True Y')
        plt.plot(time, measurements[:, 1], 'r.', alpha=0.4, label='Measured Y')
        plt.plot(time, estimates[:, 1], 'b-', label='Estimated Y')
        plt.title('Y Position Estimation')
        plt.xlabel('Time (s)')
        plt.ylabel('Y Position')
        plt.legend()
        plt.grid(True)

        # 4. Velocity Components
        plt.subplot(2, 2, 4)
        plt.plot(time, true_states[:, 2], 'g-', lw=2, label='True Vx')
        plt.plot(time, true_states[:, 3], 'm-', lw=2, label='True Vy')
        plt.plot(time, estimates[:, 2], 'b--', label='Estimated Vx')
        plt.plot(time, estimates[:, 3], 'r--', label='Estimated Vy')
        plt.title('Velocity Components')
        plt.xlabel('Time (s)')
        plt.ylabel('Velocity')
        plt.legend()
        plt.grid(True)

        plt.tight_layout()
        plt.savefig("plot.png")

    def test_by_real_parameter(self):
        radar, fighter = Radar(), Fighter()
        iteration: int = 1
        std_acc = 0.2  # Process noise magnitude
        x_std_meas = 0.5  # X measurement noise std
        y_std_meas = 0.5  # Y measurement noise std
        previus_radar_x, previus_radar_y, previus_radar_v_x, previus_radar_v_y = 0, 0, 0, 0
        true_states_at_each_point, measurements_at_each_point, estimates_at_each_point = 3 * [[]]
        true_state = None
        while iteration <= 10:
            np.random.seed(42)  # For reproducible results
            dt, total_time= 4, 20.0
            setps = int(total_time / dt)  # Time step

            if iteration == 1:
                u_x, u_y = getattr(radar, "radar_v_x") / dt, getattr(radar, "radar_v_y") / dt
                kf = KalmanFilter(dt=dt, u_x=u_x, u_y=u_y, std_acc=0.2, x_std_meas=0.5, y_std_meas=0.5)
                setattr(kf, "x", np.matrix([[110 * 1000], [110 * 1000], [1000 * (5/18)], [4 * (5/18)]]))
                true_states_at_each_point.append(np.matrix([[fighter.fighter_x, fighter.fighter_y, fighter.fighter_v_x, fighter.fighter_v_y]]).astype(np.float64))
                true_state = np.array([fighter.fighter_x / 1000, fighter.fighter_y / 1000, fighter.fighter_v_x * 3.6, fighter.fighter_v_y * 3.6]).astype(np.float64)
                measurements_at_each_point.append(np.matrix([radar.radar_x / 1000, radar.radar_y / 1000, radar.radar_v_x * 3.6, previus_radar_v_y * 3.6]).astype(np.float64))
                estimates_at_each_point.append(getattr(kf, "x"))
            else:
                u_x, u_y = (getattr(radar, "radar_v_x") - previus_radar_v_x) / dt, (getattr(radar, "radar_v_y") - previus_radar_v_y) / dt
                kf = KalmanFilter(dt=dt, u_x=u_x, u_y=u_y, std_acc=0.2, x_std_meas=0.5, y_std_meas=0.5)
                setattr(kf, "x", np.matrix([[getattr(radar, "radar_x")], [getattr(radar, "radar_y")], [getattr(radar, "radar_v_x")], [getattr(radar, "radar_v_y")]]))
                true_state = np.array([fighter.fighter_x / 1000, fighter.fighter_y / 1000, fighter.fighter_v_x * 3.6, fighter.fighter_v_y * 3.6]).astype(np.float64)  # [x, y, vx, vy]

            for t in range(setps):
                # Update true state (constant acceleration motion)
                true_state[0] += true_state[2] * dt + (0.5 * u_x * pow(dt, 2))  # 1/2 ax t^2 + vx dt
                true_state[1] += true_state[3] * dt + (0.5 * u_y * pow(dt, 2))  # 1/2 ay t^2 + vy dt
                true_state[2] += u_x * dt  # vx = ax dt
                true_state[3] += u_y * dt  # vy = ay dt

                #update fighter position
                fighter.fighter_x = true_state[0] / 1000
                fighter.fighter_y = true_state[1] / 1000
                fighter.fighter_v_x = true_state[2] * 3.6
                fighter.fighter_v_y = true_state[3] * 3.6

                # true_states_at_each_point.append(true_state.copy())
                previus_radar_x, previus_radar_y, previus_radar_v_x, previus_radar_v_y = getattr(radar, "radar_x"), getattr(radar, "radar_y"), getattr(radar, "radar_v_x"), getattr(radar, "radar_v_y")
                # Generate noisy measurement
                z_x = true_state[0] + np.random.randn() * x_std_meas  # x + random * error x
                z_y = true_state[1] + np.random.randn() * y_std_meas  # y + random * error y
                z = np.array([[z_x], [z_y]]).astype(np.float64)
                setattr(radar, "radar_x", z_x / 1000)
                setattr(radar, "radar_y", z_y / 1000)
                setattr(radar, "radar_v_x", (np.random.randn() * x_std_meas) * 3.6)
                setattr(radar, "radar_v_y", (np.random.randn() * y_std_meas) * 3.6)
                # measurements.append(z)
                # measurements_at_each_point.append(np.array([[z_x], [z_y], [getattr(radar, 'radar_v_x')], [getattr(radar, 'radar_v_y')]]).astype(np.float64))

                # Kalman Filter steps
                kf.predict()
                kf.updata(z)  # Update with measurement
                # estimates.append(kf.x.copy())  # Store full state estimate

            estimates_at_each_point.append(kf.x.copy())
            measurements_at_each_point.append(np.array([[getattr(radar, "radar_x") / 1000], [getattr(radar, "radar_y") / 1000], [getattr(radar, 'radar_v_x') * 3.6], [getattr(radar, 'radar_v_y') * 3.6]]).astype(np.float64))
            true_states_at_each_point.append(np.array([[fighter.fighter_x / 1000], [fighter.fighter_y / 1000], [fighter.fighter_v_x * 3.6], [fighter.fighter_v_y * 3.6]]).astype(np.float64))
            iteration += 1

        print(estimates_at_each_point)

        # plot_three_lines(points1=estimate_x_y, points2=measuremt_x_y, points3=truestate_x_y)

    def test_by_real_parameter_type1(self):
        radar, fighter = Radar(), Fighter()
        iteration: int = 1
        std_acc = 0.2  # Process noise magnitude
        x_std_meas = 0.5  # X measurement noise std
        y_std_meas = 0.5  # Y measurement noise std

        # Initialize empty lists for data collection
        true_states_at_each_point = []
        measurements_at_each_point = []
        estimates_at_each_point = []

        # Set seed once at the beginning for reproducibility
        np.random.seed(42)

        # Maintain true state in meters and m/s
        true_state = np.array([
            fighter.fighter_x,  # Already in meters (setter converts)
            fighter.fighter_y,  # Already in meters
            fighter.fighter_v_x,  # Already in m/s (setter converts)
            fighter.fighter_v_y  # Already in m/s
        ], dtype=np.float64)

        # Pre-calculate constant acceleration (m/s²)
        ax = 10.0
        ay = 2.0

        # Simulation parameters
        dt = 4.0  # Time step (seconds)
        total_time = 200.0  # Total simulation time (seconds)
        total_steps = int(total_time / dt)  # 50 steps

        # Initialize Kalman Filter
        kf = KalmanFilter(dt=dt, u_x=ax, u_y=ay, std_acc=std_acc,
                          x_std_meas=x_std_meas, y_std_meas=y_std_meas)

        # Set initial KF state (convert to meters and m/s)
        kf.x = np.matrix([
            [110 * 1000],  # x (m)
            [110 * 1000],  # y (m)
            [1000 * (5 / 18)],  # vx (m/s)
            [4 * (5 / 18)]  # vy (m/s)
        ])

        for t in range(total_steps):
            # Update true state (constant acceleration motion)
            true_state[0] += true_state[2] * dt + 0.5 * ax * dt ** 2
            true_state[1] += true_state[3] * dt + 0.5 * ay * dt ** 2
            true_state[2] += ax * dt
            true_state[3] += ay * dt

            # Update fighter object (convert to km and km/h for setters)
            fighter.fighter_x = true_state[0] / 1000
            fighter.fighter_y = true_state[1] / 1000
            fighter.fighter_v_x = true_state[2] * 3.6
            fighter.fighter_v_y = true_state[3] * 3.6

            # Generate noisy measurement (in meters)
            z_x = true_state[0] + np.random.randn() * x_std_meas
            z_y = true_state[1] + np.random.randn() * y_std_meas
            z = np.array([[z_x], [z_y]]).astype(np.float64)

            # Update radar's position (setter expects km)
            radar.radar_x = z_x / 1000
            radar.radar_y = z_y / 1000

            # Store data
            true_states_at_each_point.append(true_state.copy())
            measurements_at_each_point.append(z.copy())

            # Kalman Filter steps
            kf.predict()
            kf.updata(z)  # Fixed method name (was 'updata')
            estimates_at_each_point.append(kf.x.copy())

        # Convert results for plotting
        estimate_x_y = [(float(est[0]), float(est[1])) for est in estimates_at_each_point]
        measuremt_x_y = [(float(z[0]), float(z[1])) for z in measurements_at_each_point]
        truestate_x_y = [(float(state[0]), float(state[1])) for state in true_states_at_each_point]

        # Plot results (assuming this function exists)
        plot_three_lines(
            points1=estimate_x_y,
            points2=measuremt_x_y,
            points3=truestate_x_y
        )

        return {
            'estimates': estimates_at_each_point,
            'measurements': measurements_at_each_point,
            'true_states': true_states_at_each_point
        }

    def test_by_real_parameter_type2(self):
        radar, fighter = Radar(), Fighter()
        std_acc = 0.2  # Process noise magnitude
        x_std_meas = 0.5  # X measurement noise std
        y_std_meas = 0.5  # Y measurement noise std

        # Initialize lists for data collection
        true_states_at_each_point = []
        measurements_at_each_point = []
        estimates_at_each_point = []

        # Set seed once at the beginning for reproducibility
        np.random.seed(42)

        # Simulation parameters
        dt = 4.0  # Time step (seconds)
        total_time = 200.0  # Total simulation time (seconds)
        total_steps = int(total_time / dt)  # 50 steps

        # Maintain true state in meters and m/s
        true_state = np.array([
            fighter.fighter_x,  # Already in meters (setter converts)
            fighter.fighter_y,  # Already in meters
            fighter.fighter_v_x,  # Already in m/s (setter converts)
            fighter.fighter_v_y  # Already in m/s
        ], dtype=np.float64)

        # Pre-calculate constant acceleration (m/s²)
        ax = 10.0
        ay = 2.0

        # Initialize Kalman Filter with constant acceleration
        kf = KalmanFilter(dt=dt, u_x=ax, u_y=ay, std_acc=std_acc,
                          x_std_meas=x_std_meas, y_std_meas=y_std_meas)

        # Set initial KF state to match fighter's initial state
        # kf.x = np.matrix([
        #     [fighter.fighter_x],
        #     [fighter.fighter_y],
        #     [fighter.fighter_v_x],
        #     [fighter.fighter_v_y]
        # ])

        for t in range(total_steps):
            # Update true state (constant acceleration motion)
            true_state[0] += true_state[2] * dt + 0.5 * ax * dt ** 2
            true_state[1] += true_state[3] * dt + 0.5 * ay * dt ** 2
            true_state[2] += ax * dt
            true_state[3] += ay * dt

            # Update fighter object (convert to km and km/h for setters)
            fighter.fighter_x = true_state[0] / 1000
            fighter.fighter_y = true_state[1] / 1000
            fighter.fighter_v_x = true_state[2] * 3.6
            fighter.fighter_v_y = true_state[3] * 3.6

            # Generate noisy measurement (in meters)
            z_x = true_state[0] + np.random.randn() * x_std_meas
            z_y = true_state[1] + np.random.randn() * y_std_meas
            z = np.array([[z_x], [z_y]]).astype(np.float64)

            # Update radar's position (setter expects km)
            radar.radar_x = z_x / 1000
            radar.radar_y = z_y / 1000

            # Store data
            true_states_at_each_point.append(true_state.copy())
            measurements_at_each_point.append(z.copy())

            # Kalman Filter steps
            kf.predict()
            kf.updata(z)  # Fixed method name (was 'updata')
            estimates_at_each_point.append(kf.x.copy())

        # Convert results for plotting
        estimate_x_y = [(float(est[0]), float(est[1])) for est in estimates_at_each_point]
        measuremt_x_y = [(float(z[0]), float(z[1])) for z in measurements_at_each_point]
        truestate_x_y = [(float(state[0]), float(state[1])) for state in true_states_at_each_point]

        # Plot results
        plot_three_lines(
            points1=truestate_x_y,
            points2=measuremt_x_y,
            points3=estimate_x_y,
        )

    def test_by_real_parameter_type3(self):
        radar, fighter = Radar(0, 0, 0, 0), Fighter(0, 0, 0, 0)
        std_acc = 5  # Process noise magnitude 5
        x_std_meas = 5000  # X measurement noise std for position radar in direction-x 50
        y_std_meas = 5000 # Y measurement noise std for position radar in direction-y 50
        v_std_meas = 250  # Velocity measurement noise std 3

        # Initialize lists for data collection
        true_states_at_each_point = []
        measurements_at_each_point = []
        estimates_at_each_point = []

        # Set seed once at the beginning for reproducibility
        np.random.seed(42)

        # Simulation parameters
        dt = 4.0  # Time step (seconds)
        total_time = 200.0  # Total simulation time (seconds)
        total_steps = int(total_time / dt)  # 50 steps

        # Maintain true state in meters and m/s
        true_state = np.array([
            fighter.fighter_x,  # Already in meters (setter converts)
            fighter.fighter_y,  # Already in meters
            fighter.fighter_v_x,  # Already in m/s (setter converts)
            fighter.fighter_v_y  # Already in m/s
        ], dtype=np.float64)

        # Initialize Kalman Filter
        kf = KalmanFilter(
            dt=dt,
            u_x=0,  # Will be updated each step
            u_y=0,  # Will be updated each step
            std_acc=std_acc,
            x_std_meas=x_std_meas,
            y_std_meas=y_std_meas
        )

        # Initialize previous velocity for acceleration calculation
        prev_radar_vx = radar.radar_v_x
        prev_radar_vy = radar.radar_v_y

        for t in range(total_steps):
            # Generate noisy position measurement (in meters)
            z_x = true_state[0] + np.random.randn() * x_std_meas
            z_y = true_state[1] + np.random.randn() * y_std_meas

            # Generate noisy velocity measurement (in m/s)
            z_vx = true_state[2] + np.random.randn() * v_std_meas
            z_vy = true_state[3] + np.random.randn() * v_std_meas

            # Update radar's position and velocity (setter expects km and km/h)
            radar.radar_x = z_x / 1000.0
            radar.radar_y = z_y / 1000.0
            radar.radar_v_x = z_vx * 3.6  # m/s to km/h
            radar.radar_v_y = z_vy * 3.6  # m/s to km/h

            # Calculate acceleration from velocity change (in m/s²)
            ax = (radar.radar_v_x - prev_radar_vx) / dt
            ay = (radar.radar_v_y - prev_radar_vy) / dt

            # Update previous velocity
            prev_radar_vx = radar.radar_v_x
            prev_radar_vy = radar.radar_v_y

            # Update Kalman filter acceleration
            kf.u = np.matrix([[ax], [ay]])

            # Update true state with calculated acceleration
            true_state[0] += true_state[2] * dt + 0.5 * ax * dt ** 2
            true_state[1] += true_state[3] * dt + 0.5 * ay * dt ** 2
            true_state[2] += ax * dt
            true_state[3] += ay * dt

            # Update fighter object
            fighter.fighter_x = true_state[0] / 1000.0
            fighter.fighter_y = true_state[1] / 1000.0
            fighter.fighter_v_x = true_state[2] * 3.6
            fighter.fighter_v_y = true_state[3] * 3.6

            # Store data
            true_states_at_each_point.append(true_state.copy())
            measurements_at_each_point.append(np.array([[z_x], [z_y]]))

            # Kalman Filter steps
            kf.predict()
            kf.updata(np.array([[z_x], [z_y]]))
            estimates_at_each_point.append(kf.x.copy())

        # Convert results for plotting
        estimate_x_y = [(float(est[0])/1000.0, float(est[1])/1000.0) for est in estimates_at_each_point]
        measuremt_x_y = [(float(z[0])/1000.0, float(z[1])/1000.0) for z in measurements_at_each_point]
        truestate_x_y = [(float(state[0])/1000.0, float(state[1])/1000.0) for state in true_states_at_each_point]

        # Plot results
        plot_three_lines(
            points1=truestate_x_y,
            points2=measuremt_x_y,
            points3=estimate_x_y,
        )

        # Return results for analysis
        return {
            'true_states': true_states_at_each_point,
            'measurements': measurements_at_each_point,
            'estimates': estimates_at_each_point
        }



if __name__ == '__main__':
    unittest.main()
