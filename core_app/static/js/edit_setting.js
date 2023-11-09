"use strict"

$(document).ready(function () {
    let instanceofChoices = {}

    $(".choices-single").each(function (index, element) {
        // element == this
        const instance = new Choices(this)

        instanceofChoices[element.id] = instance
    })

    flatpickr(".flatpickr-date", {
        enableTime: false,
        dateFormat: "d-m-Y",
    })

    flatpickr(".flatpickr-time", {
        enableTime: true,
        noCalendar: true,
        dateFormat: "H:i",
    })

    $("#id_repeat_notif").click(function () {
        if($(this).prop("checked")) {
            $("#status").prop("checked", true)
        } else {
            $("#status").prop("checked", false)
        }
      })
    
      $("#status").on("change", function (e) {
          if($(this).prop("checked")) {
              $("#id_repeat_notif").prop("checked", true)
          } else {
              $("#id_repeat_notif").prop("checked", false)
          }
    })
    
    let id = $("#clients").val()
        
    const urlReferrer = document.referrer
    let target = "create/"
  
    const url = urlReferrer.replace(target, "")

    $.ajax({
        type: "GET",
        url: `${url}products/${id}`,
        dataType: "json",
        success: function (response) {
            let productChoices = instanceofChoices['products']
            productChoices.removeActiveItems()
            productChoices.clearChoices()
    
            response.forEach(function(product) {
                if(product.id !== "undefined" && product.nama_product !== "undefined") {
                    productChoices.setChoices([
                      {
                        value: product.id, 
                        label: product.nama_product,
                      }
                    ])
                    
                    productChoices.setChoiceByValue(product.id)
                }else {
                    productChoices.removeActiveItems()
                    productChoices.clearChoices()
                }
            })
        }
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

    $(document).on("change", "#clients", function () {
        let id = $(this).val()
        
        const urlReferrer = document.referrer
        let target = "create/"
  
        const url = urlReferrer.replace(target, "")

        $.ajax({
            type: "GET",
            url: `${url}products/${id}`,
            dataType: "json",
            success: function (response) {
                let productChoices = instanceofChoices['products']
                productChoices.removeActiveItems()
                productChoices.clearChoices()
    
                response.forEach(function(product) {
                  if(product.id !== "undefined" && product.nama_product !== "undefined") {
                    productChoices.setChoices([
                      {
                        value: product.id, 
                        label: product.nama_product,
                      }
                    ])                
                  }else {
                    productChoices.removeActiveItems()
                    productChoices.clearChoices()
                  }
                })
            }
        })
    })

    $("#btn_submit").click(function (e) { 
        e.preventDefault()

        let csrfToken = $('[name=csrfmiddlewaretoken]').val()
    
        let formDataArray = $("#form_update_setting").serializeArray()
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
                          allowOutsideClick: false,
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