#include <iostream>
#include <vector>
#include <fstream>
#include <chrono>

using namespace std;

// Load matrix from file into a 1D vector
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

// Save matrix to file
void save_matrix(const string& path, int N, const vector<double>& mat) {
    ofstream output(path);
    output << N << endl;
    for (int i = 0; i < N; i++) {
        for (int j = 0; j < N; j++) {
            output << mat[i * N + j] << " ";
        }
        output << endl;
    }
}

int main() {
    int N_A, N_B;
    vector<double> A, B;

    // Load input matrices
    if (!load_matrix("matrixA.txt", N_A, A) || !load_matrix("matrixB.txt", N_B, B)) {
        return 1;
    }

    if (N_A != N_B) {
        cerr << "Error: matrix dimensions do not match!" << endl;
        return 1;
    }

    int N = N_A;
    vector<double> C(N * N, 0.0);

    cout << "Multiplying matrices of size " << N << "x" << N << "..." << endl;

    // Record calculation start time
    auto start = chrono::high_resolution_clock::now();

    // Classic sequential algorithm O(N^3)
    for (int i = 0; i < N; i++) {
        for (int j = 0; j < N; j++) {
            double sum = 0.0;
            for (int k = 0; k < N; k++) {
                sum += A[i * N + k] * B[k * N + j];
            }
            C[i * N + j] = sum;
        }
    }

    // Record calculation end time
    auto end = chrono::high_resolution_clock::now();
    chrono::duration<double> elapsed = end - start;

    cout << "Calculations finished." << endl;
    cout << "Execution time: " << elapsed.count() << " seconds." << endl;

    // Save result
    save_matrix("result.txt", N, C);
    return 0;
}