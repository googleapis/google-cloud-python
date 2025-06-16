import google.protobuf
if google.protobuf.__version__.startswith("3"):
    from .protobuf3 import *
elif google.protobuf.__version__.startswith("4"):
    from .protobuf4 import *
elif google.protobuf.__version__.startswith("5"):
    from .protobuf5 import *
elif google.protobuf.__version__.startswith("6"):
    from .protobuf6 import *
else:
    raise NotImplemented("This package does not support this version of Protobuf runtime")
