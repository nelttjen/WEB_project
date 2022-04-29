function calculate(rank1, rank2) {
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

    var _sum = 250;
    _sum += calculate_steps(Math.max(0, rank1), Math.min(1200, rank2), 5);
    _sum += calculate_steps(Math.max(1200, rank1), Math.min(2800, rank2), 15);
    _sum += calculate_steps(Math.max(2800, rank1), Math.min(4800, rank2), 20);
    _sum += calculate_steps(Math.max(4800, rank1),  Math.min(7200, rank2), 25);
    _sum += calculate_steps(Math.max(7200, rank1),  Math.min(10000, rank2), 40);
    _sum += calculate_steps(Math.max(10000, rank1),  Math.min(20000, rank2), 65);
    return _sum;
}