function go_back() {
    window.history.back();
};

function set_id_value_to_href(id_to_href, base) {
    const el = document.getElementById(id_to_href);
    window.location.href = base + el.value;
    el.value = ''
}