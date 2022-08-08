function get_vbo() {
    document.getElementById("reload").disabled = true;
    fetch('/api/fetch_verbose_output?' + new URLSearchParams({
            d: get_ls_data()
        }))
        .then(function (response) {
            return response.json()

        }).then(function (result) {
            if (result[0] == true) {
                document.getElementById("VBO_text").value = result[1];
            } else {
                output = `==========${result[1]}==========\n${result[2]}`;
                document.getElementById("VBO_text").value = output;
            }
            document.getElementById("reload").disabled = false;
        });
}

document.addEventListener("DOMContentLoaded", (e) => {
    get_vbo();
});

function regenerate_VBO() {
    get_vbo();
}
