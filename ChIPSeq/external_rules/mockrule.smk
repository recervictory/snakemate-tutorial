rule mockAlignment:
  input:
    "inputs/{sampleName}.fastq"
  output:
    "results/alignment/{sampleName}.bam"
  threads: 1
  shell:
    """
    cat {input} > {output}
    sleep 10s
    """