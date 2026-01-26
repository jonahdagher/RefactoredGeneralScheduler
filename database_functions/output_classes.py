from file_classes.csv_classes import *
from database_functions.provider_functions import get_providers
from database_functions.date_functions import get_date_range, get_provider_dates

def previous_year_month(iso_year_month: str) -> str:
    dt = datetime.strptime(iso_year_month, "%Y-%m")
    return (dt - relativedelta(months=1)).strftime("%Y-%m")

class RankedOutput():
    def __init__(self, session, ranking_attribute, attribution_ammount = -1, date_attributes_excluded=None, provider_attributes_included=None):
        self.ranking_attr = ranking_attribute
        self.date_attr_exlcuded = date_attributes_excluded
        self.provider_attr_included = provider_attributes_included
        self.session = session
        self.attribution_ammount = attribution_ammount

    def getRankingForDate(self, date):
        return
    
class RankedPercentOutput(RankedOutput):
    def getRankingForDate(self, date):
        
        # self.session.execute(delete(DateAttribute).join(ProviderDate).where(ProviderDate.date == date))

        providers = get_providers(session=self.session,
                             date=date,
                      provider_attributes_specified=self.provider_attr_included,
                      date_attributes_excluded=self.date_attr_exlcuded)
        
        output_dict = dict()
        for p in providers:
            days_extra = get_provider_dates(self.session, p.name, [self.ranking_attr])
            days_working = get_provider_dates(self.session, p.name, date_attributes_excluded=["OFF"])
            output_dict[p.name] = 0 if len(days_working) == 0 else 100 * round(len(days_extra)/len(days_working), 2)
            sorted_list = sorted(output_dict, key=lambda x: output_dict[x], reverse=True)

            for name in sorted_list[:self.attribution_ammount]:
                provider_date = self.session.execute(
                                select(ProviderDate).where(ProviderDate.date==date).join(Provider).where(Provider.name==name)
                            ).scalar_one_or_none()
                provider_date.attributes.append(DateAttribute(
                    name = self.ranking_attr
                ))
            self.session.commit()

        return sorted_list
        
        
        