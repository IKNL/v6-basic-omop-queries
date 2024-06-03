
# v6-basic-omop-queries

This vantage6 algorithm sends a basic SQL query to an OMOP database at the node(s). This algorithm can be used to test the infrastructure of your v6 network after setting up an OMOP database.

This algorithm is designed to be run with the [vantage6](https://vantage6.ai)
infrastructure for distributed analysis and learning.

The base code for this algorithm has been created via the
[v6-algorithm-template](https://github.com/vantage6/v6-algorithm-template)
template generator.


## Local Testing of the HTTP variant
```python
import os
import importlib
import base64
lib = importlib.import_module("v6-basic-omop-queries")


os.environ["DEFAULT_DATABASE_URI"] = base64.b32encode("http://127.0.0.1:5000".encode('utf-8')).decode("ascii")
os.environ["USER_REQUESTED_DATABASE_LABELS"] = base64.b32encode("default".encode('utf-8')).decode("ascii")

 lib.send_http_person_count()
 ```

 ## Building the image

```bash
docker build -t harbor2.vantage6.ai/blueberry/v6-basic-omop-queries .
docker push harbor2.vantage6.ai/blueberry/v6-basic-omop-queries
```