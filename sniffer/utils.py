from sniffer.models import Center


def parse_centers(center_list):
    parsed_center_list = []
    for center in center_list:
        parsed_center_list.append(Center.from_json(center))
    return parsed_center_list
