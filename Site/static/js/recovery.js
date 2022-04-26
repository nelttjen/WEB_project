function recovery_validate(){
    pass1 = document.getElementById('password1');
    pass2 = document.getElementById('password2');
    if (pass1 && pass2) {
        return checkPassword(pass1, pass2);
    }
    return false;
}

function checkPassword(passw1, passw2) {
    var min_c = 8;
    var max_c = 30;
    try {
        var pass1 = passw1.value;
        var pass2 = passw2.value;
    } catch (error) {
        alert('Что-то пошло не так. Перезагрузите страницу.');
        return false;
    }
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
        var passw = pass.value;
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