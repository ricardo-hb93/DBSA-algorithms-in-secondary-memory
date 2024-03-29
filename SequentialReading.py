import mmap
import os
from time import time
from ReadWriteByChar import readln_char
from ReadWriteByLine import readln_line
from ReadWriteByBuffer import readln_buffer
from ReadWriteByMmap import read_bline_mmap
from RandomReading import cannotUseLastBuffer, usedWholeBuffer

def length_char(f):
    """
    Given a file, reads it sequentially char by char.
    Returns the number of bytes read.
    """
    sum = 0
    seekPos = 0

    # Open file for reading in binary mode switching buffering off
    file = open(f, "r+b", 0)

    # Read all lines in a file. readln_char returns the line that was read and the position of the next line to be read
    # When the end of the file is reached, seekPos will be -1, ending the loop
    while seekPos != -1:
        line, seekPos = readln_char(file,seekPos)
        sum += len(line)

    file.close()

    return sum

def length_line(fileName):
    """
    Given a file, reads it sequentially line by line.
    Returns the number of bytes read.
    """
    file = open(fileName, 'r+b')
    sum = 0
    current_position = 0

    while True:
        line, current_position = readln_line(file, current_position)
        if not line:
            break
        sum += len(line)

    file.close()
    return sum

def length_buffer(fileName, bufferSize):
    """
    Given a file and a bufferSize, reads it sequentially regarding a 
    buffer. Returns the number of bytes read.
    """
    sum = 0
    currentPositionInFile = 0

    fileSize = os.stat(fileName).st_size
    file = open(fileName, "r+b")

    # Initialize variables for the buffer
    currentPositionInBuffer = 0
    buffer = None

    while True:
        line = b''
        while line is not None and b'\n' not in line:
            # Create buffer for the first time or re-buffer
            if not buffer or usedWholeBuffer(currentPositionInBuffer, bufferSize):
                file.seek(currentPositionInFile)
                buffer = file.read(bufferSize)
                currentPositionInBuffer = 0
            tempLine, currentPositionInBuffer = readln_buffer(buffer, currentPositionInBuffer)
            # If found EOF
            if tempLine == b'':
                line = None
            else:
                line += tempLine
                currentPositionInFile += len(tempLine)        
        if line is None:
            break
        sum += len(line)

    file.close()
    return sum

def length_mmap(fileName, bufferSize):
    """
    Given a file and a bufferSize, reads it sequentially with memory
    mapping. Returns the number of bytes read.
    """
    file = open(fileName, 'r+b', bufferSize)
    sum = 0
    current_position = 0

    # Obtaining values to be used in mapping, based on the input parameters
    actualFilePosition = current_position // mmap.ALLOCATIONGRANULARITY * mmap.ALLOCATIONGRANULARITY
    actualBufferSize = (bufferSize // mmap.ALLOCATIONGRANULARITY + 1) * mmap.ALLOCATIONGRANULARITY
    fileSize = os.fstat(file.fileno()).st_size

    # Ensure legal mapping (not larger than the file)
    if fileSize < actualFilePosition + actualBufferSize:
        actualBufferSize = fileSize - actualFilePosition

    mapping = mmap.mmap(file.fileno(), actualBufferSize, access=mmap.ACCESS_READ, offset=actualFilePosition)

    incompleteLine = False
    prev_current_position = 0

    while True:
        prev_current_position = current_position
        line, current_position = read_bline_mmap(mapping, current_position, actualFilePosition, bufferSize, actualBufferSize)
        if not line:
            break
        # If line exceedes mapping
        if b'\n' not in line:
            incompleteLine = True
        # If remapping needed
        if current_position >= actualFilePosition + actualBufferSize and current_position < fileSize:
            actualFilePosition = current_position // mmap.ALLOCATIONGRANULARITY * mmap.ALLOCATIONGRANULARITY

            if fileSize < actualFilePosition + actualBufferSize:
                actualBufferSize = fileSize - actualFilePosition

            mapping = mmap.mmap(file.fileno(), actualBufferSize, access=mmap.ACCESS_READ, offset=actualFilePosition)

            if incompleteLine:
                line_part, current_position = read_bline_mmap(mapping, current_position, actualFilePosition, bufferSize, actualBufferSize)
                line += line_part
                incompleteLine = False
        sum += current_position - prev_current_position

    file.close()
    return sum
