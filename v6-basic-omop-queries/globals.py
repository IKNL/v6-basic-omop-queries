# The following global variables are algorithm settings. They can be overwritten by
# the node admin by setting the corresponding environment variables.

# Minimum value to be given as individual value in person count. To be
# overwritten by setting the ``BOQ_MIN_RECORDS`` environment variable.
DEFAULT_BOQ_MIN_RECORDS = "5"

# Whether or not to allow value of 0 in the person count. To be overwritten by
# setting the ``BOQ_ALLOW_ZERO`` environment variable.
DEFAULT_ALLOW_ZERO = "true"
