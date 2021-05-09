const statesUrl = "https://cdn-api.co-vin.in/api/v2/admin/location/states"
const districtUrl = "https://cdn-api.co-vin.in/api/v2/admin/location/districts/"

$(document).ready(function () {
    initializeSearchType()
})

function initializeSearchType() {


    var showPincode = function (status) {
        if (status) {
            $("#pincode-field").show()
        }
        else {
            $("#pincode-field").hide()
            $("#id_pincode").val('')
        }
    }

    var showDistrict = function (status) {
        if (status) {
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

    var updateSearchType = function (event) {
        showPincode(event == 'pincode')
        showDistrict(event == 'district')
    }

    var currentSelection = document.querySelector('input[name="search_type"]:checked').value
    updateSearchType(currentSelection)

    var searchType = $("#search_type-field")
    for (var i = 0; i < searchType.length; i++) {
        searchType[i].addEventListener('change', function (event) {
            updateSearchType(event.target.value)
        });
    }
}

function getStateList() {
    var states = {}
    var xhr = new XMLHttpRequest()
    xhr.onreadystatechange = function () {
        if (xhr.readyState === 4) {
            states = JSON.parse(xhr.responseText)["states"];
            var mySelect = $('#id_state');
            mySelect.empty()
            mySelect.append('<option class="form-control" value="" disabled selected>Select State</option>')
            states.forEach(element => {
                mySelect.append(
                    $('<option class="form-control"></option>').val(element["state_id"]).html(element["state_name"])
                );
            });
            mySelect.trigger('change')
        }
    }
    xhr.open('GET', statesUrl);
    xhr.send()

}

function updateDistricts() {
    
    if (this.value === "") {
        var mySelect = $('#id_district_id');
        mySelect.empty()
        mySelect.append('<option class="form-control" value="" disabled selected>Select District</option>')
        return;

    }
    var xhr = new XMLHttpRequest()
    xhr.onreadystatechange = function () {
        if (xhr.readyState === 4) {
            states = JSON.parse(xhr.responseText)["districts"];
            var mySelect = $('#id_district_id');
            mySelect.empty()
            mySelect.append('<option class="form-control" value="" disabled selected>Select District</option>')
            states.forEach(element => {
                mySelect.append(
                    $('<option class="form-control"></option>').val(element["district_id"]).html(element["district_name"])
                );
            });
            mySelect.trigger('change')
        }
    }
    xhr.open('GET', districtUrl + this.value);
    xhr.send()

}