# coding=utf-8
from __future__ import unicode_literals, print_function
from itertools import groupby

import attr
import lingpy
from pycldf.sources import Source
from clldutils.path import Path
from clldutils.misc import slug

from pylexibank.dataset import Metadata, Concept
from pylexibank.dataset import Dataset as BaseDataset
from pylexibank.util import pb


@attr.s
class HConcept(Concept):
    Spanish_Gloss = attr.ib(default=None)


class Dataset(BaseDataset):
    dir = Path(__file__).parent
    id = 'chaconcolumbian'
    concept_class = HConcept

    def cmd_install(self, **kw):
        # column "counterpart_doculect" gives us the proper names of the doculects
        wl = lingpy.Wordlist(self.raw.posix('Huber_filtered_130_basic_cult_voc'))


        with self.cldf as ds:
            ds.add_sources(*self.raw.read_bib())

            for l in self.languages:
                ds.add_language(
                        ID=slug(l['Name']),
                        Name=l['Name'],
                        Glottocode=l['Glottocode']
                        )
            for c in self.concepts:
                ds.add_concept(
                        ID=slug(c['GLOSS_IN_SOURCE']),
                        Name=c['ENGLISH'],
                        Concepticon_ID=c['CONCEPTICON_ID'] or '',
                        Spanish_Gloss=c['SPANISH']
                        )
            # specify valid entries in the data
            valid_entries = [c['GLOSS_IN_SOURCE'] for c in self.concepts]

            for k in pb(wl, desc='wl-to-cldf'):
                if wl[k, 'concept'] in valid_entries:
                    for row in ds.add_lexemes(
                            Language_ID=slug(wl[k, 'doculect']),
                            Parameter_ID=slug(wl[k, 'concept']),
                            Value=wl[k, 'counterpart'],
                            Form=wl[k, 'counterpart'],
                            Segments=wl[k, 'tokens'],
                            Source='Huber1992'
                            ):
                            cid = slug(wl[k, 'concept'] + '-' + '{0}'.format(wl[k,
                                'cogid']))
                            ds.add_cognate(
                                lexeme=row,
                                Cognateset_ID=cid,
                                Source=['Chacon2017'],
                                Alignment=wl[k, 'alignment'],
                                Alignment_Source='Chacon2017'
                                )

