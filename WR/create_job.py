#!/usr/bin/env python


import os
import sys


jdl = """\
universe = vanilla
executable = ./{PROCESS}.sh
should_transfer_files = YES
when_to_transfer_output = ON_EXIT
output = {PROCESS}_out/{PROCESS}_$(ProcId).out
error = {PROCESS}_err/{PROCESS}_$(ProcId).err
log = {PROCESS}_log/{PROCESS}_$(ProcId).log
transfer_input_files = CMSSW_DYNANO.tar.gz
transfer_output_files = CMSSW_10_6_18/src/PhysicsTools/NanoAODTools/{PROCESS}_$(ProcId).root
queue arguments from arguments.txt\
"""


def mkdir(path):
    if not os.path.exists(path):
        os.mkdir(path)


def parse_arguments():
    if not len(sys.argv) == 3:
        raise Exception("./create_job.py PROCESS PATH_TO_JOBDIR")
    return {"process": sys.argv[1], "jobdir": sys.argv[2]}


def main(args):
    process = args["process"]
    print("Process: %s" % process)

    # Build argument list
    print("Filelist:")
    arguments = []
    counter = 0
    for filename in os.listdir("datafiles/"):
        if process in filename:
            print("    %s." % filename)
            for line in open("datafiles/" + filename, "r").readlines():
                arguments.append("%u %s %s" % (counter, process, line))
                counter += 1
    print("Number of jobs: %u" % len(arguments))

    # Create jobdir and subdirectories
    jobdir = os.path.join(args["jobdir"], process)
    print("Jobdir: %s" % jobdir)
    mkdir(jobdir)
    mkdir(os.path.join(jobdir, process+"_out"))
    mkdir(os.path.join(jobdir, process+"_log"))
    mkdir(os.path.join(jobdir, process+"_err"))

    # Write jdl file
    out = open(os.path.join(jobdir, "job.jdl"), "w")
    out.write(jdl.format(PROCESS=process))
    out.close()

    # Write argument list
    arglist = open(os.path.join(jobdir, "arguments.txt"), "w")
    for a in arguments:
        arglist.write(a)
    arglist.close()

    # Write job file
    jobfile = open("job.sh", "r").read()
    job = open(os.path.join(jobdir, "{PROCESS}.sh".format(PROCESS=process)), "w")
    job.write(jobfile)
    job.close()


if __name__ == "__main__":
    args = parse_arguments()
    main(args)
