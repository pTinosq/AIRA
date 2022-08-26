document.addEventListener("DOMContentLoaded", (e) => {
    // This whole system could do with a rework. Not totally confident on its reliability.  
    contents = document.getElementsByClassName("aside_data");

    for (var i = 0; i < contents.length; i++) {
        // If LS data is unset, set it to default (undefined allowed)
        var item = contents[i];
        if (ls_get(item.id) == null) {
            ls_set(item.id, item.value);
        }

        // Now we go ahead and load all the aside LS data into the actual aside menu.
        if (ls_get(item.id) == "undefined") {
            // Do nothing (placeholder will show up)
        } else {
            // Set the item value
            item.value = ls_get(item.id);
        }

        // Add event listeners
        item.addEventListener("change", (e) => {
            var x = e.target;
            ls_set(x.id, x.value);

            // Here's the difference
            get_vbo();
            // That's it
        })
    }
});