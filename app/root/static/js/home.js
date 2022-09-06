document.addEventListener("DOMContentLoaded", (e) => {
    if (ls_get('BAG') == null) {
        ls_set('BAG', document.getElementById("BAG_text").value);
    }

    if (ls_get('BAG_LEGACY') == null) {
        ls_set('BAG_LEGACY', document.getElementById("compiletype").value);
    }

    // Now we go ahead and load all the aside LS data into the actual aside menu.
    if (ls_get('BAG') == "undefined") {
        // Do nothing (placeholder will show up)
    } else {
        // Set the item value
        document.getElementById("BAG_text").value = atob(ls_get('BAG'));
    }

    if (ls_get('BAG_LEGACY') == "legacy") {
        document.getElementById("compiletype").value = "legacy";
    } else {
        document.getElementById("compiletype").value = "modern";
    }

    document.getElementById("save_bar").addEventListener("click", (e) => {
        document.getElementById("save_bar").style.transform = "translateY(0%)";
    });

    document.getElementById("warning_bar").addEventListener("click", (e) => {
        document.getElementById("warning_bar").style.transform = "translateY(0%)";
    });
})

function set_compiletype() {
    ls_set('BAG_LEGACY', document.getElementById("compiletype").value)
}

function show_modal(modal_id) {
    document.getElementById(modal_id).style.transform = "translateY(-100%)";
}

function save_bag() {
    // Saves BAG data to localstorage
    ls_set('BAG', btoa(document.getElementById("BAG_text").value))

    ls_set('BAG_LEGACY', document.getElementById("compiletype").value)

    // Check if BAG_text contains semicolons
    if (!document.getElementById("BAG_text").value.includes(";") && document.getElementById("compiletype").value == "modern") {
        show_modal("warning_bar");
    } else {
        show_modal("save_bar");
    }
}


function clear_bag() {
    // Clears BAG - NOT FROM LS JUST FROM TEXTAREA
    document.getElementById("BAG_text").value = "";
}

function load_from_file() {
    let file = document.getElementById("BAG_load_from_file").files[0];

    var reader = new FileReader();
    reader.onload = function (e) {
        var textArea = document.getElementById("BAG_text");
        textArea.value = e.target.result;
    };
    reader.readAsText(file);

}