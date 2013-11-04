sig.keys <- function(keytable, err.rate){
   for( i in 1:dim(keytable)[1] ){
      row <- keytable[i,]
      cont <- matrix( c(row$V1, row$V3, row$V2, row$V4), ncol=2,)
      colnames(cont) <- c("Group", "All")
      rownames(cont) <- c("Contains", "Miss")
      f <- fisher.test(cont)
      if(f$p.value < err.rate){
         write(paste(row$V5, f$p.value), "fisher.out", append=T)
      }
   }
}
