"use strict"

$(document).ready(function () {
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
                let regexPattern = /update\/\d+/
        
                previousPageUrl = previousPageUrl.replace(regexPattern, "")
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

    $("#btn_update").click(function (e) { 
        e.preventDefault();

        let csrfToken = $('[name=csrfmiddlewaretoken]').val()
    
        let formDataArray = $("#form_update_client").serializeArray()
        let formData = {}
    
        $.each(formDataArray, function(index, item) {
            formData[item.name] = item.value
        })

        Swal.fire({
          title: 'Are you sure?',
          text: 'You will change your data. Are you sure to update?',
          icon: 'question',
          showCancelButton: true,
          allowOutsideClick: false,
          confirmButtonColor: '#28a745',
          cancelButtonColor: '#d33',
          confirmButtonText: 'Update'
        }).then((result) => {
          if (result.isConfirmed) {
              $.ajax({
                  type: "PUT",
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
                      confirmButtonColor: '#1b717b',
                      cancelButtonColor: '#d33',
                      confirmButtonText: 'OK'
                    }).then((result) => {
                        if (result.isConfirmed) {
                          let previousPageUrl = document.referrer
                          let regexPattern = /update\/\d+/
                  
                          previousPageUrl = previousPageUrl.replace(regexPattern, "")
                          window.location.href = previousPageUrl
                        }
                    })
                  }
              })
            }
        })
    })
})