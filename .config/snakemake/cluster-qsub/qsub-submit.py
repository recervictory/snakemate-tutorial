#!/usr/bin/env python
"""
qsub-submit.py

Script to wrap qsub command (no sync) for Snakemake. Uses the following job or
cluster parameters:

+ `threads`
+ `resources`
    - `mem_mb`: Expected memory requirements in megabytes. Overrides
      cluster.mem_mb
    - `runtime`: Expecteted time requirements in minutes. Overrides
      cluster.runtime
+ `cluster`
    - `mem_mb`: Memory that will be requested for the cluster for the job.
      Overriden by resources.mem_mb, if present.
      `resources`
    - `queue`: Which queue to run job on
    - `logdir`: Where to log stdout/stderr from cluster command
    - `output`: Name of stdout logfile
    - `error`: Name of stderr logfile
    - `jobname`: Job name (with wildcards)

Author: Joseph K Aicher
"""

import sys  # for command-line arguments (get jobscript)
from pathlib import Path  # for path manipulation
from snakemake.utils import read_job_properties  # get info from jobscript
from snakemake.shell import shell  # to run shell command nicely

# get the jobscript (last argument)
jobscript = sys.argv[-1]
# read the jobscript and get job properties
job = read_job_properties(jobscript)

# get the cluster properties
cluster = job.get("cluster", dict())

# get job information
# get the rule
rule = job.get("rule", "jobname")
# get the wildcards
wildcards = job.get("wildcards", dict())
wildcards_str = ";".join("{}={}".format(k, v) for k, v in wildcards.items())
if not wildcards_str:
    # if there aren't wildcards, this is a unique rule
    wildcards_str = "unique"

# get resources information
# get the number of threads the job wants
threads = job.get("threads", 1)
# get the resource properties
resources = job.get("resources", dict())
# get the memory usage in megabytes that we will request
mem_mb = resources.get(
    "mem_mb",  # first see if the job itself specifies the memory it needs
    # if not, check if the cluster configuration gives guidance
    cluster.get(
        "mem_mb",  # request what the cluster says, if it says anything
        int(2048)  # otherwise, use default value
    )
)
mem_per_thread = round(mem_mb / threads, 2)  # per thread...
# get the expected runtime in minutes
runtime = resources.get(
    "runtime",
    None
) or cluster.get(
    "runtime",
    None
)


# determine names to pass through for job name, logfiles
log_dir = cluster.get("logdir", "logs")
# get the name of the job
jobname = cluster.get("jobname", "smk.{0}.{1}".format(rule, wildcards_str))
# get the output file name
out_log = cluster.get("output", "{}.out".format(jobname))
err_log = cluster.get("error", "{}.err".format(jobname))
# get logfile paths
out_log_path = str(Path(log_dir).joinpath(out_log))
err_log_path = str(Path(log_dir).joinpath(err_log))

# get the queue to run the job on
queue = cluster.get("queue", "")

# set name/log information
jobinfo_cmd = (
    "-o {out_log_path:q} -e {err_log_path:q}"
    " -N {jobname:q}"
)

# set up resources part of command
# start by requesting threads in smp if threads > 1
if threads > 1:
    resources_cmd = "-pe smp {threads}"
else:
    resources_cmd = ""
# add memory limit/request to resources
resources_cmd += " -l h_vmem={mem_per_thread}M -l m_mem_free={mem_per_thread}M"
# if runtime specified, use it
if runtime:
    # make sure it is integer
    runtime = int(runtime)
    # runtime needs to be specified in HH:MM:SS, but is currently in minutes
    runtime_hr = runtime // 60
    runtime_min = runtime % 60
    # add to resources command
    resources_cmd += " -l h_rt={runtime_hr}:{runtime_min}:00"
# if resources are large, perform reservation
if (
        threads >= int(4)
        or
        mem_mb >= int(8096)
):
    resources_cmd += " -R yes"

# get queue part of command (if empty, don't put in anything)
queue_cmd = "-q {queue}" if queue else ""

# get cluster commands to pass through, if any
cluster_cmd = " ".join(sys.argv[1:-1])

# get command to do cluster command (no sync)
submit_cmd = "qsub -terse -cwd"

# run commands
shell_stdout = shell(
    # qsub submit command
    submit_cmd
    # specify required threads/resources
    + " " + resources_cmd
    # specify job name, output/error logfiles
    + " " + jobinfo_cmd
    # specify queue
    + " " + queue_cmd
    # put in pass-through commands
    + " " + cluster_cmd
    # finally, the jobscript
    + " {jobscript}",
    read=True  # get byte string from stdout
)

# obtain job id from this, and print
print(shell_stdout.decode().strip())
