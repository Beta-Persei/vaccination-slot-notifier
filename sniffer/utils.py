from sniffer.models import Center, State, District

def parse_centers(center_list):
    parsed_center_list = []
    for center in center_list:
        parsed_center_list.append(Center.from_json(center))
    return parsed_center_list

def parse_states(state_list):
    parsed_state_list = []
    for state in state_list:
        parsed_state_list.append(State.from_json(state))
    return parsed_state_list

def parse_districts(district_list):
    parsed_district_list = []
    for state in district_list:
        parsed_district_list.append(District.from_json(state))
    return parsed_district_list
