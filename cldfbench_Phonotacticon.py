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

        # TODO: better item_id?  = f"{o['Lect']}-"
        # TODO: better parameters?
        # TODO: language_id -> glottocode mapping
        # TODO: sort out code table
        
        languages, parameters = set(), set()
        for item_id, o in enumerate(self.raw_dir.read_csv('Phonotacticon1_0Segments.csv', dicts=True), 1):
            parameter_id = slug(f"{o['Sequence']}_{o['Order']}_{o['Category']}")
            #OrderedDict({'Sequence': 'ntstf', 'Order': '5', 'Lect': 'Russian', 'Category': 'Coda', 'ipa': 'f'})
            args.writer.objects['ValueTable'].append(dict(
                ID=item_id,
                Language_ID=o['Lect'],
                Parameter_ID=parameter_id,
                Sequence=o['Sequence'],
                Order=o['Order'],
                Category=o['Category'],
                Value=o['ipa'],
            ))
            
            languages.add(o['Lect'])
            parameters.add(parameter_id)
        
        args.writer.cldf.add_component(
            'LanguageTable',
            'http://cldf.clld.org/v1.0/terms.rdf#source')
        args.writer.cldf.add_component('ParameterTable')
        
        args.writer.cldf.add_columns('ValueTable', 'Sequence')
        args.writer.cldf.add_columns('ValueTable', 'Order')
        args.writer.cldf.add_columns('ValueTable', 'Category')
        
        
        args.writer.objects['LanguageTable'] = [{'ID': slug(o), 'Name': o} for o in languages]
        args.writer.objects['ParameterTable'] = [{'ID': p} for p in parameters]