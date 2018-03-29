import os
from soma_workflow.client import Job, Workflow, Helper, WorkflowController

queue = 'Unicog_run32'
path2code = '/neurospin/unicog/protocols/intracranial/FAIRNS/sentence-processing-MEG-LSTM/Code/MEG/'
list_scripts = [os.path.join(path2code, "main_alignment_model.py " + str(channel)) for channel in range(1,33,1)]

jobs = []
for b in list_scripts:
    jobs.append(Job(command=["python", os.path.abspath(b)], name=b))

workflow=Workflow(jobs)

Helper.serialize('main_alignment_model1.somawf', workflow)

# WorkflowController.retrieve_job_stdouterr(job_id, stdout_file_path, stderr_file_path=None)

# workflow submission
controller = WorkflowController("DSV_cluster_yl254115", 'yl254115', '11$Etadpu')

controller.submit_workflow(workflow=workflow,
                           name="shared resource path example", queue=queue)
