#include "kalmanfilter.h"

KalmanFilter::KalmanFilter(double dt, double u_x, double u_y, double std_acc, double x_std_meas, double y_std_meas) {
    this->setDT(dt);
    this->setUX(u_x);
    this->setUY(u_y);
    this->setStdAcc(std_acc);
    this->setXStdMeas(x_std_meas);
    this->setYStdMeas(y_std_meas);

    this->U.data = {{this->getUX()}, {this->getUY()}};
    this->X.data = {{0}, {0}, {0}, {0}};
    this->A.data = {{1, 0, this->getDT(), 0}, {0, 1, 0, this->getDT()}, {0, 0, 1, 0}, {0, 0, 0, 1}};
    this->B.data = {{pow(this->getDT(), 2) / 2, 0}, {0, pow(this->getDT(), 2)/ 2}, {this->getDT(), 0}, {0, this->getDT()}};
    this->H.data = {{1, 0, 0, 0}, {0, 1, 0, 0}};
    Matrix q({{pow(this->getDT(), 4) / 4, 0, pow(this->getDT(), 3) / 2, 0}, {0, pow(this->getDT(), 4) / 4, 0, pow(this->getDT(), 3) / 2}, {pow(this->getDT(), 3) / 2, 0, pow(this->getDT(), 2), 0}, {0, pow(this->getDT(), 3) / 2, 0, pow(this->getDT(), 2)}});
    this->Q.data = {{0, 0, 0, 0}, {0, 0, 0, 0}, {0, 0, 0, 0}, {0, 0, 0, 0}};
    for(int i = 0; i < q.data.size(); i++){
        for (int j = 0; j < q.data[i].size(); j++){
            this->Q.data[i][j] = q.data[i][j] * pow(this->getStdAcc(), 2);
        }
    }
    this->R.data = {{pow(this->getXStdMeas(), 2), 0}, {0, pow(this->getYStdMeas(), 2)}};
    this->P.data = {{1, 0, 0, 0}, {0, 1, 0, 0}, {0, 0, 1, 0}, {0, 0, 0, 1}};
    this->I.data = {{1, 0, 0, 0}, {0, 1, 0, 0}, {0, 0, 1, 0}, {0, 0, 0, 1}};
    std::cout << "initial_state:" << this->X << std::endl;
}

KalmanFilter::~KalmanFilter(){std::cout << "Kalman deleted!" << std::endl;}

void KalmanFilter::setDT(double value){this->dt = (value >= 0 ? value: 0);}

void KalmanFilter::setUX(double value){this->u_x = (value >= 0 ? value: 0);}

void KalmanFilter::setUY(double value){this->u_y = (value >= 0 ? value: 0);}

void KalmanFilter::setStdAcc(double value){this->std_acc = (value >= 0 ? value: 0);}

void KalmanFilter::setXStdMeas(double value){this->x_std_meas = (value > 0 ? value: 1);}

void KalmanFilter::setYStdMeas(double value){this->y_std_meas = (value > 0 ? value: 1);}

double KalmanFilter::getDT()const{return this->dt;}

double KalmanFilter::getUX()const{return this->u_x;}

double KalmanFilter::getUY()const{return this->u_y;}

double KalmanFilter::getStdAcc()const{return this->std_acc;}

double KalmanFilter::getXStdMeas()const{return this->x_std_meas;}

double KalmanFilter::getYStdMeas()const{return this->y_std_meas;}

void KalmanFilter::predict(){
    this->X = Matrix::dotProductMatrix(&this->A, &this->X) + Matrix::dotProductMatrix(&this->B, &this->U);
    Matrix *temp = Matrix::dotProductMatrix(&this->A, &this->P, true);
    Matrix *trans = Matrix::matrixTranspose(&this->A, true);
    this->P = Matrix::dotProductMatrix(temp, trans) + this->Q;
    delete temp;
    delete trans;
}

Matrix KalmanFilter::update(Matrix *z){
    Matrix y = *z - Matrix::dotProductMatrix(&this->H, &this->X);
    Matrix *Ht = Matrix::matrixTranspose(&this->H, true);
    Matrix *temp = new Matrix;
    temp = Matrix::dotProductMatrix(&this->H, &this->P, true);
    Matrix S = Matrix::dotProductMatrix(temp, Ht) + this->R;
    delete temp;
    Matrix *K = new Matrix;
    Eigen::MatrixXd eigenMat = Matrix::convertToEigenMatrix(&S).inverse();
    Matrix *inverse_mat = Matrix::convertToVector(&eigenMat);
    K = Matrix::dotProductMatrix(Matrix::dotProductMatrix(&this->P, Ht, true), inverse_mat, true);
    delete inverse_mat;
    this->X = Matrix::dotProductMatrix(K, &y) + this->X;
    Matrix temp1 = this->I - Matrix::dotProductMatrix(K, &this->H);
    delete K;
    this->P = Matrix::dotProductMatrix(&temp1, &this->P);
    return this->X;
}
