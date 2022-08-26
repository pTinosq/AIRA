function draw_graph() {
    try {
        document.getElementById("b64plot").remove();
    } catch (error) {}
    document.getElementById("spinner_base").style.display = 'block';
    document.getElementById("response_base").style.display = 'none';
    document.getElementById("reload").disabled = true;
    document.getElementById("toggle_auto_redraw").disabled = true;
    fetch('/api/draw_graph?' + new URLSearchParams({
            d: get_ls_data()
        }))
        .then(function (response) {
            return response.json()

        }).then(function (result) {
            if (result[0] == true) {
                document.getElementById("spinner_base").style.display = 'none';
                var plot = document.createElement("img");
                plot.alt = 'plot';
                plot.src = `data:image/png;base64, ${result[1]}`
                plot.id = "b64plot";
                document.getElementById("line_graph_image").appendChild(plot);
            } else {
                document.getElementById("spinner_base").style.display = 'none';
                document.getElementById("response_base").style.display = 'block';
                document.getElementById("response_title").innerText = `Error: ${result[1]}`;
                document.getElementById("response_body").innerText = result[2];
            }
        }).then(function (result) {
            contents = document.getElementsByClassName("aside_data");

            for (var i = 0; i < contents.length; i++) {
                // Set to undisabled (after loading) - prevents spam
                contents[i].disabled = false;
            }
            
            document.getElementById("reload").disabled = false;
            document.getElementById("toggle_auto_redraw").disabled = false;
        })
}

document.addEventListener("DOMContentLoaded", (e) => {
    draw_graph();

    if (ls_get('toggle_auto_redraw') == null) {
        ls_set('toggle_auto_redraw', true);
    }

    if (ls_get('toggle_auto_redraw') == 'true') {
        document.getElementById("toggle_auto_redraw").innerHTML = 'Turn off auto redraw';
    } else {
        document.getElementById("toggle_auto_redraw").innerHTML = 'Turn on auto redraw';
    }
})

function open_image_in_new_tab() {
    var x = document.getElementById("b64plot");
    if (typeof (x) != 'undefined' && x != null) {
        window.open(x.src);
    }
}

function is_auto_redraw() {
    if (ls_get('toggle_auto_redraw') == 'true') {
        return true;
    } else {
        return false;
    }
}

function toggle_auto_redraw() {
    if (ls_get('toggle_auto_redraw') == 'false') {
        ls_set('toggle_auto_redraw', 'true');
        document.getElementById("toggle_auto_redraw").innerHTML = 'Turn off auto redraw';
        draw_graph();
    } else {
        ls_set('toggle_auto_redraw', 'false');
        document.getElementById("toggle_auto_redraw").innerHTML = 'Turn on auto redraw';
    }

}