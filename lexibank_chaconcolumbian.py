import attr
import lingpy
from clldutils.misc import slug
from clldutils.path import Path
from pylexibank.dataset import Concept
from pylexibank.dataset import Dataset as BaseDataset
from pylexibank.util import pb


@attr.s
class ChaconColConcept(Concept):
    Spanish = attr.ib(default=None)
    Category = attr.ib(default=None)
    Gloss_in_source = attr.ib(default=None)


class Dataset(BaseDataset):
    dir = Path(__file__).parent
    id = "chaconcolumbian"
    concept_class = ChaconColConcept

    def cmd_install(self, **kw):
        # column "counterpart_doculect" gives us the proper names of the doculects
        wl = lingpy.Wordlist(self.raw.posix("Huber_filtered_130_basic_cult_voc"))

        with self.cldf as ds:
            concepts = {}
            ds.add_sources(*self.raw.read_bib())

            for l in self.languages:
                ds.add_language(ID=slug(l["Name"]), Name=l["Name"], Glottocode=l["Glottocode"])

            for concept in self.conceptlist.concepts.values():
                ds.add_concept(
                    ID=concept.id,
                    Name=concept.english,
                    Concepticon_ID=concept.concepticon_id,
                    Concepticon_Gloss=concept.concepticon_gloss,
                    Spanish=concept.attributes["spanish"],
                    Gloss_in_source=concept.attributes["gloss_in_source"],
                    Category=concept.attributes["category"],
                )
                concepts[slug(concept.attributes["gloss_in_source"])] = concept.id

            for k in pb(wl, desc="wl-to-cldf"):
                if wl[k, "concept"]:
                    for row in ds.add_lexemes(
                        Language_ID=slug(wl[k, "doculect"]),
                        Parameter_ID=concepts[slug(wl[k, "concept"])],
                        Value=wl[k, "counterpart"],
                        Segments=wl[k, "tokens"],
                        Source="Huber1992",
                    ):
                        cid = slug(wl[k, "concept"] + "-" + "{0}".format(wl[k, "cogid"]))
                        ds.add_cognate(
                            lexeme=row,
                            Cognateset_ID=cid,
                            Source=["Chacon2017"],
                            Alignment=wl[k, "alignment"],
                            Alignment_Source="Chacon2017",
                        )
