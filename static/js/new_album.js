window.onload=function(){
    var album_title_input = document.getElementById('album-title-input');

    album_title_input.addEventListener('input',function(event){
        album_title_input.value = album_title_input.value.replace(/\s+/g, '_');
        album_title_input.value = album_title_input.value.replace(/\d+/g, '')
    });
};