from datetime import datetime
from dateutil.relativedelta import relativedelta
from database_functions.provider_functions import get_providers, get_provider_by_name
from database_functions.date_functions import get_date_range, get_provider_dates

from database_functions.schema import ProviderDate, DateAttribute

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
    def getRankingForDate(self, date, rank_start=None, rank_end=None):
        
        #Get providers on date
        providers = get_providers(session=self.session,
            date=date,
            provider_attributes_specified=self.provider_attr_included,
            date_attributes_excluded=self.date_attr_exlcuded)
        
        attr_percent_dict = dict()
        for provider in providers:
            total_date_amt = len(get_provider_dates(self.session,provider,
                                                    start=rank_start,
                                                    end=rank_end))
            attr_date_amt = len(get_provider_dates(self.session,
                                                   provider,
                                                   start=rank_start,
                                                   end=rank_end,
                                                   date_attributes_included=[self.ranking_attr]))
            # if attr_date_amt != 0:
            attr_percent_dict[provider.name] = attr_date_amt/total_date_amt if total_date_amt != 0 else 0
        ranked_list = sorted(list(attr_percent_dict.keys()), key=lambda n: attr_percent_dict[n])

        attributed_names = ranked_list[:self.attribution_ammount]
        for name in attributed_names:

            provider = get_provider_by_name(self.session, name)

            provider_date = (
            self.session.query(ProviderDate)
            .filter(
                ProviderDate.provider_id == provider.id,
                ProviderDate.date == date
            )
            .one_or_none()
            )
            if provider_date:
                provider_date.attributes.append(DateAttribute(name=self.ranking_attr))
                print(provider_date.attributes)
            else:
                print("error",provider, date)
        self.session.commit()

        return
        
        
        
        
        
        
        
        