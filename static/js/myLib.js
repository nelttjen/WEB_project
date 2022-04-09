function showPassword() {
    var a = document.getElementById('inputPassword1');
    var b = document.getElementById('inputPassword2');
    setType(a);
    setType(b);
}

function setType(elem) {
    if (elem.type == "password") elem.type = 'text';
    else elem.type = 'password';
}