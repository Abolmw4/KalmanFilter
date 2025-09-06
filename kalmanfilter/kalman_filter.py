import numpy as np

class Radar:
    def __init__(self, radar_x: float=120.5, radar_y: float=118, radar_v_x: float=1100, radar_v_y: float=500) -> None:
        self.radar_x = radar_x
        self.radar_y = radar_y
        self.radar_v_x = radar_v_x
        self.radar_v_y = radar_v_y

    @property
    def radar_x(self) -> float:
        return self.__radar_x

    @property
    def radar_y(self) -> float:
        return self.__radar_y

    @property
    def radar_v_x(self) -> float:
        return self.__radar_v_x

    @property
    def radar_v_y(self) -> float:
        return self.__radar_v_y

    @radar_x.setter
    def radar_x(self, value: float) -> None:
        self.__radar_x = value * 1000

    @radar_y.setter
    def radar_y(self, value: float) -> None:
        self.__radar_y = value * 1000

    @radar_v_x.setter
    def radar_v_x(self, value: float) -> None:
        self.__radar_v_x = value * (5 / 18)

    @radar_v_y.setter
    def radar_v_y(self, value: float) -> None:
        self.__radar_v_y = value * (5 / 18)

    def __repr__(self):
        return f"Radar(radar_x={self.radar_x}km, radar_y={self.radar_y}km, radar_v_x={self.radar_v_x}km/h, radar_v_y={self.radar_v_y}km/h)"

class Fighter:
    def __init__(self, fighter_x: float=115, fighter_y: float=111, fighter_v_x: float=1010, fighter_v_y: float=700.5) -> None:
        self.fighter_x = fighter_x
        self.fighter_y = fighter_y
        self.fighter_v_x = fighter_v_x
        self.fighter_v_y = fighter_v_y

    @property
    def fighter_x(self) -> float:
        return self.__fighter_x

    @property
    def fighter_y(self) -> float:
        return self.__fighter_y

    @property
    def fighter_v_x(self) -> float:
        return self.__fighter_v_x

    @property
    def fighter_v_y(self) -> float:
        return self.__fighter_v_y

    @fighter_x.setter
    def fighter_x(self, value: float) -> None:
        self.__fighter_x = value * 1000

    @fighter_y.setter
    def fighter_y(self, value: float) -> None:
        self.__fighter_y = value * 1000

    @fighter_v_x.setter
    def fighter_v_x(self, value: float) -> None:
        self.__fighter_v_x = value * (5 / 18)

    @fighter_v_y.setter
    def fighter_v_y(self, value: float) -> None:
        self.__fighter_v_y = value * (5 / 18)

    def __repr__(self):
        return f"Fighter(fighter_x={self.fighter_x}km, fighter_y={self.fighter_y}km, fighter_v_x={self.fighter_v_x}km/h, fighter_v_y={self.fighter_v_y}km/h)"

class KalmanFilter:
    def __init__(self, dt: float, u_x: float, u_y: float, std_acc: float, x_std_meas: float, y_std_meas: float) -> None:
        '''

        :param dt: Time changes
        :param u_x: acceleration on x-direction
        :param u_y: acceleration on y-direction
        :param std_acc: process noise magnitude
        :param x_std_meas: standard deviation of the measurement in x-direction
        :param y_std_meas: standard deviation of the measurement in y-direction
        '''

        self.dt = dt    # delta time
        self.u = np.matrix([[u_x], [u_y]])  # acceleration (or control variable)
        self.x = np.matrix([[0], [0], [0], [0]])    # Initial state

        # state transition matrix
        self.A = np.matrix([[1, 0, self.dt, 0],
                            [0, 1, 0, self.dt],
                            [0, 0, 1, 0],
                            [0, 0, 0, 1]])

        # Define the Control Input Matrix B
        self.B = np.matrix([[(self.dt**2)/2, 0],
                            [0,(self.dt**2)/2],
                            [self.dt,0],
                            [0,self.dt]])

        # measurement matrix
        self.H = np.matrix([[1, 0, 0, 0],
                            [0, 1, 0, 0]])

        # initial noise covariance
        self.Q = np.matrix([[pow(self.dt, 4)/4, 0, pow(self.dt, 3)/2, 0],
                            [0, pow(self.dt, 4)/4, 0, pow(self.dt, 3)/2],
                            [pow(self.dt, 3)/2, 0, pow(self.dt, 2), 0],
                            [0, pow(self.dt, 3)/2, 0, pow(self.dt, 2)]]) * pow(std_acc, 2)

        # initial measurement noise covariance
        self.R = np.matrix([[pow(x_std_meas, 2), 0],
                            [0, pow(y_std_meas, 2)]])

        # initial covariance matrix
        self.P = np.eye(self.A.shape[1])

    def predict(self):
        self.x = self.A @ self.x + self.B @ self.u
        self.P = self.A @ self.P @ self.A.T + self.Q
        # return self.x, self.P

    def updata(self, z):
        '''

        :param z: The resulting value is what the actual system or model gave us.
        :return:
        '''
        y = z - self.H @ self.x
        s = self.H @ self.P@ self.H.T + self.R
        k = self.P @ self.H.T @ np.linalg.inv(s)
        self.x = self.x + k @ y
        self.P = (np.eye(self.H.shape[1]) - k @ self.H) @ self.P
        return self.x[0:2]

    def __repr__(self):
        return f"KalmanFilter(dt={self.dt}, u_x={self.u[0]}, u_y={self.u[1]}, std_acc={self.std_acc}, x_std_meas={self.x_std_meas}, y_std_meas={self.y_std_meas})"
