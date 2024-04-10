var btn = document.getElementById("open-btn")
var icon = document.getElementById('chatIcon')

$(document).ready(function(){

  $('#menu').click(function(){

      $(this).toggleClass('fa-times');
      $('.navbar').toggleClass('nav-toggle');

  });

  $(window).on('load scroll',function(){
    typeWriter();
    $('#menu').removeClass('fa-times');
    $('.navbar').removeClass('nav-toggle');

    if($(window).scrollTop() > 0){
      $('#scroll-top').show();
    }else{
      $('#scroll-top').hide();
    }

  });

  $('a[href*="#"]').on('click',function(e){

    e.preventDefault();

    $('html, body').animate({

      scrollTop : $($(this).attr('href')).offset().top,

    },
      500,
      'linear'
    );

  });

});

document.getElementById('chatIcon').addEventListener('click', function() {
  document.getElementById('sidebar').style.right = '0';
  icon.classList.add("display")
});

document.getElementById('closeBtn').addEventListener('click', function() {
  document.getElementById('sidebar').style.right = '-300px';
  icon.classList.remo("display")
});
