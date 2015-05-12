$(document).ready(function() {
    //  Initialize Backgound Stretcher	   
    $('BODY').bgStretcher({
        images: ['img/001校训政管.jpg', 'img/002实验室.jpg', 'img/003图书馆机电.jpg', 'img/004银杏大道英才.jpg', 'img/005机器人通信.jpg', 'img/006湖畔.jpg', 'img/007自习-微固.jpg'],
        imageWidth: 1980,
        imageHeight: 1080,
        slideDirection: 'N',
        slideShowSpeed: 1000,
        transitionEffect: 'fade',
        sequenceMode: 'normal',
        buttonPrev: '#prev',
        buttonNext: '#next',
        nextSlideDelay: '10000',
        resizeProportionally: true,
        anchoring: 'center center',
        anchoringImg: 'center center'
    });

    var $intro = $('div.intro');
    var $li = $intro.find("li");
    var page = 1;
    var page_count = $li.length;
    var repeat = null;
    var $next = $('#next');
    var $prev = $('#prev');

    $('li.active').fadeIn(1000);

    function showIntro() {
        $next.click();
    }
    repeat = setInterval(showIntro, 10000);

    $next.click(function() {
        if (!$li.is(":animated")) {
            if (page == page_count) {
                page = 1;
                $intro.find('li').eq(page - 1).fadeIn(1000).addClass("active").siblings().removeClass("active").fadeOut(300);
            } else {
                page++;
                $('li.active').removeClass("active").fadeOut(300).next().addClass("active").fadeIn(1000);
            }
        }
        clearInterval(repeat);
        repeat = setInterval(showIntro, 10000);
    });
    $prev.click(function() {
        if (!$li.is(":animated")) {
            if (page == 1) {
                page = page_count;
                $intro.find('li').eq(page - 1).fadeIn(1000).addClass("active").siblings().removeClass("active").fadeOut(300);
            } else {
                page--;
                $('li.active').removeClass("active").fadeOut(300).prev().addClass("active").fadeIn(1000);
            }
        }
        clearInterval(repeat);
        repeat = setInterval(showIntro, 10000);
    });

    var audioElement = document.getElementsByTagName('audio')[0];

    function PlayAudio() {
        audioElement.load;
        audioElement.play();
    }

    function PauseAudio() {
        audioElement.pause();
    }

    PlayAudio();

    var $stop = $("#stop");
    $stop.toggle(function() {
        $(this).css("backgroundPosition", "5px -40px");
        PauseAudio();
    }, function() {
        $(this).css("backgroundPosition", "5px 10px");
        PlayAudio();
    });


});