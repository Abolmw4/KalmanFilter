#include "matrix.h"

Matrix::Matrix(){
    this->data;
}

Matrix::Matrix(std::vector<std::vector<double>> data){
    this->data = data;
}

Matrix::Matrix(std::size_t row, std::size_t col, double initialvalue) {
    this->setRows(row);
    this->setCols(col);
    for(std::size_t i = 0; i < this->getRows(); i++){
        std::vector<double> temp;
        for(std::size_t j = 0; j < this->getCols(); j++){
            temp.push_back(initialvalue);
        }
        this->data.push_back(temp);
    }
}

Matrix::~Matrix(){
//    std::cout<< "Matirx object deleted!" << std::endl;
}

void Matrix::setRows(std::size_t value){this->rows = (value > 0 ? value : 1);}

void Matrix::setCols(std::size_t value){this->cols = (value > 0 ? value : 1);}

std::size_t Matrix::getRows(){return this->rows;}

std::size_t Matrix::getCols(){return this->cols;}

Matrix Matrix::dotProductMatrix(Matrix *a, Matrix *b){
    int rowsA = a->data.size();
    int rowsB = b->data.size();
    int colsA = a->data[0].size();
    int colsB = b->data[0].size();

    Matrix result;
    for(int i = 0; i < rowsA; i++){
        std::vector<double> temp;
        for (int l=0; l < colsB; l++){
            double sum=0;
            for(int k=0; k < colsA; k++){
                // sum += (*a)[i][k] * (*b)[k][l];
                sum += a->data[i][k] * b->data[k][l];
            }
            temp.push_back(sum);
        }
        result.data.push_back(temp);
    }
    return result;
}

Matrix * Matrix::dotProductMatrix(Matrix *mat1, Matrix *mat2, bool return_ref){
    int rowsA = mat1->data.size();
    int rowsB = mat2->data.size();
    int colsA = mat1->data[0].size();
    int colsB = mat2->data[0].size();
    Matrix *result = new Matrix;
    for(int i = 0; i < rowsA; i++){
        std::vector<double> temp;
        for (int l=0; l < colsB; l++){
            double sum=0;
            for(int k=0; k < colsA; k++){
                // sum += (*a)[i][k] * (*b)[k][l];
                sum += mat1->data[i][k] * mat2->data[k][l];
            }
            temp.push_back(sum);
        }
        result->data.push_back(temp);
    }
    return result;
}

Matrix * Matrix::matrixTranspose(Matrix *mat, bool return_ref){
    std::size_t row = mat->data.size();
    std::size_t col = mat->data[0].size();
    Matrix *temp = new Matrix(col, row, 0);
    for(int i = 0; i < row; ++i){
        for (int j = 0; j < col; ++j){
            temp->data[j][i] = mat->data[i][j];
        }
    }
    return temp;
}

Matrix Matrix::matrixTranspose(Matrix *mat){
    std::size_t row = mat->data.size();
    std::size_t col = mat->data[0].size();
    Matrix temp(col, row, 0);
    for(int i = 0; i < row; ++i){
        for (int j = 0; j < col; ++j){
            temp.data[j][i] = mat->data[i][j];
        }
    }
    return temp;
}

Eigen::MatrixXd Matrix::convertToEigenMatrix(Matrix *mat){
    int rows = mat->data.size();
    int cols = mat->data[0].size();
    Eigen::MatrixXd temp(rows, cols);
    for (int i = 0; i < rows; ++i)
        for (int j = 0; j < cols; ++j)
            temp(i, j) = mat->data[i][j];
    return temp;
}

Matrix * Matrix::convertToVector(Eigen::MatrixXd *mat){
    int rows = mat->rows();
    int cols = mat->cols();
    Matrix *temp = new Matrix(rows, cols, 0);
    for (int i = 0; i < rows; ++i)
        for (int j = 0; j < cols; ++j)
            temp->data[i][j] = (*mat)(i, j);
    return temp;
}

Matrix Matrix::operator=(const Matrix& other){

    for(std::size_t i = 0; i < this->data.size(); i++){
        for(std::size_t j = 0; j < this->data[0].size(); j++){
            this->data[i][j] = other.data[i][j];
        }
    }
    return *this;
}
