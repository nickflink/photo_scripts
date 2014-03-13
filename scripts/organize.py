#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Doit is a program to to simplify the process of organizing photos
 author:   Nick Flink <nickflink@github.com>
"""
import sys
import getopt
import hashlib;
import os
import subprocess
import shutil
import mimetypes
import multiprocessing
# import getpass
import logging
import pprint
from functools import partial

#global vars

##
##  The following options are provided.
##  --help [-h]. What you are reading now
##  --dry-run [-n] dry-run. output commands but do not execute
##  --search-dir [-s]. search-dir directory to search recursively
##  --dest-dir [-d]. dest-dir directory to store the images
##  --log-level [-l]. setting the log level dynamically

logger = logging.getLogger(__name__)


def usage():
    fh = open(__file__, "r")
    me = fh.readlines()
    sys.stderr.write("usage:\n")
    for line in me:
        if line.find("##") == 0:
            sys.stderr.write(line)

def which(program):
    def is_exe(fpath):
        return os.path.isfile(fpath) and os.access(fpath, os.X_OK)

    fpath, fname = os.path.split(program)
    if fpath:
        if is_exe(program):
            return program
    else:
        for path in os.environ["PATH"].split(os.pathsep):
            path = path.strip('"')
            exe_file = os.path.join(path, program)
            if is_exe(exe_file):
                return exe_file

    return None

def runCmd(name, cmdList):
    logger.info("=> " + name + " = " + " ".join(cmdList))
    if which(cmdList[0]) == None:
        logger.info("[KO] [" + cmdList[0] + "] command doesn't exist you must install it")
        return 1
    if subprocess.call(cmdList) == 0:
        logger.info("[OK] " + name + " = " + " ".join(cmdList))
    else:
        logger.error("[KO] " + name + " = " + " ".join(cmdList))
        return 1
    return 0

def getTimeFromImage(mediaFile):
    formattedTime = "YYYY-MM-DD_hh-mm-ss"
    exifOutput = subprocess.check_output([exifToolCmd, mediaFile])
    origDateTime = None
    for line in exifOutput.split("\n"):
        if(line.startswith("Date/Time Original")):
            origDateTime = line
            break;
    if(origDateTime != None):
        #print "checking " + origDateTime
        origDateTimeList = origDateTime.split(":", 1)[1].strip()
        #pprint.pprint(origDateTimeList)
        date = origDateTimeList.split()[0]
        time = origDateTimeList.split()[1]
        formattedTime = date.replace(":","-") + "_" + time.replace(":","-")
        #print "date: " + date + ", time: " + time + " formattedTime: " + formattedTime
    return formattedTime


def getMd5sumFromFile(mediaFile):
    with open(mediaFile, mode='rb') as f:
        d = hashlib.md5()
        for buf in iter(partial(f.read, 128), b''):
            d.update(buf)
    return d.hexdigest()

def getOrganizedImageName(mediaFile):
    formattedName = getTimeFromImage(mediaFile)
    md5 = getMd5sumFromFile(mediaFile)
    formattedName += "_" + md5
    extension = os.path.splitext(mediaFile)[1]
    formattedName += extension
    logger.debug("formattedName: " + formattedName)
    return formattedName

def organize():
    logger.info("organizing "+searchDir+"...")
    for root, dirs, files in os.walk(searchDir):
        if(root.startswith(destDir)):
            logger.info("skipping destDir: "+ root)
        else:
            for name in files:
                mediaFile = os.path.join(root, name)
                logger.debug("checking mimetype for " + mediaFile)
                mimetype, encoding = mimetypes.guess_type(mediaFile)
                if(mimetype != None and mimetype.startswith("image")):
                    imageName = getOrganizedImageName(mediaFile)
                    imagePath = os.path.join(destDir, imageName)
                    print "[image] cp " + mediaFile + " " + imagePath
                    shutil.copyfile(mediaFile, imagePath)
                    #print "[image] " + mediaFile
                elif(mimetype != None and mimetype.startswith("video")):
                    print "[video] SKIPPING: " + mediaFile

def getExifToolCmd():
    exifTool = which("exiftool")
    if(exifTool == None):
        logger.error("bailing failed to find exiftool")
        sys.exit(1)
    return exifTool

def main(argv=None):
    global exifToolCmd
    global searchDir
    global destDir
    exifToolCmd = getExifToolCmd()
    searchDir = os.environ["HOME"]
    scriptDir = os.path.dirname(os.path.realpath(__file__))
    destDir = os.path.join(os.path.dirname(scriptDir), "photos");
    logLevel = "INFO"
    logging.basicConfig(level=logging.INFO)
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hns:d:l:", ["help", "dry-run", "search-dir=", "dest-dir=", "log-level="])
    except getopt.GetoptError, err:
        # print help information and exit:
        logger.error(err)  # will print something like "option -a not recognized"
        print "ERROR 2"
        usage()
        return 1
    for o, a in opts:
        if o in ("-h", "--help"):
            usage()
            sys.exit(1)
        elif o in ("-s", "--search-dir"):
            searchDir = a
        elif o in ("-d", "--dest-dir"):
            destDir = a
        elif o in ("-l", "--log-level"):
            logLevel = a
        else:
            usage()
    if newTaskMask > 0:
        taskMask = newTaskMask
    if logLevel == "DEBUG":
        logging.basicConfig(level=logging.DEBUG)
    logger.info("Running with:\n\tsearch-dir: " + searchDir + "\n\tdest-dir: " + destDir + "\n\tlog-level: " + logLevel)
    savedPath = os.getcwd()
    os.chdir(os.path.dirname(__file__))
    organize();
    os.chdir(savedPath)
    logger.info("Done!")
    return 0

if __name__ == "__main__":
    newTaskMask = 1
    sys.exit(main())
