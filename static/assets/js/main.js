$("div #main-manu").mouseover(function() { $(this).addClass("menu-bg border rounded"); });
$("div #main-manu").mouseout(function() { $(this).removeClass("menu-bg border rounded"); });


$('.input-name-file-post').change(function(e){
    var fileName = e.target.files[0].name;
    $(".label-name-file-post").text(fileName);
});


$('.close-modal-create-post').on('click', function() {
    $(".label-name-file-post").text('Choose file');
    $(".input-name-file-post").val('');
});


$('.div-progressbar').hide();


$('.create-new-post').on('click', function(){
    $('.div-progressbar').show();

    var formData = new FormData();
    formData.append('file', $('.input-name-file-post')[0].files[0]);

    text = $('#text-create-post').val();
    formData.append('text', text);

    csrf_token =  $('input[name="csrf_token"]').attr('value');
    formData.append('csrfmiddlewaretoken', csrf_token);

    postUrl = $('#create_new_post').val();
    $.post({ xhr: function()
              {
                var xhr = new window.XMLHttpRequest();
                xhr.upload.addEventListener("progress", function(evt){
                  if (evt.lengthComputable) {
                    var percentComplete = evt.loaded / evt.total * 100;
                    percentComplete = parseInt(percentComplete)
                    progress_css = 'width: ' + percentComplete + '%'
                    $('.progress-bar').attr("style", progress_css);
                    $('.progress-bar').text(percentComplete + '%');
                  }
                }, false);
                return xhr;
             },
            url: postUrl,
            dataType: "json",
            data:formData,
            mimeType: "multipart/form-data",
            processData:false,
            contentType: false,
            statusCode: {
              500: function() {
                alert('500 status code! server error');
                $('.progress-bar').attr('style', 'width: 0%');
                $('.progress-bar').text('0%');
                $('.div-progressbar').hide();
                $('.create-new-post').text('Error, please try again!');
                function say() {
                  $('.create-new-post').text("Create")
                }
                setTimeout(say, 3000);
              }
            },
        }).done(function(result) {
                if (result._code == 0 ){
                    $('.progress-bar').attr('style', 'width: 0%');
                    $('.progress-bar').text('0%');
                    $('.div-progressbar').hide();
                    location.reload();
                    }
                else{
                    $('.progress-bar').attr('style', 'width: 0%');
                    $('.progress-bar').text('0%');
                    $('.div-progressbar').hide();
                    $('.create-new-post').text('Error, please try again!');
                    function say() {
                      $('.create-new-post').text("Create")
                    }
                    setTimeout(say, 3000);
                    }
        });
});
