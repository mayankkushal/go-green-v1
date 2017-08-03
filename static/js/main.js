function executePushNotification() {
  $.ajax({
    url: '/bills/check_notified',
    type:"GET",
    success: function(data) {
    	if(data.store){
	      	   var redirect = function() {
	  			window.location.href = data.url;
				};
		      	var options = {
		        title: "GoGreen | "+data.store,
		        options: {
		          body: "Payment successfull. Thank you for shopping.",
		          icon: "icon.png",
		          lang: 'en-US',
		          onClick: redirect
		        }
	    	};
      	$("#easyNotify").easyNotify(options); 
     }
    }
  });
  setTimeout(executePushNotification, 10000); 
}

function timer(time,update,complete) {
    var start = new Date().getTime();
    var interval = setInterval(function() {
        var now = time-(new Date().getTime()-start);
        if( now <= 0) {
            clearInterval(interval);
            complete();
        }
        else update(Math.floor(now/1000));
    },100); // the smaller this number, the more accurate the timer will be
}

	setTimeout(executePushNotification, 10000);//push notification

	function readURL(input) {		//displays the preview of the picture to be uploaded
        if (input.files && input.files[0]) {
            var reader = new FileReader();
            
            reader.onload = function (e) {
                $('#picture').attr('src', e.target.result);
            }
            
            reader.readAsDataURL(input.files[0]);
        }
    }
    
    $(".image-preview").change(function(){
        readURL(this);
    });

    $('#resend').click(function(){
      $.get('/resend_otp')
    });

 $(function(){

    $('#id_password1').pwstrength({
        ui: { showVerdictsInsideProgressBar: true, }
    });
    $('#main-carousel').owlCarousel({
    loop:true,
    margin:10,
    //nav:true, 
    items : 1, 
    dotsEach: false,
    autoplay:true,
    autoplayTimeout:7000,
    singleItem: true,
  });

    $('#insta-carousel').owlCarousel({
    loop:true,
    margin:10,
    //nav:true, 
    items : 1, 
    dotsEach: false,
    autoplay:true,
    autoplayTimeout:7000,
    singleItem: true,
  });

  $('#id_phone_no').change(function(){
    $('.username').val($('#id_phone_no').val());
  })
  
  if(window.location.search){
    $('#clear-filter').show();
  }
 
  $('#clear-filter').click(function(e){
    e.preventDefault();
    window.location = window.location.href.split("?")[0];
  });

  $('#newsletterBtn').click(function(e){
    e.preventDefault();
        $.ajax({
      type:"POST",
      url: '/newsletter',
      data:{
      email:$("#newsletter_email").val(),
      csrfmiddlewaretoken:$('input[name=csrfmiddlewaretoken]').val(),
      },
      success:function(data){
          if(data.status){
            $(".modal-body").html("<h5 style='color:green;'>"+data.msg+"</h5>");
            $(".modal-footer").html("");
          }
          else{
            $(".modal-footer").html("<p style='color:red'>* "+data.msg+"</p>");
          }
      },
    });
  });

});
//blog comment 
$(document).on('submit', '#comment-form', function(e){
    e.preventDefault();
    $.ajax({
      type:"POST",
      url: commentURL,
      data:{
      comment:$("#id_comment").val(),
      pid:$("#pid").val(),
      csrfmiddlewaretoken:$('input[name=csrfmiddlewaretoken]').val(),
      },
      success:function(data){
          $('#id_comment').val('');
          $("#show_comm").append('<li><strong>' + data.user + "</strong> says: " + data.comment + '</li>');
          $("#no-comm").hide();
          $('.comm-count').html(data.comm_count);
      },
    });
  });
 $(".like").click(function(){
      if($('.like').hasClass('btn-info')){
        $('.like').removeClass('btn-info');
        $('.like').addClass('btn-danger');
      }
      else{
        $('.like').removeClass('btn-danger');
        $('.like').addClass('btn-info');
      }
      var pid = $(this).attr('data-pid');
    $.ajax({
      type:'get',
      url: likeURL,
      data:{
        'pid':pid,
        csrfmiddlewaretoken:$('input[name=csrfmiddlewaretoken]').val(),
      },
      success:function(data){
        $('#count').html(data.count);
        }
    });
  });
    //check article like
    var pid = $('.like').attr('data-pid');
    $.get(checkURL, {'pid':pid}, function(data){
      if(data){
        $('.like').removeClass('btn-info');
        $('.like').addClass('btn-danger');
      }
    });


