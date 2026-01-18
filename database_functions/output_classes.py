from file_classes.csv_classes import *
from database_functions.provider_functions import get_providers
from database_functions.date_functions import get_date_range

def previous_year_month(iso_year_month: str) -> str:
    dt = datetime.strptime(iso_year_month, "%Y-%m")
    return (dt - relativedelta(months=1)).strftime("%Y-%m")

class AttributeList():
    def __init__(self, session, attribute, exluded_attributes=None):
        self.session = session
        self.attribute = attribute
        self.excluded_attributes = exluded_attributes

    def get_ranking(self, start_date=None, end_date=None, ammount_to_display=None):
        return 


class CycleList(AttributeList):
    def __init__(self, session, attribute, exluded_attributes=None, cycle_ammount=1):
        super().__init__(session, attribute, exluded_attributes)
        self.cycle_ammount = cycle_ammount

    def get_ranking(self, start_date=None, end_date=None, ammount_to_display=None):
        master_list = get_providers(self.session, provider_attributes_specified=self.attribute, provider_attributes_excluded=self.excluded_attributes)
        date_range = get_date_range(self.session, start_date, end_date)

        output_dict = dict()

        for date in date_range:
            providers_on_date = get_providers(self.session, provider_attributes_specified=[self.attribute])
            
            ranked_providers = [p for p in master_list if p in providers_on_date]
            top_ranked = ranked_providers[:self.cycle_ammount]
            for p in top_ranked:
                master_list.remove(p)
            master_list += top_ranked

            output_dict[date] = ranked_providers

        return output_dict

class OutputSheet():
    def __init__(self, chunk_pattern, start_date=None, end_date=None, spacing=1, chunks_per_row=5):
        self.chunk_pattern = chunk_pattern
        self.spacing = spacing
        chunks_per_row = chunks_per_row

    def generate_sheet(self):
        output = []
        for column in self.chunk_pattern.columns:
            for lst in column.lists:
                output.append(lst.get_ranking())

        return output
        
                


class OutputColumn():
    def __init__(self, lists, vertical_spacing):
        self.lists = lists
        self.vertical_sapcing = vertical_spacing

class OutputChunk():
    def __init__(self, columns, horizontal_spacing):
        self.columns = columns
        self.horizontal_spaacing = horizontal_spacing
