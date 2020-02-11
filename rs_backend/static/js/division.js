$.fn.serializeObject = function(){
    jQuery.ajaxSettings.traditional = true;
    var obj = {};
    $.each( this.serializeArray(), function(i,o){
      var n = o.name,
          v = o.value;
          obj[n] = obj[n] === undefined ? v
            : $.isArray( obj[n] ) ? obj[n].concat( v )
            : [ obj[n], v ];
    });
    return obj;
  };


function clickError(){
$('#error-dialogue').css("display","none");
}

var page_count = 1;
var max_page = 0;

    $(window).on('load',function(){
        $('#organization_page').addClass("active");
        $(' aside .aside-container li.active').addClass('open').children('ul').show();
        $('#divisions_page').addClass("active");
        var department_count = 0;
        var conditions = {};
        var paginations = {};
        paginations.page = 1;
        var data = {};
        data.action="view";   
        data.conditions=JSON.stringify(conditions);
        data.paginations = JSON.stringify(paginations);
        $.ajax({
                url: BASE_SITE_URL + `/api/v1/auth/division/`,
                type: "POST",
                dataType: "json",
                data:data,
                success: function(response){
                    if (response.status != false) {
                        for(var i=0;i<response.data.length;i++){
                            $('.listingtable').append(`<tr><td class='division-title'>${response.data[i].division}</td><td class='division-actions'><a href="javascript:void(0);" onclick="editDivision(${response.data[i].id})" class='edit-link'><i class="fa fa-pencil"></i></a><a href="javascript:void(0);" onclick="removeDivision(${response.data[i].id})"><i class="fa fa-trash"></i></a></td></tr>`);
                            department_count+=1;
                        }
                        $('#division_count').html(department_count);
                        var prev = `<a href="javascript:void(0)">prev</a>`;
                                var next = `<a href="javascript:void(0)">next</a>`;
                                $('.paginationContainer').append(prev);
                                for(var i=0;i<response.paginations.batch_numpage;i++){
                                    if(i==0){
                                        $('.paginationContainer').append(`<a href="javascript:void(0)" class="selected">${i+1}</a>`);  
                                    }
                                    else{
                                        $('.paginationContainer').append(`<a href="javascript:void(0)">${i+1}</a>`);
                                    }
                                    
                                }
                                $('.paginationContainer').append(next);
                                setPaginator();
                    }
                    else if (response.status == false) {
                        jQuery('.addDivisionDialog').removeClass('open');
                        $("#error-msg").html(response.error[0]+" !");
                    $('#error-dialogue').css("display","flex");
                    }
                    max_page = response.paginations.batch_numpage;  
                },
                error: function(response){
                    jQuery('.addDivisionDialog').removeClass('open');
                    $("#error-msg").html("there is problem on serverside"+" !");
                    $('#error-dialogue').css("display","none");
                    $('#error-dialogue').css("display","flex");
                }
            });
    });

    function editDivision(attrId){
        
        var conditions = {};
        var paginations = {};
        conditions.id = attrId;
        var data = {};
        data.action="view";   
        data.conditions=JSON.stringify(conditions);
        data.paginations=JSON.stringify(paginations);
        $.ajax({
            url: BASE_SITE_URL + `/api/v1/auth/division/`,
            type: "POST",
            // dataType: "json",
            data:data,
            success: function(response){
                if (response.status != false) {

                    $('#edit_value').val(response.data.division);
                    jQuery('#editDivisionDialog').addClass('open');
                    $('#editValueForm').on('submit',function(e){
                        e.preventDefault();
                        let conditions = {};
                        conditions.id = attrId;
                        conditions[$('#edit_value').attr("name")]=$('#edit_value').val();
                        let data = {};
                        data.action="update";   
                        data.conditions=JSON.stringify(conditions);
                        $.ajax({
                            url: BASE_SITE_URL + `/api/v1/auth/division/`,
                            type: "POST",
                            // dataType: "json",
                            data:data,
                            success: function(response){
                                if (response.status != false) {
                                    location.reload();
                                }
                                else if (response.status == false) {
                                    jQuery('.addDivisionDialog').removeClass('open');
                                    $("#error-msg").html(response.error[0]+" !");
                                $('#error-dialogue').css("display","flex");
                                }
                            },
                            error: function(response){
                                jQuery('.addDivisionDialog').removeClass('open');
                                $("#error-msg").html("there is problem on serverside"+" !");
                                $('#error-dialogue').css("display","none");
                                $('#error-dialogue').css("display","flex");
                            }

                        });
                    })
                }
            }
        });
    }

    function removeDivision(attrId){
        var conditions = {};
        conditions.id = attrId;
        var data = {};
        data.action="remove";   
        data.conditions=JSON.stringify(conditions);
        $.ajax({
            url: BASE_SITE_URL + `/api/v1/auth/division/`,
            type: "POST",
            // dataType: "json",
            data:data,
            success: function(response){
                if (response.status != false) {
                    location.reload();
                }
            }
        });

    }

    function setPaginator(){
        $('#divPagination a').off('click');
        $('#divPagination a').on('click', function(e) {
        $('#divPagination a').removeClass('selected');
        var currBtn = e.target;
        $(currBtn).addClass('selected');
        if($(currBtn).html()=="prev"){
            if(page_count==1){
                page_count = 1;
            }
            else{
                page_count-=1;
            }
        }
        else if($(currBtn).html()=="next"){
            if(page_count == max_page){
                page_count=max_page;
            }
            else{
                page_count+=1;
            }
            
        }
        else{
            page_count = $(currBtn).html();
        }
        var department_count = 0;
        var conditions = {};
        var paginations = {};
        paginations.page = page_count;
        var data = {};
        data.action="view";   
        data.conditions=JSON.stringify(conditions);
        data.paginations = JSON.stringify(paginations);
        $.ajax({
                url: BASE_SITE_URL + `/api/v1/auth/division/`,
                type: "POST",
                dataType: "json",
                data:data,
                success: function(response){
                    if (response.status != false) {
                        $('.listingtable').empty();
                        for(var i=0;i<response.data.length;i++){
                            $('.listingtable').append(`<tr><td class='division-title'>${response.data[i].division}</td><td class='division-actions'><a href="javascript:void(0);" onclick="editDivision(${response.data[i].id})" class='edit-link'><i class="fa fa-pencil"></i></a><a href="javascript:void(0);" onclick="removeDivision(${response.data[i].id})"><i class="fa fa-trash"></i></a></td></tr>`);
                            department_count+=1;
                        }
                        $('#subject_count').html(department_count);
                    }
                }
            });
    });
}


        $(' aside .aside-container li.active').addClass('open').children('ul').show();
        $('aside .aside-container li.has-sub>a').on('click', function(){
            //$(this).removeAttr('href');
            var element = $(this).parent('li');
            if (element.hasClass('open')) {
                element.removeClass('open');
                element.find('li').removeClass('open');
                element.find('ul').slideUp(200);
            }
            else {
                element.addClass('open')
                element.children('ul').slideDown(200);
                element.siblings('li').children('ul').slideUp(200);
                element.siblings('li').removeClass('open');
                element.siblings('li').find('li').removeClass('open');
                element.siblings('li').find('ul').slideUp(200);
            }
        });

         $("#upload_link").on('click', function(e){
            e.preventDefault();
            $("#upload:hidden").trigger('click');
        })

        // let tableData = [
        //     { id: '1', title: 'Classroom Contact Programmes(CCPs)'},
        //     { id: '2', title: 'Pre-foundation Career Care Programmes (PCCPs)'},
        //     { id: '3', title: 'Distance Learning Programmes (DLPs)'},
        //     { id: '4', title: 'e-Learning Programmes (e-LPs)'},
        //     { id: '5', title: 'Commerce & Law Programmes'},
          
            
        // ]


        // let paginationData = [
        //     { id: '1', title: 'Classroom Contact Programmes(CCPs)'},
        //     { id: '2', title: 'Pre-foundation Career Care Programmes (PCCPs)'},
        //     { id: '3', title: 'Distance Learning Programmes (DLPs)'},
        //     { id: '4', title: 'e-Learning Programmes (e-LPs)'},
        //     { id: '5', title: 'Commerce & Law Programmes'},
        // ]


            //  function confirmation(type){
            //      if (type === 'confirm'){
            //         console.log("confirm");
            //      }else{
            //        console.log("cancel"); 
            //      }  
            // }

            // function success(type){
            //      if (type === 'ok'){
            //         console.log("ok");
            //      }else{
            //        console.log("cancel"); 
            //      }  
            // }
    

    jQuery(document).ready(function(){

        

      
        // let tableHTML ='';
        // let paginationHTML ='';


        // tableData.forEach((val)=>{
        //     tableHTML += `<tr>
        //                 <td class='division-title'>${val.title}</td>
        //                <td class='division-actions'><a href="javascript:void(0);" class='edit-link'><i class="fa fa-pencil"></i></a><a href="#"><i class="fa fa-trash"></i></a></td>
        //             </tr>`;

                    
        // });

        
        // jQuery('.listingtable').append(tableHTML);
        
       



        // jQuery('#txt-search').keyup(function(e){
        //     let searchValue = $(this).val().toLowerCase();
        //          console.log(searchValue);
        //          console.log(tableData);
        //          let getData = tableData.find(data => data.name === searchValue);
        //          console.log(getData);
       
        //     });


       jQuery('.add-division-link').click(function(){
            //jQuery('.filter-section').css('display','flex');
            jQuery('#addDivisionDialog').addClass('open');

        });  

        // jQuery(' table td .edit-link').click(function(){
        //     jQuery('.addDivisionDialog.foredit').addClass('open');

        // });  

       $('#namedd').selectpicker(); 

        jQuery('.addDivisionDialog .form-actions a').click(function(){
            jQuery('.addDivisionDialog').removeClass('open');
        });

         jQuery('.addDivisionDialog.foredit .form-actions a').click(function(){
            jQuery('.addDivisionDialog.foredit').removeClass('open');
        });

        $('#add-division').on('submit',function(e){
            e.preventDefault();
            var data = $(this).serializeObject();
            data["action"]="add";
            $.ajax({
                url: BASE_SITE_URL + `/api/v1/auth/division/`,
                type: "POST",
                dataType: "json",
                data:data,
                success: function(response){
                    if (response.status != false) {
                        location.reload();
                      }
                    else if (response.status == false) {
                        jQuery('.addDivisionDialog').removeClass('open');
                        $("#error-msg").html(response.error[0]+" !");
                    $('#error-dialogue').css("display","flex");
                    }
                },
                error: function(response){
                    jQuery('.addDivisionDialog').removeClass('open');
                    $("#error-msg").html("there is problem on serverside"+" !");
                    $('#error-dialogue').css("display","none");
                    $('#error-dialogue').css("display","flex");
                }
            });
        });

    });
