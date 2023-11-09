"use strict"

$(document).ready(function () {
    let instanceofChoices = {}

    $(".choices-single").each(function (index, element) {
        // element == this
        const instance = new Choices(this)

        instanceofChoices[element.id] = instance
    })

    $("#email").attr("readonly", "readonly")
    $("#no_wa").attr("readonly", "readonly")

    $("#btn_previous").click(function (e) { 
        e.preventDefault()
        
        window.close()
    })

    $("#btn_cancel").click(function (e) { 
        e.preventDefault()
        
        const swalWithBootstrapButtons = Swal.mixin({
            customClass: {
              confirmButton: 'btn btn-danger',
              cancelButton: 'btn btn-success',
            },
            buttonsStyling: true
          })
          
        swalWithBootstrapButtons.fire({
            title: 'Warning !',
            text: "You will lose your data. Are you sure to exit?",
            icon: 'error',
            showCancelButton: true,
            confirmButtonText: 'Exit',
            confirmButtonColor: '#dc3545',
            cancelButtonText: 'No',
            cancelButtonColor: '#28a745',
            reverseButtons: true
          }).then((result) => {
            if (result.isConfirmed) {
                let previousPageUrl = document.referrer
                let target = "create/"
        
                previousPageUrl = previousPageUrl.replace(target, "")
                
                window.location.href = previousPageUrl
            } else if (
              /* Read more about handling dismissals below */
              result.dismiss === Swal.DismissReason.cancel
            ) {
              swalWithBootstrapButtons.fire(
                'Cancelled',
                'Your data is safe :)',
                'error'
              )
              shouldWarn = true
            }
          })
    })

    $("#send_form").submit(function (e) { 
        e.preventDefault()
        
        let csrfToken = $('[name=csrfmiddlewaretoken]').val()
        let formData = new FormData(this)

        Swal.fire({
            title: 'Sending Email...',
            text: 'Please wait...',
            icon: 'info',
            showConfirmButton: false,
            allowOutsideClick: false, 
            onBeforeOpen: () => {
                Swal.showLoading()
            }
        })

        $.ajax({
            type: "POST",
            url: window.location.href,
            headers: {
                'X-CSRFToken': csrfToken
            },
            data: formData,
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
                        let previousPageUrl = document.referrer
                        let target = "create/"
                
                        previousPageUrl = previousPageUrl.replace(target, "")
                        
                        window.location.href = previousPageUrl
                    }
                })
            },
            error: function(jqXHR, textStatus, errorThrown) {
                console.error("AJAX Error:", textStatus, errorThrown)
            },
            cache: false,
            contentType: false,
            processData: false
        })
    })
})