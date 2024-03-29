def readln_buffer(chunk, bufferPosition):
    """
    Takes a File Object inputFile, an int filePosition that indicates
    a position in a file and an int bufferSize that indicates the 
    size of the buffer to read from the file. Returns the str 
    existing from the position indicated until the next newline, as 
    well as the position the File Object indicates now.
    
    This function assumes that the inputFile parameter is an already 
    opened file with mode "r+b" and specifying a certain buffering
    parameter
    """
    auxChunk = chunk[bufferPosition:]
    retPos = auxChunk.find(b"\n")
    if retPos != -1:
        retPos += 1
        bline = auxChunk[:retPos]
    else:
        bline = auxChunk
    
    lineLength = len(bline)
    bufferPosition += lineLength

    return bline, bufferPosition

def writeln_buffer(outputFile, line, bufferSize):
    """
    Takes a File Object outputFile, a str line containing a text line
    to be written to the outputFile and a bufferSize. Then writes
    line to the outputFile by decomposing it into chunks of size
    bufferSize.
    
    This function assumes that the outputFile parameter is an already 
    opened file with mode "a+b" and specifying a certain buffering
    parameter (bufferSize)
    """
    chunkList = [line[i:i+bufferSize] for i in range(0, len(line), bufferSize)]
    for chunk in chunkList:
        outputFile.write(chunk)
