"use strict"

$(document).ready(function () {
    $(document).on("change", "#switch_cron", function () {
        if($(this).prop("checked")) {
            let id = $(this).val()
            let csrfToken = $('[name=csrfmiddlewaretoken]').val()

            let formDataArray = $("#form_switch_cron").serializeArray()
            let formData = {"status": "True"}
        
            $.each(formDataArray, function(index, item) {
                formData[item.name] = item.value
            })
            
            $.ajax({
                type: "PUT",
                url: `${window.location.href}run/${id}`,
                headers: {
                    'X-CSRFToken': csrfToken
                },
                data: JSON.stringify({payload: formData}),
                dataType: "json",
                success: function (response) {
                    const Toast = Swal.mixin({
                        toast: true,
                        position: 'top-end',
                        showConfirmButton: false,
                        timer: 3000,
                        timerProgressBar: true,
                        didOpen: (toast) => {
                          toast.addEventListener('mouseenter', Swal.stopTimer)
                          toast.addEventListener('mouseleave', Swal.resumeTimer)
                        }
                      })
                      
                    Toast.fire({
                        icon: 'success',
                        title: response.message
                    })
                }
            })
        } else {
            let id = $(this).val()
            let csrfToken = $('[name=csrfmiddlewaretoken]').val()

            let formDataArray = $("#form_switch_cron").serializeArray()
            let formData = {"status": "False"}
        
            $.each(formDataArray, function(index, item) {
                formData[item.name] = item.value
            })
            
            $.ajax({
                type: "PUT",
                url: `${window.location.href}run/${id}`,
                headers: {
                    'X-CSRFToken': csrfToken
                },
                data: JSON.stringify({payload: formData}),
                dataType: "json",
                success: function (response) {
                    const Toast = Swal.mixin({
                        toast: true,
                        position: 'top-end',
                        showConfirmButton: false,
                        timer: 3000,
                        timerProgressBar: true,
                        didOpen: (toast) => {
                          toast.addEventListener('mouseenter', Swal.stopTimer)
                          toast.addEventListener('mouseleave', Swal.resumeTimer)
                        }
                      })
                      
                    Toast.fire({
                        icon: 'success',
                        title: response.message
                    })
                }
            })
        }
    })
})