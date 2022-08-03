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