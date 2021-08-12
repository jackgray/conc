import glob, os, shutil
from pathlib import Path

# TODO: add loop for session IDs

concDir = os.path.abspath(os.path.relpath('./conc', start=os.curdir))
print('writing files to: ' + concDir)
if os.path.isdir(concDir):
    shutil.rmtree(concDir, ignore_errors=False, onerror=None)
os.mkdir(concDir)
subjPaths = glob.glob('../derivatives/abcd/sub*')
subjFolders = []
for i in subjPaths:
    p = Path(i)
    p=p.parts[-1] 
    subjFolders.append(p)

# MATRIX
for subject in subjFolders:
    matrixGlob = '../derivatives/abcd/' + subject + '/ses-*/files/*/*/*ptseries*'
    motionGlob = '../derivatives/abcd/' + subject + '/ses-*/files/DCAN*/*/motion/*FD_only*'
    matrixPaths = glob.glob(matrixGlob)
    motionPaths = glob.glob(motionGlob)
    
    writePath = concDir + '/' + subject + '/'
    if not os.path.isdir(writePath):
        os.mkdir(writePath)
    print('Created directory for subject \' ' + subject)
    # collect all matrix paths for the subject we are iterating on
    subjectMatrixPaths, subjectMotionPaths=[],[]
    for matrixPath in matrixPaths:
        subjectMatrixPaths.append(matrixPath)
        # print(matrixPath)
    for motionPath in motionPaths:
        subjectMotionPaths.append(motionPath)
        print('motionpath: ' + motionPath)

    # now we have all the matrix file paths for a single subject stored in subjectMatrixPaths
    # before leaving the subject loop we need to parse the path to grab the task name for each path
    for subjectMatrixPath in subjectMatrixPaths:
        p = Path(subjectMatrixPath)
        matrixFileNames = p.parts[-1:]      # separates path by /'s and grabs the last in the list

        # extract task name from current file name and store them 
        matrixTaskNames, taskMatrixPaths=[],[]
        for matrixFilePart in matrixFileNames:

            matrixTaskName = matrixFilePart.lstrip('task-').split('_')[0]
            matrixConcFileName = str(matrixTaskName + '_matrix.conc')
            matrixConcFile = writePath + matrixConcFileName
            matrixf = open(matrixConcFile, 'a')
            matrixf.write(subjectMatrixPath[15:] + '\n')
    
    for subjectMotionPath in subjectMotionPaths:
        p = Path(subjectMotionPath)
        motionFileNames = p.parts[-1:]
        
        motionTaskNames, taskMotionPaths=[],[]
        for motionFilePart in motionFileNames:
            motionTaskName = motionFilePart.lstrip('task-').split('_')[0]
            motionConcFileName = str(motionTaskName + '_motion.conc')
            print(motionConcFileName)
            motionConcFile = writePath + motionConcFileName
            motionf = open(motionConcFile, 'a')
            motionf.write(subjectMotionPath[15:] + '\n')

