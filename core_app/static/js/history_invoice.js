"use strict"

$(document).ready(function () {
    $('#history_table').DataTable({
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
                data: 'nama',
                name: 'Nama'
            },
            {
                data: 'product',
                name: 'Product'
            },
            {
                data: 'no_invoice',
                name: 'No. Invoice'
            },
            {
                data: 'invoice_date',
                name: 'Invoice Date',
                render: function(data, type, row) {
                    let dateFormatter = new Date(data)
                    return `${dateFormatter.toLocaleDateString('id-ID', {dateStyle: "long"})}`
                }
            },
            {
                data: 'status',
                name: 'Status'
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
    
    $(document).on("click", "#btn_detail", function (e) {
        e.preventDefault()
        window.location.href = `${window.location.href}detail/${$(this).val()}`
    })
})