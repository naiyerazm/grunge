var BaseUrl = 'http://89.116.21.141:8000/'

$(document).ready(function () {

    $('button').click(function () {
        var module_type = $(this).attr('id').split('-')[2];
        var module_list = ['client','supplier','expense','item','inventory']
        if(module_list.indexOf(module_type) !== -1){        
        $.ajax({
            type: 'POST',
            url: BaseUrl + 'master/'+module_type+'/',
            data: $('#frm-new-'+module_type).serialize(),
            dataType: "json",
            beforeSend: function () {
                $('.error').text();
            },
            success: function (response) {
                if (response.status_code == 400) {
                    $.each(response.errorList, function (index, val) {
                        $('#error-' + index).text(val);
                    });
                    alert(response.msg);
                }
                else if (response.status_code == 500) {
                    alert(response.msg);
                }
                else {
                    if(module_type == 'inventory'){module_type = 'item';}
                    window.location = BaseUrl + 'master/'+module_type+'/list'
                }

            }
        });
    }
        return false;
    });

    $('#btn-login').click(function () {
        $.ajax({
            type: 'POST',
            url: BaseUrl + 'account/login/',
            data: $('#frm-login').serialize(),
            dataType: "json",
            beforeSend: function () {
                $('.error').text();
            },
            success: function (response) {
                if (response.status_code == 400) {
                    $.each(response.errorList, function (index, val) {
                        $('#error-' + index).text(val);
                    });
                    alert(response.msg);
                }
                else {
                    window.location = BaseUrl + 'master/client/list'
                }
                if (response.status_code == 500) {
                    alert(response.msg);
                }
            }
        });
        return false;
    });

    $('#btn-create-invoice').click(function () {
        $.ajax({
            type: 'POST',
            url: BaseUrl + 'sale/invoice/create/',
            data: $('#frm-create-invoice').serialize(),
            dataType: "json",
            beforeSend: function () {
                $('.error').text();
            },
            success: function (response) {
                if (response.status_code == 400) {
                    $.each(response.errorList, function (index, val) {
                        $('#error-' + index).text(val);
                    });
                    alert(response.msg);
                }
                else {
                    window.location = BaseUrl + 'sale/invoice/print/'+response.id
                }
                if (response.status_code == 500) {
                    alert(response.msg);
                }
            }
        });
        return false;
    });


    $('#btn-create-foc-invoice').click(function () {
        $.ajax({
            type: 'POST',
            url: BaseUrl + 'sale/foc/invoice/create/',
            data: $('#frm-create-foc-invoice').serialize(),
            dataType: "json",
            beforeSend: function () {
                $('.error').text();
            },
            success: function (response) {
                if (response.status_code == 400) {
                    $.each(response.errorList, function (index, val) {
                        $('#error-' + index).text(val);
                    });
                    alert(response.msg);
                }
                else {
                    window.location = BaseUrl + 'foc/invoice/print/'+response.id
                }
                if (response.status_code == 500) {
                    alert(response.msg);
                }
            }
        });
        return false;
    });


    $('#btn-client-receipt').click(function () {
        $.ajax({
            type: 'POST',
            url: BaseUrl + 'sale/client/receipt',
            data: $('#frm-client-receipt').serialize(),
            dataType: "json",
            beforeSend: function () {
                $('.error').text();
            },
            success: function (response) {
                if (response.status_code == 400) {
                    $.each(response.errorList, function (index, val) {
                        $('#error-' + index).text(val);
                    });
                    alert(response.msg);
                }
                else {
                    window.location = BaseUrl + 'sale/client/statement/'+response.id
                }
                if (response.status_code == 500) {
                    alert(response.msg);
                }
            }
        });
        return false;
    });

});



function action_module(id,module_type,method_name,post_type) {
    if (!confirm('Are you sure to perform the action?')) {
        return false;
    }
    $.ajax({
        type: post_type,
        url: BaseUrl + 'master/'+module_type+'/'+method_name+'/id/' + id,
        dataType: "json",
        success: function (response) {
            if (response.status_code == 400) {
                alert(response.msg);
            }
            else if (response.status_code == 500) {
                alert(response.msg);
            }
            else {
                if(module_type == 'inventory'){module_type = 'item';}
                window.location = BaseUrl + 'master/'+module_type+'/list'
            }

        }
    });
}

function update_cart(counter){
    var id = $('#item'+counter).val();
    $.ajax({
        type: 'get',
        url: BaseUrl + 'sale/item/inventory/' + id,
        dataType: "json",
        success: function (response) {
            if (response.status_code == 400) {
                alert(response.msg);
            }
            else if (response.status_code == 500) {
                alert(response.msg);
            }
            else {
                var qty = $('#item_qty'+counter).val();
                var item_price = $('#item_price'+counter).val();
                var item_sub_total = $('#item_sub_total'+counter).val();
                var item_vat = $('#item_vat'+counter).val();
                var item_total = $('#item_total'+counter).val();

                item_price = response.sale_price;
                item_sub_total = item_price * qty;
                item_vat = item_sub_total * response.vat/100;
                item_total = item_sub_total + item_vat;
                $('#item_price'+counter).val(item_price);
                $('#item_sub_total'+counter).val(item_sub_total);
                $('#item_vat'+counter).val(item_vat);
                $('#item_total'+counter).val(item_total);

        }
    }
    });
}

function update_client_detail(id){
    $.ajax({
        type: 'get',
        url: BaseUrl + 'master/client/detail/' + id,
        dataType: "html",
        success: function (response) {
            $('#client-detail').html(response);
        }
    });
}

function get_client_invoice(id){
    $.ajax({
        type: 'get',
        url: BaseUrl + 'sale/client/invoice/list/' + id,
        dataType: "html",
        success: function (response) {
            $('#invoice-list').html(response);
        }
    });

}