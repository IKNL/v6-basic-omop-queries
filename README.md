
# v6-basic-omop-queries

This vantage6 algorithm sends a basic SQL query to an OMOP database at the node(s). This algorithm can be used to test the infrastructure of your v6 network after setting up an OMOP database.

This algorithm is designed to be run with the [vantage6](https://vantage6.ai)
infrastructure for distributed analysis and learning.

The base code for this algorithm has been created via the
[v6-algorithm-template](https://github.com/vantage6/v6-algorithm-template)
template generator.

### Checklist

Note that the template generator does not create a completely ready-to-use
algorithm yet. There are still a number of things you have to do yourself.
Please ensure to execute the following steps. The steps are also indicated with
TODO statements in the generated code - so you can also simply search the
code for TODO instead of following the checklist below.

- Include a URL to your code repository in setup.py.
- Implement your algorithm functions.
  - You are free to add more arguments to the functions. Be sure to add them
    *after* the `client` and dataframe arguments.
  - When adding new arguments, if you run the `test/test.py` script, be sure
    to include values for these arguments in the `client.task.create()` calls
    that are available there.
- If you are using Python packages that are not in the standard library, add
  them to the `requirements.txt` and `setup.py` file.
- We strongly recommend adding documentation to your code. This will help
  others to understand your code and will help you to understand your own code
  in the future.
- Finally, remove this checklist section.

### Dockerizing your algorithm

To finally run your algorithm on the vantage6 infrastructure, you need to
create a docker image of your algorithm. This can be done by executing the
following command in the root of your algorithm directory:

```bash
docker build -t [my_docker_image_name] .
```

where you should provide a sensible value for the Docker image name. The
`docker build` command will create a docker image that contains your algorithm.
You can create an additional tag for it by running

```bash
docker tag [my_docker_image_name] [another_image_name]
```

This way, you can e.g. do
`docker tag local_average_algorithm harbor2.vantage6.ai/algorithms/average` to
make the algorithm available on a remote Docker registry (in this case
`harbor2.vantage6.ai`).

Finally, you need to push the image to the Docker registry. This can be done
by running

```bash
docker push [my_docker_image_name]
```

Note that you need to be logged in to the Docker registry before you can push
the image. You can do this by running `docker login` and providing your
credentials. Check [this page](https://docs.docker.com/get-started/04_sharing_app/)
For more details on sharing images on Docker Hub. If you are using a different
Docker registry, check the documentation of that registry and be sure that you
have sufficient permissions.