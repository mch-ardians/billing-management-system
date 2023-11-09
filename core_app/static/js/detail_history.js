"use strict"

$(document).ready(function () {
    $("#id_nama_client").attr("disabled", "disabled")
    $("#id_email").attr("disabled", "disabled")
    $("#id_date").attr("disabled", "disabled")
    $("#id_sub_total").attr("disabled", "disabled")
    $("#id_payment_date").attr("disabled", "disabled")
    $("#id_nama_client").attr("disabled", "disabled")
    $("#file").attr("disabled", "disabled")
    $("#btn_done").attr("disabled", "disabled")

    const currencyFormatter = new Intl.NumberFormat(
        "id-ID", {
            style: "currency",
            currency: "IDR",
            minimumFractionDigits: 0
        }
      )

    $("#tf_total_subtotal").text(currencyFormatter.format(parseInt($("#tf_total_subtotal").text())))
})