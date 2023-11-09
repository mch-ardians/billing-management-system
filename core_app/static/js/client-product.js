"use strict"

$(document).ready(function () {
    $(".choices-single").each(function (index, element) {
        // element == this
        new Choices(this)
    });
});