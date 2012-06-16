from mpi4py import MPI
comm = MPI.COMM_WORLD
rank = comm.Get_Rank()
size = comm.Get_Size()
print( "Hello world from process %d of %d\n", rank, size )
