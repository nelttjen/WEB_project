$.event.special.inputchange = {
    setup: function() {
        var self = this, val;
        $.data(this, 'timer', window.setInterval(function() {
            val = self.value;
            if ($.data(self, 'cache') != val) {
                $.data(self, 'cache', val);
                $(self).trigger('inputchange');
            }
        }, 20));
    },
    teardown: function() {
        window.clearInterval($.data(this, 'timer'));
    },
    add: function() {
        $.data(this, 'cache', this.value);
    }
};

from_slider = $('#from');
to_slider = $('#to');
from_input = $('#from-input');
to_input = $('#to-input');
all = $('.track-value');
sum = $('#sum')

from_slider.on("inputchange", function () {
    let _this = Number(from_slider.val());
    if (0 <= _this && _this <= 20000) {
        from_input.val(_this);
    }

});

to_slider.on("inputchange", function () {
    let _this = Number(to_slider.val());
    if (0 <= _this && _this <= 20000) {
        to_input.val(_this);
    }
});

from_input.on("inputchange", function() {
    let _this = Number(from_input.val());
    if (0 <= _this && _this <= 20000) {
        from_slider.val(_this);
    } else {
        if (_this < 0) {
            from_slider.val(0);
            from_input.val(0);
        } else if (_this > 20000) {
            from_slider.val(20000);
            from_input.val(20000);
        }
    }
})

to_input.on("inputchange", function() {
    let _this = Number(to_input.val());
    if (0 <= _this && _this <= 20000) {
        to_slider.val(_this);
    } else {
        if (_this < 0) {
            to_slider.val(0);
            to_input.val(0);
        } else if (_this > 20000) {
            to_slider.val(20000);
            to_input.val(20000);
        }
    }
})

function calculate_steps(from, to, per_step) {
    let _steps = to - from;
    if (from > to) return 0;
    var _sum = 0;
    while (_steps > 0) {
        _steps -= 25;
        _sum += per_step;
    }
    return _sum;
}

function calculate(rank1, rank2) {
    var _sum = 250;
    _sum += calculate_steps(Math.max(0, rank1), Math.min(1200, rank2), 5);
    _sum += calculate_steps(Math.max(1200, rank1), Math.min(2800, rank2), 15);
    _sum += calculate_steps(Math.max(2800, rank1), Math.min(4800, rank2), 20);
    _sum += calculate_steps(Math.max(4800, rank1),  Math.min(7200, rank2), 30);
    _sum += calculate_steps(Math.max(7200, rank1),  Math.min(10000, rank2), 40);
    _sum += calculate_steps(Math.max(10000, rank1),  Math.min(20000, rank2), 65);
    return _sum;
}

all.on('inputchange', function () {
    let rank1 = Number(from_input.val());
    let rank2 = Number(to_input.val());
    if (rank1 >= rank2) {
        sum.text(0);
    } else {
        let text = calculate(rank1, rank2);
        sum.text(String(text));
    }
})

$(document).ready(sum.text(calculate(5000, 10000)))

