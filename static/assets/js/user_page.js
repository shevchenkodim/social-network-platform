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
