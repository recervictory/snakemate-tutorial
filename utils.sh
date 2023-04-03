#!/usr/bin/bash
## Create the project folder
#mkdir demo-subworkflows
#cd demo-subworkflows
## create the folder and the file for the conda environment
mkdir envs
touch envs/environment.yaml
## create the folder and the file for the profile
mkdir profile
touch profile/config.yaml
## create the Snakefile that will connect the subworkflows ChIPSeq and RNASeq
touch Snakefile
## Create the ChIPSeq workflow files
mkdir ChIPSeq
touch ChIPSeq/Snakefile-ChIPSeq
mkdir ChIPSeq/profileChIPSeq
touch ChIPSeq/profileChIPSeq/config.yaml
touch ChIPSeq/profileChIPSeq/status-sacct.sh
mkdir ChIPSeq/inputs
touch ChIPSeq/inputs/exp1.fastq  # This is a toy example, the file is empty
touch ChIPSeq/inputs/exp2.fastq  # This is a toy example, the file is empty
mkdir ChIPSeq/external_rules
touch ChIPSeq/external_rules/mockrule.smk
touch ChIPSeq/external_rules/callscript.smk
mkdir ChIPSeq/scripts
touch ChIPSeq/scripts/mockscript.R
## Create the RNASeq workflow files
mkdir RNASeq
touch RNASeq/Snakefile-RNASeq
mkdir RNASeq/profileRNASeq
touch RNASeq/profileRNASeq/config.yaml
touch RNASeq/profileRNASeq/status-sacct.sh
mkdir RNASeq/inputs
touch RNASeq/inputs/exp1.fastq  # This is a toy example, the file is empty
touch RNASeq/inputs/exp2.fastq  # This is a toy example, the file is empty
mkdir RNASeq/external_rules
touch RNASeq/external_rules/mockrule.smk
touch RNASeq/external_rules/callscript.smk
mkdir RNASeq/scripts
touch RNASeq/scripts/mockscript.R
## Create the MultiOmics workflow files
mkdir MultiOmics
touch MultiOmics/Snakefile-MultiOmics
mkdir MultiOmics/profileMultiOmics
touch MultiOmics/profileMultiOmics/config.yaml
mkdir MultiOmics/external_rules
touch MultiOmics/external_rules/mockrule.smk