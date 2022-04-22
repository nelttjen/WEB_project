$("#change-password").click(function () { 
    $(".password-inputs").toggle(500);
});

$("#show-select").click(function () { 
    $(".birth-select ").toggle(500);
});

function validate_profile() {
    var change_pass = $('#change-password').prop("checked");

    var pass1 = $('#new-pass');
    var pass2 = $('#new-pass2');
    if (change_pass) return checkPassword(pass1, pass2);
    return true;
}

function checkPassword(passw1, passw2) {
    var min_c = 8;
    var max_c = 30;
    var pass1 = passw1.val();
    var pass2 = passw2.val();
    if (!pass1 || !pass2) {
        alert("Введите и повторите пароль");
        return false;
    } else if (pass1.length < min_c || pass1.length > max_c){
        alert("Пароль должен быть не короче 8 и не длиннее 30 символов");
        return false;
    } else if (!testPassword(passw1)) {
        return false;
    } else if (pass1 !== pass2) {
        alert("Пароли не совпадают");
        return false;
    }
    return true;
    
    function testPassword(pass) {
        var passw = pass.val();
        var r = /[^A-Z-a-z-0-9*_~$#&-]/g; 
        if(r.test(passw)){
            alert("В пароле введены недопустимые символы. Разрешены латинские буквы и цифры и (*_~$#&-)");
            pass.focus();
            return false;
        }
        var re = /[0-9]/;
        if(!re.test(passw)) {
            alert("Пароль должен содержать хотя бы 1 число (0-9)!");
            pass.focus();
            return false;
        }
        var re = /[a-z]/;
        if(!re.test(passw)) {
            alert("Пароль должен содержать хотя бы 1 строчкную латинскую букву (a-z)!");
            pass.focus();
            return false;
        }
        var re = /[A-Z]/;
        if(!re.test(passw)) {
            alert("Пароль должен содержать хотя бы 1 заглавную латинскую букву (A-Z)!");
            pass.focus();
            return false;
        }
        return true;
    }
}