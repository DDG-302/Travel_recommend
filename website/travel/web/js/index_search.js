// JavaScript source code
function search_click() {
    search_txt = $("#search_box").val()
    if (search_txt != "") {
        window.location.href = "pages/search.html?keyword=" + search_txt + "&type=0"
    }
}