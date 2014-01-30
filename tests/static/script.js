$(document).ready(function ($) {
    "use strict";

    var $checkbox = $(":checkbox");

    if ( $.cookie("pjax") !== undefined )
        $checkbox.prop("checked", $.cookie("pjax", Number));

    if ( !$checkbox.prop("checked") )
        $.fn.pjax = $.noop;

    $checkbox.on("change", function() {
        if ( $.pjax == $.noop ) {
            $(this).prop("checked", false);
            return alert( "Sorry, your browser doesn't support pjax :(" )
        }
        if ( $(this).prop("checked") )
            $.cookie("pjax", 1);
        else
            $.cookie("pjax", 0);
        window.location = location.href;
    });

    $(document).pjax("a", "#pjax-container", {timeout: 10000});

    $(document).on("pjax:beforeSend", function(e) {
        if( !$(":checkbox").prop("checked") ){
            return false;
        }
    });

    $(document).on("pjax:send", function(e) {
        $("#loading").removeClass("hidden")
    });

    $(document).on("pjax:complete", function() {
        $("#loading").addClass("hidden")
    });

    $("[data-toggle='tooltip']").tooltip();

});
