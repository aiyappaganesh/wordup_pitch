$(document).ready(function(){
    var height = $(window).height() * 0.95;
    $('.section').height(height);
    $('.content').height(height * 6);
});

$(document).ready(function(){
    $('#section-2-carousel').carousel('cycle');
});