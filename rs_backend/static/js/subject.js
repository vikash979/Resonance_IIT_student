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
var filter_by={};

    $(window).on('load',function(){
        $('#classsubject_page').addClass("active");
        $(' aside .aside-container li.active').addClass('open').children('ul').show();
        $('#subject_page').addClass("active");
        var department_count = 0;
        var conditions = {};
        var paginations = {};
        paginations.page = 1;
        var data = {};
        data.action="view";
        // data.fields="department id";
        data.conditions=JSON.stringify(conditions);
        data.paginations = JSON.stringify(paginations);
        $.ajax({
                url: BASE_SITE_URL + `/api/v1/subject/has_subject/`,
                type: "POST",
                dataType: "json",
                data:data,
                success: function(response){
                    if (response.status != false) {
                        for(var i=0;i<response.data.length;i++){
                            $('.listingtable').append(`<tr><td>${response.data[i].name}</td><td>${response.data[i].code}</td><td>${response.data[i].master_subject.name}</td><td>${response.data[i].class_name}</td><td>${response.data[i].description}</td><td><a href="javascript:void(0);" class='edit-link' onclick="editSubject(${response.data[i].id})"><i class="fa fa-pencil"></i></a><a href="javascript:void(0);" onclick="removeSubject(${response.data[i].id})"><i class="fa fa-trash"></i></a></td></tr>`);
                            department_count+=1;
                        }
                        $('#subject_count').html(department_count);
                        var prev = `<a href="javascript:void(0)">prev</a>`;
                        var next = `<a href="javascript:void(0)">next</a>`;
                        if(response.paginations.batch_numpage!=0){
                            if(response.paginations.batch_numpage!=1){
                                $('.paginationContainer').append(prev);
                            }
                        for(var i=0;i<response.paginations.batch_numpage;i++){
                            if(i==0){
                                $('.paginationContainer').append(`<a id="page${i+1}" href="javascript:void(0)" class="selected">${i+1}</a>`);  
                            }
                            else{
                                $('.paginationContainer').append(`<a id="page${i+1}" href="javascript:void(0)">${i+1}</a>`);
                            }
                            
                        }
                        if(response.paginations.batch_numpage!=1){
                            $('.paginationContainer').append(next);
                        }
                        }
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


            var department_count = 0;
            var conditions = {};
            var paginations = {};
            paginations.page = 0;
            var data = {};
            data.action="view";
            // data.fields="department id";
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
                            $('#mastersubjectdd').append(`<option value="${response.data[i].id}">${response.data[i].name}</option>`);
                            $('#editMasterSubject').append(`<option value="${response.data[i].id}">${response.data[i].name}</option>`);
                        }
                        $('#mastersubjectdd').selectpicker('refresh');
                        $('#editMasterSubject').selectpicker('refresh');
                        
                    }
                    else if (response.status == false) {
                        $("#error-msg").html(response.error[0]+" !");
                    $('#error-dialogue').css("display","flex");
                    }
                },
                error: function(response){
                    $("#error-msg").html("there is problem on serverside"+" !");
                    $('#error-dialogue').css("display","none");
                    $('#error-dialogue').css("display","flex");
                }
            });

            var department_count = 0;
            // var conditions = {};
            var paginations = {};
            paginations.page = 0;
            var data = {};
            data.action="view";
            data.attrid="attrid"
            // data.fields="department id";
            // data.conditions=JSON.stringify(conditions);
            data.paginations = JSON.stringify(paginations);
            $.ajax({
                url: BASE_SITE_URL + `/api/v1/institute/institutes/`,
                type: "POST",
                dataType: "json",
                data:data,
                success: function(response){
                    if (response.status != false) {
                        $('#filter-by').append(`<option value="0">All</option>`);
                        for(var i=0;i<response.data.length;i++){
                            $('#class_id').append(`<option value="${response.data[i].id}">${response.data[i].name}</option>`);
                            $('#edit_class_id').append(`<option value="${response.data[i].id}">${response.data[i].name}</option>`);
                            $('#filter-by').append(`<option value="${response.data[i].id}">${response.data[i].name}</option>`);
                        }
                        $('#class_id').selectpicker('refresh');
                        $('#edit_class_id').selectpicker('refresh');    
                    }
                    else if (response.status == false) {
                        $("#error-msg").html(response.error[0]+" !");
                    $('#error-dialogue').css("display","flex");
                    }
                },
                error: function(response){
                    $("#error-msg").html("there is problem on serverside"+" !");
                    $('#error-dialogue').css("display","none");
                    $('#error-dialogue').css("display","flex");
                }
            });


    });

    function editSubject(attrId){
        
        var department_count = 0;
        var conditions = {};
        var paginations = {};
        conditions.id = attrId;
        var data = {};
        data.action="view";
        // data.fields="department id";
        data.conditions=JSON.stringify(conditions);
        data.paginations = JSON.stringify(paginations);
        $.ajax({
            url: BASE_SITE_URL + `/api/v1/subject/has_subject/`,
            type: "POST",
            // dataType: "json",
            data:data,
            success: function(response){
                console.log(response.data);
                if (response.status != false) {
                    // $('#edit_class_id').val(response.data.class_id);
                    $('#edit_value_name').val(response.data.name);
                    $('#edit_value_shortCode').val(response.data.code);
                    $('#edit_value_description').val(response.data.description);
                    $(`select[id="edit_class_id"] option[value="${response.data.class_id}"]`).attr('selected', 'selected');
                    $(`select[id="edit_class_id"]`).selectpicker('refresh');
                    $(`select[id="editMasterSubject"] option[value="${response.data.master_subject.id}"]`).attr('selected', 'selected');
                    $(`select[id="editMasterSubject"]`).selectpicker('refresh');
                    jQuery('#editEmployementDialog').addClass('open');
                    $('#editValueForm').on('submit',function(e){
                        e.preventDefault();
                        let conditions = $(this).serializeObject();
                        conditions.id = attrId;
                        let data = {};
                        data.action="update";   
                        data.conditions=JSON.stringify(conditions);
                        $.ajax({
                            url: BASE_SITE_URL + `/api/v1/subject/has_subject/`,
                            type: "POST",
                            data:data,
                            success: function(response){
                                if (response.status != false) {
                                    location.reload();
                                }
                                else if (response.status == false) {
                                    $("#error-msg").html(response.error[0]+" !");
                                $('#error-dialogue').css("display","flex");
                                }
                                
                            },
                            error: function(response){
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

    function removeSubject(attrId){
        console.log(attrId);
        var conditions = {};
        conditions.id = attrId;
        var data = {};
        data.action="remove";   
        data.conditions=JSON.stringify(conditions);
        $.ajax({
            url: BASE_SITE_URL + `/api/v1/subject/has_subject/`,
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
        // $(currBtn).addClass('selected');
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
                url: BASE_SITE_URL + `/api/v1/subject/has_subject/`,
                type: "POST",
                dataType: "json",
                data:data,
                success: function(response){
                    if (response.status != false) {
                        $('.listingtable').empty();
                        for(var i=0;i<response.data.length;i++){
                            $('.listingtable').append(`<tr><td>${response.data[i].name}</td><td>${response.data[i].code}</td><td>${response.data[i].master_subject.name}</td><td>${response.data[i].class_name}</td><td>${response.data[i].description}</td><td><a href="javascript:void(0);" class='edit-link' onclick="editSubject(${response.data[i].id})"><i class="fa fa-pencil"></i></a><a href="javascript:void(0);" onclick="removeSubject(${response.data[i].id})"><i class="fa fa-trash"></i></a></td></tr>`);
                            department_count+=1;
                        }
                        $('#subject_count').html(department_count);
                        
                    }
                }
            });
    });
}


function filterUsingFilter(){
    var e= document.getElementById("filter-by");
    var req_option= e.options[e.selectedIndex].value;
    var department_count = 0;
        var conditions = {};
        // var filter_by={};
        filter_by.class_id=req_option;
        conditions.filter_by=filter_by;
        var paginations = {};
        paginations.page = 1;
        var data = {};
        data.action="view";   
        data.conditions=JSON.stringify(conditions);
        data.paginations = JSON.stringify(paginations);
        $.ajax({
                url: BASE_SITE_URL + `/api/v1/subject/has_subject/`,
                type: "POST",
                dataType: "json",
                data:data,
                success: function(response){
                    if (response.status != false) {
                        $('.listingtable').empty();
                        for(var i=0;i<response.data.length;i++){
                            $('.listingtable').append(`<tr><td>${response.data[i].name}</td><td>${response.data[i].code}</td><td>${response.data[i].master_subject.name}</td><td>${response.data[i].class_name}</td><td>${response.data[i].description}</td><td><a href="javascript:void(0);" class='edit-link' onclick="editSubject(${response.data[i].id})"><i class="fa fa-pencil"></i></a><a href="javascript:void(0);" onclick="removeSubject(${response.data[i].id})"><i class="fa fa-trash"></i></a></td></tr>`);
                            department_count+=1;
                        }
                        $('#subject_count').html(department_count);
                    }
                }
            });
}

function filterUsingSearch(){
    req_val=$('#txt-search').val();
    var department_count = 0;
        var conditions = {};
        filter_by.name=req_val;
        conditions.filter_by=filter_by;
        var paginations = {};
        paginations.page = 1;
        var data = {};
        data.action="view";   
        data.conditions=JSON.stringify(conditions);
        data.paginations = JSON.stringify(paginations);
        console.log("data",data);
        $.ajax({
            url: BASE_SITE_URL + `/api/v1/subject/has_subject/`,
            type: "POST",
            dataType: "json",
            data:data,
            success: function(response){
                if (response.status != false) {
                    $('.listingtable').empty();
                    for(var i=0;i<response.data.length;i++){
                        $('.listingtable').append(`<tr><td>${response.data[i].name}</td><td>${response.data[i].code}</td><td>${response.data[i].master_subject.name}</td><td>${response.data[i].class_name}</td><td>${response.data[i].description}</td><td><a href="javascript:void(0);" class='edit-link' onclick="editSubject(${response.data[i].id})"><i class="fa fa-pencil"></i></a><a href="javascript:void(0);" onclick="removeSubject(${response.data[i].id})"><i class="fa fa-trash"></i></a></td></tr>`);
                        department_count+=1;
                    }
                    $('#subject_count').html(department_count);
                }
            }
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
//     { id: '1', title: 'Physics', uniquecode: 'PH', mastersubject: 'Physics', class: 'class1', description: 'Physics'},
//     { id: '2', title: 'Chemistry', uniquecode: 'CA', mastersubject: 'Chemistry', class: 'class2', description: 'Chemistry'},
//    { id: '3', title: 'Maths', uniquecode: 'MA', mastersubject: 'Maths', class: 'class3', description: 'Mathematics'},
//    { id: '4', title: 'Biology', uniquecode: 'BI', mastersubject: 'Biology', class: 'class4', description: 'Biology'},
    
    
    
// ]


// let paginationData = [
//    { id: '1', title: 'Physics', uniquecode: 'PH', mastersubject: 'Physics', class: 'class1', description: 'Physics'},
//     { id: '2', title: 'Chemistry', uniquecode: 'CA', mastersubject: 'Chemistry', class: 'class2', description: 'Chemistry'},
//    { id: '3', title: 'Maths', uniquecode: 'MA', mastersubject: 'Maths', class: 'class3', description: 'Mathematics'},
//    { id: '4', title: 'Biology', uniquecode: 'BI', mastersubject: 'Biology', class: 'class4', description: 'Biology'},
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
//                <td>${val.title}</td>
//                <td>${val.uniquecode}</td>
//                <td>${val.mastersubject}</td>
//                <td>${val.class}</td>
//                <td>${val.description}</td>
//                <td><a href="javascript:void(0);" class='edit-link'><i class="fa fa-pencil"></i></a><a href="#"><i class="fa fa-trash"></i></a></td>
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
    jQuery('#addDivisionDialog').addClass('open');
    // var department_count = 0;
    // var conditions = {};
    // var paginations = {};
    // paginations.page = 0;
    // var data = {};
    // data.action="view";
    // // data.fields="department id";
    // data.conditions=JSON.stringify(conditions);
    // data.paginations = JSON.stringify(paginations);
    // $.ajax({
    //     url: BASE_SITE_URL + `/api/v1/subject/master_subject/`,
    //     type: "POST",
    //     dataType: "json",
    //     data:data,
    //     success: function(response){
    //         if (response.status != false) {
    //             for(var i=0;i<response.data.length;i++){
    //                 $('#mastersubjectdd').append(`<option value="${response.data[i].id}">${response.data[i].name}</option>`);
    //                 $('#editMasterSubject').append(`<option value="${response.data[i].id}">${response.data[i].name}</option>`);
    //             }
    //             $('#mastersubjectdd').selectpicker('refresh');
    //             $('#editMasterSubject').selectpicker('refresh');
    //             jQuery('#addDivisionDialog').addClass('open');
                
    //         }
    //     }
    // });

});  

// jQuery('table td .edit-link').click(function(){
//     jQuery('.addDivisionDialog.foredit').addClass('open');
    

// });  

$('#classdd, #mastersubjectdd').selectpicker(); 
$('#editMasterSubject').selectpicker();

jQuery('.addDivisionDialog .form-actions a').click(function(){
    jQuery('.addDivisionDialog').removeClass('open');
});

jQuery('.addDivisionDialog .form-actions a').click(function(){
    jQuery('.addDivisionDialog.foredit').removeClass('open');
});

$('#add-subject').on('submit',function(e){
    e.preventDefault();
    var data = $(this).serializeObject();
    data["action"]="add";
    $.ajax({
        url: BASE_SITE_URL + `/api/v1/subject/has_subject/`,
        type: "POST",
        dataType: "json",
        data:data,
        success: function(response){
            if (response.status != false) {
                location.reload();
                }
                else if (response.status == false) {
                    jQuery('#addDivisionDialog').removeClass('open');
                    $("#error-msg").html(response.error[0]+" !");
                $('#error-dialogue').css("display","flex");
                }
        },
        error: function(response){
            jQuery('#addDivisionDialog').removeClass('open');
            $("#error-msg").html("there is problem on serverside"+" !");
            $('#error-dialogue').css("display","none");
            $('#error-dialogue').css("display","flex");
        }
    });
});


});
