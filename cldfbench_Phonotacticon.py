import pathlib
from pycldf import term_uri
from pycldf.sources import Sources
from cldfbench import CLDFSpec
from cldfbench import Dataset as BaseDataset
from clldutils.misc import slug

class Dataset(BaseDataset):
    dir = pathlib.Path(__file__).parent
    id = "Phonotacticon"

    def cldf_specs(self):
        # set this to a structure dataset
        return CLDFSpec(
            dir=self.cldf_dir,
            module="StructureDataset", 
            metadata_fname='cldf-metadata.json')
        
    def cmd_makecldf(self, args):
        """
        Convert the raw data to a CLDF dataset.
        """
        # add LanguageTable
        args.writer.cldf.add_component(
            'LanguageTable', 'Lect', 'Note', 'http://cldf.clld.org/v1.0/terms.rdf#source')
        
        # add ParameterTable
        args.writer.cldf.add_component('ParameterTable')

        # load notes
        notes = {
            o['Lect']: o['Note'] for o in self.raw_dir.read_csv('Phonotacticon1_0Notes.csv', dicts=True)
        }

        # sources
        sources = {
            o['Lect']: f"{o['Lect']}{o['Year']}".replace(" ", "")
            for o in self.raw_dir.read_csv('Phonotacticon1_0Sources.csv', dicts=True)
        }
        
        # Load language data
        languages = {}  # mapping of `Lect` to a language ID
        for o in self.raw_dir.read_csv('Phonotacticon1_0Lects.csv', dicts=True):
            # create a language id from a tidy version of Lect
            languages[o['Lect']] = slug(o['Lect'])
            # add language to LanguageTable
            args.writer.objects['LanguageTable'].append(dict(
                ID=languages[o['Lect']],
                Name=o['Lect'], Lect=o['Lect'], 
                Glottocode=o['Glottocode'],
                Note=notes.get(o['Lect'], ''),
                Source=[sources.get(o['Lect'], '')],
            ))
        
        # store parameters
        parameters = {'phoneme', 'tone'}
        args.writer.objects['ParameterTable'] = [{'ID': p} for p in parameters]
        
        # add tones
        for item_id, o in enumerate(self.raw_dir.read_csv('Phonotacticon1_0Tones.csv', dicts=True), 1):
            args.writer.objects['ValueTable'].append(dict(
                ID=f'tone_{item_id}',
                Language_ID=languages.get(o['Lect'], o['Lect']),
                Parameter_ID='tone',
                Value=o['Tone'],
            ))

        # add phonemes
        for item_id, o in enumerate(self.raw_dir.read_csv('Phonotacticon1_0Phonemes.csv', dicts=True), 1):
            args.writer.objects['ValueTable'].append(dict(
                ID=f'phoneme_{item_id}',
                Language_ID=languages.get(o['Lect'], o['Lect']),
                Parameter_ID='phoneme',
                Value=o['Phoneme'],
            ))
        
        # add new table for sequences
        args.writer.cldf.add_table('sequences.csv', term_uri('id'), 'Language_ID', 'Sequence', 'Order', 'Category', 'Segment')
        args.writer.cldf.add_foreign_key('sequences.csv', 'Language_ID', 'LanguageTable')
        for item_id, o in enumerate(self.raw_dir.read_csv('Phonotacticon1_0Sequences.csv', dicts=True), 1):
           args.writer.objects['sequences.csv'].append(dict(
               ID=f'seq_{item_id}',
               Language_ID=languages.get(o['Lect'], o['Lect']),
               Sequence=o['Sequence'],
               Order=o['Order'],
               Category=o['Category'],
               Segment=o['Segment'],
           ))
        
        # add sources
        args.writer.cldf.add_sources(
            *Sources.from_file(self.raw_dir / 'sources.bib')
        )

