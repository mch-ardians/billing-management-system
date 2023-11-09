"use strict"

$(document).ready(function () {
    $("#upload_button").click(function (e) { 
        e.preventDefault();
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

    flatpickr(".flatpickr-date", {
        enableTime: false,
        dateFormat: "d-m-Y",
    })

    $(".flatpickr-date").attr("disabled", "disabled")

    const currencyFormatter = new Intl.NumberFormat(
        "id-ID", {
            style: "currency",
            currency: "IDR",
            minimumFractionDigits: 0
        }
      )

    $("#tf_total_subtotal").text(currencyFormatter.format(parseInt($("#tf_total_subtotal").text())))

    $("#payment_form").submit(function (e) { 
        e.preventDefault()

        let csrfToken = $('[name=csrfmiddlewaretoken]').val()
        let formData = new FormData(this)
        formData.append("payment_date", $("#id_payment_date").val())

        console.log(formData)

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
                        $("#btn_done").attr("disabled", "disabled")

                        let previousPageUrl = document.referrer
                        let regexPattern = /detail\/\d+/
                    
                        previousPageUrl = previousPageUrl.replace(regexPattern, "")
                        window.location.href = previousPageUrl
                      }
                    }
                )
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