$(document).ready(function () {
    rank1 = $('#from-input');
    rank2 = $('#to-input');
    log = $('#order_1');
    pas = $('#order_2'); 
});

$('.coupon-image').click(function() {$('#code').val($('span#promocode').text());});
$('.coupon-button').click(function() {$('#code').val($('span#promocode').text());});

function order_validate() {
    let _val1 = rank1.val();
    let _val2 = rank2.val();
    let _val_log = log.val();
    let _val_pas = pas.val();
    console.log(_val2);
    console.log({1: _val1, 2: _val2, 3: _val_log, 4: _val_pas});
    if (!/^[0-9]+$/.test(_val1) || !/^[0-9]+$/.test(_val2)) {
        alert('Введите корректный ранг');
        return false;
    }
    if (!_val1 || !_val2 || !_val_log || !_val_pas) {
        alert('Заполните данные заказа');
        return false;
    }
    if (Number(_val1) > Number(_val2)) {
        alert('Текущий ранг не может быть больше желаемого');
        return false;
    }
    return true;
}

