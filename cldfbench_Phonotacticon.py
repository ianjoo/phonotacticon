import pathlib
from cldfbench import CLDFSpec
from cldfbench import Dataset as BaseDataset
from clldutils.misc import slug


class Dataset(BaseDataset):
    dir = pathlib.Path(__file__).parent
    id = "Phonotacticon"

    def cldf_specs(self):
        # set this to a structure dataset
        return CLDFSpec(dir=self.cldf_dir, module="StructureDataset")
        
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
                Note=notes.get(o['Lect'], '')
            ))
        
        # store parameters
        parameters = {'phoneme', 'tone'}
        
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


        # TODO: better item_id?  = f"{o['Lect']}-"
        # TODO: better parameters?
        # TODO: sort out code table
        # TODO Phonotacticon1_0Sequences.csv
        # TODO Phonotacticon1_0Sources.csv
        
        #for item_id, o in enumerate(self.raw_dir.read_csv('Phonotacticon1_0Segments.csv', dicts=True), 1):
        #    parameter_id = slug(f"{o['Sequence']}_{o['Order']}_{o['Category']}")
        #    args.writer.objects['ValueTable'].append(dict(
        #        ID=f'seg_{item_id}',
        #        Language_ID=languages.get(o['Lect'], o['Lect']),
        #        Parameter_ID=parameter_id,
        #        Sequence=o['Sequence'],
        #        Order=o['Order'],
        #        Category=o['Category'],
        #        Value=o['ipa'],
        #    ))
        #    parameters.add(parameter_id)
            
        
        
        
        
        
        

        # args.writer.cldf.add_columns('ValueTable', 'Sequence')
        # args.writer.cldf.add_columns('ValueTable', 'Order')
        # args.writer.cldf.add_columns('ValueTable', 'Category')

        args.writer.objects['ParameterTable'] = [{'ID': p} for p in parameters]