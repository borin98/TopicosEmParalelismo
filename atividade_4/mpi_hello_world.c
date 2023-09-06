#include <stdio.h>
#include <mpi.h>

int main(int argc, char** argv) {
    int rank, size;

    // Initialize MPI
    MPI_Init(&argc, &argv);

    // Get the rank (ID) of the current MPI process
    MPI_Comm_rank(MPI_COMM_WORLD, &rank);

    // Get the total number of MPI processes
    MPI_Comm_size(MPI_COMM_WORLD, &size);

    // Print "Hello, world!" from each MPI process
    printf("Hello, world from MPI !! I'm rank %d of %d\n", rank, size);

    // Finalize MPI
    MPI_Finalize();

    return 0;
}