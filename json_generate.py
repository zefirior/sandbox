import json
import uuid


COL_NUM = 6
ROW_NUM = 100000


s = str(uuid.uuid4())

d = {str(uuid.uuid4()): [str(uuid.uuid4()) for _ in range(COL_NUM)] + [[s, s, s], [s, s, s, s]] for _ in range(ROW_NUM)}

with open("test_data.json", "w") as f:
    f.write(json.dumps(d))
