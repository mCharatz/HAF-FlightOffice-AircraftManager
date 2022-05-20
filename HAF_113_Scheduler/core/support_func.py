def is_between(start_month, start_year, end_month, end_year, month, year):
    months = {
        'ΙΑΝΟΥΑΡΙΟΣ': 1,
        'ΦΕΒΡΟΥΑΡΙΟΣ': 2,
        'ΜΑΡΤΙΟΣ': 3,
        'ΑΠΡΙΛΙΟΣ': 4,
        'ΜΑΙΟΣ': 5,
        'ΙΟΥΝΙΟΣ': 6,
        'ΙΟΥΛΙΟΣ': 7,
        'ΑΥΓΟΥΣΤΟΣ': 8,
        'ΣΕΠΤΕΜΒΡΙΟΣ': 9,
        'ΟΚΤΩΒΡΙΟΣ': 10,
        'ΝΟΕΜΒΡΙΟΣ': 11,
        'ΔΕΚΕΜΒΡΙΟΣ': 12
    }

    month = months.get(month, None)
    start_month = months.get(start_month, None)
    end_month = months.get(end_month, None)

    start_date = (start_year, start_month,)
    end_date = (end_year, end_month,)
    search_date = (year, month)

    if start_date <= search_date <= end_date:
        return True
    else:
        return False
