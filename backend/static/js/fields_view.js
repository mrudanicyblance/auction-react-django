$(document).ready(function () {
    $('#addFields').submit(function(e){
        e.preventDefault();
        var field_id = $('#fieldId').val();
        var url = field_id ? 'http://127.0.0.1:8000/edit_field/' : 'http://127.0.0.1:8000/add_field/';
        var form_type = field_id ? 'updated' : 'created';
        $.ajax({
            type: "post",
            url:url,
            data: $(this).serialize(),
            success: function (response) {
                if (response.status == 'success'){
                    // alert('added')
                    $('#general_messages').show()
                    $('#general_messages').addClass('alert alert-success').text(`Field ${response.field_name} ${form_type}`)
                    setTimeout(() => {
                        $('#general_messages').hide()
                        $('#general_messages').removeClass('alert alert-success').text(``)
                    }, 3000);
                }else{
                    // alert('error')
                    $('#general_messages').show()
                    $('#general_messages').addClass('alert alert-danger').text(`Some error occured`)
                    setTimeout(() => {
                        $('#general_messages').hide()
                        $('#general_messages').removeClass('alert alert-danger').text(``)
                    }, 3000);
                }
            }
        });
    })
});

function update_field(button){
    var fieldId = $(button).data('field-id');
    var fieldName = $(button).data('field-name');
    var fieldType = $(button).data('field-type')
    // console.log(fieldId, "name", fieldName)

    $('#addFieldsModalLabel').text('Update Field');
    $('#addFieldForm input[type="submit"]').val('Update Field');

    $('#fieldId').val(fieldId);
    $('#fieldName').val(fieldName);

    $('#addFieldsModal').modal('show');
}