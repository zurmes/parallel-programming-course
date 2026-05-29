#include <iostream>
#include <vector>
#include <fstream>
#include <chrono>
#include <omp.h>

using namespace std;

// Функция загрузки матрицы
bool load_matrix(const string& path, int& N, vector<double>& mat) {
    ifstream input(path);
    if (!input.is_open()) {
        cerr << "Error: failed to open file " << path << endl;
        return false;
    }
    input >> N;
    mat.resize(N * N);
    for (int i = 0; i < N * N; i++) {
        input >> mat[i];
    }
    return true;
}

int main(int argc, char* argv[]) {
    // Количество потоков передается первым аргументом командной строки (по умолчанию 4)
    int threads = (argc > 1) ? atoi(argv[1]) : 4;

    int N_A, N_B;
    vector<double> A, B;

    if (!load_matrix("matrixA.txt", N_A, A) || !load_matrix("matrixB.txt", N_B, B)) {
        return 1;
    }

    if (N_A != N_B) {
        cerr << "Error: matrix dimensions do not match!" << endl;
        return 1;
    }

    int N = N_A;
    vector<double> C(N * N, 0.0);

    // Задаем количество потоков для OpenMP
    omp_set_num_threads(threads);

    cout << "Multiplying matrices of size " << N << "x" << N << " with " << threads << " threads..." << endl;

    // Используем высокоточный таймер OpenMP для замеров времени
    double start = omp_get_wtime();

    // collapse(2) объединяет два внешних цикла в одно пространство итераций
    // и распределяет их между потоками.
    #pragma omp parallel for collapse(2)
    for (int i = 0; i < N; i++) {
        for (int j = 0; j < N; j++) {
            double sum = 0.0;
            for (int k = 0; k < N; k++) {
                sum += A[i * N + k] * B[k * N + j];
            }
            C[i * N + j] = sum;
        }
    }

    double elapsed = omp_get_wtime() - start;

    cout << "Calculations finished." << endl;
    cout << "Execution time: " << elapsed << " seconds." << endl;

    // Сохранение результатов для проверки
    ofstream output("result.txt");
    output << N << endl;
    for (int i = 0; i < N; i++) {
        for (int j = 0; j < N; j++) {
            output << C[i * N + j] << " ";
        }
        output << endl;
    }

    return 0;
}