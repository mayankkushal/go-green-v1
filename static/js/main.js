function executePushNotification() {
    $.ajax({
        url: '/bills/check_notified',
        type: "GET",
        success: function(data) {
            if (data.store) {
                var redirect = function() {
                    window.location.href = data.url;
                };
                var options = {
                    title: "GoGreen | " + data.store,
                    options: {
                        body: "Payment successfull. Thank you for shopping.",
                        icon: "icon.png",
                        lang: 'en-US',
                        onClick: redirect
                    }
                };
                $("#easyNotify").easyNotify(options);
            }
        }
    });
    setTimeout(executePushNotification, 10000);
}

function timer(time, update, complete) {
    var start = new Date().getTime();
    var interval = setInterval(function() {
        var now = time - (new Date().getTime() - start);
        if (now <= 0) {
            clearInterval(interval);
            complete();
        } else update(Math.floor(now / 1000));
    }, 100); // the smaller this number, the more accurate the timer will be
}

setTimeout(executePushNotification, 10000); //push notification

function readURL(input) { //displays the preview of the picture to be uploaded
    if (input.files && input.files[0]) {
        var reader = new FileReader();

        reader.onload = function(e) {
            $('#picture').attr('src', e.target.result);
        }

        reader.readAsDataURL(input.files[0]);
    }
}

$(".image-preview").change(function() {
    readURL(this);
});

$('#resend').click(function() {
    $.get('/resend_otp')
});

function b_total() {
    var sale = 0.0
    var tax = 0.0
    $('.total').each(function() {
        var all = $(this).attr('id').split("-");
        var no = all[1];
        var base = all[0];
        var taxId = "#" + base + "-" + no + "-tax";
        var deleteId = "#" + base + "-" + no + "-DELETE";

        if (!$(deleteId).is(":checked")) {
            tax += parseFloat($(this).val()) * (parseFloat($(taxId).val()) / 100);
            sale += parseFloat($(this).val());
        }
    });
    var tot = tax + sale;
    return {
        'sale': sale,
        'tax': tax,
        'tot': tot,
    }
}

function b_fill(sale, tot, tax) {

    $('#sale_amount').html(sale);
    $('#tax_amount').html(tax);
    $('#total_amount').html(tot);
}

$(function() {
    $('.field-franchise').addClass('hidden');
    $('.field-store').addClass('hidden');
    $('.field-store_chain').addClass('hidden');

    if ($("#id_type_of_product").val() == 'F') {
        $('.field-store').addClass('hidden');
        $('.field-store_chain').removeClass('hidden');
    } else if ($("#id_type_of_product").val() == 'S') {
        $('.field-store').removeClass('hidden');
        $('.field-store_chain').addClass('hidden');
    }

    $('#id_stand_alone').change(function() {
        if ($(this).is(':checked')) {
            $('.field-franchise').addClass('hidden');
            $('.field-category').removeClass('hidden');
        } else {
            $('.field-franchise').removeClass('hidden');
            $('.field-category').addClass('hidden');
        }
    });

    $("#id_type_of_product").change(function() {
        if ($(this).val() == 'F') {
            $('.field-store').addClass('hidden');
            $('.field-store_chain').removeClass('hidden');
        } else {
            $('.field-store').removeClass('hidden');
            $('.field-store_chain').addClass('hidden');
        }
    });

    $('#id_password1').pwstrength({
        ui: {
            showVerdictsInsideProgressBar: true,
        }
    });
    $('#main-carousel').owlCarousel({
        loop: true,
        margin: 10,
        //nav:true, 
        items: 1,
        dotsEach: false,
        autoplay: true,
        autoplayTimeout: 7000,
        singleItem: true,
    });

    $('#insta-carousel').owlCarousel({
        loop: true,
        margin: 10,
        //nav:true, 
        items: 1,
        dotsEach: false,
        autoplay: true,
        autoplayTimeout: 7000,
        singleItem: true,
    });

    $('#id_phone_no').change(function() {
        $('.username').val($('#id_phone_no').val());
    })

    if (window.location.search) {
        $('#clear-filter').show();
    }

    $('#clear-filter').click(function(e) {
        e.preventDefault();
        window.location = window.location.href.split("?")[0];
    });

    $('#newsletterBtn').click(function(e) {
        e.preventDefault();
        $.ajax({
            type: "POST",
            url: '/newsletter',
            data: {
                email: $("#newsletter_email").val(),
                csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val(),
            },
            success: function(data) {
                if (data.status) {
                    $(".modal-body").html("<h5 style='color:green;'>" + data.msg + "</h5>");
                    $(".modal-footer").html("");
                } else {
                    $(".modal-footer").html("<p style='color:red'>* " + data.msg + "</p>");
                }
            },
        });
    });

    $('#billingForm').submit(function(e, submit) {
        if (!submit) e.preventDefault();
        $('#billingModal').modal('show');
        $('#payment').html($('#total_amount').text());
    });

    $('#returnForm').submit(function(e, submit) {
        if (!submit) e.preventDefault();
        cal = b_total();
        $('#billingModal').modal('show');
        $('#return-amount').html($('#id_total').val() - cal.tot);
    });

    $('#proceedBtn').click(function() { // Submits the form again as it was prevented earlier
        $('#billingForm').trigger('submit', [true]);
        $('#returnForm').trigger('submit', [true]);
    });
});

//blog comment 
$(document).on('submit', '#comment-form', function(e) {
    e.preventDefault();
    $.ajax({
        type: "POST",
        url: commentURL,
        data: {
            comment: $("#id_comment").val(),
            pid: $("#pid").val(),
            csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val(),
        },
        success: function(data) {
            $('#id_comment').val('');
            $("#show_comm").append('<li><strong>' + data.user + "</strong> says: " + data.comment + '</li>');
            $("#no-comm").hide();
            $('.comm-count').html(data.comm_count);
        },
    });
});

$(".like").click(function() {
    if ($('.like').hasClass('btn-info')) {
        $('.like').removeClass('btn-info');
        $('.like').addClass('btn-danger');
    } else {
        $('.like').removeClass('btn-danger');
        $('.like').addClass('btn-info');
    }
    var pid = $(this).attr('data-pid');
    $.ajax({
        type: 'get',
        url: likeURL,
        data: {
            'pid': pid,
            csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val(),
        },
        success: function(data) {
            $('#count').html(data.count);
        }
    });
});

//check article like
var pid = $('.like').attr('data-pid');
$.get(checkURL, {
    'pid': pid
}, function(data) {
    if (data) {
        $('.like').removeClass('btn-info');
        $('.like').addClass('btn-danger');
    }
});

function productDetail(value, id, obj) {
    var all = id.split("-");
    var no = all[1];
    var base = all[0];
    var product_pk = value
    if (product_pk) {
        $.ajax({
            type: 'get',
            url: '/pos/product_detail',
            data: {
                'product_pk': product_pk,
            },
            success: function(data) {
                var skuId = "#" + base + "-" + no + "-sku";
                var priceId = "#" + base + "-" + no + "-price";
                var selectSku = "#select2-" + base + "-" + no + "-sku_number-container";
                var selectProduct = "#select2-" + base + "-" + no + "-product_number-container";
                var product_val = "#" + base + "-" + no + "-product_pk";
                var taxId = "#" + base + "-" + no + "-tax";
                var qtyId = "#" + base + "-" + no + "-quantity";
                var totalId = "#" + base + "-" + no + "-total";

                $(skuId).val(data.sku);
                $(priceId).val(data.price);
                $(taxId).val(data.tax);
                $(product_val).val(data.num);
                
                $obj = $(obj);
                $sku = $obj.closest('tr').children('td:eq(1)');
                $sku.find('#select2-id_items-0-sku_number-container').text(data.sku)

                $prd = $obj.closest('tr').children('td:eq(0)');
                $prd.find('#select2-id_items-0-product_number-container').text(data.name);
                
                if ($(qtyId).val() > 0) {
                    $(totalId).val($(priceId).val() * $(qtyId).val());
                } else {
                    $(qtyId).val(1);
                    $(totalId).val($(priceId).val() * $(qtyId).val());
                }
                cal = b_total();
                b_fill(cal.sale, cal.tot, cal.tax);
            },
            error: function(xhr, status, error) {
                var err = eval("(" + xhr.responseText + ")");
                console.log(err.Message);
            }
        });
    }
}

function calculateTotal(x, value) {
    id = x.id;
    var all = id.split("-");
    var no = all[1];
    var base = all[0];
    var priceId = "#" + base + "-" + no + "-price";
    var totalId = "#" + base + "-" + no + "-total";
    total = $(priceId).val() * value;
    $(totalId).val(total);
    cal = b_total();
    b_fill(cal.sale, cal.tot, cal.tax);

}