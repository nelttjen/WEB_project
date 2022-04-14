function selectMonth() {
    var month = document.getElementById("select-month");
    var day = document.getElementById("select-day");

    m_num = Number(month.value);
    if (m_num == 2) {
        setProps(true, true);
        setDay(29);
    } else if ([4, 6, 9, 11].includes(m_num)) {
        setProps(false, true);
        setDay(30);
    } else {
        setProps(false, false);
    }

                             
    function setDay(max) {
        if (Number(day.value) > max) day.value = "0";
    }

    function setProps(p1, p2) {
        $("#select30").prop("hidden", p1);
        $("#select31").prop("hidden", p2);
    }
}

function validate() {
    var login = $("#login");
    var pass1 = $("#pass1");
    var pass2 = $("#pass2");
    var day = $("#select-day");
    var month = $("#select-month");
    var year = $("#select-year");
    var accept = $("#rule-accepted");
    if (!login.val()) {
        alert("Введите логин");
        return false;
    } else if (login.val() === pass1.val()){
        alert("Пароль не может совпадать с логином");
        return false;
    } else if (!testLogin(login.val())) {
        return false;
    } else if (!checkPassword(pass1, pass2)) {
        return false;
    } else if (day.val() === "0" || month.val() === "0" || year.val() === "0") {
        alert("Выберите дату рождения");
        return false;
    } else if (!accept.prop('checked')) {
        alert("Вы должны быть согласны с правилами сервиса");
        return false;
    }
    return true;
}

function testLogin(login) {
    var r = /[^A-Z-a-z-0-9_]/g; 
    if (r.test(login)) {
        alert("В логине введены недопустимые символы. Разрешены латинские буквы, цифры и символ подчеркивания");
        return false;
    }
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

