(function($) {

    $("#submit-schedule").on('click', function() {
        const days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
        var all_schedules = {};
        var schedule_info = [];
        info = {};
        info.title = $('#schedule-name').val();
        if (!info.title)
        {
        $('#schedule-name').addClass('is-invalid').append("* required")
        return false
        }
        info.description = $('#schedule-desc').val();
        info.time_zone = $('#id_timezone').val();
        schedule_info.push(info);
        all_schedules.info = schedule_info;

        details = []
        for (const day of days) {
            schedule = {};
            schedule.day_name = day;
            schedule.order = $('#' + day + '_order').val();
            schedule.start_hour = $('#id_' + day + '_start_hour').val();
            schedule.start_minute = $('#id_' + day + '_start_minute').val();
            schedule.stop_hour = $('#id_' + day + '_stop_hour').val();
            schedule.stop_minute = $('#id_' + day + '_stop_minute').val();
            details.push(schedule);
        }
        all_schedules.details = details;

        tags = []
        $('#tag-list-group li').each(function() {
            tag = {};
            tag.key_name = $(this).attr('key');
            tag.value = $(this).attr('value')
            tags.push(tag);
        });

        all_schedules.tags = tags

        action = $('#action_type').val();

        var schedules = JSON.stringify(all_schedules)
        console.log(JSON.parse(schedules));

        $.ajax({
            url: action,
            method: 'POST',
            dataType: "json",
            data: schedules,
            beforeSend: function(xhr) {
                // we are fetching csrf_token from base.html
                xhr.setRequestHeader('X-CSRFToken', csrf_token)
            },
            success: function() {
                 $('#schedule-name').removeClass('is-invalid')
                $('#submit-schedule').removeClass('btn-info').addClass('btn-success');
                $('#submit-schedule').html("Saved!")
//.attr("disabled", "disabled");
            }
        })

        return false;
    });

    $("#addtag").on('click', function() {

        var key = $('#inputkey'),
            value = $('#inputvalue');

        if (key.val().length > 0 && value.val().length > 0) {

            $('#tag-list-group')
                .append('<li class="list-group-item list-group-item-light" key="' + key.val() + '" value="' + value.val() + '"><span class="badge badge-info">' + key.val() + '</span>&nbsp;<span class="badge badge-secondary">' + value.val() + '</span><a href="#" class="removeitem pull-right">x</a></li>');

        } else {
            key.addClass('is-invalid');
            value.addClass('is-invalid');
            $('#show-tag-message').text('error');
        }

        return false;

    }); // click


    $('#tag-list-group').on('click', 'a.removeitem', function() {
        $(this).parent().remove();
        return false;
    });


}(jQuery));