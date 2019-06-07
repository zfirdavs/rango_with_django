$(document).ready(function () {
    $('#about-btn').click(function (event) {
        var msgstr = $('#msg').html();
        msgstr += 'ooo';
        $('#msg').html(msgstr);
    });
});
