function showPassword() {
    var a = document.getElementById('pass1');
    var b = document.getElementById('pass2');
    setType(a);
    setType(b);
}

function setType(elem) {
    if (elem.type == "password") elem.type = 'text';
    else elem.type = 'password';
}