$(document).ready(function () {
    // subcategory.html
    $('#addSubcategoryFields').on('submit', function(event) {
        event.preventDefault();

        $.ajax({
            url: 'http://127.0.0.1:8000/subcategories/link-create/',
            type: 'POST',
            data: $(this).serialize(),
            success: function(response) {
                if (response.status == 'success') {
                    $('#addFields').modal('hide');
                    $('#general_messages').show()
                    $('#general_messages').addClass('alert alert-success').text('Subcategory and Field Linked Successfully!')
                    setTimeout(() => {
                        $('#general_messages').hide()
                        $('#general_messages').removeClass('alert alert-success').text(``)
                        location.reload();
                    }, 2000);
                    // alert('Fields successfully linked to subcategory.');
                } else {
                    // alert('Error: ' + response.message);
                    $('#general_messages').show()
                    $('#addFieldsModal').modal('hide');
                    $('#general_messages').addClass('alert alert-danger').text(`Some error occured`)
                    setTimeout(() => {
                        $('#general_messages').hide()
                        $('#general_messages').removeClass('alert alert-danger').text(``)
                        location.reload();
                    }, 2000);
                }
            },
            error: function(xhr, status, error) {
                alert('An error occurred: ' + error);
            }
        });
    });

    // fields.html
    $('#addFields').submit(function(e){
        e.preventDefault();
        var field_id = $('#fieldId').val();
        var url = field_id ? 'http://127.0.0.1:8000/field/edit/' : 'http://127.0.0.1:8000/field/add/';
        var form_type = field_id ? 'updated' : 'created';
        $.ajax({
            type: "post",
            url:url,
            data: $(this).serialize(),
            success: function (response) {
                if (response.status == 'success'){
                    // alert('added')
                    $('#general_messages').show()
                    $('#addFieldsModal').modal('hide');
                    $('#general_messages').addClass('alert alert-success').text(`Field ${response.field_name} ${form_type}`)
                    setTimeout(() => {
                        $('#general_messages').hide()
                        $('#general_messages').removeClass('alert alert-success').text(``)
                        location.reload();
                    }, 2000);
                }else{
                    // alert('error')
                    $('#general_messages').show()
                    $('#addFieldsModal').modal('hide');
                    $('#general_messages').addClass('alert alert-danger').text(`Some error occured`)
                    setTimeout(() => {
                        $('#general_messages').hide()
                        $('#general_messages').removeClass('alert alert-danger').text(``)
                        location.reload();
                    }, 2000);
                }
            }
        });
    })

    // dynamic form
    // adds input field in field-options.html
    var fieldCount = 1;

    $('#add-field').click(function() {
        fieldCount++;
        var newField = `
            <div class="form-group" id="option-${fieldCount}">
                <label for="newOptionValue${fieldCount}">Option Value ${fieldCount}:</label>
                <input type="text" class="form-control" id="newOptionValue${fieldCount}" name="new_options[]" required>
                <button type="button" class="btn btn-danger btn-sm remove-field" data-option-id="${fieldCount}">Remove</button>
            </div>
        `;
        $('#dynamic-options').append(newField);
    });

    // Event delegation to handle dynamic removal of fields
    $('#dynamic-options').on('click', '.remove-field', function() {
        var optionId = $(this).data('option-id');
        $('#option-' + optionId).remove();
    });

    $('#addOptionForm').submit(function(event) {
        event.preventDefault();
        var formData = $(this).serialize();

        $.ajax({
            type: 'POST',
            url: $(this).attr('action'),
            data: formData,
            success: function(response) {
                if (response.status === 'success') {
                    location.href = response.location_url;
                    $('#general_messages').show();
                    $('#general_messages').addClass('alert alert-success').text('Options added successfully !');
                    setTimeout(() => {
                        $('#general_messages').hide();
                        $('#general_messages').removeClass('alert alert-success').text('');
                    }, 3000);
                } else {
                    $('#error-message').show();
                    $('#error-message').text(response.message);
                    setTimeout(() => {
                        $('#error-message').hide();
                        $('#error-message').text('');
                    }, 3000);
                    // alert(response.message);
                }
            },
            error: function(error) {
                console.error('An error occurred:', error);
            }
        });
    });

    // update options modal
    $('.update-option-button').click(function() {
        var optionId = $(this).data('option-id');
        var optionValue = $(this).data('option-value');
        var fieldId = $(this).data('field-id');

        $('#updateOptionModal input[name="option_id"]').val(optionId);
        $('#updateOptionModal input[name="option_value"]').val(optionValue);
        $('#updateOptionModal input[name="field_id"]').val(fieldId);
    });

    $('#updateOptionForm').submit(function(event) {
        event.preventDefault();
        var formData = $(this).serialize();

        $.ajax({
            type: 'POST',
            url: $(this).attr('action'),
            data: formData,
            success: function(response) {
                if (response.status == 'success') {
                    $('#updateOptionModal').modal('hide')
                    $('#general_messages').show();
                    $('#general_messages').addClass('alert alert-success').text('Option updated successfully !');
                    setTimeout(() => {
                        $('#general_messages').hide();
                        $('#general_messages').removeClass('alert alert-success').text('');
                        location.reload();
                    }, 3000);
                } else {
                    $('#error-update-message').show()
                    $('#error-update-message').text(response.message);
                    setTimeout(() => {
                        $('#error-update-message').hide();
                        $('#error-update-message').text('');
                    }, 3000);
                    // console.log(response)
                }
            },
            error: function(error) {
                console.error('An error occurred:', error);
            }
        });
    });
});

// update fields
function update_field(button){
    var fieldId = $(button).data('field-id');
    var fieldName = $(button).data('field-name');
    var fieldType = $(button).data('field-type')
    // console.log(fieldId, "name", fieldName)

    $('#addFieldsModalLabel').text('Update Field');
    $('#addFieldForm input[type="submit"]').val('Update Field');

    $('#fieldId').val(fieldId);
    $('#fieldName').val(fieldName);
    $('#fieldType').val(fieldType);

    $('#addFieldsModal').modal('show');
}

function delete_field(button){
    var fieldId = $(button).data('field-id');
    console.log(fieldId)
    var result = confirm('Are you sure you want to delete this field?')
    if (result){
        $.ajax({
            type: "post",
            url: "http://127.0.0.1:8000/field/delete/",
            data: {'fieldId':fieldId},
            success: function (response) {
                if (response.status == 'success'){
                    // alert('added')
                    $('#general_messages').show()
                    $('#general_messages').addClass('alert alert-success').text(`Field has been deleted!`)
                    setTimeout(() => {
                        $('#general_messages').hide()
                        $('#general_messages').removeClass('alert alert-success').text(``)
                        location.reload()
                    }, 2000);
                }else{
                    // alert('error')
                    $('#general_messages').show()
                    $('#general_messages').addClass('alert alert-danger').text(`Some error occured`)
                    setTimeout(() => {
                        $('#general_messages').hide()
                        $('#general_messages').removeClass('alert alert-danger').text(``)
                        location.reload()
                    }, 2000);
                }
            }
        });
    }
}

// for subcategory + field link up
function delete_link(button){
    var linkId = $(button).data('link-id');
    var csrfToken = $('[name=csrfmiddlewaretoken]').val();
    var formData = {'linkId':linkId,'csrfmiddlewaretoken':csrfToken};
    var result = confirm('Are you sure you want to delete this link?')
    if (result){
        $.ajax({
            type: "post",
            url: "http://127.0.0.1:8000/subcategories/link-delete/",
            data: formData,
            success: function (response) {
                if (response.status == 'success'){
                    // alert('added')
                    $('#general_messages').show();
                    $('#general_messages').addClass('alert alert-success').text(`Link has been deleted!`);
                    setTimeout(() => {
                        $('#general_messages').hide();
                        $('#general_messages').removeClass('alert alert-success').text(``);
                        location.reload();
                    }, 2000);
                }else{
                    // alert('error')
                    $('#general_messages').show();
                    $('#general_messages').addClass('alert alert-danger').text(`Some error occured`);
                    setTimeout(() => {
                        $('#general_messages').hide();
                        $('#general_messages').removeClass('alert alert-danger').text(``);
                        location.reload();
                    }, 2000);
                }
            }
        });
    }
}