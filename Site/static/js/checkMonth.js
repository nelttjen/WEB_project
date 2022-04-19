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
