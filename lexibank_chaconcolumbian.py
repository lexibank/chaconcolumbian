import attr
import lingpy
from clldutils.misc import slug
from clldutils.path import Path
from pylexibank import Concept
from pylexibank.dataset import Dataset as BaseDataset
from pylexibank.util import progressbar


@attr.s
class CustomConcept(Concept):
    Spanish = attr.ib(default=None)
    Category = attr.ib(default=None)
    Gloss_in_source = attr.ib(default=None)


class Dataset(BaseDataset):
    dir = Path(__file__).parent
    id = "chaconcolumbian"
    concept_class = CustomConcept

    def cmd_makecldf(self, args):
        # Read the raw data
        wl_filename = self.raw_dir / "Huber_filtered_130_basic_cult_voc"
        wl = lingpy.Wordlist(wl_filename.as_posix())

        # Write sources
        args.writer.add_sources()

        # Write languages
        languages = args.writer.add_languages(lookup_factory="Name")

        # Write concepts
        concepts = {}
        for concept in self.conceptlists[0].concepts.values():
            concept_cldf_id = "%s_%s" % (
                concept.id.split("-")[-1],
                slug(concept.english),
            )
            args.writer.add_concept(
                ID=concept_cldf_id,
                Name=concept.english,
                Concepticon_ID=concept.concepticon_id,
                Concepticon_Gloss=concept.concepticon_gloss,
                Spanish=concept.attributes["spanish"],
                Gloss_in_source=concept.attributes["gloss_in_source"],
                Category=concept.attributes["category"],
            )
            concepts[concept.attributes["gloss_in_source"]] = concept_cldf_id

        # Hard-coded fixes to segment errors in raw source
        segments = {
            " #h ": " h ",
            " #s ": " s ",
            " aⁱ ": " a j ",
            " aᵘ ": " a w ",
            " eⁱ ": " e j ",
            " hh ": " h h ",
            " hs ": " h s ",
            " i̵ ": " ɨ ",
            " ĩ̵ ": " ɨ̃ ",
            " ĩ̵: ": " ɨ̃ɨ̃ ",
            " i̵: ": " ɨɨ ",
            " ĩ̵ĩ̵ ": " ɨ̃ɨ̃ ",
            " i̵i̵ ": " ɨɨ ",
            " i̵i̵i̵ ": " ɨ ɨɨ ",
            " ɩ ": " ɪ ",
            " ɩɩ ": " ɪɪ ",
            " k jh ": " kʲ h ",
            " ll ": " l l ",
            " ls ": " l s ",
            " mm ": " m m ",
            " nn ": " n n  ",
            " nss ": " n s ",
            " ŋŋ ": " ŋ ŋ ",
            " oᵘ ": " o w ",
            " rh ": " r h ",
            " rr ": " r r ",
            " rs ": " r s ",
            " ɾh ": " ɾ h ",
            " ɾs ": " ɾ s ",
            " sh ": " s h ",
            " ss ": " s s ",
            " vh ": " vʰ ",
            " vhs ": " vʰ s ",
            " xh ": " x h ",
        }

        # write lexemes
        for entry in progressbar(wl, desc="makecldf"):
            if wl[entry, "concept"]:
                # fix errors in segments: as in some cases there is no
                # direct mapping (one segment in source becoming two, or
                # similar) we need to manipulate the string directly.
                fixed_segments = " %s " % " ".join(wl[entry, "tokens"])
                for source, target in segments.items():
                    fixed_segments = fixed_segments.replace(source, target)
                fixed_segments = fixed_segments.strip().split()

                # add form
                lex = args.writer.add_form_with_segments(
                    Language_ID=languages[wl[entry, "doculect"]],
                    Parameter_ID=concepts[wl[entry, "concept"]],
                    Value=wl[entry, "counterpart"],
                    Form=wl[entry, "counterpart"],
                    Segments=fixed_segments,
                    Source="Huber1992",
                )

                # add cogid
                cid = "%s-%s" % (
                    concepts[wl[entry, "concept"]],
                    wl[entry, "cogid"],
                )
                args.writer.add_cognate(
                    lexeme=lex,
                    Cognateset_ID=cid,
                    Source=["Chacon2017"],
                    Alignment=wl[entry, "alignment"],
                    Alignment_Source="Chacon2017",
                )
