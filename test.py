# coding: utf-8
from __future__ import unicode_literals
import csvw


def test_valid(cldf_dataset, cldf_logger):
    assert cldf_dataset.validate(log=cldf_logger)

def test_forms(cldf_dataset):
    assert len(list(cldf_dataset["FormTable"])) == 9030
    assert any(f["Form"] == "jãpirika" for f in cldf_dataset["FormTable"])

def test_parameters(cldf_dataset):
    assert len(list(cldf_dataset["ParameterTable"])) == 128

def test_languages(cldf_dataset):
    assert len(list(cldf_dataset["LanguageTable"])) == 69

def test_valid_title(cldf_dataset, cldf_logger):
    title = cldf_dataset.metadata_dict['dc:title']
    assert title.startswith('CLDF dataset derived from')
    assert title[-4:].isdigit()

