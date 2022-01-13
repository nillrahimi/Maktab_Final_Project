$( document ).ready(function() {

    console.log(URL) 
  
    $(".formsearch").on("click", function() {
       
        send_ajax($('#text_search').val())
    });
        function send_ajax(input_data){
            data={
                'csrfmiddlewaretoken':CSRF_TOKEN,
                'search_input':input_data
                };
                console.log(data)
            $.ajax({
                type: 'POST',
                url: URL,
                dataType: 'json',
                data:data,
                success: function(res) {
                    console.log(res);
                    show_branches(res)
                }
            });
        }
        
        function show_branches(data){
            branch_ul_tag= $('#branch_ul')
            food_ul_tag= $('#food_ul')
            branch_ul_tag.empty()
            food_ul_tag.empty()
           
            var branch = data.branches;
            var food = data.foods ;    
           
            if ( branch ){
              
                $.each(branch, function(i, branch){
                    var li = document.createElement("li");

                    var a = document.createElement("a");

                    var link = document.createTextNode(branch.name);
                    a.appendChild(link); 
                    
                    a.href = "{% url 'menu_list' branch.id %}"; 
                    li.append(a)
                    branch_ul_tag.append(li)
                   
                });

            }else{
                branch_ul_tag.append()
            }
            if ( food ){
                $.each(food, function(i, food){
                    var li = document.createElement("li");
                    var span = document.createElement("span");
                    span.append(food.name) 
                    li.append(span)
                    
                    food_ul_tag.append(li)
                   
                });
               
                
            }else{
                food_ul_tag.append()
            }
            
        }
      });