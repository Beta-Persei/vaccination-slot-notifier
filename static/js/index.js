const statesUrl = "https://cdn-api.co-vin.in/api/v2/admin/location/states"
const districtUrl = "https://cdn-api.co-vin.in/api/v2/admin/location/districts"

$(document).ready(function () {
    let showPincode = (show) => {
        if (show) {
            $("#pincode-field").show()
        }
        else {
            $("#pincode-field").hide()
            $("#id_pincode").val('')
        }
    }

    let showDistrict = (show) => {
        if (show) {
            $("#district-id-field").show()
            $("#state-field").show()
            $('#id_state').change(updateDistricts);
            getStateList()
        }
        else {
            $("#district-id-field").hide()
            $("#state-field").hide()
            $("#district-id-field").val('')
            $("#state-field").val('')
        }
    }

    let updateSearchType = function (event) {
        showPincode(event == 'pincode')
        showDistrict(event == 'district')
    }

    let currentSelection = document.querySelector('input[name="search_type"]:checked').value
    updateSearchType(currentSelection)

    let searchType = $("#search_type-field")
    for (const type of searchType) {
        type.addEventListener('change', function (event) {
            updateSearchType(event.target.value)
        })
    }
})

function getStateList() {
    let state = $('#id_state');

    fetch(statesUrl)
        .then((response) => response.json())
        .then(({ states }) => {
            state.empty()
            state.append('<option class="form-control" value="" disabled selected>Select State</option>')
            states.forEach(element => {
                state.append(
                    $('<option class="form-control"></option>').val(element["state_id"]).html(element["state_name"])
                )
            })
            state.trigger('change')
        })
        .catch((error) => alert("An error occurred, please try again."))
}

function updateDistricts() {
    let district = $('#id_district_id');
    
    if (!this.value) {
        district.empty()
        district.append('<option class="form-control" value="" disabled selected>Select District</option>')
        return
    }

    fetch(`${districtUrl}/${this.value}`)
        .then((response) => response.json())
        .then(({ districts }) => {
            district.empty()
            district.append('<option class="form-control" value="" disabled selected>Select District</option>')
            districts.forEach(element => {
                district.append(
                    $('<option class="form-control"></option>').val(element["district_id"]).html(element["district_name"])
                )
            })
            district.trigger('change')
        })
        .catch((error) => alert("An error occurred, please try again."))
}