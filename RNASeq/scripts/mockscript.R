outputFile <- snakemake@output[[1]]
message("Writing to ", outputFile)
towrite <- "This is a differential gene expression analysis normally performed with a package such as deseq2"
write(towrite, file=outputFile, ncolumns=1)