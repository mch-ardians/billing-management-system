"use strict"

$(document).ready(function () {
    setInterval(() => {
        let target = new Date()

        let months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"];
        let day = target.getDate();
        let month = months[target.getMonth()];
        let year = target.getFullYear();

        let formattedTarget = `${month} ${day}, ${year}`

        $(".flatpickr-day").each(function () {
            // console.log($(this).attr("aria-label"));
            if($(this).attr("aria-label") == formattedTarget) {
                $(this).attr("class", "flatpickr-day selected");
            }else {
                $(this).removeClass("selected");
            }
        })

    }, 0);
});