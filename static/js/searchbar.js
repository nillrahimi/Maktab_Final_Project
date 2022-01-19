$( document ).ready(function() {

    // console.log(URL) 
  
    $(".formsearch").on("click", function() {
       
        send_ajax($('#text_search').val())
    });
        function send_ajax(input_data){
            data={
                'csrfmiddlewaretoken':CSRF_TOKEN,
                'search_input':input_data
            };
        
            $.ajax({
                type: 'POST',
                url: URL,
                dataType: 'json',
                data:data,
                success: function(res) {
                    show_branches(res)
                }
            });
        }
        
        function show_branches(data){
            serachbar_div_tag = $("#searchbar_result")[0]            
            branch_ul_tag= $('#branch_ul')
            food_ul_tag= $('#food_ul')
            branch_ul_tag.empty()
            food_ul_tag.empty()
           
            var branch = data.branches;
            var food = data.foods;

            if(branch || food){
                serachbar_div_tag.style.display = 'unset'
            }
           
            if ( Array.isArray(branch) &&  branch.length > 0 ){
                $.each(branch, function(i, branch){
                    var li = document.createElement("li");
                    var a = document.createElement("a");
                    var text = document.createTextNode(branch.name);
                    
                    a.appendChild(text); 
                    a.href = `http://127.0.0.1:8000/menu_list/${branch.id}`;
                    
                    li.append(a)
                    branch_ul_tag.append(li)
                });
            } 
            else {
                branch_ul_tag[0].innerText = 'Not Found!'
            }
            
            if ( Array.isArray(food) &&  food.length > 0 ){
                $.each(food, function(i, food){
                    var li = document.createElement("li");
                    var a = document.createElement("a");
                    var text = document.createTextNode(food.name);
                    
                    a.appendChild(text); 
                    a.href = `http://127.0.0.1:8000/search_result_menu/${food.id}`;
                    
                    li.append(a)
                    food_ul_tag.append(li)
                });
            } 
            else {
                food_ul_tag[0].innerText = 'Not Found!'
            }
        }
      });