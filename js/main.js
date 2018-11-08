            $(document)
              .ready(function() {
                
                //rating 
                $(".rating").rating();

                // fix menu when passed
                $('.banner')
                  .visibility({
                    once: false,
                    onBottomPassed: function() {
                      $('.fixed.menu').transition('fade in');
                    },
                    onBottomPassedReverse: function() {
                      $('.fixed.menu').transition('fade out');
                    }
                  })
                ;
          
                // create sidebar and attach to menu open
                $('.ui.sidebar')
                  .sidebar('attach events', '.toc.item')
                ;
          
              })
            ;

