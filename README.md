# agsconfig &middot; [![GitHub](https://img.shields.io/badge/license-BSD--3--Clause-brightgreen.svg)](LICENSE) [![Build Status](https://api.travis-ci.com/DavidWhittingham/agsconfig.svg?branch=develop)](https://app.travis-ci.com/github/DavidWhittingham/agsconfig)

agsconfig is a Python library for editing ArcGIS Server service configuration, either before deployment by editing a Service Definition Draft file (generated by either ArcMap, ArcGIS Pro, or via arcpy), or after deployment by editing the JSON configuration provided by ArcGIS Server (via the ArcGIS Server REST Admin API).

This helps to programmatically configure services as part of automated service deployment or configuration patching processes.

## Installation

agsconfig is made available on PyPi, simply install it with `pip`.

```
> pip install agsconfig
```

## Usage

agsconfig contains many classes to alter the configuration of different service types. However, it is not recommended these classes be instantiated directly. Helper functions are available in the top-level module to load different types of services with either Service Defintion Draft based configuration, or ArcGIS Server JSON configuration. These functions are:

- agsconfig.load_image_sddraft
- agsconfig.load_image_service
- agsconfig.load_map_sddraft
- agsconfig.load_map_service
- agsconfig.load_vector_tile_sddraft
- agsconfig.load_vector_tile_service

Each function expects one or more file or file-like objects to be passed in. For functions dealing with Service Definition Drafts, only one file-like object is required. For ArcGIS Server JSON based functions, two are required, the first being the main service JSON, and the second being the _ItemInfo_ JSON. Each file should be opened in binary mode, and with write enabled if you wish to save the changes (as opposed to just reading settings). Save changes seeks the file-like object back to the beginning and overwrites the stream.

### Example: Load/Save a MapServer Service Definiton Draft

```python
import agsconfig

sddraft_path = "path/to/MyService.sddraft"

with open(sddraft_path, mode="rb+") as sddraft:
    map_service = agsconfig.load_map_sddraft(sddraft)

    # Edit your map service configuration
    map_service.capabilities = [agsconfig.MapServer.Capability.map]
    map_service.min_instances = 3
    map_service.max_instances = 6
    map_service.summary = "This is my awesome map service."
    map_service.kml_server.enabled = True

    # Save configuration changes
    map_service.save()
```

## Development

To get started on developing agsconfig, simply fork the repository and get it with your favourite Git client. In the root of the repository is a standalone task runner, [`pie.py`](https://github.com/adamkerz/pie), that can excute tasks contained in `pie_tasks.py`.

You'll need a Python install with `pip` and `virtualenv`, but other than that, no pre-installed dependencies are necessary.

On a shell, simply run the setup task as follows to create a virtual environment for development work:

```
> python .\pie.py setup
```

To get a list of all available tasks, exceute the following:

```
> python .\pie.py -l
```
