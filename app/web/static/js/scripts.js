function go_back() {
    window.history.back();
};

function clear_elem(elem_id) {
    var div = document.getElementById(elem_id);
    while (div.firstChild) {
        div.removeChild(div.firstChild);
    }
};