outputFile <- snakemake@output[[1]]
message("Writing to ", outputFile)
towrite <- "hello"
write(towrite, file=outputFile, ncolumns=1)