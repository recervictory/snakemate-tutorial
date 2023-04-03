rule mockpeakDetection:
  input:
    "results/alignment/{sampleName}.bam"
  output:
    "results/peaks/{sampleName}.peaks"
  threads: 1
  script:
    "../scripts/mockscript.R"