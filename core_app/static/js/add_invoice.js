"use strict"

$(document).ready(function () {
  let invoice_id = null

  if(window.location.pathname == "/invoice/daftar-invoice/create/") {
    let shouldWarn = true

    $(document).on("click", "#btn_print", function (e) {
      shouldWarn = false
      e.preventDefault()

      const urlReferrer = document.referrer
      let target = "create/"

      const url = urlReferrer.replace(target, "")

      $.ajax({
        type: "GET",
        url: `${url}print/${invoice_id}`,
        dataType: "json",
        success: function (response) {
        }
      })

      window.open(`${url}print/${invoice_id}`, '_blank')
      shouldWarn = true
    })

    $("#btn_cancel").click(function (e) { 
      shouldWarn = false
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
            shouldWarn = true
          }
        })
    })

    $(document).on("click", "#btn_send", function (e) {
      shouldWarn = false
      e.preventDefault()

      let previousPageUrl = document.referrer
      let target = "create/"

      previousPageUrl = previousPageUrl.replace(target, "")
      window.open(`${previousPageUrl}send/${invoice_id}`, '_blank') 
      shouldWarn = true
    })

    window.addEventListener("beforeunload", function(e) {
      if (!shouldWarn) return

      e.preventDefault()

      const message = 'Data yang Anda masukkan tidak akan disimpan!'

      e.returnValue = message

      return message
    })
  }
  
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

    $(document).on("change", "#clients", function () {
      let id = $(this).val()
      
      const urlReferrer = document.referrer
      let target = "create/"

      const url = urlReferrer.replace(target, "")

      if(id) {
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
      }
    })

    $("#btn_submit").click(function (e) { 
      e.preventDefault()
      
      let csrfToken = $('[name=csrfmiddlewaretoken]').val()
    
      let formDataArray = $("#form_add_invoice").serializeArray()
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
          invoice_id = response.invoice_id
          
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
                  $("#no_invoice").attr("disabled", "disabled")
                  instanceofChoices["clients"].disable()
                  $(".flatpickr-date").attr("disabled", "disabled") 
                  $("#btn_submit").attr("disabled", "disabled")
                  $("#btn_cancel").after(`<button class="btn btn-main" id="btn_send">Next</button>`)
                  $(`<button class="btn btn-success" id="btn_print">Preview Invoice</button><button class="btn btn-warning" id="btn_edit">Edit</button>`).appendTo("#next_step_btns")
              }
          })          
        },
        error: function (xhr, status, error) {
          $("#no_invoice_validation").text(xhr.responseJSON.errors.no_invoice[0])
          $("#invoice_client_validation").text(xhr.responseJSON.errors.client[0])
          $("#invoice_date_validation").text(xhr.responseJSON.errors.invoice_date[0])
          $("#invoice_due_date_validation").text(xhr.responseJSON.errors.due_date[0])
        }
      })
    })

    $("#btn_submit_product").click(function (e) { 
      e.preventDefault()

      let id = invoice_id
      
      const urlReferrer = document.referrer
      let target = "create/"

      const url = urlReferrer.replace(target, "")

      let csrfToken = $('[name=csrfmiddlewaretoken]').val()
    
      let formDataArray = $("#form_add_product").serializeArray()
      let formData = {}
  
      $.each(formDataArray, function(index, item) {
          formData[item.name] = item.value
      })

      $.ajax({
        type: "POST",
        url: `${url}products/create/${id}`,
        headers: {
          'X-CSRFToken': csrfToken
        }, 
        data: JSON.stringify({payload: formData}),
        dataType: "json",
        success: function (response) {
          console.log(response)
          $("#product_table tbody").html(response.html)
          $("#tf_total_qty").text(response.total_qty?? 0)

          const currencyFormatter = new Intl.NumberFormat(
            "id-ID", {
                style: "currency",
                currency: "IDR",
                minimumFractionDigits: 0
            }
          )

          $("#tf_total_subtotal").text(currencyFormatter.format(response.total_subtotal))

          feather.replace()
        },
        error: function (xhr, status, error) {            
          Swal.fire({
            icon: 'error',
            title: 'Oops...',
            text: 'Submit your invoice first please!',
            allowOutsideClick: false,
          })
        }
      })
    })

    $(document).on("click", "#btn_delete_product", function (e) {
      e.preventDefault()

      const row = $(this).closest("tr")
      let csrfToken = $('[name=csrfmiddlewaretoken]').val()
      let id = $(this).val()

      const urlReferrer = document.referrer
      let target = "create/"

      const url = urlReferrer.replace(target, "")

      $.ajax({
        type: "DELETE",
        headers: {
          'X-CSRFToken': csrfToken
        },
        url: `${url}products/delete/${id}`,
        dataType: "json",
        success: function (response) {
          row.remove()

          let totalQuantity = 0
          let totalSubtotal = 0
      
          $("#product_table tbody#product_body_table tr").each(function() {
              let quantity = parseInt($(this).find("td:nth-child(5)").text(), 10)
              let subtotal = parseFloat($(this).find("td:nth-child(6)").text())
      
              totalQuantity += (isNaN(quantity) ? 0 : quantity)
              totalSubtotal += (isNaN(subtotal) ? 0 : subtotal)
          })

          const currencyFormatter = new Intl.NumberFormat(
            "id-ID", {
                style: "currency",
                currency: "IDR",
                minimumFractionDigits: 0
            }
          )
      
          $("#tf_total_qty").text(totalQuantity)
          $("#tf_total_subtotal").text(currencyFormatter.format(totalSubtotal))
        }
      })
    })

    $(document).on("click", "#btn_edit", function (e) {
      e.preventDefault()

      $("#no_invoice").removeAttr("disabled")
      $(".flatpickr-date").removeAttr("disabled")
      $(this).remove()
      $("<button class='btn btn-warning' id='btn_update'>Update</button>").appendTo("#next_step_btns")
    })

    $(document).on("click", "#btn_update", function (e) {
      e.preventDefault()

      let csrfToken = $('[name=csrfmiddlewaretoken]').val()
    
      let formDataArray = $("#form_add_invoice").serializeArray()
      let formData = {}
  
      $.each(formDataArray, function(index, item) {
          formData[item.name] = item.value
          formData["client"] = instanceofChoices["clients"].getValue(true)
      })

      const urlReferrer = document.referrer
      let target = "create/"

      const url = urlReferrer.replace(target, "")

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
            url: `${url}update/${invoice_id}`,
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
                      $("#no_invoice").attr("disabled", "disabled")
                      instanceofChoices["clients"].disable()
                      $(".flatpickr-date").attr("disabled", "disabled") 
                      $("#btn_update").remove()
                      $("<button class='btn btn-warning' id='btn_edit'>Edit</button>").appendTo("#next_step_btns")
                    }
                })
            }
        })
      }
    })
  })
})