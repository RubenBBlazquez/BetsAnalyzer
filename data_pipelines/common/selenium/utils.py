def get_stat(row, stat_name: str, cast_type, is_link=False):
    """
    Helper method to extract a stat from a row and cast it to the desired type.
    """
    try:
        if is_link:
            return row.select_one(f"td[data-stat='{stat_name}'] > a").text
        return row.find("td", {"data-stat": stat_name}).text
    except (AttributeError, ValueError):
        return None if cast_type is str else cast_type()
