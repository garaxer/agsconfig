# coding=utf-8
"""This module contains the MapServer class for editing MapServer configuration pre or post publish"""

# Python 2/3 compatibility
# pylint: disable=wildcard-import,unused-wildcard-import,wrong-import-order,wrong-import-position
from __future__ import (absolute_import, division, print_function, unicode_literals)
from future.builtins.disabled import *
from future.builtins import *
from future.standard_library import install_aliases

install_aliases()
# pylint: enable=wildcard-import,unused-wildcard-import,wrong-import-order,wrong-import-position

from .._enum import IntEnum, StrEnum
from ..editing.edit_prop import EditorProperty
from .cacheable_core_mixin import CacheableCoreMixin
from .cacheable_ext_mixin import CacheableExtMixin
from .image_dimensions_mixin import ImageDimensionsMixin
from .jpip_server_extension import JPIPServerExtension
from .max_record_count_mixin import MaxRecordCountMixin
from .output_dir_mixin import OutputDirMixin
from .scale_range_mixin import ScaleRangeMixin
from .service_base import ServiceBase
from .wcs_server_extension import WCSServerExtension
from .wms_server_extension import WMSServerExtension

__all__ = ["ImageServer"]


class ImageServer(
    ScaleRangeMixin, OutputDirMixin, CacheableExtMixin, CacheableCoreMixin, ImageDimensionsMixin, MaxRecordCountMixin,
    ServiceBase
):

    _SDDRAFT_IS_CACHED_PATHS = CacheableCoreMixin._SDDRAFT_IS_CACHED_PATHS + [
        {#yapf: disable
            "path": "./Configurations/SVCConfiguration/Definition/Props/PropertyArray/PropertySetProperty[Key = 'IsCached']/Value"
        }#yapf: enable
    ]
    _SDDRAFT_KEY_MAX_RECORD_COUNT = "MaxRecordCount"

    _jpip_server_extension = None
    _wcs_server_extension = None
    _wms_server_extension = None

    class Capability(StrEnum):
        catalog = "Catalog"
        edit = "Edit"
        mensuration = "Mensuration"
        pixels = "Pixels"
        download = "Download"
        image = "Image"
        metadata = "Metadata"
        uploads = "Uploads"

    class CompressionMethod(StrEnum):
        none = "None"
        jpeg = "JPEG"
        lz77 = "LZ77"
        lerc = "LERC"

    class MosaicMethod(StrEnum):
        north_west = "NorthWest"
        center = "Center"
        lock_raster = "LockRaster"
        by_attribute = "ByAttribute"
        nadir = "Nadir"
        viewpoint = "Viewpoint"
        seamline = "Seamline"
        none = "None"

    class ResamplingMethod(IntEnum):
        nearest_neighbor = 0
        bilinear = 1
        cubic = 2
        majority = 3

    def __init__(self, editor):
        super().__init__(editor)
        self._jpip_server_extension = JPIPServerExtension(editor)
        self._wcs_server_extension = WCSServerExtension(editor)
        self._wms_server_extension = WMSServerExtension(editor)

    @property
    def jpip_server(self):
        """Gets the properties for the JPIP Server extension."""
        return self._jpip_server_extension

    @property
    def wcs_server(self):
        """Gets the properties for the WCS Server extension."""
        return self._wcs_server_extension

    @property
    def wms_server(self):
        """Gets the properties for the WMS Server extension."""
        return self._wms_server_extension

    allowed_mosaic_methods = EditorProperty(
        {
            "formats": {
                "agsJson": {
                    "paths": [{
                        "document": "main",
                        "path": "$.properties.allowedMosaicMethods"
                    }],
                    "conversions": [{
                        "id": "enumToString",
                        "enum": "MosaicMethod"
                    }, {
                        "id": "stringToCsv"
                    }]
                },
                "sddraft": {
                    "paths": [
                        {
                            "path": "./Configurations/SVCConfiguration/Definition/ConfigurationProperties/PropertyArray/PropertySetProperty[Key='AllowedMosaicMethods']/Value"
                        }
                    ],
                    "conversions": [{
                        "id": "enumToString",
                        "enum": "MosaicMethod"
                    }, {
                        "id": "stringToCsv"
                    }]
                }
            }
        }
    )

    allowed_compressions = EditorProperty(
        {
            "formats": {
                "agsJson": {
                    "paths": [{
                        "document": "main",
                        "path": "$.properties.allowedCompressions"
                    }],
                    "conversions": [{
                        "id": "enumToString",
                        "enum": "CompressionMethod"
                    }, {
                        "id": "stringToCsv"
                    }]
                },
                "sddraft": {
                    "paths": [
                        {
                            "path": "./Configurations/SVCConfiguration/Definition/ConfigurationProperties/PropertyArray/PropertySetProperty[Key='AllowedCompressions']/Value"
                        }
                    ],
                    "conversions": [{
                        "id": "enumToString",
                        "enum": "CompressionMethod"
                    }, {
                        "id": "stringToCsv"
                    }]
                }
            }
        }
    )

    available_fields = EditorProperty(
        {
            "formats": {
                "sddraft": {
                    "paths": [
                        {
                            "path": "./Configurations/SVCConfiguration/Definition/ConfigurationProperties/PropertyArray/PropertySetProperty[Key='AvailableFields']/Value"
                        }
                    ],
                    "conversions": [{
                        "id": "stringToCsv"
                    }]
                }
            }
        }
    )

    capabilities = EditorProperty(
        {
            "formats": {
                "agsJson": {
                    "paths": [{
                        "document": "main",
                        "path": "$.capabilities"
                    }],
                    "conversions": [{
                        "id": "enumToString",
                        "enum": "Capability"
                    }, {
                        "id": "stringToCsv"
                    }]
                },
                "sddraft": {
                    "paths": [
                        {
                            "path": "./Configurations/SVCConfiguration/Definition/Info/PropertyArray/PropertySetProperty[translate(Key, 'abcdefghijklmnopqrstuvwxyz', 'ABCDEFGHIJKLMNOPQRSTUVWXYZ') = 'WEBCAPABILITIES']/Value"
                        }
                    ],
                    "conversions": [{
                        "id": "enumToString",
                        "enum": "Capability"
                    }, {
                        "id": "stringToCsv"
                    }]
                }
            }
        }
    )

    credits = EditorProperty(
        {
            "formats": {
                "agsJson": {
                    "paths": [
                        {
                            "document": "itemInfo",
                            "path": "$.accessInformation",
                            "parent": {
                                "children": [{
                                    "key": "accessInformation"
                                }]
                            }
                        }, {
                            "document": "main",
                            "path": "$.properties.copyright"
                        }
                    ]
                },
                "sddraft": {
                    "paths": [
                        {
                            "path": "./ItemInfo/Credits"
                        }, {
                            "path": "./Configurations/SVCConfiguration/Definition/ConfigurationProperties/PropertyArray/PropertySetProperty[Key='copyright']/Value"
                        }
                    ]
                }
            }
        }
    )

    default_jpeg_compression_quality = EditorProperty(
        {
            "constraints": {
                "int": True,
                "min": 1,
                "max": 100
            },
            "formats": {
                "agsJson": {
                    "paths": [{
                        "document": "main",
                        "path": "$.properties.defaultCompressionQuality"
                    }]
                },
                "sddraft": {
                    "paths": [
                        {
                            "path": "./Configurations/SVCConfiguration/Definition/ConfigurationProperties/PropertyArray/PropertySetProperty[Key='DefaultCompressionQuality']/Value",
                            "parent": {
                                "children": [
                                    {
                                        "tag": "Value",
                                        "attributes": {
                                            "{http://www.w3.org/2001/XMLSchema-instance}type": "xs:string"
                                        }
                                    }
                                ],
                                "parent": {
                                    "children": [
                                        {
                                            "tag": "PropertySetProperty",
                                            "attributes": {
                                                "{http://www.w3.org/2001/XMLSchema-instance}type": "typens:PropertySetProperty"
                                            },
                                            "children": [{
                                                "tag": "Key",
                                                "value": "DefaultCompressionQuality"
                                            }]
                                        }
                                    ]
                                }
                            }
                        }
                    ],
                    "conversions": [{
                        "id": "numberToString"
                    }]
                }
            }
        }
    )

    default_resampling_method = EditorProperty(
        {
            "formats": {
                "agsJson": {
                    "conversions": [{
                        "id": "enumToString",
                        "enum": "ResamplingMethod"
                    }],
                    "paths": [{
                        "document": "main",
                        "path": "$.properties.defaultResamplingMethod"
                    }]
                },
                "sddraft": {
                    "conversions": [{
                        "id": "enumToString",
                        "enum": "ResamplingMethod"
                    }],
                    "paths": [
                        {
                            "path": "./Configurations/SVCConfiguration/Definition/ConfigurationProperties/PropertyArray/PropertySetProperty[Key='DefaultResamplingMethod']/Value"
                        }
                    ]
                }
            }
        }
    )

    has_valid_sr = EditorProperty(
        {
            "constraints": {
                "readOnly": True
            },
            "formats": {
                "agsJson": {
                    "paths": [{
                        "document": "main",
                        "path": "$.properties.hasValidSR"
                    }]
                },
                "sddraft": {
                    "paths": [
                        {
                            "path": "./Configurations/SVCConfiguration/Definition/ConfigurationProperties/PropertyArray/PropertySetProperty[Key='HasValidSR']/Value"
                        }
                    ]
                }
            }
        }
    )

    max_download_image_count = EditorProperty(
        {
            "constraints": {
                "int": True,
                "min": 0
            },
            "formats": {
                "agsJson": {
                    "conversions": [{
                        "id": "numberToString"
                    }],
                    "paths": [{
                        "document": "main",
                        "path": "$.properties.maxDownloadImageCount"
                    }]
                },
                "sddraft": {
                    "conversions": [{
                        "id": "numberToString"
                    }],
                    "paths": [
                        {
                            "path": "./Configurations/SVCConfiguration/Definition/ConfigurationProperties/PropertyArray/PropertySetProperty[Key='MaxDownloadImageCount']/Value"
                        }
                    ]
                }
            }
        }
    )

    max_download_size_limit = EditorProperty(
        {
            "constraints": {
                "int": True,
                "min": 0
            },
            "formats": {
                "agsJson": {
                    "conversions": [{
                        "id": "numberToString"
                    }],
                    "paths": [{
                        "document": "main",
                        "path": "$.properties.maxDownloadSizeLimit"
                    }]
                },
                "sddraft": {
                    "paths": [
                        {
                            "path": "./Configurations/SVCConfiguration/Definition/ConfigurationProperties/PropertyArray/PropertySetProperty[Key='MaxDownloadSizeLimit']/Value"
                        }
                    ],
                    "conversions": [{
                        "id": "numberToString"
                    }]
                }
            }
        }
    )

    max_mosaic_image_count = EditorProperty(
        {
            "constraints": {
                "int": True,
                "min": 0
            },
            "formats": {
                "agsJson": {
                    "conversions": [{
                        "id": "numberToString"
                    }],
                    "paths": [{
                        "document": "main",
                        "path": "$.properties.maxMosaicImageCount"
                    }]
                },
                "sddraft": {
                    "paths": [
                        {
                            "path": "./Configurations/SVCConfiguration/Definition/ConfigurationProperties/PropertyArray/PropertySetProperty[Key='MaxMosaicImageCount']/Value"
                        }
                    ],
                    "conversions": [{
                        "id": "numberToString"
                    }]
                }
            }
        }
    )

    raster_functions = EditorProperty(
        {
            "formats": {
                "agsJson": {
                    "paths": [{
                        "document": "main",
                        "path": "$.properties.rasterFunctions"
                    }],
                    "conversions": [{
                        "id": "stringToCsv"
                    }]
                },
                "sddraft": {
                    "paths": [
                        {
                            "path": "./Configurations/SVCConfiguration/Definition/ConfigurationProperties/PropertyArray/PropertySetProperty[Key='RasterFunctions']/Value",
                            "parent": {
                                "children": [
                                    {
                                        "tag": "Value",
                                        "attributes": {
                                            "{http://www.w3.org/2001/XMLSchema-instance}type": "xs:string"
                                        }
                                    }
                                ],
                                "parent": {
                                    "children": [
                                        {
                                            "tag": "PropertySetProperty",
                                            "attributes": {
                                                "{http://www.w3.org/2001/XMLSchema-instance}type": "typens:PropertySetProperty"
                                            },
                                            "children": [{
                                                "tag": "Key",
                                                "value": "RasterFunctions"
                                            }]
                                        }
                                    ]
                                }
                            }
                        }
                    ],
                    "conversions": [{
                        "id": "stringToCsv"
                    }]
                }
            }
        }
    )

    return_jpgpng_as_jpg = EditorProperty(
        {
            "formats": {
                "agsJson": {
                    "conversions": [{
                        "id": "boolToString"
                    }],
                    "paths": [{
                        "document": "main",
                        "path": "$.properties.returnJPGPNGAsJPG"
                    }]
                },
                "sddraft": {
                    "conversions": [{
                        "id": "boolToString"
                    }],
                    "paths": [
                        {
                            "path": "./Configurations/SVCConfiguration/Definition/ConfigurationProperties/PropertyArray/PropertySetProperty[Key='ReturnJPGPNGAsJPG']/Value",
                            "parent": {
                                "children": [
                                    {
                                        "tag": "Value",
                                        "attributes": {
                                            "{http://www.w3.org/2001/XMLSchema-instance}type": "xs:string"
                                        }
                                    }
                                ],
                                "parent": {
                                    "children": [
                                        {
                                            "tag": "PropertySetProperty",
                                            "attributes": {
                                                "{http://www.w3.org/2001/XMLSchema-instance}type": "typens:PropertySetProperty"
                                            },
                                            "children": [{
                                                "tag": "Key",
                                                "value": "ReturnJPGPNGAsJPG"
                                            }]
                                        }
                                    ]
                                }
                            }
                        }
                    ]
                }
            }
        }
    )
