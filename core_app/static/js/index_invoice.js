"use strict"

$(document).ready(function () {
    $('#invoice_table').DataTable({
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
                data: 'invoice_date',
                name: 'Invoice Date',
                render: function(data, type, row) {
                    let dateFormatter = new Date(data)
                    return `${dateFormatter.toLocaleDateString('id-ID', {dateStyle: "long"})}`
                }
            },
            {
                data: 'no_invoice',
                name: 'No. Invoice'
            },
            {
                data: 'total',
                name: 'Total',
                render: function(data) {
                    const currencyFormatter = new Intl.NumberFormat(
                        "id-ID", {
                            style: "currency",
                            currency: "IDR",
                            minimumFractionDigits: 0
                        }
                    )

                    return currencyFormatter.format(data)
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
    
    $(document).on("click", "#btn_detail", function () {
        let id = $(this).val()

        window.location.href = `${window.location.href}detail/${id}`
    })
})