from kalmanfilter.kalman_filter import KalmanFilter
from kalmanfilter.kalman_filter import Radar, Fighter

def main():
    # dt = 4s
    # vx = ?
    # vy =?
    # u_x = calculate
    # u_y = calcualte
    # measurment(km)
    # acc
    # kf = KalmanFilter(dt=4, u_x=, u_y=, x_std_meas=, y_std_meas=, std_acc=, )
    radar = Radar()
    plane = Fighter()
    print(radar)
    print(plane)

if __name__ == "__main__":
    main()
