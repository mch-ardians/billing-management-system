"use strict"

$(document).ready(function () {
    $(".choices-single").each(function (index, element) {
        // element == this
        new Choices(this)
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
            allowOutsideClick: false,
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
            }
        })
    })

    $("#btn_submit").click(function (e) { 
        e.preventDefault()
        
        let csrfToken = $('[name=csrfmiddlewaretoken]').val()
    
        let formDataArray = $("#form_add_product").serializeArray()
        let formData = {}
    
        $.each(formDataArray, function(index, item) {
            formData[item.name] = item.value
        })
    
        $.ajax({
            type: "POST",
            url: window.location.href,
            headers: {
                'X-CSRFToken': csrfToken
            },
            data: JSON.stringify({payload: formData}),
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
            error: function (xhr) {            
                $("#product_nama_validation").append(xhr.responseJSON.errors.nama_product[0])
                $("#product_type_validation").append(xhr.responseJSON.errors.type[0])
                $("#product_client_validation").append(xhr.responseJSON.errors.client[0])
            }
        })
    })
})