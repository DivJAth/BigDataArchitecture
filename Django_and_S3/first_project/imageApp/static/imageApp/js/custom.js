

  /*-------------------------------------------------------------------------------
    PRE LOADER
  -------------------------------------------------------------------------------*/

  $(window).load(function(){
    $('.preloader').fadeOut(1000); // set duration in brackets
  });


  /*-------------------------------------------------------------------------------
    jQuery Parallax
  -------------------------------------------------------------------------------*/

    function initParallax() {
    $('#home').parallax("50%", 0.3);

  }
  initParallax();


  /* Back top
  -----------------------------------------------*/

  $(window).scroll(function() {
        if ($(this).scrollTop() > 200) {
        $('.go-top').fadeIn(200);
        } else {
          $('.go-top').fadeOut(200);
        }
        });
        // Animate the scroll to top
      $('.go-top').click(function(event) {
        event.preventDefault();
      $('html, body').animate({scrollTop: 0}, 300);
      })

  /* Upload Image
  -----------------------------------------------*/

  $('.file-input').change(function(){
      var curElement = $(this).parent().parent().parent().find('.image');
      console.log(curElement);
      var reader = new FileReader();

      reader.onload = function (e) {
          // get loaded data and render thumbnail.
          curElement.attr('src', e.target.result);
      };

      // read the image file as a data URL.
      reader.readAsDataURL(this.files[0]);

      let req = new XMLHttpRequest();
      let formData = new FormData();

      formData.append("upload", this.files[0]);                                
      req.open("POST", '/pretty/tagUploadedImage/');
      req.send(formData);
  });

$("#viewSimilar").click(function (e) {
  e.preventDefault();
  $.ajax({
      type: "GET",
      url: '/imageSearch/searchResults',
      data: {
        'imageToSearch': ""
      },
      success: function (data) {
         for (imageName in data['resultImageNames']) {
            //var result = "<li>" + '<img src= "https://s3-us-west-1.amazonaws.com/flickrbigdatacu/'+data['resultImageNames'][imageName]+'">' + "</li>";
            var result = '<div class="col-md-6 col-sm-6">' + '<div class="gallery-thumb">'+ '<a class="image-popup">'+'<img src= "https://s3-us-west-1.amazonaws.com/flickrbigdatacu/'+data['resultImageNames'][imageName]+'"'+' alt="Gallery Image">'+'</a>'+'</div>'+'</div>';
            $("#resultImages").append(result); 
          }
      }
    });

  });
