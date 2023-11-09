"use strict"

$(document).ready(function () {
    $("#btn_submit").click(function (e) { 
        e.preventDefault()
        
        let csrfToken = $('[name=csrfmiddlewaretoken]').val()
    
        let formDataArray = $("#form_add_client").serializeArray()
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
                $("#client_nama_validation").append(xhr.responseJSON.errors.nama[0])
                $("#alamat_kode_pos_validation").append(xhr.responseJSON.errors.kode_pos[0])
                $(`<div id='alamat_jalan_validation' class='text-danger mb-3'>${xhr.responseJSON.errors.jalan[0]}</div>`).insertAfter("#id_jalan")
                $(`<div id='alamat_provinsi_validation' class='text-danger mb-3'>${xhr.responseJSON.errors.provinsi[0]}</div>`).insertAfter("#id_provinsi")
                $(`<div id='alamat_kota_kab_validation' class='text-danger mb-3'>${xhr.responseJSON.errors.jalan[0]}</div>`).insertAfter("#id_kota_kab")
                $("#client_email_validation").append(xhr.responseJSON.errors.email[0])
                $("#client_no_wa_validation").append(xhr.responseJSON.errors.no_wa[0])
            }
        })
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
})