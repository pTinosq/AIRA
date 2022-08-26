hotkey_data = {}

document.addEventListener('DOMContentLoaded', (e) => {
    document.getElementById("keybinds_modal").addEventListener('click', (e) => {
        if (e.target.id == 'keybinds_modal') {
            close_keybind_modal();
        }
    })

    // Add evt listeners to all data-hotkey elements
    var hotkey_elements = document.querySelectorAll('[data-hotkey]');
    var i = 0;
    for (i = 0; i < hotkey_elements.length; i++) {
        let hk_e = hotkey_elements[i];
        let hk = hotkey_elements[i].getAttribute('data-hotkey');
        let keybinds = [hk];

        if (hk.includes(',')) {
            keybinds = hk.split(',');
            keybinds.forEach((element) => {
                hotkey_data[element] = hk_e;
            });

        } else {
            hotkey_data[hk_e.getAttribute('data-hotkey')] = hk_e;
        }
    }

    // populate keybinds modal
    Object.keys(hotkey_data).forEach(keybind => {
        let keybinds = [keybind];

        if (keybind.includes(',')) {
            keybinds = keybind.split(',');
        }


        let hotkey_desc = hotkey_data[keybind].getAttribute('data-hotkey-desc');

        let kb_e = document.createElement("div");
        kb_e.className = "kb_e";

        let kb_e_h3 = document.createElement("h3");
        kb_e_h3.textContent = hotkey_desc;

        kb_e.appendChild(kb_e_h3);

        keybinds.forEach(element => {
            let kb_e_kbd = document.createElement("kbd");
            kb_e_kbd.textContent = element.toUpperCase().replace("+", " + ");
            kb_e.appendChild(kb_e_kbd);
        });


        document.getElementById("kb_main").append(kb_e);

    });

})

document.addEventListener('keydown', (e) => {
    let press_name = "";
    if (e.shiftKey)(press_name = press_name + "shift+");
    if (e.ctrlKey)(press_name = press_name + "ctrl+");
    if (e.altKey)(press_name = press_name + "alt+");
    press_name = press_name + e.key.toLowerCase();

    if (press_name == "escape") {
        close_keybind_modal();
        window.focus();
        if (document.activeElement) {
            document.activeElement.blur();
        }
    }
    if ((e.target.type == "textarea" || e.target.type == "number" || e.target.type == "text") && !e.ctrlKey) {

    } else {

        var element_to_focus = hotkey_data[press_name];
        if (element_to_focus) {
            element_to_focus.focus();
            if (press_name = "ctrl+s") {
                element_to_focus.click();
            }
            e.preventDefault();
        }

    }
})

function open_keybind_modal() {
    document.getElementById("keybinds_modal").style.display = 'block';
}

function close_keybind_modal() {
    document.getElementById("keybinds_modal").style.display = 'none';
}