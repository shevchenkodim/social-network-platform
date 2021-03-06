function bookmarks(el) {
    data_id = $(el).attr('data-id');
    let formData = new FormData();
    csrf_token =  $('input[name="csrf_token"]').attr('value');
    formData.append('csrfmiddlewaretoken', csrf_token);

    postUrl = $(el).attr('data-url');
    $.post({url: postUrl,
            dataType: "json",
            data:formData,
            processData:false,
            contentType: false,
        }).done(function(result) {
                if (result._code == 0 ){
                        $('i#bookmarks_icon_' + data_id).attr('class', result._class_icon);
                    }
                else{
                    }
        });
};


function post_likes(a) {
    var formData = new FormData();
    post_id = $(a).attr('id');
    formData.append('post_id', post_id);

    csrf_token =  $('input[name="csrf_token"]').attr('value');
    formData.append('csrfmiddlewaretoken', csrf_token);
    postUrl = $('#post_likes_url').val();
    $.post({url: postUrl,
            dataType: "json",
            data:formData,
            processData:false,
            contentType: false,
        }).done(function(result) {
                if (result._code == 0 ){
                    $('#heart-likes-' + post_id).attr('class',result._class_likes);
                    $('#count-likes-' + post_id).text(result._likes);
                    }
                else{
                    }
        });
};


function post_likes_modal(a) {
    var formData = new FormData();
    post_id = $(a).attr('id');
    formData.append('post_id', post_id);

    csrf_token =  $('input[name="csrf_token"]').attr('value');
    formData.append('csrfmiddlewaretoken', csrf_token);
    postUrl = $('#post_likes_url').val();
    $.post({url: postUrl,
            dataType: "json",
            data:formData,
            processData:false,
            contentType: false,
        }).done(function(result) {
                if (result._code == 0 ){
                    $('#modal-heart-likes-' + post_id).attr('class',result._class_likes);
                    $('#modal-count-likes-' + post_id).text(result._likes);
                    $('#heart-likes-' + post_id).attr('class',result._class_likes);
                    $('#count-likes-' + post_id).text(result._likes);
                    }
                else{
                    }
        });
};


function open_page_post_detail(a) {
    remove_body_modal_data(a)
    url = $(a).attr('data-url');
    $.get(url, function (data) {
        $('#modal-body-content-post').append(data);
    });
};

function remove_body_modal_data(a) {
    $('#modal-body-content-post').text('');
}


$("div #main-manu").mouseover(function() { $(this).addClass("menu-bg border rounded"); });
$("div #main-manu").mouseout(function() { $(this).removeClass("menu-bg border rounded"); });


$('.input-name-file-post').change(function(e){
    var filenames = '';
    for (var i = 0; i < this.files.length; i++) {
        filenames += this.files[i].name + '; ';
    }
    $(".filename").html('<ul>' + filenames + '</ul>');
    $(".label-name-file-post").text(filenames);
});


$('.close-modal-create-post').on('click', function() {
    $(".label-name-file-post").text('Choose file');
    $(".input-name-file-post").val('');
});


$('.div-progressbar').hide();

$(".input-name-file-post").on("change", function() {
    if ($(".input-name-file-post")[0].files.length > 5) {
        alert("You can select only 5 images");
        $('.label-name-file-post').text('Choose file');
        document.getElementById('input-name-file-post').value = "";
    }
});

$('.create-new-post').on('click', function(){
    $('.div-progressbar').show();
    $('#progress').attr("class", "spinner-border spinner-border-sm")
    var formData = new FormData();

    var files = $('.input-name-file-post')[0].files;
    max_count = 5;
    count = 1;
    for (var i = 0; i < files.length; i++) {
        if (count > max_count) break;
        file = files.item(i);
        formData.append("file", file);
        count += 1;
    }

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
                $('#progress').attr("class", "fi fi-check")
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
                    $('#progress').attr("class", "fi fi-check")
                    $('.div-progressbar').hide();
                    location.reload();
                    }
                else{
                    $('.progress-bar').attr('style', 'width: 0%');
                    $('.progress-bar').text('0%');
                    $('.div-progressbar').hide();
                    $('#progress').attr("class", "fi fi-check")
                    $('.create-new-post').text('Error, please try again!');
                    function say() {
                      $('.create-new-post').text("Create")
                    }
                    setTimeout(say, 3000);
                    }
        });
});


function addComment(a) {
    id = $(a).attr('id');
    user = $(a).attr('data-username');

    var formData = new FormData();
    text = $('#comment_text_' + id).val();
    formData.append('text', text);

    csrf_token =  $('input[name="csrf_token"]').attr('value');
    formData.append('csrfmiddlewaretoken', csrf_token);

    postUrl = $(a).attr('data-url');
    $.post({
            url: postUrl,
            dataType: "json",
            data:formData,
            mimeType: "multipart/form-data",
            processData:false,
            contentType: false,
            statusCode: {
              500: function() {
                  $(a).text('Error');
                  function say() {
                    $(a).text("Post")
                  }
                  setTimeout(say, 3000);
              }
            },
        }).done(function(result) {
                if (result._code == 0 ){
                    $('#comment-div-' + id).append('<span><b>'+ user +'</b> '+ text +'</span><br>');
                    text = $('#comment_text_' + id).val('');
                    }
                else{
                    text = $('#comment_text_' + id).val('');
                    $(a).text('Error');
                    function say() {
                      $(a).text("Post")
                    }
                    setTimeout(say, 3000);
                    }
        });
}


function addCommentPageInfo(a) {
    id = $(a).attr('id');
    user = $(a).attr('data-username');

    var formData = new FormData();
    text = $('.comment-text-' + id).val();
    formData.append('text', text);

    csrf_token =  $('input[name="csrf_token"]').attr('value');
    formData.append('csrfmiddlewaretoken', csrf_token);

    postUrl = $(a).attr('data-url');
    $.post({
            url: postUrl,
            dataType: "json",
            data:formData,
            mimeType: "multipart/form-data",
            processData:false,
            contentType: false,
            statusCode: {
              500: function() {
                  $(a).text('Error');
                  function say() {
                    $(a).text("Post")
                  }
                  setTimeout(say, 3000);
              }
            },
        }).done(function(result) {
                if (result._code == 0 ){
                    $('.comment-div-' + id).append('<span><b>'+ user +'</b> '+ text +'</span><br>');
                    text = $('.comment-text-' + id).val('');
                    }
                else{
                    text = $('.comment-text-' + id).val('');
                    $(a).text('Error');
                    function say() {
                      $(a).text("Post")
                    }
                    setTimeout(say, 3000);
                    }
        });
}
