$(document).ready(function() {
    $('#addSubCategoryModal').on('hide.bs.modal', function(event) {
        $('#addSubCategoryForm')[0].reset();
    });

    $('#addCategoryModal').on('hide.bs.modal', function(event) {
        $('#addCategoryForm')[0].reset();
        $('#addCategoryModalLabel').text('Add Category');
        $('#categoryId').val('')
        $('#addCategoryForm input[type="submit"]').val('Add Category');
    });

    $('#addCategoryForm').on('submit', function(event) {
        event.preventDefault();

        var categoryId = $('#categoryId').val();
        var url = categoryId ? 'http://127.0.0.1:8000/categories/edit/' : 'http://127.0.0.1:8000/categories/add/';
        var form_type = categoryId ? 'updated' : 'created';

        $.ajax({
            type: 'post',
            url: url,
            data: $('#addCategoryForm').serialize(),
            success: function(response) {
                $('#addCategoryModal').modal('hide');
                $('#general_messages').show()
                if (response.status=='success'){
                    $('#general_messages').addClass('alert alert-success').text(`Category ${form_type} successfully!`)
                    setTimeout(() => {
                        $('#general_messages').removeClass('alert alert-success').text('')
                        $('#general_messages').hide()
                        location.reload()
                    }, 2000);
                }
                else{
                    $('#general_messages').addClass('alert alert-danger').text(response.message)
                    setTimeout(() => {
                        $('#general_messages').removeClass('alert alert-danger').text('')
                        $('#general_messages').hide()
                        location.reload()
                    }, 2000);
                }
            },
            error: function(response) {
                // alert(categoryId ? 'Error updating category' : 'Error adding category');
                $('#addCategoryModal').modal('hide');
                // console.log(response)
                $('#general_messages').show()
                $('#general_messages').addClass('alert alert-danger').text(response.message)
                setTimeout(() => {
                    $('#general_messages').removeClass('alert alert-danger').text('')
                    $('#general_messages').hide()
                }, 2000);
            }
        });
    });

    $('#addSubCategoryModal').on('show.bs.modal', function(event) {
        var button = $(event.relatedTarget);
        var categoryId = button.data('category-id');
        console.log(button.data('category-id'))
        $('#sub_categoryId').val(categoryId);
    });

    $('#addSubCategoryForm').submit(function(event) {
        event.preventDefault();
        var subcategoryId = $('#subcategory_id').val();
        var url = subcategoryId ? 'http://127.0.0.1:8000/subcategories/edit/' : 'http://127.0.0.1:8000/subcategories/add/';
        var form_type = subcategoryId ? 'updated' : 'created';

        $.ajax({
            type: 'POST',
            url: url,
            data: $('#addSubCategoryForm').serialize(),
            success: function(response) {
                $('#addSubCategoryModal').modal('hide');
                $('#general_messages').show()
                if (response.status=='success'){
                    $('#general_messages').addClass('alert alert-success').text('New subcategory added!')
                    setTimeout(() => {
                        $('#general_messages').removeClass('alert alert-success').text('')
                        $('#general_messages').hide()
                        location.reload()
                    }, 2000);
                }
                else{
                    $('#general_messages').addClass('alert alert-danger').text('Error in subcategory addition!')
                    setTimeout(() => {
                        $('#general_messages').removeClass('alert alert-danger').text('')
                        $('#general_messages').hide()
                        location.reload()
                    }, 2000);
                }
            },
            error: function(response) {
                alert('Error in subcategory operation');
            }
        });
    });

});

function update_category(button){
    var categoryId = $(button).data('category-id');
    var categoryName = $(button).data('category-name');
    console.log(categoryId, "name", categoryName)

    $('#addCategoryModalLabel').text('Update Category');
    $('#addCategoryForm input[type="submit"]').val('Update Category');

    $('#categoryId').val(categoryId);
    $('#categoryName').val(categoryName);

    $('#addCategoryModal').modal('show');
}

// function delete_category(button){
//     swal({
//         title: "Are you sure?",
//         text: "You will not be able to recover this imaginary file!",
//         type: "warning",
//         showCancelButton: !0,
//         confirmButtonColor: "#DD6B55",
//         confirmButtonText: "Yes, delete it!",
//         closeOnConfirm: !1
//     }, function() {
//         swal("Deleted!", "Your imaginary file has been deleted.", "success")
//     })
// }

function delete_category(button){
    categoryId = $(button).data('category-id')
    var csrfToken = $('[name=csrfmiddlewaretoken]').val();
    // swal({
    //     title: "Are you sure want to delete?",
    //     text: "",
    //     type: "warning",
    //     showCancelButton: true,
    //     confirmButtonColor: '#1a83bf',
    //     confirmButtonText: 'Yes, delete it!',
    //     closeOnConfirm: false,
    //   }, function(isConfirm) {
    //     if (!isConfirm) return;
    //     $.ajax({
    //         type: "post",
    //         url: "http://127.0.0.1:8000/categories/delete/",
    //         data: {'id': categoryId,'csrfmiddlewaretoken': csrfToken},
    //         success: function (response) {
    //             if (response.status === 'success') {
    //                 alert('Category deleted successfully');
    //                 location.reload()
    //             } else {
    //                 alert('Error: ' + response.message);
    //             }
    //         },
    //         error: function(xhr, status, error) {
    //             alert('An error occurred: ' + error);
    //         }
    //     });
    //   });
    var result = confirm('Are you sure you want to Delete this Category Completely?')
    if (result){
        $.ajax({
            type: "post",
            url: "http://127.0.0.1:8000/categories/delete/",
            data: {'id': categoryId,'csrfmiddlewaretoken': csrfToken},
            success: function (response) {
                if (response.status === 'success') {
                    $('#general_messages').show()
                    $('#general_messages').addClass('alert alert-success').text('Category deleted successfully!')
                    setTimeout(() => {
                        $('#general_messages').removeClass('alert alert-success').text('')
                        $('#general_messages').hide()
                        location.reload()
                    }, 2000);
                } else {
                    alert('Error: ' + response.message);
                }
            },
            error: function(xhr, status, error) {
                alert('An error occurred: ' + error);
            }
        });
    }
}