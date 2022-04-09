function checkMonth() {
    var a = document.getElementById("select-month");
    if (a.value == 2) {
        console.log(true);
    }
    else console.log(false);
}

function infoOnLoad() {
    var a = document.getElementById("info");
    if (a.innerHTML != "" || a.innerHTML != null) {
        a.setAttribute("style", "margin-top: 10px; margin-bottom: 10px");
        a.setAttribute("class", "info info-content");
        console.log(true);
    }
    else console.log(false);
}

function addElements() {
    var a = document.getElementById("select-day");
    for (i = 0; i < 31; i++) {
        a.setAttribute("value", i);
        a.innerHTML = i;
    }
}