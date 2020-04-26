function update_user_avatar(a) {
    var formData = new FormData();
    formData.append('file', $('.input-name-file-avatar')[0].files[0]);
    csrf_token =  $('input[name="csrf_token"]').attr('value');
    formData.append('csrfmiddlewaretoken', csrf_token);
    postUrl = $('#update_user_avatar_url').val();
    $.post({url: postUrl,
            dataType: "json",
            data:formData,
            processData:false,
            contentType: false,
        }).done(function(result) {
                if (result._code == 0 ){
                    location.reload();
                    }
                else{
                    $(a).text('Error');
                    function replace_t() {
                      $(a).text("Update")
                    }
                    setTimeout(replace_t, 3000);
                    }
        });
};


function upload_img(input) {
    if (input.files && input.files[0]) {
        var reader = new FileReader();
        reader.onload = function (e) {
            $('.image-preview').empty();;
            $('.image-preview').append('<img src="'+ e.target.result +'" style="max-height: 150px;">')
        }
        reader.readAsDataURL(input.files[0]);
    }
}

function clear_modal_upload_avatar() {
    $('.image-preview').empty();
    $('.label-name-file-avatar').text('Choose file');
}

$('.input-name-file-avatar').change(function(e){
    var filenames = '';
    for (var i = 0; i < this.files.length; i++) {
        filenames += this.files[i].name;
    }
    $(".filename").html('<ul>' + filenames + '</ul>');
    $(".label-name-file-avatar").text(filenames);
});
