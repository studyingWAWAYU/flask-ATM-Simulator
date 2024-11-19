document.addEventListener("DOMContentLoaded", function() {
    var currentGender = document.getElementById("currentGender").value;
    var genderSelect = document.getElementById("gender");
    for (var i = 0; i < genderSelect.options.length; i++) {
        if (genderSelect.options[i].value === currentGender) {
            genderSelect.options[i].selected = true;
            break;
        }
    }
});