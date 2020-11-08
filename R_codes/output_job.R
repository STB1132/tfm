      #making bash files
      
      tmp <-c()
      mesh_files <-c()
      mesh_files <- list.files(path="/home/sara/Desktop/TFM/Mesh convergence study/Meshes_tal//", pattern = "\\.mesh")
      
      
      #cortical_thick <-c("0.74","1.48","1.98","2.48 ","2.98 ","5.96 ")
      cortical_thick <-c("2.48")
      cortical_thick <- as.numeric(as.character(cortical_thick))
      
      
      for (k in 1:length(cortical_thick)){
        
        cortical_thick[k] <- cortical_thick[k]/59
        
      }
      
      cortical_thick <- lapply(cortical_thick, round, 4)
      cortical_thick <- as.vector(cortical_thick)
      
      for (number in mesh_files){
        
        
        for (i in cortical_thick){
          
        
          
          L1<- c("#!/bin/bash")
          L2 <- paste0("#SBATCH --job-name=\"CT-",i,"_MESH-",number,"\"")
          L3 <-c("#SBATCH --nodes=1")
          L4 <-c("#SBATCH --ntasks-per-node=1")
          L5 <- c("#SBATCH --cpus-per-task=26")
          L6 <- c("#SBATCH --mem=36G")
          L7 <- c("#SBATCH -p high #")
          L8 <- c("#SBATCH -o /homedtic/sazidane/Mesh_convergence/Outputs_and_errors/%x-%j_03.out # File to which STDOUT will be written")
          L9 <- c("#SBATCH -e /homedtic/sazidane/Mesh_convergence/Outputs_and_errors/%x-%j_03.err # File to which STDERR will be written")
          L10 <- c("export OMP_NUM_THREADS=${SLURM_CPUS_PER_TASK}")
          L11 <- c("module load GCC/6.3.0-2.27")
          L12 <- c("module load GCCcore/6.3.0")
          L13 <- paste0("g++ -Ofast -fopenmp main.cpp eig3.cpp vema.cpp -o main_0",number," -DPATH_DIR='\"./Decimation-0",number,"_CT-",i,"\"' -DTHICKNESS_CORTEX=",i," -DMESH_FILE='\"./",number,"\"'")
          L14 <- paste0("./main_0",number,"")
          
          
          filename <-paste0("~/Desktop/CT-",i,"_0",number,"_main.sl")
          writeLines(c(L1,L2,L3,L4,L5,L6,L7,L8,L9,L10,L11,L12,L13,L14),filename)
        }
        
      }
      
      
      
