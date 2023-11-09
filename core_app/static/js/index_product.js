"use strict"
$(document).ready(function () {
    $('#product_table').DataTable({
        processing: true,
        serverSide: true,
        "pageLength": 5,
        "lengthMenu": [
            [5, 10, 20, -1],
            [5, 10, 20, "All"]
        ],
        ajax: {
            url: window.location.href
        },
        columns: [{
                data: 'DT_RowIndex',
                name: 'DT_RowIndex',
                orderable: false,
                searchable: false,
                class: "text-center",
            },
            {
                data: 'product',
                name: 'Nama Produk'
            },
            {
                data: 'type',
                name: 'Type'
            },
            {
                data: 'client',
                name: 'Client'
            },
            {
                data: "action",
                name : "",
                render: function(data, type, row) {
                    if(type === 'display') {
                        return data
                    }
                    return ''
                }
            },
        ],
        drawCallback: function() {
            feather.replace()
        },
    })

    $(document).on("click", ".btn-delete", function (e) {
        e.preventDefault()
        
        let csrfToken = $('[name=csrfmiddlewaretoken]').val()
        let id = $(this).val()
    
        Swal.fire({
            title: 'Are you sure?',
            text: "You won't be able to revert this!",
            icon: 'warning',
            showCancelButton: true,
            confirmButtonColor: '#28a745',
            cancelButtonColor: '#d33',
            confirmButtonText: 'Yes, delete it!'
          }).then((result) => {
            if (result.isConfirmed) {
                $.ajax({
                    type: "DELETE",
                    url: `delete/${id}`,
                    headers: {
                        'X-CSRFToken': csrfToken
                    },
                    dataType: "json",
                    success: function (response) {
                        Swal.fire(
                            'Deleted!',
                            response.message,
                            'success'
                        )
    
                        $("#product_table").DataTable().ajax.reload()
                    }
                })
            }
        })
    })

    $(document).on("click", ".btn-edit", function (e) {
        e.preventDefault()

        let id = $(this).val()
        let url = `update/${id}`
        
        window.location.href = url
    })
})