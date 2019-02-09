function deleteScheduleEntry(entry) {
    if (confirm("Are you sure?")) {
        var $entry = $(entry)
        $entry.parentsUntil('.each-box').remove(); // Delete from front-end
        var id = $entry.data('id')
        $.ajax({
            url: 'delete/' + id,
            method: 'DELETE',
            beforeSend: function(xhr) {
                xhr.setRequestHeader('X-CSRFToken', csrf_token)
            }
        })
    }

}