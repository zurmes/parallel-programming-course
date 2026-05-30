#include <stdio.h>
#include <stdlib.h>
#include <iostream>
#include <vector>
#include <fstream>
#include <cuda_runtime.h>

#ifndef TILE_SIZE
#define TILE_SIZE 16
#endif

using namespace std;

__global__ void matrixMulKernel(float* A, float* B, float* C, int N) {
    __shared__ float sA[TILE_SIZE][TILE_SIZE];
    __shared__ float sB[TILE_SIZE][TILE_SIZE];

    int tx = threadIdx.x; 
    int ty = threadIdx.y;
    int row = blockIdx.y * TILE_SIZE + ty;
    int col = blockIdx.x * TILE_SIZE + tx;

    float val = 0.0f;

    for (int m = 0; m < N / TILE_SIZE; ++m) {
        if (row < N && (m * TILE_SIZE + tx) < N) {
            sA[ty][tx] = A[row * N + (m * TILE_SIZE + tx)];
        } else {
            sA[ty][tx] = 0.0f;
        }

        if (col < N && (m * TILE_SIZE + ty) < N) {
            sB[ty][tx] = B[(m * TILE_SIZE + ty) * N + col];
        } else {
            sB[ty][tx] = 0.0f;
        }

        __syncthreads();

        for (int k = 0; k < TILE_SIZE; ++k) {
            val += sA[ty][k] * sB[k][tx];
        }

        __syncthreads();
    }

    if (row < N && col < N) {
        C[row * N + col] = val;
    }
}

bool load_matrix(const string& path, int& N, vector<float>& mat) {
    ifstream input(path);
    if (!input.is_open()) return false;
    input >> N;
    mat.resize(N * N);
    for (int i = 0; i < N * N; i++) {
        input >> mat[i];
    }
    return true;
}

void save_matrix(const string& path, int N, const vector<float>& mat) {
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
    vector<float> h_A, h_B;

    if (!load_matrix("matrixA.txt", N_A, h_A) || !load_matrix("matrixB.txt", N_B, h_B)) {
        cerr << "Error loading matrices" << endl;
        return 1;
    }

    int N = N_A;
    vector<float> h_C(N * N, 0.0f);

    size_t bytes = N * N * sizeof(float);

    float *d_A, *d_B, *d_C;
    cudaMalloc(&d_A, bytes);
    cudaMalloc(&d_B, bytes);
    cudaMalloc(&d_C, bytes);

    cudaMemcpy(d_A, h_A.data(), bytes, cudaMemcpyHostToDevice);
    cudaMemcpy(d_B, h_B.data(), bytes, cudaMemcpyHostToDevice);

    dim3 block(TILE_SIZE, TILE_SIZE);
    dim3 grid((N + TILE_SIZE - 1) / TILE_SIZE, (N + TILE_SIZE - 1) / TILE_SIZE);

    cudaEvent_t start, stop;
    cudaEventCreate(&start);
    cudaEventCreate(&stop);

    cudaEventRecord(start);
    matrixMulKernel<<<grid, block>>>(d_A, d_B, d_C, N);
    cudaEventRecord(stop);

    cudaEventSynchronize(stop);

    float milliseconds = 0;
    cudaEventElapsedTime(&milliseconds, start, stop);

    cudaMemcpy(h_C.data(), d_C, bytes, cudaMemcpyDeviceToHost);

    cout << "Grid: " << grid.x << "x" << grid.y << " | Block: " << TILE_SIZE << "x" << TILE_SIZE << endl;
    cout << "GPU Kernel Time: " << milliseconds << " ms" << endl;

    save_matrix("result.txt", N, h_C);

    cudaFree(d_A);
    cudaFree(d_B);
    cudaFree(d_C);
    cudaEventDestroy(start);
    cudaEventDestroy(stop);

    return 0;
}