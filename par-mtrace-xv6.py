#!/usr/bin/python

import os, multiprocessing, subprocess

ncpu = multiprocessing.cpu_count()

os.system("make HW=mtrace")

null = open('/dev/null', 'rw')
procs = []
for n in range(0, ncpu):
  args = ["make", "HW=mtrace",
                  "MTRACEOUT=mtrace.out.%03d" % n,
                  "RUN=fstest -t -n %d -p %d; halt" % (ncpu, n),
                  "QEMUNOREDIR=x",
                  "QEMUOUTPUT=qemu.out.%03d" % n,
                  "mtrace.out.%03d-scripted" % n]
  p = subprocess.Popen(args, stdout=null, stdin=null)
  procs.append(p)

for p in procs:
  p.wait()

