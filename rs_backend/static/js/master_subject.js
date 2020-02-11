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
        $('#classsubject_page').addClass("active");
        $(' aside .aside-container li.active').addClass('open').children('ul').show();
        $('#mastersubject_page').addClass("active");
        var department_count = 0;
        var conditions = {};
        var paginations = {};
        paginations.page = 1;
        var data = {};
        data.action="view";   
        data.conditions=JSON.stringify(conditions);
        data.paginations = JSON.stringify(paginations);
        $.ajax({
                url: BASE_SITE_URL + `/api/v1/subject/master_subject/`,
                type: "POST",
                dataType: "json",
                data:data,
                success: function(response){
                    if (response.status != false) {
                        for(var i=0;i<response.data.length;i++){
                            $('.listingtable').append(`<tr><td>${response.data[i].name}</td><td>${response.data[i].short_code}</td><td>${response.data[i].description}</td><td class='division-actions'><a href="javascript:void(0);" onclick="editSubjects(${response.data[i].id})" class='edit-link'><i class="fa fa-pencil"></i></a><a href="javascript:void(0);" onclick="removeSubjects(${response.data[i].id})"><i class="fa fa-trash"></i></a></td></tr>`);
                            department_count+=1;
                        }
                        $('#subject_count').html(department_count);
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

    function editSubjects(attrId){

        var conditions = {};
        var paginations = {};
        conditions.id = attrId;
        var data = {};
        data.action="view";   
        data.conditions=JSON.stringify(conditions);
        data.paginations=JSON.stringify(paginations);
        $.ajax({
            url: BASE_SITE_URL + `/api/v1/subject/master_subject/`,
            type: "POST",
            // dataType: "json",
            data:data,
            success: function(response){
                if (response.status != false) {
                    $('#edit_value_name').val(response.data.name);
                    $('#edit_value_shortCode').val(response.data.short_code);
                    $('#edit_value_description').val(response.data.description);
                    jQuery('#editMaterSubjectDialog').addClass('open');
                    $('#edit-subjects').on('submit',function(e){
                        e.preventDefault();
                        let conditions = $(this).serializeObject();
                        conditions.id = attrId;
                        let data = {};
                        data.action="update";   
                        data.conditions=JSON.stringify(conditions);
                        $.ajax({
                            url: BASE_SITE_URL + `/api/v1/subject/master_subject/`,
                            type: "POST",
                            // dataType: "json",
                            data:data,
                            success: function(response){
                                if (response.status != false) {
                                    location.reload();
                                }
                                else if (response.status == false) {
                                    jQuery('#editMaterSubjectDialog').removeClass('open');
                                    $("#error-msg").html(response.error[0]+" !");
                                $('#error-dialogue').css("display","flex");
                                }
                            },
                            error: function(response){
                                jQuery('#editMaterSubjectDialog').removeClass('open');
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

    function removeSubjects(attrId){
        var conditions = {};
        conditions.id = attrId;
        var data = {};
        data.action="remove";   
        data.conditions=JSON.stringify(conditions);
        $.ajax({
            url: BASE_SITE_URL + `/api/v1/subject/master_subject/`,
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
            url: BASE_SITE_URL + `/api/v1/subject/master_subject/`,
            type: "POST",
            dataType: "json",
            data:data,
            success: function(response){
                if (response.status != false) {
                    $('.listingtable').empty();
                    for(var i=0;i<response.data.length;i++){
                        $('.listingtable').append(`<tr><td>${response.data[i].name}</td><td>${response.data[i].short_code}</td><td>${response.data[i].description}</td><td class='division-actions'><a href="javascript:void(0);" onclick="editSubjects(${response.data[i].id})" class='edit-link'><i class="fa fa-pencil"></i></a><a href="javascript:void(0);" onclick="removeSubjects(${response.data[i].id})"><i class="fa fa-trash"></i></a></td></tr>`);
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
//     { id: '1', shortcode: 'PhM001', title: 'Physics',description: 'Physics Master'},
//     { id: '2', shortcode: 'CHM001' , title: 'Chemistry' ,description: 'Chemistry Master'},
//     { id: '3', shortcode: 'MAM001' , title: 'Mathematics' ,description: 'Mathematics Master'},
 
  
    
// ]


// let paginationData = [
//     { id: '1', shortcode: '123434', title: 'title1',description: 'description1'},
//     { id: '2', shortcode: 'ycyyde' , title: 'title2' ,description: 'description2'},
//     { id: '3', shortcode: '5hhfyr' , title: 'title3' ,description: 'description3'},
//     { id: '4', shortcode: '9lgiyy' , title: 'title4' ,description: 'description4'},
//     { id: '5', shortcode: '857ffg' , title: 'title5' ,description: 'description5'},
//     { id: '6', shortcode: '855jfuy' , title: 'title6' ,description: 'description6'},
  
// ]


     function confirmation(type){
         if (type === 'confirm'){
            console.log("confirm");
         }else{
           console.log("cancel"); 
         }  
    }

    function success(type){
         if (type === 'ok'){
            console.log("ok");
         }else{
           console.log("cancel"); 
         }  
    }


jQuery(document).ready(function(){




// let tableHTML ='';
// let paginationHTML ='';


// tableData.forEach((val)=>{
//     tableHTML += `<tr>
//                 <td>${val.title}</td>
//                 <td>${val.shortcode}</td>
//                 <td>${val.description}</td>
//                <td class='division-actions'><a href="javascript:void(0);" class='edit-link'><i class="fa fa-pencil"></i></a><a href="#"><i class="fa fa-trash"></i></a></td>
//             </tr>`;

            
// });


// jQuery('.listingtable').append(tableHTML);





jQuery('#txt-search').keyup(function(e){
    let searchValue = $(this).val().toLowerCase();
         console.log(searchValue);
         console.log(tableData);
         let getData = tableData.find(data => data.name === searchValue);
         console.log(getData);

    });


jQuery('.add-session-link').click(function(){
    jQuery('.addSessionDialog').addClass('open');
    jQuery('.addSessionDialog.foredit').removeClass('open');
});  

jQuery('table td .edit-link').click(function(){
    jQuery('.addSessionDialog.foredit').addClass('open');
    

});  

 jQuery('.datepicker').datetimepicker();

jQuery('.addSessionDialog .form-actions a').click(function(){
    jQuery('.addSessionDialog').removeClass('open');
});


//  jQuery('.addSessionDialog.foredit .form-actions a').click(function(){
//     jQuery('.addSessionDialog.foredit').removeClass('open');
// });
$('#add-subjects').on('submit',function(e){
    e.preventDefault();
    var data = $(this).serializeObject();
    data["action"]="add";
    $.ajax({
        url: BASE_SITE_URL + `/api/v1/subject/master_subject/`,
        type: "POST",
        dataType: "json",
        data:data,
        success: function(response){
            if (response.status != false) {
                location.reload();
              }
              else if (response.status == false) {
                jQuery('#addMaterSubjectDialog').removeClass('open');
                $("#error-msg").html(response.error[0]+" !");
            $('#error-dialogue').css("display","flex");
            }
        },
        error: function(response){
            jQuery('#addMaterSubjectDialog').removeClass('open');
            $("#error-msg").html("there is problem on serverside"+" !");
            $('#error-dialogue').css("display","none");
            $('#error-dialogue').css("display","flex");
        }
    });
})


});
