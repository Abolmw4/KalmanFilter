#include <iostream>
#include"kalmanfilter.h"
#include"matrix.h"
#include<eigen3/Eigen/Dense>
using namespace std;

ostream &operator<<(ostream&, const Matrix&);
Matrix operator+(const Matrix&, const Matrix&);
Matrix operator-(const Matrix &, const Matrix&);
void setState(KalmanFilter &, const Matrix &);

int main()
{
//     Matrix mat1({{2, 2}, {1, 0}});
//     Matrix mat2(2, 2, 1);
//     Matrix *mat3 = new Matrix(2, 2, 1);
//     Matrix Result = Matrix::dotProductMatrix(&mat1, &mat2);
//     cout << Result;
//     Matrix transposed_mat = Matrix::matrixTranspose(&Result);
//     Matrix *trans = Matrix::matrixTranspose(&transposed_mat, true);
//     cout << *trans;
//     delete mat3;
    KalmanFilter kalman(4, 0, 0, 0.2, 0.5, 0.5);
    Matrix z;
    Matrix f;
    f.data = {{118.5}, {117.54}, {76}, {77}};
    setState(kalman, f);
    z.data = {{120.5}, {118.5}};
    kalman.predict();
    Matrix result = kalman.update(&z);
    cout << result << endl;
    return 0;
}

ostream &operator<<(ostream& output, const Matrix& mat){
    int rows = mat.data.size();
    int cols = mat.data[0].size();
    for(size_t i = 0; i < rows; i++){
        for(size_t j = 0; j < cols; j++){
            std::cout << mat.data[i][j] << '\t';
        }
        output << endl;
    }
    output << "---------------" << endl;
}

Matrix operator+(const Matrix& mymat, const Matrix& other){
    std::size_t row = other.data.size();
    std::size_t col = other.data.size();
    Matrix result(row, col, 0);
    for (std::size_t i = 0; i < row; i++){
        for (std::size_t j = 0; j < col; j++){
            result.data[i][j] = mymat.data[i][j] + other.data[i][j];
        }
    }
    return result;
}

Matrix operator-(const Matrix &mymat, const Matrix& other){
    std::size_t row = other.data.size();
    std::size_t col = other.data.size();
    Matrix result(row, col, 0);
    for (std::size_t i = 0; i < row; i++){
        for (std::size_t j = 0; j < col; j++){
            result.data[i][j] = mymat.data[i][j] - other.data[i][j];
        }
    }
    return result;
}

void setState(KalmanFilter& kalman, const Matrix & mat){
    kalman.X = mat;
}

