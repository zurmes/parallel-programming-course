#define MS_MPI_NO_SAL
#include <mpi.h>
#include <iostream>
#include <vector>
#include <fstream>

using namespace std;

bool load_matrix(const string& path, int& N, vector<double>& mat) {
    ifstream input(path);
    if (!input.is_open()) {
        return false;
    }
    input >> N;
    mat.resize(N * N);
    for (int i = 0; i < N * N; i++) {
        input >> mat[i];
    }
    return true;
}

int main(int argc, char** argv) {
    MPI_Init(&argc, &argv);
    int p_rank, p_size;
    MPI_Comm_rank(MPI_COMM_WORLD, &p_rank);
    MPI_Comm_size(MPI_COMM_WORLD, &p_size);

    int size = 0;
    vector<double> A, B, C;

    if (p_rank == 0) {
        if (!load_matrix("matrixA.txt", size, A) || !load_matrix("matrixB.txt", size, B)) {
            cerr << "Error: failed to load matrices!" << endl;
            MPI_Abort(MPI_COMM_WORLD, 1);
            return 1;
        }
    }

    MPI_Bcast(&size, 1, MPI_INT, 0, MPI_COMM_WORLD);

    if (size % p_size != 0) {
        if (p_rank == 0) {
            cerr << "Error: Matrix size " << size << " is not divisible by process count " << p_size << endl;
        }
        MPI_Finalize();
        return 1;
    }

    int chunk = size / p_size;
    vector<double> local_A(chunk * size);
    vector<double> local_C(chunk * size);

    if (p_rank != 0) {
        B.resize(size * size);
    }

    double start = MPI_Wtime();

    MPI_Bcast(B.data(), size * size, MPI_DOUBLE, 0, MPI_COMM_WORLD);
    MPI_Scatter(A.data(), chunk * size, MPI_DOUBLE, local_A.data(), chunk * size, MPI_DOUBLE, 0, MPI_COMM_WORLD);

    for (int i = 0; i < chunk; i++) {
        for (int j = 0; j < size; j++) {
            double sum = 0.0;
            for (int k = 0; k < size; k++) {
                sum += local_A[i * size + k] * B[k * size + j];
            }
            local_C[i * size + j] = sum;
        }
    }

    if (p_rank == 0) {
        C.resize(size * size);
    }

    MPI_Gather(local_C.data(), chunk * size, MPI_DOUBLE, C.data(), chunk * size, MPI_DOUBLE, 0, MPI_COMM_WORLD);

    if (p_rank == 0) {
        cout << "MPI Processes: " << p_size << " | Time: " << MPI_Wtime() - start << " seconds." << endl;
        
        ofstream out("result.txt");
        out << size << endl;
        for (int i = 0; i < size; i++) {
            for (int j = 0; j < size; j++) {
                out << C[i * size + j] << " ";
            }
            out << endl;
        }
    }

    MPI_Finalize();
    return 0;
}