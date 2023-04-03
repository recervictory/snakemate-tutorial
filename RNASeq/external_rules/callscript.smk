rule mockDifferentialAnalysis:
  input:
    "results/featureCounts/{sampleName}.txt"
  output:
    "results/differentialAnalysis/{sampleName}.csv"
  threads: 1
  script:
    "../scripts/mockscript.R"