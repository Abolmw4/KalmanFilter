#ifndef KALMANFILTER_H
#define KALMANFILTER_H
#include<vector>
#include<iostream>
#include<cmath>
#include"matrix.h"

class KalmanFilter
{
    friend void setState(KalmanFilter&, const Matrix &);
public:
    KalmanFilter(double dt, double u_x, double u_y, double std_acc, double x_std_meas, double y_std_meas);
    ~KalmanFilter();
    void setDT(double);
    void setUX(double);
    void setUY(double);
    void setStdAcc(double);
    void setXStdMeas(double);
    void setYStdMeas(double);

    double getDT()const;
    double getUX()const;
    double getUY()const;
    double getStdAcc()const;
    double getXStdMeas()const;
    double getYStdMeas()const;
    void predict();
    Matrix update(Matrix *);

private:
    double dt;
    double u_x, u_y, std_acc, x_std_meas, y_std_meas;
    Matrix U, X, A, B, H, Q, R, P, I;
};

#endif // KALMANFILTER_H
