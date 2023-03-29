function COMMS_HANDLER(init_time) {

    this.time = init_time;
    this.queue = [];

    setInterval(function () { this.time += 1; }, 1000);
    setInterval(function () {
        list = this.queue.splice(0, this.queue.length);
        list.forEach(function (m, i) {
            alert(m);
        });
    }, 6000);

    function buildMessage(url, data = {}, callback = null) {
        return;
    }

    function sendMessage(url, data = {}, callback = null) {
        return;
    }

    function queueMessage(url, data = {}, callback = null) {
        return;
    }

    this.ping = function () {
        buildMessage('/api/ping');
    };

    this.reception = {};
    this.reception.entry = function (data, callback = null) {
        buildMessage('/reception/entry', data, callback);
    };

    return this;
}