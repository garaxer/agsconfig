# coding=utf-8
"""Tests for ogc metadata attributes. """

# Python 2/3 compatibility
# pylint: disable=wildcard-import,unused-wildcard-import,wrong-import-order,wrong-import-position
from __future__ import (absolute_import, division, print_function, unicode_literals)
from future.builtins import *
from future.builtins.disabled import *
from future.standard_library import install_aliases
install_aliases()
# pylint: enable=wildcard-import,unused-wildcard-import,wrong-import-order,wrong-import-position

import pytest

from .helpers import map_service_config, image_service_config


GETTER_TEST_VALUES = [
    ("britney_spears", "should cause an", AttributeError),  # because she isn't a member
    ("abstract", "This is the abstract.", None),
    ("access_constraints", "There are no access constraints.", None),
    ("city", "Brisbane", None),
    ("country", "Australia", None),
    ("keyword", "These Are Keywords", None),
    ("fees", "There are no fees.", None),
    ("name", "Test_Service", None),
    ("title", "Test Service", None)
]

SETTER_TEST_VALUES = [
    ("britney_spears", "should cause an", TypeError),  # because she isn't a member
    ("abstract", "This is the new abstract.", None),
    ("access_constraints", "Access is not allowed.", None),
    ("city", "Panama City", None),
    ("country", "Republic of Panama", None),
    ("keyword", "These Are Also Keywords", None),
    ("fees", "nil", None),
    ("name", "FooBar_Service", None),
    ("title", "The FooBar Service", None)
]

@pytest.fixture(params=["wcs_server", "wfs_server", "wms_server"])
def map_service_extension(request):
    return request.param

@pytest.fixture(params=["wcs_server", "wms_server"])
def image_service_extension(request):
    return request.param

@pytest.mark.parametrize(
    ("attribute", "expected_value", "exception"),
    GETTER_TEST_VALUES
)
def test_map_ogc_getters(map_service_config, map_service_extension, attribute, expected_value, exception):
    _test_ogc_getters(map_service_config, map_service_extension, attribute, expected_value, exception)

@pytest.mark.parametrize(
    ("attribute", "expected_value", "exception"),
    GETTER_TEST_VALUES
)
def test_image_ogc_getters(image_service_config, image_service_extension, attribute, expected_value, exception):
    _test_ogc_getters(image_service_config, image_service_extension, attribute, expected_value, exception)

@pytest.mark.parametrize(
    ("attribute", "new_value", "exception"),
    SETTER_TEST_VALUES
)
def test_map_ogc_setters(map_service_config, map_service_extension, attribute, new_value, exception):
    _test_ogc_setters(map_service_config, map_service_extension, attribute, new_value, exception)

@pytest.mark.parametrize(
    ("attribute", "new_value", "exception"),
    SETTER_TEST_VALUES
)
def test_image_ogc_setters(image_service_config, image_service_extension, attribute, new_value, exception):
    _test_ogc_setters(image_service_config, image_service_extension, attribute, new_value, exception)

def _test_ogc_getters(service_config, service_extension, attribute, expected_value, exception):
    def get_and_compare():
        assert getattr(service_config[service_extension], attribute) == expected_value

    if exception is not None:
        with pytest.raises(exception):
            get_and_compare()
    else:
        get_and_compare()

def _test_ogc_setters(service_config, service_extension, attribute, new_value, exception):
    def set_and_compare():
        setattr(service_config[service_extension], attribute, new_value)
        assert getattr(service_config[service_extension], attribute) == new_value

    if exception is not None:
        with pytest.raises(exception):
            set_and_compare()
    else:
        set_and_compare()