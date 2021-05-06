const statesUrl = "https://cdn-api.co-vin.in/api/v2/admin/location/states"
const districtUrl = "https://cdn-api.co-vin.in/api/v2/admin/location/districts/"

$(document).ready(function () {
    initializeSearchType()
})

function initializeSearchType() {
    var searchType = $("#search-type-selector")

    var showPincode = function (status) {
        if (status) {
            $("#pincode-field").show()
            $("#district-id-field").val('')
        }
        else {
            $("#pincode-field").hide()
            $("#id_pincode").val('')
        }
    }

    var showDistrict = function (status) {
        if (status) {
            $("#district-field").show()
            $('#state-select').change(updateDistricts);
            getStateList()
        }
        else {
            $("#district-field").hide()
            $("#district-id-field").val('')
        }
    }

    var updateSearchType = function (event) {
        showPincode(event == 'pincode')
        showDistrict(event == 'district')
    }

    var currentSelection = document.querySelector('input[name="search-type"]:checked').value
    updateSearchType(currentSelection)


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
            var mySelect = $('#state-select');
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
    console.log(this.value)
    var xhr = new XMLHttpRequest()
    xhr.onreadystatechange = function () {
        if (xhr.readyState === 4) {
            states = JSON.parse(xhr.responseText)["districts"];
            var mySelect = $('#district-select');
            mySelect.empty()
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