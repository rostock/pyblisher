# What is Pyblisher?
Pyblisher is a Python-Interface for the [VCPublisher](https://vc.systems/en/products/vc-publisher/) API by [Virtual City Systems](https://vc.systems).
It is developed by the City of Rostock to integrate Functions of the VCPublisher into the Datenwerft-Software

# Features
Pyblisher is closely developed to the Datenwerft-Software and therefore only supports the functions, which are needed by the City of Rostock.
Actually, the following functions are implemented:
- get existing projects (`get_project()`)
- create a new data bucket for a project (`project.create_bucket()`)
- get existing data buckets for a project (`project.get_bucket()`)
- upload a files to data-buckets (`bucket.upload()`)
- download a file or folder from data-buckets (`bucket.download-file()` or `bucket.download()`)
- create new datasources for a project (`project.create_source()`)
- get existing datasources of a project (`project.get_source()`)
- create new tasks for a project (`project.create_task()`)
- get existing tasks of a project (`project.get_task()`)

# Installation
Pyblisher is develeped for Python 3.11 or heigher and can be installed via pip:
```bash
pip install pyblisher
```

# Configuration
You need to configure the connection to the VCPublisher API by creating a file named `pyblisher.toml` in the root of your project.
If you are using a Django-Project (like Datenwerft), you can also add the configuration to your `settings.py` file by defining a dictionary named `PYBLISHER`.

If you are using the `pyblisher.json` file, it should look like this:
```json
{
  // The URL of the VCPublisher (not the API)
  "host": "https://your-publisher-url.tld",
  // The Version of the API, actually only "v1" is supported
  "api_version": "v1",
  // The Username, which is used to authenticate at the API
  "username": "username",
  // The Password, which is used to authenticate at the API
  "password": "password"
}
```

In case you're using the Django-Configuration, your `settings.py` shoud contain a `PYBLISHER`-Dictionary like this:
```python
PYBLISHER = {
    # The URL of the VCPublisher (not the API)
    "host": "https://your-publisher-url.tld",
    # The Version of the API, actually only "v1" is supported
    "api_version": "v1",
    # The Username, which is used to authenticate at the API
    "username": "username",
    # The Password, which is used to authenticate at the API
    "password": "password"
}
```

If you are using the `pyproject.toml` file, it should have a pyblisher section like this:
```toml
# a pyblisher section
[pyblisher]
# The URL of the VCPublisher (not the API)
host = "https://your-publisher-url.tld"
# The Version of the API, actually only "v1" is supported
api_version = "v1"
# The Username, which is used to authenticate at the API
username = "username"
# The Password, which is used to authenticate at the API
password = "password"
```


# Quickstart
If you have configured the connection to the VCPublisher API, you can start using Pyblisher by importing the `get_project` function and calling it with the ID of the project you want to get.

```python
from pyblisher import get_project

# get existing project
p = get_project(id=<project id>)
```

Create a new data bucket or get an existing and upload/download a file to it:
```python
# get existing data bucket
bucket = p.get_bucket(id=<bucket id>)

# create new data bucket
bucket = p.create_bucket(name="new bucket")

# upload a file to the data bucket
bucket.upload(key=<object_key>, path="path/to/file")

# download a file from the data bucket
with bucket.download_file(key=<object_key>) as response:
    with open("path/to/save/file", "wb") as f:
        for byte in response.iter_bytes():
            f.write(byte)

# download a folder or file from the data bucket as tar.gz
with bucket.download(key=<object_key>) as response:
    with open("path/to/save/file.tar.gz", "wb") as f:
        for byte in response.iter_bytes():
            f.write(byte)
```

Create a new datasource or get an existing one:
```python
# create new datasource with existing bucket
source = p.create_source(
    name="new source",
    sourceProperties={
        "type": "internal",
        "dataBucketId": <bucket id>,
        "dataBucketKey": "/"
    },
    type="tileset"
)

# get existing datasource
source = p.get_source(id=<source id>)
```

Create a new task or get an existing one:
```python
# create new task
task = p.create_task(
	name="Crazy Task name",
	parameters = {
		epsgCode: 25833, # your prefered epsg code
		dataset: {
			type: "internal",
			dataBucketId: <bucket id>,
			dataBucketKey: "/"  # Pfad innerhalb des Buckets
		},
		datasource: {
		    "command": "update",
		    "datasourceId": <source id>,
	    }
	},
	jobType = "pointcloud",
	schedule = Schedule(type="immediate")
)

# get existing task
task = p.get_task(id=<task id>)
```

# Missing Features?
If you want to add features or fix bugs, feel free to fork the repository and open a pull request. We are happy about every contribution.
If you can't or don't want to contribute, you can also open an issue and describe your problem or feature request. We will try to help you as soon as possible.

# License
Pyblisher is licensed under the MIT License. For more information, see the LICENSE file.
