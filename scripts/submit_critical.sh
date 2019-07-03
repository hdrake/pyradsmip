#!/bin/bash

#SBATCH --partition sched_mit_raffaele
#SBATCH --nodes 1
#SBATCH --ntasks 1
#SBATCH --mem 64000
#SBATCH --time=48:00:00
#SBATCH --error stderr
#SBATCH --output stdout
#SBATCH --job-name python
#SBATCH --mail-type FAIL,END
#SBATCH --mail-user hdrake@mit.edu

module load engaging/anaconda/2.3.0

source activate pyradsmip

SECONDS=0
python compute_OLR.py > output.txt
echo "Completed in $SECONDS seconds"

