window.addEventListener('DOMContentLoaded', () => {
  const button = document.querySelector('#emoji-button');
  const picker = new EmojiButton();

  picker.on('emoji', emoji => {
    document.querySelector('#chat-message-input').value += emoji;
  });

  button.addEventListener('click', () => {
    picker.togglePicker(button);
  });
});

$('#block-messages').scrollTop($('#block-messages')[0].scrollHeight);

let count_status = true
document.querySelector('#block-messages').addEventListener('scroll', function(){
    if (count_status) {
        if (parseInt(this.scrollTop) < 100) {
            // console.log('Позиция скрола у элемента: '+ this.scrollTop)
            count_status = false
            setTimeout(() => count_status = true, 5000);
            load_chat_messages()
        }
    }

});

function load_chat_messages() {
    page = $('#url_messages_load').attr('data-next');
    page = parseInt(page);
    url = $('#url_messages_load').val();
    $.get(url + '?page=' + page, function (data) {
        if (data === '') {
            console.log('No messages');
        } else {
            $('#block-messages .created-chat').after(data);
            $('#url_messages_load').attr('data-next', page + 1);
        }
    });
};
