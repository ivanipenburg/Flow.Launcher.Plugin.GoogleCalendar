def check_leap_year(year):
    # Check if year is leap year
    if year % 4 == 0:
        # Check if year is century year
        if year % 100 == 0:
            # Check if year is divisible by 400
            if year % 400 == 0:
                # Leap year
                return True 
        else:
            # Leap year
            return True

    return False

def date_to_glyph_id(datetime):
    base_id = 0xe900

    # Convert date to number of day in year from 1 to 366
    day = datetime.timetuple().tm_yday - 1

    if not check_leap_year(datetime.year) and day >= 59:
        # Leap year
        day += 1

    # Convert day to glyph id with string of form "e900"
    glyph_id = base_id + day

    return chr(glyph_id)


