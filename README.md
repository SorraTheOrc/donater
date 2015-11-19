An application designed to use spare resources on an Azure Container
Service cluster (although it could be made to work on other services -
patches welcome).

# How it works

Run the manageDonateTasks.py script on a regular basis (Chronos is
perfect for this). If there are no jobs in the Marathon queue it will
attempt to schedule a new job using the rgardler/fah container (this
folds proteins in an attempt to find new therapies for various
diseases such as Cancer, Alzheimers and Parkinsons, for more info
check out the Folding at Home project).


If a task is in the queue when the script runs it will scale down the
number of rgardler/fah tasks and enter a cooldown period in which no
new tasks will be scheduled.

The more frequently you run this script the less delay the script will
cause in the startup of actual workloads.
