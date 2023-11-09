"use strict"

$(document).ready(function () {
    $(document).on("click", "#upload_button", function (e) {
        e.preventDefault()
        $("#file").click()
    })

    $("#file").change(function (e) { 
        if (this.value) {
            $("#custom-msg").html(
                this.value.match(/[\/\\]([\w\d\s\.\-\(\)]+)$/)[1]
            )
            
        }else {
            $("#custom-msg").html("No file chosen, yet.")
        }
    })

    $("#btn_edit").click(function (e) { 
        e.preventDefault()
        
        $("#btn_edit").remove();
        $(`<span id='custom-msg' class='d-flex align-items-center'>No file chosen, yet.</span>
           <button type='button' class='rounded rounded-3 btn btn-main' id='upload_button'>Change</button>
           <button class='btn btn-outline-danger' id='btn_profile_delete'>Remove</button>`)
        .appendTo('#trigger_container')
        $(`<button class='btn btn-outline-success' id='btn_cancel'>Cancel</button>
           <button class='btn btn-main' id='btn_submit'>Save Changes</button>`)
        .appendTo("#btn_actions")
        $("#file").removeAttr("required")
        $("#username, #full_name, #position, #email, #no_telp").removeAttr("disabled")
    })

    $(document).on("click", "#btn_cancel", function (e) {
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
                window.location.href = window.location.href
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

    $("#form_profile").submit(function (e) { 
        e.preventDefault()

        let csrfToken = $('[name=csrfmiddlewaretoken]').val()
        let formData = new FormData(this)

        formData.append('_method', 'PUT')

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
                        window.location.href = window.location.href
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

    $(document).on("click", "#btn_profile_delete", function (e) {
        e.preventDefault()

        let csrfToken = $('[name=csrfmiddlewaretoken]').val()

        Swal.fire({
            title: 'Are you sure?',
            text: 'You will remove your profile. Are you sure to remove?',
            icon: 'question',
            showCancelButton: true,
            allowOutsideClick: false,
            confirmButtonColor: '#28a745',
            cancelButtonColor: '#d33',
            confirmButtonText: 'Remove'
          }).then((result) => {
            if (result.isConfirmed) {
                $.ajax({
                    type: "DELETE",
                    url: window.location.href,
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