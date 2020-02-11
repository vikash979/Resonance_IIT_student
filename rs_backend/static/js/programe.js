$(window).on('load',function(){
    $('#programspage').addClass("active");
    $(' aside .aside-container li.active').addClass('open').children('ul').show();
    $('#program_page').addClass("active");
    var display_name = $('#name').val()


    $.ajax({
        url: BASE_SITE_URL + '/api/v1/institute/program_target/',
        type: "POST",
        dataType: "json",
        data:{"action":"view"},
        success: function(response){
            if (response.status==true)
            {
                let lineNo = 1;
                tableBody = $("table tbody");
                let tableData = JSON.stringify(response.data)
                for(var i=0;i<response.data.length;i++){
                    //alert(JSON.stringify(response.data))
                    // $('#program_id').append(`<option value="${response.data[i].id}" selected="selected">${response.data[i].display_name}</option>`);
                    $('#target_id').append(`<option value="${response.data[i].id}" selected="selected">${response.data[i].name}</option>`);
                    $('#target_id_edit').append(`<option value="${response.data[i].id}" selected="selected">${response.data[i].name}</option>`);
               
                
                }
                // alert(length(tableData))
            }
            
        }
        })
    
    $("#add_program").click( function(e){
        
        
        var display_name = $('#display_name').val()
        var description = $('#description').val()
        var name = $('#name').val()
        var target = $('#target_id').val()
       
        dataString = {"action":"add","display_name":display_name,"description":description,"name":name,"target":target}
        // var order = $('#order').val()
        
        $.ajax({
            url: BASE_SITE_URL + '/api/v1/institute/program/',
            type: "POST",
            dataType: "json",
            data:dataString,
            success: function(response){
                if (response.status ==true){
                    var class_saved = "Success Fully Saved"
                    $('#name').val(' ')
                    $('#description').val(' ')
                    location.reload();

                }
                else{
                    var class_saved = "Failed"
                }
            }

       })

    })

    ////////////////////View//
   programe()

    ////////////////////////////////View////////////////
})


function programe(programId)
{
    if (programId== undefined)
    {
        $.ajax({
            url: BASE_SITE_URL + '/api/v1/institute/program/',
            type: "POST",
            dataType: "json",
            data:{"action":"view"},
            success: function(response){
                if (response.status==true)
                {
                    let lineNo = 1;
                    tableBody = $("table tbody");
                    let tableData = JSON.stringify(response.data)
                    $('#listingtable').html('')
                    $('#pagination').html(' ')
                            for(var i=0;i<response.data.length;i++){
                                //alert(JSON.stringify(response.data))
                              
                           
                            //var totalrecord = (response.data[i].id+"_"+response.data[i].display_name+"_"+response.data[i].order+"_"+response.data[i].name+"_"+response.data[i].description)
                            //alert(totalrecord)
                            $('#listingtable').append(`<tr> <td>    ${response.data[i].display_name}</td><td>${response.data[i].name}</td><td>${response.data[i].target.name}</td><td></td><td><a href='javascript:void(0);' onclick="editClass(${response.data[i].id})" class='edit-link'><i class='fa fa-pencil'></i></a><a href="#" onclick="remove(${response.data[i].id})"><i class="fa fa-trash"></i></a></td></tr>`)
                           //$('#listingtable').append(`<tr> <td>lklk</td></tr>`)
                            }
        
                            var pagi_length =response.paginations['program_numpage']+1
                             
                            if (response.paginations['program_numpage'] > 0){
                                
                                if(response.paginations['program_user_changes']==true)
                                {
                                   if(response.paginations['program_previous']==true){
           
                                       $('#pagination').append(`<a href="#" onclick="programe(${response.paginations['program_previous_page']})">prev</a>`)
                                       
                                   }
                                   // else{
                                   //     $('#pagination').append(`<span>prev</span>`)
                                   // }
                                   for (var i=1;i<pagi_length;i++)
                                   {
                                    if (response.paginations['current_page']==i)
                                    {
                                        
                                       $('#pagination').append(`<a href="#" onclick="programe(${i}") class="selected">${i}</a>`)
                                    }  
                                    else{
                                        
                                       $('#pagination').append(`<a href="#" class="paginate" id="${i}" onclick="programe(${i});">${i}</a>`)
                                    }
                                   }
                                   if (response.paginations['program_next']==true)
                                   {
                                       $('#pagination').append(`<a href="#" onclick="programe(${response.paginations['program_next_page_number']})">next</a>`)
                                   }
                                   
                                }
                                //location.reload();
                            }
                    // alert(length(tableData))
                }
                
            }
        })
    }
    else{
        $.ajax({
            url: BASE_SITE_URL + '/api/v1/institute/program/',
            type: "POST",
            dataType: "json",
            
            data:{"action":"view","page":programId},
            success: function(response){
                if (response.status==true)
                {
                    let lineNo = 1;
                    tableBody = $("table tbody");
                    let tableData = JSON.stringify(response.data)
                    $('#listingtable').html('')
            $('#pagination').html(' ')
                    for(var i=0;i<response.data.length;i++){
                   
                    //var totalrecord = (response.data[i].id+"_"+response.data[i].display_name+"_"+response.data[i].order+"_"+response.data[i].name+"_"+response.data[i].description)
                    //alert(totalrecord)
                    $('#listingtable').append(`<tr> <td>    ${response.data[i].display_name}</td><td>${response.data[i].name}</td><td>${response.data[i].target.name}</td><td></td><td><a href='javascript:void(0);' onclick="editClass(${response.data[i].id})" class='edit-link'><i class='fa fa-pencil'></i></a><a href="#"><i class="fa fa-trash"></i></a></td></tr>`)
                   //$('#listingtable').append(`<tr> <td>lklk</td></tr>`)
                    }

                    var pagi_length =response.paginations['program_numpage']+1
                     
                    if (response.paginations['program_numpage'] > 0){
                        
                        if(response.paginations['program_user_changes']==true)
                        {
                           if(response.paginations['program_previous']==true){
   
                               $('#pagination').append(`<a href="#" onclick="programe(${response.paginations['program_previous_page']})">prev</a>`)
                               
                           }
                           // else{
                           //     $('#pagination').append(`<span>prev</span>`)
                           // }
                           for (var i=1;i<pagi_length;i++)
                           {
                            if (response.paginations['current_page']==i)
                            {
                                
                               $('#pagination').append(`<a href="#" onclick="programe(${i}") class="selected">${i}</a>`)
                            }  
                            else{
                                
                               $('#pagination').append(`<a href="#" class="paginate" id="${i}" onclick="programe(${i});">${i}</a>`)
                            }
                           }
                           if (response.paginations['program_next']==true)
                           {
                               $('#pagination').append(`<a href="#" onclick="programe(${response.paginations['program_next_page_number']})">next</a>`)
                           }
                           
                        }
                        //location.reload();
                    }
                    // alert(length(tableData))
                }
                
            }
        })
    }
}
//////////////////////////////
/////////////////
function editClass(attrId){
    var hidden_class_id = $('#hidden_class_id').val(attrId)
    $.ajax({
        url: BASE_SITE_URL + '/api/v1/institute/program/',
        type: "POST",
        dataType: "json",
        data:{"action":"view","id":attrId},
        success: function(response){
            if (response.status ==true){
                
                
               
                // var class_saved = "Success Fully Saved"
                $('#display_name_edit').val(response.data[0]['display_name'])
                 var display_name = $('#progr_name').val(response.data[0]['name'])
                 var description = $('#desc').val(response.data[0]['description'])
              
               
            }
            else{
                var class_saved = "Failed"
            }
           
        }
    })
    var  cl_id = $('#hidden_class_id').val()
    jQuery('.addSessionDialog.foredit').addClass('open');
   // jQuery('.addSessionDialog.foredit').removeClass('open');
}

function updateclass()
{
    var display_name = $('#display_name_edit').val()
    var description = $('#desc').val()
    var name = $('#progr_name').val()
    var target = $('#target_id_edit').val()
    
    var  cl_id = $('#hidden_class_id').val()
    dataString  = {"action":"Update","name":name,"display_name":display_name,"description":description,"id": cl_id,"target":target}
    $.ajax({
        url: BASE_SITE_URL + '/api/v1/institute/program/',
        type: "POST",
        dataType: "json",
        data:dataString,
        success: function(response){
           
            location.reload();

        }
    })
}

//////////////////////////////////////remove////////////////



function remove(removeid)
{
    $.ajax({
        url: BASE_SITE_URL + '/api/v1/institute/program/',
        type: "POST",
        dataType: "json",
        data:{"action":"remove","id":removeid},
        success: function(response){
            if (response.status ==true){
                var class_saved = "Success Fully Saved"
                
                location.reload();

            }
            else{
                var class_saved = "Failed"
            }
        }

   })
}


/////////////////////////////////////////////////////Program/////////////////////////////////////////
////////////////////////////////////////////////////////////////////////////////////////////////////
/////////////////////////////////////////////////////////////////////////////////////////////////////



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

let tableData = [
    
  
    
]


// let paginationData = [
//     { id: '1', uniquecode: 'JR', target: 'JEE MAINS and Advanced', title: 'VIJAY JR'},
//     { id: '2', uniquecode: 'G&J' , target: 'NEET', title: 'VIJAY G&J'},
//     { id: '3', uniquecode: 'JR' , target: 'Boards Revision', title: 'VIKAAS JR'},
  
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

let tableHTML ='';
let paginationHTML ='';


tableData.forEach((val)=>{
    tableHTML += `<tr>
                <td><a href='program-details.html' class="title-link">${val.title}</a></td>
                <td>${val.uniquecode}</td>
                <td>${val.target}</td>
               <td class='division-actions'><a href="javascript:void(0);" class='edit-link'><i class="fa fa-pencil"></i></a><a href="#"><i class="fa fa-trash"></i></a></td>
            </tr>`;

            
});


jQuery('.listingtable').append(tableHTML);





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



jQuery('.addSessionDialog .form-actions a').click(function(){
    jQuery('.addSessionDialog').removeClass('open');
});



});







$('.startdatepicker').datetimepicker({
    locale: 'ru',
   debug:true,
   pickTime: false 
});

$('.enddatepicker').datetimepicker({
  locale: 'ru',
  debug:true,
  pickTime: false 

});

jQuery('.timepicker').datetimepicker({
 pickDate: false

});