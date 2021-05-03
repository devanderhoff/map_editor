# File containing custom exceptions; best practice regarding their usage (frequency, or at all)
# seems to be unclear. I suppose it is better used sparsely; for most situations a rather clear
# built-in exception already exists anyway.

class MethodCannotBeCalledOnBaseClassError(Exception):
    pass
