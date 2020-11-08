                #read in required packages
        f2si2<-function (number,rounding=F){
          lut <- c(1e-24, 1e-21, 1e-18, 1e-15, 1e-12, 1e-09, 1e-06, 
                   0.001, 1, 1000, 1e+06, 1e+09, 1e+12, 1e+15, 1e+18, 1e+21, 
                   1e+24)
          pre <- c("y", "z", "a", "f", "p", "n", "u", "m", "", "k", 
                   "M", "G", "T", "P", "E", "Z", "Y")
          ix <- findInterval(number, lut)
          if (lut[ix]!=1) {
            if (rounding==T) {
              sistring <- paste(round(number/lut[ix], digits = 2), pre[ix])
            }
            else {
              sistring <- paste(number/lut[ix], pre[ix])
            } 
          }
          else {
            sistring <- as.character(number)
          }
          return(sistring)
        }
        
        library(data.table)
        library(ggplot2)
        library(ggrepel)
        library(readODS)
        library(gt)
        out_files_ct <- list()
        
        options(digits = 4)
        current_path <- getActiveDocumentContext()$path
        setwd(dirname(current_path ))
        setwd("..")
        getwd() 
        path <- getwd()
        #create a list of the files from your target directory
        file_list <- list.files(path= path , pattern = "\\.out")
        type <- c("Area")
        
        #initiate a blank data frame, each iteration of the loop will append the data from the given file to this variable
        dataset <- data.frame()
    
        descritive <- list()
        #had to specify columns to get rid of the total column
        for (i in 1:length(file_list)){
          d <- read.delim(file_list[i], header=FALSE, stringsAsFactors = FALSE)#read in files using the fread function from the data.table package
         
           nodes <- d$V1[grep("nn:",d$V1)]
          nodes <- gsub("([[:alpha:]]*\\:)(*)","\\2",nodes)
          Elements <- d$V1[grep("ne:",d$V1)]
          Elements <- gsub("([[:alpha:]]*\\:)(*)","\\2", Elements)
          faces <- d$V1[grep("nf:",d$V1)]
          faces <- gsub("([[:alpha:]]*\\:)(*)","\\2", faces)
          maxdist0 <- d$V1[grep("maxdistance:",d$V1)]
          maxdist0 <- gsub("([[:alpha:]]*\\:)(*)","\\2", maxdist0)
          
        
          
          
          
          Elements <- as.numeric(as.character(Elements)) 
           Elements <- f2si2(Elements,T)
         
         
          
          nodes <- as.numeric(as.character(nodes))
          faces <- as.numeric(as.character(faces))
          
          maxdist0 <- as.numeric(as.character(maxdist0))
          
          
          print(Elements)
          print(maxdist0)
          
          d <-as.data.frame( d[-c(1:38),], stringsAsFactors = FALSE)
          colnames(d) <- c("param")
          out <-data.frame()
          
          for (j in 1:length(d$param)){
            
            d$param[j] <- gsub("\\s\\s\\s\\s\\s\\s\\s"," ",d$param[j])
            d$param[j] <- gsub("\\s\\s\\s\\s\\s\\s"," ",d$param[j])
            d$param[j] <- gsub("\\s\\s\\s\\s\\s"," ",d$param[j])
            d$param[j] <- gsub("\\s\\s\\s\\s"," ",d$param[j])
            d$param[j] <- gsub("\\s\\s\\s"," ",d$param[j])
            d$param[j] <- gsub("\\s\\s"," ",d$param[j])
            d$param[j] <- gsub("^\\s","",d$param[j])
            
            outt <- strsplit(as.character(d$param[j]),' ')
            outt <- as.vector(unlist(outt))
            outt <- as.numeric(as.character(outt))
            
            
            out <- rbind(out,outt)
            
            
          }
          
          colnames <-c("Time step","Execution time","MaxDist","time","Uk","Ue","Area","Volume","Xrange","Yrange")
          
          colnames(out) <- colnames
          out$Uk <- abs(out$Uk)
          out$Volume <- abs(out$Volume)
           t<- tail(out$time,1)
           out$Area <- (out$Area*(maxdist0^2))
           out$Volume <- out$Volume*out$MaxDist^3
          
          out <- cbind(out,Elements)
         
           line <- c(nodes,Elements,faces)
           print(line)
         descritive[[i]] <- line
           
          
          out_files_ct[[i]] <-out
          name <- paste0("Decimation : Mesh ",Elements)
          assign(name, out)
          
          }
        
        
          
          library(directlabels)
          info <- data.frame()
          p <- ggplot() + 
            ggtitle("Mesh sensitivity analysis")
          
          for (i in 1:length(out_files_ct) ){
            
          
           p <- p  +  geom_line( data = out_files_ct[[i]], aes(x= time, y= type, colour=Elements)) 
           
           
           tmp <- tail(out_files_ct[[i]],1)
           
          info <- rbind(info , tmp )
           
             
          }
          
          p <- p+  geom_label_repel(family = "Times New Roman",data = info ,
                                    aes(x= time, y= Area, label = Elements),
                                    hjust=0.6, nudge_x = 1, size=4) 
          
          p <- p +  theme_classic(base_size = 16, base_family =  "Times New Roman" )
           
           p <- p+ xlim(0, 1.1)
          
           
           
           if (type=="Volume"){
               
               
                p <- p + geom_rect(aes(ymin =400 , ymax = 500, xmin = 0, xmax = 1),
                          fill = "pink", alpha = 0.7)
               
               
           }else{
               
               p <- p + geom_rect(aes(ymin = 800 , ymax = 1000, xmin = 0, xmax = 1),
                                  fill = "pink", alpha = 0.7)
               
               
           }
          
            print(p)
              
            
            
          
            
        
            
            