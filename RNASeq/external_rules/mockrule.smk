rule mockFeatureCounts:
  input:
    "inputs/{sampleName}.fastq"
  output:
    "results/featureCounts/{sampleName}.txt"
  threads: 1
  shell:
    """
    cat {input} > {output}
    sleep 10s
    """