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
            "#": "+",
            "ks": "k s",
            "ms": "m s",
            "ᵑg": "ⁿg",
            "bs": "b s",
            "gs": "g s",
            "#h": "+ h",
            "#s": "+ s",
            "a:": "aː",
            "ãã": "ãː",
            "aⁱ": " ai",
            "aᵘ": " au",
            "bb": "bː",
            "bh": "bʱ",
            "ch": "tʃ",
            "ʤ": "dʒ",
            "e:": "eː",
            "ee": "eː",
            "ẽẽ": "ẽː",
            "eee": "eː",
            "eⁱ": " ei",
            "ɛɛ": "ɛː",
            "gg": "gː",
            "hh": " h + h",
            "hs": " h + s",
            "i̵:": " ɨː",
            "ĩ̵:": " ɨ̃ː",
            "i:": "iː",
            "i̵": " ɨ",
            "ĩ̵": " ɨ̃",
            "i̵i̵": " ɨː ",
            "ĩ̵ĩ̵": " ɨ̃ː",
            "ii": "iː",
            "ĩĩ": "ĩː",
            "i̵i̵i̵": "ɨː",
            "ɩ": " ɪ",
            "ɩɩ": " ɪː",
            "jh": " jh/j",
            "kh": "kʰ",
            "kʰʲ": "kʲʰ",
            "kk": "kː",
            "kw": "kʷ",
            "ll": " lː",
            "ls": " l s",
            "ls": "l s",
            "mh": "m h",
            "mm": " mː",
            "nh": "n̥",
            "nn": " nː",
            "ns": "n s",
            "nss": "n + s",
            "ŋh": "ŋ h",
            "ŋŋ": " ŋ ŋ",
            "ŋŋ": "ŋː",
            "õ:": "oː",
            "oo": "oː",
            "oᵘ": " ou",
            "ph": "pʰ",
            "pp": "pː",
            "rh": " rh/r̥",
            "rr": " r r",
            "rs": " r s",
            "ɾh": " ɾ̥",
            "ɾs": " ɾ s",
            "sh": " s h",
            "ss": " s s",
            "ss": "sː",
            "th": "tʰ",
            "tʰʲ": "tʲʰ",
            "tʲh": "tʲʰ",
            "ʧ": "tʃ",
            "ʧʰ": "tʃʰ",
            "tt": "tː",
            "uu": "uː",
            "ũũ": "ũː",
            "ɯɯ": "ɯː",
            "ɯ̃ɯ̃": "ɯ̃ː",
            "vh": " vh/v",
            "vhs": " vh/v s",
            "xh": " xh/x",
            "ʔh": "ʔʰ",
            "ʔs": "ʔ s",
        }

        # write lexemes
        for idx in progressbar(wl, desc="makecldf"):
            if wl[idx, "concept"]:
                lex = args.writer.add_form_with_segments(
                    Language_ID=languages[wl[idx, "doculect"]],
                    Parameter_ID=concepts[wl[idx, "concept"]],
                    Value=wl[idx, "counterpart"],
                    Form=wl[idx, "counterpart"],
                    Segments=" ".join(
                        [segments.get(x, x) for x in wl[idx, "tokens"]]
                    ).split(),
                    Source=["Huber1992"],
                )

                args.writer.add_cognate(
                    lexeme=lex,
                    Cognateset_ID=wl[idx, "cogid"],
                    Source=["Chacon2017"],
                )
