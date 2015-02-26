$(window).on("orientationchange", function(event) {
    window.location.reload(false);
});

$(document).ready(function(){
    setHeights();
});

function setHeights() {
    var height = $(window).height() * 0.99;
    var normal_section_height = Math.max($('.normal-section').height(), height);
    $('.normal-section').height(normal_section_height);
    var medium_short_section_height = Math.max($('.medium-short-section').height(), height);
    $('.medium-short-section').height(medium_short_section_height);
    var medium_long_section_height = Math.max($('.medium-long-section').height(), height);
    $('.medium-long-section').height(medium_long_section_height);
    var long_section_height = Math.max($('.long-section').height(), height);
    $('.long-section').height(long_section_height);
    centerAlign();
}

function centerAlign() {
    $('.section').each(function(){
        var content_overlay = $($(this).find('.content-overlay')[0]).height();
        var section_content = $($(this).find('.section-content')[0]).height();
        var section_content_margin = (content_overlay/2) - (section_content/2);
        $($(this).find('.section-content')[0]).css('margin-top', section_content_margin);
    });
}