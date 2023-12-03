
$(document).ready(function () {
    $("#toggleInfoButton").click(function () {
        $("#infoTable").toggle();
    });
    $("#toggleMainButton").click(function () {
        $("#mainTable").toggle();
    });
    $("#toggleAdLab2").click(function () {
        $("#adLab2").toggle();
    });
    $("#toggleLab3").click(function () {
        $("#lab3").toggle();
    });
    $('#search_keyword').on('input', function(){
        keyword = new URLSearchParams(window.location.search).get("search_keyword")
        console.log(keyword)
        $('<input />').attr('type', 'hidden')
            .attr('name', "keyword")
            .attr('value', keyword)
            .appendTo('#commentForm');
    });

    return true;
});