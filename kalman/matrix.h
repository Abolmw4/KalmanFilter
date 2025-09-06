#ifndef MATRIX_H
#define MATRIX_H
#include<iostream>
#include<vector>
#include<eigen3/Eigen/Dense>

class Matrix
{
    friend std::ostream &operator<<(std::ostream&, const Matrix&);
    friend Matrix operator+(const Matrix&, const Matrix&);
    friend Matrix operator-(const Matrix&, const Matrix&);
public:
    Matrix();
    Matrix(std::vector<std::vector<double>>);
    Matrix(std::size_t rows, std::size_t cols, double initialvalue=0);
    ~Matrix();
    std::vector<std::vector<double>> data;
    void setRows(std::size_t);
    void setCols(std::size_t);
    std::size_t getRows();
    std::size_t getCols();
    static Matrix dotProductMatrix(Matrix *, Matrix *);
    static Matrix matrixTranspose(Matrix *);
    static Matrix * dotProductMatrix(Matrix*, Matrix*, bool return_ref);
    static Matrix * matrixTranspose(Matrix *, bool return_ref);
    static Eigen::MatrixXd convertToEigenMatrix(Matrix *);
    static Matrix * convertToVector(Eigen::MatrixXd *);
    Matrix operator=(const Matrix& other);

private:
    std::size_t rows;
    std::size_t cols;
};

#endif // MATRIX_H
