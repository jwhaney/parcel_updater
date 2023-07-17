from iterator import floop
from renamer import rename

# setup variables
data_dir = 'DRIVE:\\PARCEL\\DATA\\LIVES\\HERE\\'
out_workspace = 'parcel_update.gdb'

# run the repair function first which then calls the state_compiler
run = floop(data_dir, out_workspace)
