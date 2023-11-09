"use strict"

$(document).ready(function () {
    $(document).on("click", "#btn_done", function (e) {
        e.preventDefault()
        
        let csrfToken = $('[name=csrfmiddlewaretoken]').val()
        let id = $(this).val()

        console.log(id);

        Swal.fire({
            title: 'Are you sure?',
            text: "You won't be able to revert this!",
            icon: 'warning',
            showCancelButton: true,
            confirmButtonColor: '#28a745',
            cancelButtonColor: '#d33',
            confirmButtonText: 'Yes, done it!'
          }).then((result) => {
            if (result.isConfirmed) {
                $.ajax({
                    type: "DELETE",
                    url: `${window.location.href}delete/${id}`,
                    headers: {
                        'X-CSRFToken': csrfToken
                    },
                    dataType: "json",
                    success: function (response) {
                        Swal.fire({
                            title: 'Success!',
                            text: response.message,
                            icon: 'success',
                            showCancelButton: false,
                            allowOutsideClick: false,
                            confirmButtonColor: '#1b717b',
                            cancelButtonColor: '#d33',
                            confirmButtonText: 'OK'
                            }).then((result) => {
                                if (result.isConfirmed) {
                                    window.location.href = window.location.href
                                }
                            })
                    }
                })
            }
        })
    })
})