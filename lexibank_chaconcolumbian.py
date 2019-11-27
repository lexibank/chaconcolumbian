import attr
import lingpy
from clldutils.misc import slug
from clldutils.path import Path
from pylexibank import Concept
from pylexibank.dataset import Dataset as BaseDataset
from pylexibank.util import progressbar


@attr.s
class ChaconColConcept(Concept):
    Spanish = attr.ib(default=None)
    Category = attr.ib(default=None)
    Gloss_in_source = attr.ib(default=None)


class Dataset(BaseDataset):
    dir = Path(__file__).parent
    id = "chaconcolumbian"
    concept_class = ChaconColConcept

    def cmd_makecldf(self, args):
        # Read the raw data
        wl_filename = self.raw_dir / "Huber_filtered_130_basic_cult_voc"
        wl = lingpy.Wordlist(wl_filename.as_posix())

        # Write sources
        args.writer.add_sources()

        # Write languages
        languages = args.writer.add_languages(
            lookup_factory="Name"
        )

        # Write concepts
        concepts = {}
        for concept in self.conceptlists[0].concepts.values():
            concept_cldf_id = "%s_%s" % (concept.id.split("-")[-1], slug(concept.english))
            args.writer.add_concept(
                    ID=concept_cldf_id,
                    Name=concept.english,
                    Concepticon_ID=concept.concepticon_id,
                    Concepticon_Gloss=concept.concepticon_gloss,
                    Spanish=concept.attributes["spanish"],
                    Gloss_in_source=concept.attributes["gloss_in_source"],
                    Category=concept.attributes["category"],
                )
            concepts[concept.attributes['gloss_in_source']] = concept_cldf_id

        # write lexemes
        for entry in progressbar(wl, desc="makecldf"):
            if wl[entry, "concept"]:
                # add form
                lex = args.writer.add_form_with_segments(
                        Language_ID=languages[wl[entry, "doculect"]],
                        Parameter_ID=concepts[wl[entry, "concept"]],
                        Value=wl[entry, "counterpart"],
                        Form=wl[entry, "counterpart"],
                        Segments=wl[entry, "tokens"],
                        Source="Huber1992",
                )

                # add cogid
                cid = "%s-%s" % (concepts[wl[entry, 'concept']], wl[entry, "cogid"])
                args.writer.add_cognate(
                        lexeme=lex,
                        Cognateset_ID=cid,
                        Source=["Chacon2017"],
                        Alignment=wl[entry, "alignment"],
                        Alignment_Source="Chacon2017",
                    )
