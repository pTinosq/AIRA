function draw_graph() {
    fetch('/api/draw_graph?' + new URLSearchParams({
            d: get_ls_data()
        }))
        .then(function (response) {
            return response.json()

        }).then(function (result) {
            if (result[0] == true) {
                var plot = document.createElement("img");
                plot.alt = 'plot';
                plot.src = `data:image/png;base64, ${result[1]}`
                document.getElementById("line_graph_image").innerHTML = "";
                document.getElementById("line_graph_image").appendChild(plot);
            } else {
                alert("error", result[1]);
            }
        });
}

document.addEventListener("DOMContentLoaded", (e) => {
    draw_graph();
})

function open_image_in_new_tab() {
    if(document.getElementById("line_graph_image").children.length > 0){
               
        window.open(document.getElementById("line_graph_image").children[0].src);
    }
}