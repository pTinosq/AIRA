document.addEventListener("DOMContentLoaded", function (event) {
    var w = window.innerWidth;
    if (w < 900) {
        alert("This website was built for desktop use only. A larger screen is highly recommended.");
    }

    if (document.getElementById("delta_aside_fl").value == "") {
        document.getElementById("delta_aside_fl").value = 10e-2;
    }

    if (document.getElementById("epsilon_aside_fl").value == "") {
        document.getElementById("epsilon_aside_fl").value = 10e-4;
    }




});