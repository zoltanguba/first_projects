{% block javascript %}



<script>

//Pass the content word's text clicked on to the original word field AND check if the word exists in the database

    $('span').on('click', function(e) {
      e.preventDefault();
      $("input:text").val("");
      var wordtocheck = $(this).text();
	  $('#word-original').text(wordtocheck);
      $.ajax({
        type: 'GET',
        url: 'wordclass/',
        data: {
            'wordtocheck': wordtocheck
        },
        success: function(data){
            if (data.wordexists) {
                 $('button').removeClass();
                 $('#'+data.knownlevel).addClass('button-known-level-'+data.knownlevel);
                 $('#translation-input').val(data.translatedWord1);
                 $('#container').removeClass();
                 $('#container').addClass('container-known');
      }
            else {
                 $('button').removeClass();
                 $('#container').removeClass();
                 $('#container').addClass('container-unknown');
            };
        }
        })
      });

//Pass the translation option text value to the translation input field

    $('.word-translation').on('click', function() {
      var trans = $(this).text();
	  $("input:text").val(trans);
    });



//Ajax POST request to save the data provided to the "Word database" model

    $('button').on('click', function(e){
        e.preventDefault();

        $.ajax({
            type: 'POST',
            url: 'word/',
            data: {
                srcLanguage: $('#word-original-data-value').text(),
                word: $('#word-original').text(),
                destLanguage: 'EN',
                translatedWord: $('#translation-input').val(),
                knownlevel: $(this).attr("value"),
                csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val()
            },
            success: function(){
            }
            // End of AJAX call
        });
        $("span").each(function() {
            var wordtocheck = $(this).text();
            var spantoclassify = $(this)
            $.ajax({
                type: 'GET',
                url: 'wordclass/',
                data: {
                    'wordtocheck': wordtocheck
                },
                success: function(data){
                    if (data.wordexists) {
                         $(spantoclassify).removeClass();
                         $(spantoclassify).addClass("word-known-level-"+data.knownlevel);
              }
                    else {
                         $(spantoclassify).removeClass();
                         $(spantoclassify).addClass("word-known-level-unknown");
                    };
                }
            })
        //This is the end of the loop
        })
    });



//Ajax GET request to return the 'knownlevel' attribute of a word from the content in the database

    $('.get-knownlevel').on('click', function() {

        $("span").each(function() {

            var wordtocheck = $(this).text();
            var spantoclassify = $(this)
            $.ajax({
                type: 'GET',
                url: 'wordclass/',
                data: {
                    'wordtocheck': wordtocheck
                },
                success: function(data){
                    if (data.wordexists) {
                         $(spantoclassify).removeClass();
                         $(spantoclassify).addClass("word-known-level-"+data.knownlevel);
              }
                    else {
                         $(spantoclassify).removeClass();
                         $(spantoclassify).addClass("word-known-level-unknown");
                    };
                }
            })
        //This is the end of the loop
        });
    //This is the end of the onclick event script
    });



  </script>

  {% endblock %}