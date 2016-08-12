App.updateTaskTable = function() {
    $.ajax({
        url: '/tasks',
        method: 'get',
        dataType: 'json'
    }).done(function(resp) {
        var tableBody = $('#taskTable tbody');
        tableBody.html('');

        $.each(resp, function(idx, task) {
            $('<tr>')
                .append('<td>' + task.id + '</td>')
                .append('<td>' + task.create_time + '</td>')
                .append('<td>' + task.status + '</td>')
                .append('<td>' + (task.finish_time || '&mdash;') + '</td>')
                .appendTo(tableBody);
        });
    });
};

$(function() {
    App.updateTaskTable();

    $('#createTask').click(function() {
        $.ajax({
            url: '/tasks',
            method: 'post',
            dataType: 'json'
        }).done(App.updateTaskTable);
    });

    $('#resetTasks').click(function() {
        $.ajax({
            url: '/reset',
            method: 'post',
            dataType: 'json'
        }).done(App.updateTaskTable);
    });

    setInterval(App.updateTaskTable, 1000);
});
