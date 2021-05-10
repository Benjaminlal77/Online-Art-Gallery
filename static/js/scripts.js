window.onload=function(){
    var videos = document.getElementsByTagName('video')

    videos.forEach(video => {
        video.addEventListener('loadstart', function(event){
            video.addclass('loading');
        });
        video.addEventListener('canplay', function(event){
            video.removeClass('loading');
            video.attr('poster', '')
        });
    });
};