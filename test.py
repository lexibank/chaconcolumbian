# coding: utf-8
from __future__ import unicode_literals
import csvw


def test_valid(cldf_dataset, cldf_logger):
    assert cldf_dataset.validate(log=cldf_logger)

def test_valid_title(cldf_dataset, cldf_logger):
    title = cldf_dataset.metadata_dict['dc:title']
    assert title.startswith('CLDF dataset derived from')
    assert title[-4:].isdigit()
