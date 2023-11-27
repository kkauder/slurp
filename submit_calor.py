#!/usr/bin/env python

import slurp

from slurp import SPhnxRule  as Rule
from slurp import SPhnxMatch as Match
from slurp import SPhnxCondorJob as Job
from slurp import matches
from slurp import submit

indir ="/sphenix/lustre01/sphnxpro/commissioning/aligned_2Gprdf/"
outdir="/sphenix/lustre01/sphnxpro/slurp/"
#outdir="/sphenix/u/jwebb2/work/2023/slurp/out/"

DST_CALOR_query = """
select filename,runnumber,segment from datasets
   where dsttype = 'beam'
   and filename like 'beam-%'
   and runnumber > 22000
   order by runnumber,segment
   limit 5
"""


job=Job(
    executable            = "/sphenix/u/sphnxpro/slurp/MDC2/submit/rawdata/caloreco/rundir/run_caloreco.sh",
    initialdir            = "/sphenix/u/sphnxpro/slurp/MDC2/submit/rawdata/caloreco/rundir/",
    #output_destination:    str = "file:////sphenix/data/data02/sphnxpro/condorlog/$$($(run)/100)00"         
    output_destination    = "file:///sphenix/data/data02/sphnxpro/condorlogs/$$([$(run)/100])00",
    transfer_output_files = "$(name)_$(build)_$(tag)-$INT(run,%08d)-$INT(seg,%04d).log,$(name)_$(build)_$(tag)-$INT(run,%08d)-$INT(seg,%04d).errlog",
    transfer_input_files  = "/sphenix/u/sphnxpro/slurp/MDC2/submit/rawdata/caloreco/rundir/",
    )


# DST_CALOR rule
DST_CALOR_rule = Rule( name              = "DST_CALOR_auau23",
                       files             = DST_CALOR_query,
                       script            = "run_caloreco.sh",
                       build             = "ana.387",        
                       tag               = "2023p003",
                       job               = job)

submit(DST_CALOR_rule, nevents=10, indir=indir, outdir=outdir, dump=False, resubmit=True )  
