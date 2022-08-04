document.addEventListener("DOMContentLoaded", (e) => {
    if (ls_get('BAG') == null) {
        ls_set('BAG', document.getElementById("BAG_text").value);
    }

    // Now we go ahead and load all the aside LS data into the actual aside menu.
    if (ls_get('BAG') == "undefined") {
        // Do nothing (placeholder will show up)
    } else {
        // Set the item value
        document.getElementById("BAG_text").value = atob(ls_get('BAG'));
    }
})

function save_bag() {
    // Saves BAG data to localstorage
    ls_set('BAG', btoa(document.getElementById("BAG_text").value))
}