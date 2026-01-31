from database_functions.date_functions import get_date_range, get_providers_on_date, get_date_attributes

def get_provider_calendar_entries(session, start:str, end:str, attributes_filter:set[str] = None, filterExclusively:bool = True):
    """
    Returns entry dictionaries for providers working within a date range, optionally filtered
    by DateAttribute names

    For each date in the specified range, the function checks which providers are scheduled to
    work and checks if their associated DateAttributes meet the required criteria
    
    Args:
        :param session: Active SQLAlchemy session used for database queries

        :param start_date: Inclusive start date for date range
        :type start_date: str ("YYYY-MM-DD")
        :param end_date: Inclusive end date for date range
        :type end_date: str ("YYYY-MM-DD")

        :param attributes_filter: Set of DateAttribute names used to filter providers. 
            If None, all working providers will be returned
        :type attributes_filter: set[str]

        :param filterExclusively: If True, ALL filters must be met for a calendar entry to be returned
        :type filterExclusively: bool
    Returns:
        list[dict]: A list of calendar entry dictionaries. Each dioct contains:
            - "date" (str) an ISO formatted string ("YYYY-MM-DD")
            - "title" (str) Provider name and attribute list ("Name [attr1, attr2, ...]) 
    """

    entries = []
    print(get_date_range(session, start_date=start, end_date=start))
    for d in get_date_range(session, start, end):
        providers_on_day = get_providers_on_date(session, d)

        #Get the DateAttributes for each provider working on a given day
        for provider in providers_on_day:
            attributes_on_day = {a.name for a in get_date_attributes(session, provider, d)}

            #Determine if the provider should be displayed
            if not attributes_filter: #Add all if no attributes are provided
                isValid = True
            elif not filterExclusively: #Add if ANY specified attribute is met
                isValid = bool(attributes_on_day & attributes_filter)
            elif filterExclusively: #add if ALL specified attributes are met
                isValid = attributes_filter.issubset(attributes_on_day)

            #Add provider name/day to calendar
            if isValid:
                entry = {
                    "date": d,
                    "title": provider.name + " [" + ", ".join(attributes_on_day) + "]"
                }
                entries.append(entry)
    return entries