// I'm well aware of the issues surrounding localstorage, however, none of them apply to this use case.
// No sensitive data is stored, string data is sufficient, the impact on performance is minimal, size of data is tiny
// So don't cry about it. xx

function ls_get(key) {
    return localStorage.getItem(key);
}

function ls_set(key, value) {
    try {
        localStorage.setItem(key, value);
        return true;
    } catch (error) {
        return error
    }
}

function get_ls_data() {
    return btoa(JSON.stringify(localStorage));
}

function q(e) {
    // Adds localstorage to page parameters for flask to decipher
    // Again, I understand it's not best practice but it'll do.
    e.children[0].value = get_ls_data();

    // Save BAG if on BAG page.
    // Check if on homepage

    if (window.location.pathname == "/" || window.location.pathname == '/home') {
        save_bag();
    }
}