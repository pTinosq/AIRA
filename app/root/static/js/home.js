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
})

function set_compiletype() {
    ls_set('BAG_LEGACY', document.getElementById("compiletype").value)

}

function save_bag() {
    // Saves BAG data to localstorage
    ls_set('BAG', btoa(document.getElementById("BAG_text").value))

    ls_set('BAG_LEGACY', document.getElementById("compiletype").value)

    alert("Saved");
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